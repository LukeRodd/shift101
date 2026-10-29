"use strict";
const q = selector => document.querySelector(selector);
const state = { mission: null, evidence: [], actionIds: [] };
function el(tag, cls = "", text) { const node = document.createElement(tag); if(cls) node.className = cls; if(text !== undefined) node.textContent = text; return node; }
async function api(url, options) { const response = await fetch(url, options); if(!response.ok) throw new Error("Falha HTTP " + response.status); return response.json(); }
function renderEvidence() { const area = q("#evidence"); area.replaceChildren(); if(!state.evidence.length) { area.textContent = "Nenhum teste executado."; return; } state.evidence.forEach(item => area.appendChild(el("p", "", item))); }
function renderMission(mission) {
  state.mission = mission;
  q("#mission-title").textContent = mission.title;
  q("#mission-desc").textContent = mission.description;
  const actions = q("#actions"); actions.replaceChildren();
  mission.actions.forEach(action => {
    const button = el("button", "", action.label); button.type = "button";
    button.addEventListener("click", async () => {
      button.disabled = true;
      try { const result = await api("/api/action/" + encodeURIComponent(action.id)); state.evidence.push(result.result); state.actionIds.push(action.id); renderEvidence(); }
      catch(error) { button.disabled = false; state.evidence.push("Erro: " + error.message); renderEvidence(); }
    });
    actions.appendChild(button);
  });
  const questions = q("#questions"); questions.replaceChildren();
  mission.questions.forEach((question, i) => {
    const field = el("fieldset", "quiz-question");
    field.dataset.questionId = question.id;
    field.appendChild(el("legend", "", (i + 1) + ". " + question.text));
    question.options.forEach((option, index) => {
      const label = el("label"); const input = el("input");
      input.type = "radio"; input.name = question.id; input.value = String(index); input.required = true;
      label.append(input, document.createTextNode(option)); field.appendChild(label);
    });
    questions.appendChild(field);
  });
}
async function checkAI() {\n  try { const status = await api("/api/ai/status"); const toggle = q("#ai-toggle"); toggle.disabled = !status.enabled; q("#ai-status").textContent = status.enabled ? "Ollama local disponível para tentativa; modelos precisam estar instalados." : "IA desabilitada: busca textual ativa."; }\n  catch { q("#ai-status").textContent = "Estado da IA indisponível; utilizando busca textual."; }\n}\nasync function renderRunbooks() {
  const documents = await api("/api/runbooks"); const area = q("#runbooks"); area.replaceChildren();
  documents.forEach(doc => { const details = el("details"); details.append(el("summary", "", doc.id + ": " + doc.title), el("p", "", doc.text)); area.appendChild(details); });
}
function setupTabs() {
  document.querySelectorAll(".tab").forEach(button => button.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(tab => tab.classList.toggle("active", tab === button));
    document.querySelectorAll(".workspace > .panel").forEach(panel => panel.classList.toggle("active", panel.id === button.dataset.panel));
  }));
}
function setupMentor() {
  q("#mentor-form").addEventListener("submit", async event => {
    event.preventDefault(); const output = q("#mentor-response"); output.textContent = "Consultando runbook…";
    try {
      const useAI = q("#ai-toggle").checked && !q("#ai-toggle").disabled;\n      const result = await api(useAI ? "/api/ai/mentor" : "/api/mentor", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question:q("#question").value, action_ids:state.actionIds})});
      output.replaceChildren(el("p", "", result.message));
      if(result.sources.length) output.appendChild(el("small", "", "Fonte: " + result.sources.map(source => source.id + " · " + source.title).join("; ")));
    } catch(error) { output.textContent = "Falha na consulta: " + error.message; }
  });
}
function setupQuiz() {
  q("#quiz-form").addEventListener("submit", async event => {
    event.preventDefault(); const form = event.currentTarget; const answers = {};
    state.mission.questions.forEach(question => {
      const selection = form.querySelector('input[name="' + question.id + '"]:checked');
      if(selection) answers[question.id] = Number(selection.value);
    });
    if(Object.keys(answers).length !== 5) return;
    const output = q("#quiz-result");
    try {
      const result = await api("/api/evaluate", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({answers})});
      output.textContent = "Resultado: " + result.score + "/" + result.total + ". " + (result.passed ? "Aprovado." : "Revisão necessária.");
      result.review.forEach(item => q('fieldset[data-question-id="' + item.question_id + '"]').appendChild(el("div", "correction", (item.is_correct ? "Correto. " : "Incorreto. ") + item.explanation)));
      form.querySelectorAll("input, button").forEach(element => { element.disabled = true; });
    } catch(error) { output.textContent = "Falha na avaliação: " + error.message; }
  });
}
async function start() {
  setupTabs(); setupMentor(); setupQuiz();
  try { const mission = await api("/api/mission"); renderMission(mission); await renderRunbooks(); await checkAI(); }
  catch(error) { q("#mission-title").textContent = "Não foi possível iniciar"; q("#mission-desc").textContent = "Verifique a API: " + error.message; }
}
start();

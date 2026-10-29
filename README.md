# Shift101

**Aprenda a operar. Investigue antes de agir.**

Plataforma educacional aberta, baseada em missões simuladas de operação de data centers e NOC. O aluno atua como integrante da equipe, analisa evidências, consulta runbooks e registra decisões.

> **Status: protótipo público (v0.1).** A missão demonstrativa é funcional. O módulo de LLM/RAG, autenticação, progresso persistente e a trilha completa de sete dias ainda **não foram implementados**.

## Demonstração atual

- Uma missão **100% fictícia** de indisponibilidade de aplicação, com monitoramento de conectividade e resposta HTTP.
- Painel de chamado e ambiente de inspeção (dados simulados).
- Cinco questões com correção **somente após o envio**; aprovação com 4/5.
- Apostila de referência e assistente de **recuperação textual simples**, com trechos citados (não é um LLM e não é RAG semântico).
- Layout responsivo, com áreas lado a lado no desktop e abas no mobile.
- API FastAPI e testes automatizados no GitHub Actions.

## Executar localmente

**Requisitos:** Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m uvicorn backend.shift101.main:app --reload
```

Abra `http://localhost:8000` no navegador. Documentação da API: `http://localhost:8000/docs`.

**Testar:**

```bash
pytest -q
```

**Docker:**

```bash
docker build -t shift101 .
docker run --rm -p 8000:8000 shift101
```

## Visão de produto

- **7 dias**, com missões contextualizadas e apostilas consultáveis.
- Desbloqueio por missão concluída e pelo menos **4 acertos em 5 questões**.
- Simulado final de **65 questões**, sem acesso à apostila/tutor durante a prova.
- Contas com progresso salvo, histórico de tentativas e painel administrativo — **planejados**.
- Novo módulo opcional **AI Incident Mentor** para orientação baseada em runbooks, com RAG, critérios de avaliação e supervisão humana — **planejado**.

Veja [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), [`docs/ROADMAP.md`](docs/ROADMAP.md), [`docs/AI_EVALUATION.md`](docs/AI_EVALUATION.md) e [`docs/SECURITY.md`](docs/SECURITY.md).

## Limites e integridade

Nenhum incidente real, log de cliente, endereço corporativo, credencial ou informação interna de empresas é usado neste projeto. **Todos os dados de demonstração são sintéticos.** Nenhuma ação de mudança é executada em equipamentos reais.

Não há imagens geradas por IA neste repositório. Os elementos visuais atuais são CSS e ícones tipográficos; novas fotografias devem ter licença compatível, atribuição e registro em [`docs/ASSET_CREDITS.md`](docs/ASSET_CREDITS.md).

## Licença

Código disponibilizado sob a [MIT License](LICENSE). Materiais externos e fotografias futuras terão suas próprias condições de licença.

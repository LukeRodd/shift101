# Shift101 — implementação AWS por etapas e checkpoints

**Regra:** implementar -> validar -> apresentar evidências -> aprovar ou ajustar -> avançar. Nenhum checkpoint é aprovado automaticamente por CI, e nenhum gasto AWS é autorizado por este documento.

**Escopo de referência:** [PR #1 — Tutor experimental](https://github.com/LukeRodd/shift101/pull/1); [PR #2 — AWS serverless](https://github.com/LukeRodd/shift101/pull/2). As mudanças permanecem em draft até revisão.

## C0 — Inventário e revisão de arquitetura
- [x] Localizar o código principal e confirmar PRs #1 e #2 em draft
- [x] Confirmar que a CI de ambos os PRs terminou com sucesso (29/10/2026)
- [ ] Revisar os riscos de acesso público, custos, autenticação, timeout, permissões e requisitos de dados
- [ ] Validar a sintaxe e o empacotamento AWS SAM (`sam validate` e `sam build`)
- [ ] Publicar a lista de correções/decisões e obter aprovação explícita
**Saída:** arquitetura revisada, restrições definidas, nenhuma conta AWS alterada.

## C1 — Baseline local
- [ ] Executar os testes da aplicação e da API em ambiente local limpo
- [ ] Verificar a missão, as cinco questões e a correção somente após o envio
- [ ] Executar teste manual em navegador desktop e mobile
- [ ] Confirmar que o módulo generativo é opcional e a missão funciona sem ele
**Saída:** relatório de testes reproduzível, falhas corrigidas; autorização para integração do baseline.

## C2 — Fundação AWS e controles financeiros
- [ ] Selecionar região AWS e conta de sandbox
- [ ] Revisar privilégios IAM de implantação, sem credenciais no repositório
- [ ] Configurar AWS Budget, alarmes e limites de concorrência; reconhecer que alertas não bloqueiam cobranças
- [ ] Validar template SAM, estimar componentes faturáveis e obter aprovação explícita do provisionamento
**Saída:** plano financeiro e técnico aprovado; nenhum recurso criado sem consentimento.

## C3 — Site estático e HTTPS
- [ ] Provisionar S3 privado e CloudFront, com acesso via OAC
- [ ] Publicar apenas o frontend sintético
- [ ] Verificar HTTPS, acesso negado diretamente ao bucket, headers, responsividade e cache
- [ ] Revisar custos observados e rollback
**Saída:** URL de demonstração estática, sem IA e sem exposição de dados.

## C4 — Backend Lambda e API
- [ ] Implantar API Gateway HTTP API e Lambda com Bedrock desligado
- [ ] Testar health, runbooks, missão, cinco questões e limites de entrada
- [ ] Confirmar CORS/origem, logs, tempo de resposta, erros e tratamento de falhas
- [ ] Verificar que apenas dados de laboratório são expostos
**Saída:** missão funcional end-to-end sem modelo generativo.

## C5 — IA generativa controlada
- [ ] Integrar o Bedrock inicialmente em ambiente restrito/autenticado
- [ ] Habilitar modelos apenas com acesso, limitação de tráfego e controle de custo efetivos
- [ ] Verificar retrieval/embeddings, citações dos runbooks e não exposição de gabaritos
- [ ] Testar prompts adversariais, respostas insuficientes e indisponibilidade do modelo
**Saída:** tutor RAG validado em condições controladas; **não** publicar o endpoint aberto.

## C6 — Avaliação técnica e pedagógica
- [ ] Montar dataset de 30–50 incidentes 100% sintéticos
- [ ] Comparar baseline lexical e RAG; calcular recall@k, referências corretas e taxa de alucinações
- [ ] Medir latência, custos por pergunta, taxa de erros e qualidade da orientação
- [ ] Revisar resultados e aprovar ou reprovar o lançamento com métricas documentadas
**Saída:** relatório reproduzível; reivindicações públicas apenas de resultados medidos.

## C7 — Portfólio e lançamento
- [ ] Revisar segurança, licença MIT, créditos de mídia e documentação
- [ ] Estabelecer monitoramento, processo de rollback e política de desligamento
- [ ] Publicar repositório, README, arquitetura, demonstração e resultados medidos
- [ ] Revisar apresentação no LinkedIn e currículo
**Saída:** demonstração pública revisada e documentação de aprendizado.

## Template de checkpoint

**Etapa:**  
**Objetivo:**  
**Entregas:**  
**Evidências e links:**  
**Testes (passou/falhou/não executado):**  
**Riscos e custo esperado/observado:**  
**Bloqueadores e ajustes:**  
**Decisão do responsável:** APROVAR / REVISAR / REPROVAR  
**Próxima etapa:** não iniciada até aprovação explícita.

## Princípios
- Provas finais sem acesso ao tutor, e avaliação de acertos determinística.
- Não usar logs reais, informações de clientes, segredos, nem dados internos.
- Não usar imagens geradas por IA; citar autor/licença de qualquer imagem externa.
- Recursos AWS são opcionais na fase de desenvolvimento. É necessário autorização explícita para despesas e deployment.

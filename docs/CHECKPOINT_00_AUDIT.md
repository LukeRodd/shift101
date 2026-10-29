# Checkpoint 00 — Auditoria técnica

Data: 29/10/2026. **Estado: validação pendente; não aprovado automaticamente.**

## Evidências confirmadas
- PR #1 (IA local): CI concluída com sucesso, **13 testes passaram**, 1 aviso.
- PR #2 (AWS): CI concluída com sucesso no commit anterior, **15 testes passaram**, 1 aviso.
- Cópia local do protótipo-base: **7 testes passaram**.
- PRs #1 e #2 permanecem **draft**. Nenhum recurso AWS foi criado por esta revisão.

## Lacuna detectada e ação
O workflow original executava Pytest, mas **não** validava o template AWS SAM nem executava o build de Lambda. Foi criado `.github/workflows/aws-sam-validation.yml` na branch `feat/aws-serverless-bedrock` para executar `sam validate --lint`, `sam build` e verificar o bundle. O resultado dessa execução ainda está **pendente de confirmação**; portanto, não há evidência de template implantável.

## Riscos técnicos/financeiros a resolver antes de provisionar
1. A HTTP API é pública e sem autenticação. **Manter Bedrock desabilitado** em qualquer demonstração pública até haver controles de acesso e consumo.
2. Concurrency Lambda e Budgets **não são teto de gasto garantido**. Necessário custo estimado, alertas e monitoramento.
3. Validar existência/disponibilidade regional dos modelos Bedrock e permissões IAM antes de ativar.
4. Revisar configuração do origin da API no CloudFront para não encaminhar cabeçalhos incorretos.
5. Revisar resposta de bloqueio do tutor, prompt injection, comportamento em indisponibilidade e métricas antes de liberar IA.
6. Validar roteamento da API, CORS/HTTPS, log retention e comportamento sob falhas em testes controlados.
7. A preparação da aplicação para implantação real ainda exige smoke tests e controle de versão da infraestrutura.

## Decisão
**Checkpoint 00: REVISÃO PENDENTE**, aguardando o novo workflow de validação SAM e revisão dos itens bloqueadores. Não avançar para o Checkpoint 01 e não mesclar PRs antes de apresentar evidências.

Links:
- https://github.com/LukeRodd/shift101/pull/1
- https://github.com/LukeRodd/shift101/pull/2

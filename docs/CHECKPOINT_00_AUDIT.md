# Checkpoint 00 — auditoria e correções da arquitetura AWS

Data: 29/10/2026. **Status técnico: APROVADO para avançar à validação local, sem autorização de deploy.**

## Evidências de testes

- PR #1 (AI Incident Mentor, Ollama): **13 testes aprovados** na CI.
- PR #2 (versão final após correções): **18 testes aprovados**, 1 warning de teste.
- AWS SAM (PR #2, commit `2c0bd0e`): `sam validate --lint`, `sam build` e inspeção do bundle Lambda **aprovados** no workflow #40929309823.
- A versão do código foi validada em GitHub Actions sem credenciais AWS e **não foi provisionada**.

## Ajustes realizados

1. Bucket S3 protegido contra exclusão/substituição involuntária com `DeletionPolicy` e `UpdateReplacePolicy`, e criptografia SSE-S3.
2. S3 com bloqueio de acesso público e Origin Access Control do CloudFront.
3. API Gateway com limitação de requisições (rate 2/s, burst 5) e Lambda com concorrência reservada 2.
4. CloudWatch Logs com retenção de 7 dias.
5. CloudFront usando política gerenciada `AllViewerExceptHostHeader` (adequada ao API Gateway), sem cache na API, e `SecurityHeadersPolicy`.
6. **Bedrock não pode ser ativado no template atual**: flag da IA fixada em `false`, política `bedrock:InvokeModel` removida. Reintroduzir apenas após autenticação, rate limiting/quotas e orçamento validados no Checkpoint 05.
7. Workflow independente de validação SAM e testes de regressão de configurações de segurança.

## Limitações e riscos residuais

- A API HTTP (rotas de demonstração sem IA) continua pública; throttle e concorrência **não estabelecem teto financeiro**. Confirmar orçamento e alertas antes de criar recursos.
- A disponibilidade dos modelos Bedrock na região/conta escolhida e as permissões IAM não foram verificadas em uma conta AWS; pertencem às etapas futuras.
- Autenticação, banco persistente, proteção completa contra abuso, avaliação pedagógica e implantação end-to-end ainda não fazem parte desta versão.
- Não há validação de navegação em desktop/mobile nem testes em ambiente AWS. Essas atividades pertencem ao Checkpoint 01 e aos checkpoints de implantação.
- O código de IA é experimental e permanece em PR draft. O merge dos PRs #1/#2 requer revisão e aprovação separadas.

## Decisão e próximo gate

**Checkpoint 00 tecnicamente concluído** no commit `2c0bd0e`, com GitHub Actions verde.
Aguardar aprovação do responsável para iniciar o **Checkpoint 01 — teste local funcional e revisão da interface**.

Referências:
- [PR #1](https://github.com/LukeRodd/shift101/pull/1)
- [PR #2](https://github.com/LukeRodd/shift101/pull/2)
- [Workflow SAM aprovado](https://github.com/LukeRodd/shift101/actions/runs/40929309823)
- [Workflow Pytest aprovado](https://github.com/LukeRodd/shift101/actions/runs/40929309799)
- [CloudFront AllViewerExceptHostHeader](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-managed-origin-request-policies.html)

# Deploy controlado do Shift101 na AWS

**Estado:** automação preparada, mas não executada. Este repositório não possui acesso à conta AWS a partir da conexão GitHub. Somente o proprietário da conta pode configurar o papel IAM e executar o deploy.

## Arquitetura inicial (Bedrock desligado)

- S3 privado + SSE-S3 + CloudFront via OAC (HTTPS);
- API Gateway HTTP API + Lambda (FastAPI/Mangum), rotas `/api/*`;
- limite API: 2 requisições/s, burst 5; Lambda concurrency reservada em 2;
- Logs CloudWatch com retenção de 7 dias;
- **`SHIFT101_AI_ENABLED=false` fixo no template, sem permissão `bedrock:InvokeModel`.**

O endpoint HTTP API permanece publicamente acessível e consome recursos faturáveis, embora use dados 100% sintéticos. Não é um sistema multiusuário de produção.

## Pré-requisitos antes de executar

1. Escolher conta e região (sugestão: `us-east-1` para o MVP; a região dos modelos só será analisada no checkpoint de Bedrock).
2. Criar um **AWS Budget mensal do tipo COST**, em USD, com limite entre USD 0 e USD 10 e **ao menos uma notificação**, e guardar seu nome. Recomendação inicial: `shift101-demo-budget`, USD 5/mês e avisos em 50%, 80%, 100%. **Budget gera alertas; NÃO bloqueia cobranças.** Pode haver cobrança acima do limite.
3. Criar um provedor IAM OpenID Connect para `https://token.actions.githubusercontent.com` com audiência `sts.amazonaws.com` se não existir.
4. Criar um papel IAM **dedicado** para deploy, com relação de confiança limitada ao repositório exato e ambiente `aws-demo`. Escopar permissões de CloudFormation, IAM (criação/passagem do papel do Lambda), API Gateway, Lambda, S3 (incluindo artefatos SAM), CloudFront, CloudWatch Logs, `sts:GetCallerIdentity` e leitura do Budget. **Evitar AdministratorAccess e qualquer política irrestrita.** Para conta de produção, preferir role de serviço do CloudFormation e política revisada por administrador.
5. No repositório GitHub: **Settings → Environments → New environment**, criar `aws-demo` e definir proteção de implantação, como revisão obrigatória, quando disponível.
6. No ambiente `aws-demo`, adicionar as seguintes **variables** (não são credenciais permanentes):

| Variable | Valor |
| --- | --- |
| `AWS_DEPLOY_ROLE_ARN` | ARN do papel IAM dedicado, ex. `arn:aws:iam::<ACCOUNT_ID>:role/Shift101DemoDeploy` |
| `AWS_REGION` | Região desejada, ex. `us-east-1` |
| `AWS_ACCOUNT_ID` | ID de 12 dígitos da conta autorizada |
| `AWS_BUDGET_NAME` | Nome exato do AWS Budget mensal com notificações |

**Nota sobre confiança OIDC:** o repositório `LukeRodd/shift101` foi criado em 2026 e os claims OIDC podem trazer IDs estáveis de proprietário e repositório; workflows com ambiente usam `:environment:aws-demo` em vez de `:ref:refs/heads/main`. Conferir o `sub` efetivo do token com a [documentação atual do GitHub](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws) antes de fixar a trust policy. Não usar curingas amplos (`repo:LukeRodd/*`, `repo:*:* `, etc.).

## Executar manualmente pelo GitHub Actions

**Depois da revisão e merge dos PRs dependentes (#1 e #2) na `main`**:

1. GitHub → Actions → `Deploy Shift101 to AWS (manual)`.
2. Selecionar `Run workflow`, branch `main`.
3. Marcar `I authorize AWS resource creation and possible charges`.
4. Autorizar o ambiente `aws-demo` conforme as regras configuradas.
5. Acompanhar logs; após concluir, copiar a URL `https://*.cloudfront.net` gerada.

O workflow `.github/workflows/deploy-aws.yml` utiliza `aws-actions/configure-aws-credentials` com OIDC e credenciais de curta duração, sem armazenar access keys. Não existe deploy automático por push.

### Operação local (alternativa)

É possível executar `bash deploy/aws/deploy.sh` no próprio terminal com AWS CLI autenticado por SSO ou outra identidade de curta duração. Configure antes as variáveis:

```bash
export AWS_REGION=us-east-1
export AWS_EXPECTED_ACCOUNT_ID=SEU_ID_DE_12_DIGITOS
export AWS_BUDGET_NAME=shift101-demo-budget
export DEPLOY_ACKNOWLEDGE_CHARGES=YES
bash deploy/aws/deploy.sh
```

O script confirma a conta por `sts get-caller-identity`, consulta o AWS Budget, valida/compila SAM, executa `sam deploy` (stack `shift101-demo`), envia os assets ao S3, invalida CloudFront e testa `/api/health` e a homepage. Em caso de erro, **não** considera a implantação concluída.

## Checkpoint de publicação

| Verificação | Critério |
| --- | --- |
| CI e dependências | Pytest, `pip check`, lockfiles e `sam validate --lint` aprovados |
| Identidade | Account ID de STS é exatamente o configurado |
| Custo | Budget mensal <= USD 10 e pelo menos uma notificação; aceitabilidade de cobrança confirmada |
| Autenticação | Papel OIDC restrito a repo/ambiente; nenhuma access key armazenada |
| Backend | `GET /api/health` retorna `{"status":"ok"}` |
| Frontend | URL CloudFront entrega HTML e recursos estáticos |
| IA | `GET /api/ai/status` informa `enabled: false` |
| Dados | Somente conteúdo sintético |
| Pós-deploy | Monitorar CloudWatch, Budget e métricas básicas; documentar URL e operação de rollback |

## Desligamento

A stack CloudFormation pode ser excluída com `aws cloudformation delete-stack --stack-name shift101-demo --region us-east-1` **após** garantir que não há dependências externas e rever recursos retidos. O bucket S3 tem política `Retain` e não é apagado automaticamente; pode exigir limpeza e exclusão manual. Verifique custos e recursos remanescentes no console. É possível configurar deploy futuro controlado após o MVP.

## Referências

- [GitHub OIDC na AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)
- [GitHub Actions AWS Credentials](https://github.com/aws-actions/configure-aws-credentials)
- [AWS SAM em GitHub Actions](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/deploying-using-github.html)
- [AWS Budget por CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-budgets-budget.html)

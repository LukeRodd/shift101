# Plano de avaliação de IA (não implementado)

O protótipo não possui LLM nem RAG: a busca atual é lexical e funcionará como baseline.

Criar 30–50 incidentes sintéticos com descrição, evidências, runbook aplicável, resposta esperada, casos sem evidência e decisões de escalonamento seguro.

## Métricas
- Recall@k na recuperação de runbooks.
- Precisão de citações e correspondência com trechos recuperados.
- Taxa de respostas sem fundamento, usando rubrica humana.
- Reconhecimento de incerteza.
- Latência, custo por solicitação e qualidade pedagógica sem spoilers.

Comparar busca lexical, LLM sem contexto e LLM com RAG. Não publicar valores antes de medi-los em testes reproduzíveis.

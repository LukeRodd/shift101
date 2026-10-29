# AI Incident Mentor — implementação experimental

Este módulo é opcional e está **desabilitado por padrão**. A missão, a apostila e a avaliação continuam funcionando sem IA.

## Operação local

Instale [Ollama](https://ollama.com/) e os modelos:

```bash
ollama pull qwen2.5:1.5b
ollama pull embeddinggemma
ollama serve
```

Em outro terminal, na raiz do Shift101:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
SHIFT101_AI_ENABLED=true python -m uvicorn backend.shift101.main:app --reload
```

Abra http://127.0.0.1:8000, vá até **Apostila**, ative **Utilizar IA generativa local (RAG)** e faça uma pergunta. O modelo Ollama e o servidor devem estar operacionais na mesma máquina. No Docker, localhost do contêiner não representa o host: use a configuração de rede apropriada e, se necessário, `SHIFT101_OLLAMA_HOST=http://host.docker.internal:11434`.

Variáveis:
- `SHIFT101_AI_ENABLED`: por padrão `false`.
- `SHIFT101_OLLAMA_HOST`: por padrão `http://127.0.0.1:11434`, restrito a hosts locais.
- `SHIFT101_AI_CHAT_MODEL`: por padrão `qwen2.5:1.5b`.
- `SHIFT101_AI_EMBED_MODEL`: por padrão `embeddinggemma`.

## Funcionamento

1. O backend gera embeddings dos **quatro runbooks fictícios** e os mantém em cache de memória.
2. Recupera até dois documentos por similaridade de cosseno (limiar inicial 0,35; requer calibração).
3. Envia ao LLM apenas a pergunta, a missão, as evidências efetivamente inspecionadas e o texto recuperado.
4. O modelo é instruído a agir como tutor socrático: orientar sem entregar gabaritos.
5. As referências são selecionadas pelo backend, e não inventadas pelo modelo.
6. A avaliação continua determinística, fora do LLM.

**Limitações conhecidas:** protótipo sem autenticação, rate limiting, persistência ou avaliação de qualidade humana. Prompt injection e vazamento indireto de respostas não estão formalmente eliminados. Nenhum sistema real deve ser conectado. O limiar de recuperação é heurístico e o corpus é pequeno. Não publicar o serviço com IA na Internet sem endurecimento de segurança.

## Testes

```bash
python -m pytest -q
```

Os testes unitários de IA usam simulações, sem baixar modelos ou acessar rede. Para validar qualidade pedagógica e precisão do RAG, ainda é preciso executar avaliação com cenários sintéticos, registrar métricas e revisar respostas manualmente.

"""Entirely synthetic demonstration data, unrelated to any real infrastructure."""
MISSION = {
    "id": "demo-001", "day": 1,
    "title": "Serviço indisponível: por onde começar?",
    "site": "LAB-01 (ambiente fictício)", "priority": "P2 — Simulado", "status": "Em investigação",
    "description": "Usuários relatam que a aplicação de treinamento não abre. O painel indica que o host responde na rede, mas o serviço web apresenta erro. Seu objetivo é investigar evidências, determinar o próximo passo e registrar a decisão.",
    "actions": [
        {"id": "ping", "label": "Verificar conectividade ICMP", "result": "4 respostas recebidas, perda 0%. A conectividade IP básica está presente."},
        {"id": "http", "label": "Consultar a resposta HTTP", "result": "GET /health → HTTP 502 Bad Gateway. A aplicação não está saudável."},
        {"id": "logs", "label": "Consultar logs simulados", "result": "backend-service: upstream connection refused. Registrar evidências e escalar com o procedimento de recuperação."},
        {"id": "runbook", "label": "Consultar runbook do serviço", "result": "Runbook WEB-01: confirmar alcance IP, verificar HTTP, revisar logs e escalar antes de reinicializar."}
    ],
    "questions": [
        {"id": "q1", "text": "O ping responde, mas a página apresenta erro HTTP 502. Qual conclusão é correta?", "options": ["Toda a rede está indisponível", "O host é alcançável, mas há falha no caminho da aplicação", "O problema foi resolvido"]},
        {"id": "q2", "text": "Qual evidência diferencia conectividade IP de disponibilidade da aplicação?", "options": ["Cor da interface", "Quantidade de cabos", "Resposta HTTP e logs do serviço"]},
        {"id": "q3", "text": "Antes de sugerir uma reinicialização, qual atitude é adequada?", "options": ["Registrar evidências e consultar o procedimento", "Reiniciar tudo sem registro", "Apagar os logs"]},
        {"id": "q4", "text": "O log indica 'upstream connection refused'. O que ele sugere?", "options": ["Falha necessariamente no cabo óptico", "Problema de conexão entre proxy e serviço de origem", "Perda de energia no prédio inteiro"]},
        {"id": "q5", "text": "Qual anotação de incidente é mais útil para o escalonamento?", "options": ["Está ruim", "Não sei", "ICMP OK; HTTP 502; logs indicam falha no upstream; runbook consultado"]}
    ]
}
ANSWERS = {
    "q1": (1, "ICMP funcional não garante saúde de um serviço HTTP."),
    "q2": (2, "Resposta HTTP e logs revelam o comportamento da camada de aplicação."),
    "q3": (0, "Mudanças exigem procedimento, registro e autorização apropriada."),
    "q4": (1, "Connection refused indica que o upstream recusou a conexão; a causa precisa ser confirmada."),
    "q5": (2, "Um bom registro contém observações reproduzíveis, não palpites.")
}
RUNBOOKS = [
    {"id": "RB-ICMP-01", "title": "Conectividade básica", "text": "Um ping bem-sucedido demonstra resposta ICMP e alcance IP naquele momento. Não confirma que a aplicação HTTP funciona."},
    {"id": "RB-HTTP-02", "title": "HTTP 502", "text": "HTTP 502 Bad Gateway sugere que um gateway ou proxy recebeu resposta inválida do serviço upstream. Verifique health checks e logs da aplicação."},
    {"id": "RB-OPS-03", "title": "Escalonamento seguro", "text": "Documente horário, serviço, impacto, resultados dos testes, alterações recentes e evidências. Consulte runbooks antes de qualquer ação de mudança."},
    {"id": "RB-LOG-04", "title": "Interpretação de logs", "text": "Um erro upstream connection refused sugere falha na abertura de conexão com o serviço de origem. Investigue status do processo e configuração do proxy."}
]

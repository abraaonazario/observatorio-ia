# Copiloto Executivo: Agente de IA para a Gestão

Em resposta à necessidade de dar agilidade à tomada de decisão na Secretaria de Educação (SEDUC), o Observatório de IA documenta e prototipa a arquitetura do **Agente Especializado para a Área Executiva** (Copiloto Educacional).

Este projeto visa substituir a busca manual em dezenas de relatórios por uma interface conversacional de linguagem natural, permitindo que Secretários, Adjuntos e Diretores interajam diretamente com o Data Lake.

---

## 🚀 Experimente o Protótipo do Agente

Para demonstrar o poder da interface conversacional, eu construí este **Simulador Interativo** do Copiloto. 

*(Digite uma pergunta sobre a rede estadual de ensino ou clique em "Enviar" para testar uma simulação automática)*

<div class="chat-container">
  <div class="chat-header">
    <div class="avatar"><i class="fa-solid fa-robot"></i> IA</div>
    <div>
      <div style="font-weight: 700; color: #fff;">Copiloto Executivo (GovData)</div>
      <div style="font-size: 0.75rem; color: #34d399;">● Online - Conectado à Zona Gold</div>
    </div>
  </div>
  
  <div class="chat-messages" id="chatMessages">
    <div class="msg ai">
      Olá, Secretário(a). Sou o Copiloto de IA do Governo. Tenho acesso aos dados atualizados de Educação, Saúde e Segurança. Como posso ajudar na sua tomada de decisão hoje?
    </div>
  </div>
  <div class="typing" id="typingIndicator">O Copiloto está analisando o Data Lake...</div>
  
  <div class="chat-input-area">
    <input type="text" id="chatInput" class="chat-input" placeholder="Ex: Qual a escola com maior queda de IDEB na região norte?" autocomplete="off" onkeypress="handleKeyPress(event)">
    <button class="btn-send" onclick="sendMessage()"><i class="fa-solid fa-paper-plane"></i> Enviar</button>
  </div>
</div>

<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
<style>
  .chat-container {
    background: #09090b;
    border: 1px solid #1f2937;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    height: 450px;
    font-family: 'Inter', sans-serif;
    color: #fff;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    margin: 2rem 0;
    overflow: hidden;
  }
  .chat-header {
    background: linear-gradient(90deg, #111827, #0f172a);
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #1f2937;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .chat-header .avatar {
    width: 38px; height: 38px; background: #3b82f6; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.2rem;
  }
  .chat-messages {
    flex: 1; padding: 1.5rem; overflow-y: auto; display: flex; flex-direction: column; gap: 1rem;
  }
  .msg { max-width: 85%; padding: 1rem; border-radius: 8px; line-height: 1.5; font-size: 0.95rem; }
  .msg.user { background: #334155; align-self: flex-end; border-bottom-right-radius: 0; color: #f8fafc; }
  .msg.ai { background: rgba(30, 58, 138, 0.3); align-self: flex-start; border-bottom-left-radius: 0; border: 1px solid #1e3a8a; }
  .msg.ai .source { 
    display: inline-flex; align-items: center; gap: 6px; margin-top: 12px; font-size: 0.75rem; color: #93c5fd; 
    background: rgba(59, 130, 246, 0.1); padding: 6px 10px; border-radius: 6px; border: 1px solid rgba(59, 130, 246, 0.3); 
    text-decoration: none; font-weight: 600; cursor: pointer; transition: 0.2s;
  }
  .msg.ai .source:hover { background: rgba(59, 130, 246, 0.3); }
  .chat-input-area {
    padding: 1rem; background: #111827; border-top: 1px solid #1f2937; display: flex; gap: 10px;
  }
  .chat-input {
    flex: 1; background: #1f2937; border: 1px solid #374151; color: white; padding: 0.85rem 1rem; border-radius: 8px; outline: none; font-size: 0.95rem; font-family: 'Inter', sans-serif;
  }
  .chat-input:focus { border-color: #3b82f6; box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3); }
  .btn-send {
    background: #3b82f6; color: white; border: none; padding: 0 1.5rem; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.2s; font-size: 0.95rem; display: flex; align-items: center; gap: 8px;
  }
  .btn-send:hover { background: #2563eb; }
  .typing { color: #9ca3af; font-size: 0.85rem; font-style: italic; margin: 0 1.5rem 1rem 1.5rem; display: none; }
</style>

<script>
  function handleKeyPress(e) {
    if(e.key === 'Enter') {
      sendMessage();
    }
  }

  function sendMessage() {
    const input = document.getElementById('chatInput');
    let text = input.value.trim();
    if(!text) text = "Qual o resumo da evasão escolar na região norte?"; // Default question if empty
    
    // Add User Message
    const messages = document.getElementById('chatMessages');
    messages.innerHTML += `<div class="msg user">${text}</div>`;
    input.value = '';
    messages.scrollTop = messages.scrollHeight;
    
    // Show Typing
    const typing = document.getElementById('typingIndicator');
    typing.style.display = 'block';
    
    // Simulate AI Response after 1.5s
    setTimeout(() => {
      typing.style.display = 'none';
      const aiResponse = `
        <div class="msg ai">
          De acordo com os dados mais recentes do Data Warehouse (SEDUC), a <strong>Região Norte</strong> apresentou uma queda de <strong>12% na frequência escolar</strong> nos últimos 30 dias.<br><br>
          Cruzando esses dados com o banco da Saúde (SES), notamos um pico de 35% de atendimentos ambulatoriais por síndromes gripais na mesma região, o que justifica a ausência dos alunos.<br>
          <a href="#" class="source"><i class="fa-solid fa-table"></i> Fonte: DW_SEDUC_FREQ_2026 (Zona Gold)</a>
        </div>
      `;
      messages.innerHTML += aiResponse;
      messages.scrollTop = messages.scrollHeight;
    }, 1500);
  }
</script>

---

## Arquitetura da Solução (Agente RAG + Text-to-SQL)

Para garantir que a IA não invente dados (alucinação) e respeite a LGPD, utilizamos uma arquitetura híbrida que conecta Grandes Modelos de Linguagem (LLMs) diretamente às bases seguras do Estado.

```mermaid
graph TD
    A[Executivo / Secretário] -->|Pergunta em Linguagem Natural| B(Interface do Copiloto / Chat)
    B --> C{Motor do Agente de IA}
    
    C -->|Busca Semântica| D[RAG - Recuperação de Textos <br> Leis, Portarias, Diário Oficial]
    C -->|Text-to-SQL| E[Consulta a Dados Estruturados <br> Zona Gold do Data Lake]
    
    D --> F((Geração da Resposta <br> LLM Soberano))
    E --> F
    
    F -->|Resposta com Fontes e Gráficos| B
    
    style C fill:#071d41,color:#fff
    style F fill:#0055a4,color:#fff
```

## Componentes Técnicos

1. **LLM Base:** Utilização de um modelo de linguagem avançado (podendo ser hospedado localmente no Data Center do Estado para dados sensíveis, ou via API segura com zero-retention policy).
2. **Text-to-SQL:** A habilidade do agente de traduzir a pergunta do Secretário ("Qual o gasto total?") para uma query SQL (`SELECT SUM(gasto) FROM...`) que roda diretamente no Data Warehouse da Educação.
3. **RAG (Retrieval-Augmented Generation):** Banco de dados vetorial contendo o Plano Estadual de Educação, Diretrizes Curriculares e Atas de Reuniões, permitindo que a IA cite as leis corretas.

## Governança e Transparência (Model Card)

A implementação deste agente na área executiva segue diretrizes estritas do nosso modelo de gestão de riscos (NIST AI RMF):

* **Controle de Acesso (IAM):** O agente herda as permissões do usuário logado. Um diretor regional só consegue perguntar e receber respostas sobre a sua própria região.
* **Auditabilidade:** Todas as interações (prompts) feitas pelo alto escalão ficam registradas em um log de auditoria, garantindo a rastreabilidade das decisões tomadas com apoio da IA.
* **Verificação de Fontes (Grounding):** A interface do agente é obrigada a exibir o link direto para a fonte que gerou a resposta (ex: tabela do banco de dados), permitindo checagem técnica rigorosa.

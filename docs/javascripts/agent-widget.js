document.addEventListener("DOMContentLoaded", function () {
  // Inject Font Awesome if not present
  if (!document.querySelector('link[href*="font-awesome"]')) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css';
    document.head.appendChild(link);
  }

  // Create the Floating Button
  const btn = document.createElement('div');
  btn.id = 'govdata-agent-btn';
  btn.innerHTML = '<i class="fa-solid fa-robot"></i>';
  document.body.appendChild(btn);

  // Create the Chat Window Modal
  const chatWindow = document.createElement('div');
  chatWindow.id = 'govdata-agent-window';
  chatWindow.innerHTML = `
    <div class="agent-header">
      <div class="agent-header-left">
        <div class="avatar"><i class="fa-solid fa-robot"></i></div>
        <div>
          <div class="agent-header-title">Copiloto IA (GovData)</div>
          <div class="agent-header-status">● Online - Escopo Global</div>
        </div>
      </div>
      <button class="agent-close-btn" id="agent-close-btn"><i class="fa-solid fa-xmark"></i></button>
    </div>
    
    <div class="agent-messages" id="agent-messages">
      <div class="agent-msg ai">
        Olá! Eu sou o Copiloto da Plataforma de Governança de Dados do Estado. Estou presente em todas as páginas para tirar suas dúvidas técnicas, buscar legislações ou consultar dados da Zona Gold. O que deseja procurar?
      </div>
    </div>
    <div class="agent-typing" id="agent-typing">Procurando nos catálogos do Data Lake...</div>
    
    <div class="agent-input-area">
      <input type="text" id="agent-input" class="agent-input" placeholder="Faça sua pergunta aqui..." autocomplete="off">
      <button class="agent-btn-send" id="agent-btn-send"><i class="fa-solid fa-paper-plane"></i></button>
    </div>
  `;
  document.body.appendChild(chatWindow);

  // Interaction Logic
  const closeBtn = document.getElementById('agent-close-btn');
  const messagesArea = document.getElementById('agent-messages');
  const inputField = document.getElementById('agent-input');
  const sendBtn = document.getElementById('agent-btn-send');
  const typingIndicator = document.getElementById('agent-typing');

  // Toggle Chat Window
  btn.addEventListener('click', () => {
    chatWindow.classList.toggle('active');
    if (chatWindow.classList.contains('active')) {
      inputField.focus();
    }
  });

  // Close Chat Window
  closeBtn.addEventListener('click', () => {
    chatWindow.classList.remove('active');
  });

  // Handle Sending Messages
  function sendAgentMessage() {
    let text = inputField.value.trim();
    if (!text) text = "Como está a arrecadação este ano?"; // Exemplo padrão

    // Add User Message
    const userMsg = document.createElement('div');
    userMsg.className = 'agent-msg user';
    userMsg.textContent = text;
    messagesArea.appendChild(userMsg);
    
    inputField.value = '';
    messagesArea.scrollTop = messagesArea.scrollHeight;
    
    // Show Typing
    typingIndicator.style.display = 'block';
    
    // Simular RAG + Consulta (Resposta Fake de IA)
    setTimeout(() => {
      typingIndicator.style.display = 'none';
      const aiMsg = document.createElement('div');
      aiMsg.className = 'agent-msg ai';
      
      // Respostas randômicas baseadas em contexto da plataforma
      const responses = [
        `Baseado nos registros da <strong>SEFAZ</strong> na nossa Zona Gold, a arrecadação superou a meta em 4.5% no último trimestre.<br><a href="#" class="agent-source"><i class="fa-solid fa-database"></i> DW_SEFAZ_ARR_2026</a>`,
        `Para analisar os dados da <strong>Educação</strong>, recomendo consultar os painéis na Camada 2 (Secretarias). A evasão escolar está em monitoramento constante.<br><a href="#" class="agent-source"><i class="fa-solid fa-file-contract"></i> Plano Estadual de Educação</a>`,
        `O Data Lake possui pipelines automatizados. Se precisar solicitar acesso a novos metadados, você deve abrir um chamado no Catálogo Governamental.<br><a href="#" class="agent-source"><i class="fa-solid fa-shield"></i> Política IAM - Segurança</a>`
      ];
      
      const randomResponse = responses[Math.floor(Math.random() * responses.length)];
      aiMsg.innerHTML = randomResponse;
      
      messagesArea.appendChild(aiMsg);
      messagesArea.scrollTop = messagesArea.scrollHeight;
    }, 1200);
  }

  sendBtn.addEventListener('click', sendAgentMessage);
  inputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendAgentMessage();
  });
});

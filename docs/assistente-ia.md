---
hide:
  - navigation
  - toc
---

<script>document.body.classList.add('dashboard-page');</script>

<style>
  :root {
    --theme-color: #f59e0b; /* Laranja/Amarelo para a IA */
  }
  
  /* Reset and Layout */
  .dashboard-container {
    padding: 0 0 0 78px !important;
    margin: 90px 0 0 0 !important; /* Push down exactly 90px to stay below the fixed header */
    display: flex;
    flex-direction: row;
    height: calc(100vh - 90px);
    height: calc(100dvh - 90px);
    width: 100%;
    overflow: hidden;
    background: #0b0f19;
    font-family: 'Inter', sans-serif;
  }
  
  /* Left Sidebar */
  .ai-sidebar {
    width: 380px;
    background: #0f172a;
    border-right: 1px solid #1e293b;
    display: flex;
    flex-direction: column;
    padding: 1.5rem 1rem;
    overflow-y: auto;
    flex-shrink: 0;
  }
  
  .ai-new-chat-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
    background: transparent;
    border: 1px solid #f59e0b;
    color: #f59e0b;
    padding: 0.8rem 1rem;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 1.5rem;
    width: 100%;
  }
  .ai-new-chat-btn:hover {
    background: rgba(245, 158, 11, 0.1);
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
  }
  
  /* Left Sidebar Custom Scrollbar */
  .ai-sidebar::-webkit-scrollbar {
    width: 6px;
  }
  .ai-sidebar::-webkit-scrollbar-track {
    background: transparent;
  }
  .ai-sidebar::-webkit-scrollbar-thumb {
    background: #1e293b;
    border-radius: 4px;
  }
  .ai-sidebar::-webkit-scrollbar-thumb:hover {
    background: #334155;
  }

  /* Section title for history */
  .ai-history-title {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #475569;
    font-weight: 700;
    margin: 0.5rem 0 0.5rem 0.5rem;
  }
  
  .ai-history-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .ai-history-item {
    color: #94a3b8;
    font-size: 0.88rem;
    padding: 0.8rem 1rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    overflow: hidden;
    width: 100%;
    border: 1px solid transparent;
  }
  .ai-history-item span {
    flex: 1;
    line-height: 1.4;
  }
  .ai-history-item:hover {
    background: rgba(255, 255, 255, 0.04);
    color: #f1f5f9;
  }
  .ai-history-item.active {
    background: rgba(245, 158, 11, 0.1);
    color: #fbbf24;
    border-color: rgba(245, 158, 11, 0.25);
    font-weight: 500;
  }
  .ai-history-item.active svg {
    color: #fbbf24;
  }

  /* Chat Messages CSS */
  .ai-chat-messages {
    display: flex;
    width: 100%;
    max-width: 1000px;
    flex-direction: column;
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .ai-message {
    display: flex;
    gap: 1rem;
    width: 100%;
    animation: fadeIn 0.3s ease;
  }
  
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  
  .ai-message.user {
    justify-content: flex-end;
  }
  
  .ai-message-avatar {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  
  .ai-message.assistant .ai-message-avatar {
    background: linear-gradient(135deg, #f59e0b, #fbbf24);
    color: #0f172a;
  }
  
  .ai-message.user .ai-message-avatar {
    background: #3b82f6;
    color: #ffffff;
    order: 2;
  }
  
  .ai-message-bubble {
    max-width: 80%;
    padding: 1rem 1.25rem;
    border-radius: 14px;
    font-size: 0.95rem;
    line-height: 1.5;
    color: #e2e8f0;
  }
  
  .ai-message.assistant .ai-message-bubble {
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid #1e293b;
    border-top-left-radius: 2px;
  }
  
  .ai-message.user .ai-message-bubble {
    background: #2563eb;
    border-top-right-radius: 2px;
    color: #ffffff;
  }
  
  /* Collapsible Sidebar Styles */
  .ai-sidebar-toggle {
    position: absolute;
    top: 1.5rem;
    left: 1.5rem;
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid #1e293b;
    color: #cbd5e1;
    border-radius: 8px;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 100;
    transition: all 0.2s;
  }
  .ai-sidebar-toggle:hover {
    background: rgba(30, 41, 59, 0.9);
    border-color: #f59e0b;
    color: #f8fafc;
  }
  
  /* Sidebar state transitions */
  .ai-sidebar {
    transition: width 0.3s ease, padding 0.3s ease, border-color 0.3s ease;
  }
  
  .ai-sidebar.collapsed {
    width: 0 !important;
    padding: 1.5rem 0 !important;
    border-right-color: transparent !important;
    overflow: hidden;
  }
  
  /* Typing Indicator */
  .typing-indicator {
    display: flex;
    gap: 4px;
    padding: 4px 8px;
    align-items: center;
  }
  .typing-indicator span {
    width: 6px;
    height: 6px;
    background-color: #cbd5e1;
    border-radius: 50%;
    display: inline-block;
    animation: typing 1.4s infinite ease-in-out both;
  }
  .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
  .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
  
  @keyframes typing {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1.0); }
  }
  
  /* Main Chat Area Wrapper */
  .ai-main-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    position: relative;
    background: #0b0f19;
    overflow: hidden;
  }
  
  /* Scrollable Content Area */
  .ai-main-scroll {
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
  }
  
  /* Empty state layout centering (Astra model) */
  .ai-main-wrapper.empty-state {
    justify-content: center;
  }
  .ai-main-wrapper.empty-state .ai-main-scroll {
    display: none;
  }
  .ai-main-wrapper.empty-state .ai-input-area {
    margin: 0 auto;
    width: 100%;
    max-width: 1000px;
    padding: 2rem;
    box-sizing: border-box;
  }

  /* Welcome Header (Astra Model) */
  .ai-welcome-header {
    display: none;
    text-align: left;
    width: 100%;
    max-width: 1000px;
    margin-bottom: 1.5rem;
    padding-left: 0.2rem;
    animation: fadeIn 0.4s ease;
  }
  .ai-main-wrapper.empty-state .ai-welcome-header {
    display: block;
  }
  .ai-welcome-title {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin: 0 0 0.3rem 0 !important;
    font-family: 'Inter', sans-serif;
    letter-spacing: -0.5px;
  }
  .ai-welcome-subtitle {
    font-size: 1rem;
    font-weight: 400;
    color: #94a3b8;
    margin: 0 0 0.5rem 0;
    font-family: 'Inter', sans-serif;
    line-height: 1.5;
  }

  /* Input area at Bottom */
  .ai-input-area {
    width: 100%;
    padding: 1rem 2rem 2rem 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    background: linear-gradient(transparent, #0b0f19 20%);
    z-index: 10;
    box-sizing: border-box;
  }
  
  .ai-input-container {
    width: 100%;
    max-width: 1000px;
    background: #181c26;
    border: 1px solid #272d3d;
    border-radius: 20px;
    padding: 1.2rem;
    display: flex;
    flex-direction: column;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    box-sizing: border-box;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  .ai-input-container:focus-within {
    border-color: #f59e0b;
    box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.15);
  }
  
  .ai-input {
    width: 100%;
    background: transparent;
    border: none;
    color: #f8fafc;
    font-size: 1.05rem;
    outline: none;
    resize: none;
    font-family: 'Inter', sans-serif;
    min-height: 24px;
    max-height: 150px;
    overflow-y: auto;
    line-height: 1.5;
  }
  .ai-input::placeholder { color: #475569; }
  
  /* Input tools row */
  .ai-input-tools {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin-top: 0.8rem;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    padding-top: 0.8rem;
  }
  
  .ai-tools-left, .ai-tools-right {
    display: flex;
    align-items: center;
    gap: 0.6rem;
  }
  
  .ai-tool-btn-circle {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: #94a3b8;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
  }
  .ai-tool-btn-circle:hover {
    background: rgba(255,255,255,0.08);
    color: #ffffff;
  }
  
  .ai-tool-pill-btn {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: #cbd5e1;
    padding: 0.4rem 0.9rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }
  .ai-tool-pill-btn:hover {
    background: rgba(255,255,255,0.08);
    color: #ffffff;
  }
  .ai-tool-pill-btn.active {
    background: rgba(245, 158, 11, 0.1);
    border-color: rgba(245, 158, 11, 0.3);
    color: #f59e0b;
  }
  
  .ai-model-label {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: #475569;
    padding: 0.4rem 0.6rem;
    border-radius: 8px;
    cursor: pointer;
    transition: color 0.2s;
  }
  .ai-model-label:hover {
    color: #94a3b8;
  }
  
  .ai-send-btn-new {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #f59e0b;
    border: none;
    color: #0b0f19;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
  }
  .ai-send-btn-new:hover {
    background: #fbbf24;
    transform: scale(1.05);
  }
  
  /* Shortcut Pills (below input container) */
  .ai-action-pills {
    display: none;
    justify-content: center;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-top: 1.5rem;
    width: 100%;
    max-width: 1000px;
    animation: fadeIn 0.4s ease;
  }
  .ai-main-wrapper.empty-state .ai-action-pills {
    display: flex;
  }
  
  .ai-pill-btn {
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 0.6rem 1.2rem;
    border-radius: 20px;
    color: #cbd5e1;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
  }
  .ai-pill-btn:hover {
    background: rgba(30, 41, 59, 0.8);
    border-color: #f59e0b;
    color: #ffffff;
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(0,0,0,0.25);
  }
  
  .ai-input-footer {
    margin-top: 1rem;
    font-size: 0.75rem;
    color: #475569;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
  }

  @media (max-width: 768px) {
    .dashboard-container {
      padding-left: 0 !important;
    }
    
    .ai-sidebar {
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 100% !important;
      max-width: 300px;
      z-index: 1000;
      box-shadow: 4px 0 15px rgba(0,0,0,0.5);
    }
    
    .ai-sidebar.collapsed {
      width: 0 !important;
      padding: 1.5rem 0 !important;
      border-right-color: transparent !important;
    }

    /* Move toggle button to right to avoid being covered by sidebar if possible, 
       or just keep it left. We will add a close button inside sidebar. */
    .ai-sidebar-toggle {
      top: 1rem;
      right: 1rem;
      left: auto;
    }

    .ai-input-area {
      padding: 1rem 0.5rem;
    }

    .ai-action-pills {
      flex-direction: row;
      flex-wrap: nowrap;
      overflow-x: auto;
      justify-content: flex-start;
      width: 100%;
      padding-bottom: 0.5rem;
    }
    
    /* Esconde barra de rolagem mas permite scroll */
    .ai-action-pills::-webkit-scrollbar {
      height: 4px;
    }
    .ai-action-pills::-webkit-scrollbar-thumb {
      background: rgba(255,255,255,0.1);
      border-radius: 4px;
    }

    .ai-pill-btn {
      width: auto;
      flex-shrink: 0;
      white-space: nowrap;
    }

    .ai-welcome-title {
      font-size: 1.5rem !important;
    }

    .ai-welcome-subtitle {
      font-size: 0.85rem;
    }
    
    .ai-input-tools {
      flex-direction: column;
      align-items: stretch;
      gap: 1rem;
    }
    
    .ai-tools-left {
      justify-content: center;
    }
    
    .ai-tools-right {
      justify-content: space-between;
    }
    
    .ai-sidebar-mobile-close {
      display: flex !important;
    }
  }
  
  .ai-sidebar-mobile-close {
    display: none;
    position: absolute;
    top: 1rem;
    right: 1rem;
    width: 32px;
    height: 32px;
    background: rgba(255,255,255,0.1);
    border-radius: 8px;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: #fff;
  }
</style>

<!-- O MESMO MENU DOS DASHBOARDS! -->
<!-- Menu Lateral do Dashboard -->
<aside class="pbi-sidebar">
  <!-- Home -->
  <div class="pbi-nav-btn" title="Início" onclick="window.location.href='../'" style="cursor:pointer;">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
    <span class="nav-label">Início</span>
  </div>
  <div style="width:52px; height:1px; background:rgba(255,255,255,0.15); margin: 2px 0;"></div>
  
  <!-- Saúde -->
  <div class="pbi-nav-btn theme-saude" title="Saúde" onclick="window.location.href='../saude/'" style="cursor:pointer;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#22d3ee" stroke-width="2.5"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>
    <span class="nav-label" style="color:#22d3ee;">Saúde</span>
  </div>
  
  <!-- Educação -->
  <div class="pbi-nav-btn theme-edu" title="Educação" onclick="window.location.href='../educacao/'" style="cursor:pointer;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2.5"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
    <span class="nav-label" style="color:#a78bfa;">Educação</span>
  </div>
  
  <!-- Segurança -->
  <div class="pbi-nav-btn theme-seg" title="Segurança" onclick="window.location.href='../seguranca/'" style="cursor:pointer;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fb923c" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
    <span class="nav-label" style="color:#fb923c;">Segurança</span>
  </div>
  
  <!-- Infraestrutura -->
  <div class="pbi-nav-btn theme-inf" title="Infraestrutura" onclick="window.location.href='../infraestrutura/'" style="cursor:pointer;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#facc15" stroke-width="2.5"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
    <span class="nav-label" style="color:#facc15;">Infraest.</span>
  </div>
  
  <!-- Finanças -->
  <div class="pbi-nav-btn theme-fin" title="Finanças" onclick="window.location.href='../financas/'" style="cursor:pointer;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2.5"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
    <span class="nav-label" style="color:#4ade80;">Finanças</span>
  </div>
  
  <!-- Social -->
  <div class="pbi-nav-btn theme-soc" title="Social" onclick="window.location.href='../assistencia/'" style="cursor:pointer;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f472b6" stroke-width="2.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
    <span class="nav-label" style="color:#f472b6;">Social</span>
  </div>

  <!-- Assistente IA -->
  <div class="pbi-nav-btn theme-saude active" title="Assistente IA" onclick="window.location.href='../assistente-ia/'" style="cursor:pointer; margin-top: auto;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#22d3ee" stroke-width="2.5"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
    <span class="nav-label" style="color:#22d3ee;">Assis. IA</span>
  </div>
  
  <!-- Mapa -->
  <div class="pbi-nav-btn theme-fin" title="Mapa de Ativos" onclick="window.location.href='../mapa-ativos/'" style="cursor:pointer;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
    <span class="nav-label" style="color:#4ade80;">Mapa</span>
  </div>
  
  <!-- Settings at bottom -->
  <div class="pbi-nav-btn" style="margin-bottom:6px;" title="Configurações">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
    <span class="nav-label">Config.</span>
  </div>
</aside>

  <!-- Painel Lateral Esquerdo -->
  <aside class="ai-sidebar" id="ai-sidebar-element">
    <script>
      if (window.innerWidth <= 768) {
        document.getElementById('ai-sidebar-element').classList.add('collapsed');
      }
    </script>
    <div class="ai-sidebar-mobile-close" id="ai-sidebar-mobile-close">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
    </div>
    <button class="ai-new-chat-btn">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
      Nova Conversa
    </button>
    <div class="ai-history-title">Conversas Recentes</div>
    <div class="ai-history-list">
      <div class="ai-history-item">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        <span>Qual é a situação atual da saúde no estado?</span>
      </div>
      <div class="ai-history-item">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        <span>Compare os indicadores de educação com as metas</span>
      </div>
      <div class="ai-history-item">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        <span>Resumo do investimento em infraestrutura em 2024</span>
      </div>
      <div class="ai-history-item">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        <span>Alertas da Segurança Pública</span>
      </div>
      <div class="ai-history-item">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        <span>Diretrizes do Planejamento Estratégico</span>
      </div>
    </div>
  </aside>

  <!-- Área Central do Chat -->
  <main class="ai-main-wrapper empty-state">
    <!-- Botão de recolher/expandir sidebar -->
    <button class="ai-sidebar-toggle" id="ai-sidebar-toggle" title="Menu de Histórico">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
    </button>
    
    <div class="ai-main-scroll">
      <!-- Container de Mensagens Ativas -->
      <div id="ai-chat-messages" class="ai-chat-messages"></div>
    </div>

    <!-- Barra de Digitação (Chat Input) Fixada na Base -->
    <div class="ai-input-area">
      
      <!-- Welcome Header (only visible in empty-state) -->
      <div class="ai-welcome-header">
        <h1 class="ai-welcome-title">Olá!</h1>
        <p class="ai-welcome-subtitle">MT 360º | Central de Dados Unificados de Mato Grosso</p>
      </div>

      <div class="ai-input-container">
        <!-- Top Row: Textarea -->
        <textarea class="ai-input" placeholder="Pergunte ao Assistente..." rows="1"></textarea>
        
        <!-- Bottom Row: Tools -->
        <div class="ai-input-tools">
          <div class="ai-tools-left">
            <button class="ai-tool-btn-circle" title="Adicionar arquivo ou contexto">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
            </button>
            <button class="ai-tool-pill-btn active" title="Pesquisar na Web">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
              <span>Pesquisa web</span>
            </button>
          </div>
          <div class="ai-tools-right">
            <div class="ai-model-label">
              <span>MT-IA</span>
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
            </div>
            <button class="ai-send-btn-new" title="Enviar mensagem">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Action Pills (only visible in empty-state) -->
      <div class="ai-action-pills">
        <button class="ai-pill-btn" data-query="saude">
          <span>🏥 Análise de Saúde</span>
        </button>
        <button class="ai-pill-btn" data-query="evasao">
          <span>🎓 Metas de Educação</span>
        </button>
        <button class="ai-pill-btn" data-query="seguranca">
          <span>🛡️ Alertas de Segurança</span>
        </button>
        <button class="ai-pill-btn" data-query="infraestrutura">
          <span>🏗️ Obras de Infraestrutura</span>
        </button>
        <button class="ai-pill-btn" data-query="planejamento">
          <span>📊 Diretrizes de Planejamento</span>
        </button>
      </div>

      <div class="ai-input-footer">IA especializada em indicadores públicos · Feito para o MT</div>
    </div>
  </main>
</div>

<script>
document.addEventListener("DOMContentLoaded", function() {
  const sidebar = document.querySelector('.ai-sidebar');
  const sidebarToggle = document.getElementById('ai-sidebar-toggle');
  const sidebarMobileClose = document.getElementById('ai-sidebar-mobile-close');
  const newChatBtn = document.querySelector('.ai-new-chat-btn');
  const historyItems = document.querySelectorAll('.ai-history-item');
  const chatMessages = document.getElementById('ai-chat-messages');
  const welcomeHeader = document.querySelector('.ai-header-content');
  const chatInput = document.querySelector('.ai-input');
  const sendBtn = document.querySelector('.ai-send-btn-new');
  const mainScroll = document.querySelector('.ai-main-scroll');
  const mainWrapper = document.querySelector('.ai-main-wrapper');
  
  // Collapse sidebar on mobile by default
  if (window.innerWidth <= 768) {
    sidebar.classList.add('collapsed');
  }

  // Toggle Sidebar
  sidebarToggle.addEventListener('click', function() {
    sidebar.classList.toggle('collapsed');
  });

  // Mobile close button
  sidebarMobileClose.addEventListener('click', function() {
    sidebar.classList.add('collapsed');
  });

  // Auto collapse sidebar on mobile when interacting
  function autoCollapseSidebar() {
    if (window.innerWidth <= 768) {
      sidebar.classList.add('collapsed');
    }
  }

  // Simulated Answers database
  const responses = {
    saude: `A situação da saúde em Mato Grosso mostra avanços consistentes em agosto de 2024:

* 🛏️ **Leitos Disponíveis:** Chegou a **4.800 leitos**, representando uma alta de +3,4% vs. mês anterior.
* 🏥 **Atendimentos/mês:** Atingiu **24.000 atendimentos**, com expansão de +5,2%.
* 💉 **Cobertura Vacinal:** Mantém-se elevada em **95%**.
* ⏳ **Tempo Médio de Espera:** Reduziu para **28 minutos** (melhoria de -12% vs. mês anterior).

Os indicadores de alerta mostram a ocupação de leitos de UTI estável em **72%** (meta < 80%). Contudo, a taxa de mortalidade infantil está em **12,3%** (acima da meta de < 10%), exigindo foco estratégico nas ações de atenção básica do estado.`,

    evasao: `Os indicadores de Educação indicam:

* 🎓 **Matrículas:** Totalizam **340.000** alunos ativos.
* 📈 **Taxa de Aprovação:** Atingiu **89%**, em crescimento contínuo desde o início do ano.
* ⚠️ **Evasão Escolar:** Está em **2,1%**, mantendo-se dentro da meta de tolerância do estado (2,5%).

As ações do programa de busca ativa escolar e apoio financeiro a famílias vulneráveis têm ajudado a manter o abandono escolar nos menores patamares históricos recentes.`,

    seguranca: `No setor de Segurança Pública em Mato Grosso:

* 🛡️ **Índice de Ocorrências:** Teve redução para **1.420 casos** registrados no mês (-5,3% vs. mês anterior).
* 🔍 **Taxa de Resolução:** Aumentou para **80%** das investigações concluídas no período.
* 📉 **Crimes Contra a Vida:** O indicador consolidado está em **2,55 por mil habitantes**, em tendência de queda desde 2020.

Os alertas críticos apontam a necessidade de ampliação do patrulhamento comunitário nas divisas do estado e fortalecimento de canais de atendimento à mulher.`,

    infraestrutura: `Em relação à Infraestrutura no ano de 2024:

* 🏗️ **Investimento Consolidado:** O estado aplicou **R$ 1,2 Bilhões** em obras rodoviárias e de saneamento básico.
* 🛣️ **Obras Rodoviárias:** Cerca de **850 km de estradas** foram pavimentadas ou receberam recapeamento completo.
* 💧 **Saneamento:** A rede de coleta de esgoto e água encanada expandiu 8% no interior do estado.`,

    meta: `No painel consolidado atual, os indicadores que estão abaixo da meta ou em estado de alerta são:

1. ⚠️ **Mortalidade Infantil (Saúde):** Registrado **12,3%** (Meta: < 10%).
2. ⚠️ **Acreditação Hospitalar (Saúde):** Hospitais com acreditação em **38%** (Meta: > 50%).
3. ⚠️ **Tempo de Resposta Policial (Segurança):** Em algumas regiões periféricas está em **18 minutos** (Meta: < 15 minutos).

Por outro lado, leitos de UTI (72%), cobertura vacinal (95%) e taxa de evasão escolar (2,1%) estão operando de forma saudável dentro das metas governamentais.`,

    default: `Olá! Sou o Assistente Estratégico de IA do MT 360º. Posso te fornecer análises, resumos e tendências sobre os principais setores públicos do estado:

* 🏥 **Saúde** (Leitos, atendimentos, mortalidade, vacinação)
* 🎓 **Educação** (Matrículas, aprovação, evasão escolar)
* 🛡️ **Segurança** (Crimes contra a vida, resolução de ocorrências)
* 🏗️ **Infraestrutura** (Investimentos e obras rodoviárias)
* 📊 **Planejamento** (Diretrizes estratégicas e metas do PPA)

Como posso te ajudar hoje?`,

    planejamento: `O **Planejamento Estratégico de Mato Grosso (PPA 2024-2027)** foca em resultados integrados e eficiência fiscal:

* 📈 **Execução de Metas do PPA:** Atingiu **87% de conformidade** física e financeira nas ações programadas para o ciclo anual.
* 🏛️ **Modernização da Gestão:** Integração de **100% das secretarias** ao sistema unificado de monitoramento de metas (SIGPAS e sistemas internos).
* 💼 **Gestão de Recursos:** Investimento recorde em capital humano e infraestrutura governamental, com economia de custeio de **R$ 240 milhões** via reengenharia de processos.
* 👥 **Participação Popular:** Realização de consultas públicas e audiências para o planejamento participativo, engajando mais de **15.000 cidadãos** nas decisões orçamentárias.

Os alertas de planejamento recomendam foco contínuo na agilização de licenciamentos e processos licitatórios nas áreas de saneamento e educação.`
  };

  // Helper to add a message bubble
  function addMessage(text, sender) {
    if (mainWrapper.classList.contains('empty-state')) {
      mainWrapper.classList.remove('empty-state');
      chatMessages.style.display = 'flex';
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `ai-message ${sender}`;
    
    // Avatar
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'ai-message-avatar';
    if (sender === 'user') {
      avatarDiv.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>`;
    } else {
      avatarDiv.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path></svg>`;
    }

    // Bubble
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'ai-message-bubble';
    
    // Format markdown-like bullet points to HTML
    let formattedText = text
      .replace(/\n/g, '<br>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\* (.*?)(<br>|$)/g, '<li>$1</li>');
      
    // Wrap lists nicely if they contain <li> tags
    if (formattedText.includes('<li>')) {
      formattedText = formattedText.replace(/(<li>.*?<\/li>)+/g, '<ul>$&</ul>');
    }

    bubbleDiv.innerHTML = formattedText;
    
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(bubbleDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    mainScroll.scrollTop = mainScroll.scrollHeight;
    
    return messageDiv;
  }

  // Handle bot typing indicator and response
  function handleBotResponse(query) {
    // Show typing indicator
    const typingMessage = document.createElement('div');
    typingMessage.className = 'ai-message assistant';
    typingMessage.innerHTML = `
      <div class="ai-message-avatar">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path></svg>
      </div>
      <div class="ai-message-bubble">
        <div class="typing-indicator">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    `;
    chatMessages.appendChild(typingMessage);
    mainScroll.scrollTop = mainScroll.scrollHeight;

    // Select response based on keywords
    const lowerQuery = query.toLowerCase();
    let responseText = responses.default;
    
    if (lowerQuery.includes('saude') || lowerQuery.includes('saúde') || lowerQuery.includes('leito') || lowerQuery.includes('atendimento')) {
      responseText = responses.saude;
    } else if (lowerQuery.includes('evasao') || lowerQuery.includes('evasão') || lowerQuery.includes('educa') || lowerQuery.includes('matrícula') || lowerQuery.includes('escola')) {
      responseText = responses.evasao;
    } else if (lowerQuery.includes('seguran') || lowerQuery.includes('crime') || lowerQuery.includes('políc') || lowerQuery.includes('ocorrência')) {
      responseText = responses.seguranca;
    } else if (lowerQuery.includes('infra') || lowerQuery.includes('obra') || lowerQuery.includes('saneamento') || lowerQuery.includes('estrada')) {
      responseText = responses.infraestrutura;
    } else if (lowerQuery.includes('meta') || lowerQuery.includes('alerta') || lowerQuery.includes('crítico')) {
      responseText = responses.meta;
    } else if (lowerQuery.includes('planeja') || lowerQuery.includes('ppa') || lowerQuery.includes('diretriz') || lowerQuery.includes('estratégico')) {
      responseText = responses.planejamento;
    }

    // Simulate typing delay
    setTimeout(() => {
      typingMessage.remove();
      addMessage(responseText, 'assistant');
    }, 1200);
  }

  // Send message handler
  function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;
    
    addMessage(text, 'user');
    chatInput.value = '';
    chatInput.style.height = '24px'; // Reset height
    handleBotResponse(text);
  }

  // Event Listeners
  sendBtn.addEventListener('click', sendMessage);
  chatInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Auto-grow textarea
  chatInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
  });

  // New Chat btn
  newChatBtn.addEventListener('click', function() {
    chatMessages.innerHTML = '';
    chatMessages.style.display = 'none';
    mainWrapper.classList.add('empty-state');
    chatInput.value = '';
    chatInput.style.height = '24px'; // Reset height
    document.querySelectorAll('.ai-history-item').forEach(i => i.classList.remove('active'));
    autoCollapseSidebar();
  });

  // History items click
  historyItems.forEach(item => {
    item.addEventListener('click', function() {
      document.querySelectorAll('.ai-history-item').forEach(i => i.classList.remove('active'));
      this.classList.add('active');
      
      const queryText = this.querySelector('span').textContent.trim();
      chatMessages.innerHTML = '';
      addMessage(queryText, 'user');
      chatInput.value = '';
      chatInput.style.height = '24px'; // Reset height
      handleBotResponse(queryText);
      autoCollapseSidebar();
    });
  });

  // Pill buttons click
  document.querySelectorAll('.ai-pill-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const queryType = this.getAttribute('data-query');
      let queryText = "";
      if (queryType === 'saude') queryText = "Qual é a situação atual da saúde no estado?";
      else if (queryType === 'evasao') queryText = "Como está a taxa de evasão escolar?";
      else if (queryType === 'seguranca') queryText = "Quais indicadores de segurança estão abaixo da meta?";
      else if (queryType === 'infraestrutura') queryText = "Resumo do investimento em infraestrutura em 2024";
      else if (queryType === 'planejamento') queryText = "Quais são as diretrizes do planejamento estratégico?";
      
      if (queryText) {
        addMessage(queryText, 'user');
        chatInput.value = '';
        chatInput.style.height = '24px';
        handleBotResponse(queryText);
      }
    });
  });
});
</script>
  </main>
</div>

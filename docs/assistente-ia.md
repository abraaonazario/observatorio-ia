---
hide:
  - navigation
  - toc
  - footer
---

<script>document.body.classList.add('dashboard-page');</script>

<style>
  :root {
    --theme-color: #f59e0b; /* Laranja/Amarelo para a IA */
  }
  
  /* Reset and Layout */
  .dashboard-container {
    position: fixed !important;
    top: 90px !important;
    left: 78px !important; /* Pula a pbi-sidebar principal */
    right: 0 !important;
    bottom: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    display: grid !important;
    grid-template-columns: 260px 1fr !important;
    height: calc(100vh - 90px) !important;
    width: calc(100% - 78px) !important;
    overflow: hidden !important;
    background: #0b0f19 !important;
    font-family: 'Inter', sans-serif;
  }
  
  /* Left Sidebar */
  .ai-sidebar {
    width: 100%;
    background: #0f172a;
    border-right: 1px solid #1e293b;
    display: flex;
    flex-direction: column;
    padding: 1.5rem 1rem;
    overflow-y: auto;
  }
  
  .ai-sidebar-logo {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 2rem;
    padding-left: 0.5rem;
  }
  .ai-sidebar-logo-icon {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #f59e0b, #fbbf24);
  }
  .ai-sidebar-logo-text {
    display: flex;
    flex-direction: column;
  }
  .ai-sidebar-logo-text strong {
    color: #fff;
    font-size: 1rem;
    line-height: 1.2;
  }
  .ai-sidebar-logo-text span {
    color: #94a3b8;
    font-size: 0.75rem;
  }
  
  .ai-new-chat-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
    background: #1e293b;
    border: none;
    color: #f8fafc;
    padding: 0.8rem 1rem;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 0.5rem;
    width: 100%;
  }
  .ai-new-chat-btn:hover {
    background: #334155;
  }
  .ai-sidebar-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
    background: transparent;
    border: 1px solid #1e293b;
    color: #94a3b8;
    padding: 0.8rem 1rem;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 1.5rem;
    width: 100%;
  }
  .ai-sidebar-btn:hover {
    background: #1e293b;
    color: #f8fafc;
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

  /* Section title for history */
  .ai-history-title {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #475569;
    font-weight: 700;
    margin: 1.5rem 0 0.5rem 0.5rem;
  }
  
  .ai-history-list {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
  }
  .ai-history-item {
    color: #94a3b8;
    font-size: 0.85rem;
    padding: 0.6rem 0.8rem;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .ai-history-item:hover {
    background: rgba(255, 255, 255, 0.04);
    color: #f1f5f9;
  }
  .ai-history-item.active {
    background: rgba(245, 158, 11, 0.1);
    color: #fbbf24;
    font-weight: 500;
  }
  


  /* Chat Messages CSS */
  .ai-chat-messages {
    display: flex;
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    flex-direction: column;
    gap: 1.5rem;
    padding-bottom: 2rem;
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
  
  /* Top Breadcrumb Header */
  .ai-top-header {
    width: 100%;
    padding: 1rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    background: #0b0f19;
    z-index: 20;
  }
  .ai-breadcrumb {
    color: #64748b;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }
  .ai-breadcrumb strong {
    color: #cbd5e1;
    font-weight: 500;
  }
  .ai-top-actions {
    display: flex;
    gap: 1rem;
    color: #64748b;
  }
  .ai-top-actions svg {
    cursor: pointer;
  }

  /* Main Chat Area Wrapper */
  .ai-main-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    position: relative;
    background: #0b0f19;
    overflow: hidden;
    height: 100%;
  }
  
  /* Scrollable Content Area */
  .ai-main-scroll {
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    padding: 2rem;
    transition: all 0.3s;
  }
  
  /* Empty state layout centering */
  .ai-main-wrapper.empty-state {
    justify-content: center;
    align-items: center;
  }
  .ai-main-wrapper.empty-state .ai-main-scroll {
    flex: 0 0 auto;
    width: 100%;
    justify-content: center;
    align-items: center;
    padding-bottom: 0;
  }
  .ai-main-wrapper.empty-state .ai-chat-messages {
    display: none;
  }

  /* Welcome Header */
  .ai-welcome-header {
    display: none;
    text-align: center;
    width: 100%;
    max-width: 800px;
    margin: 0 auto 1.5rem auto;
    animation: fadeIn 0.4s ease;
  }
  .ai-main-wrapper.empty-state .ai-welcome-header {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .ai-welcome-icon {
    width: 56px;
    height: 56px;
    background: linear-gradient(135deg, #a3e635, #22c55e); /* Greenish gradient from mockup */
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    margin-bottom: 1rem;
    box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
  }
  
  .ai-welcome-subtitle {
    font-size: 0.95rem;
    font-weight: 500;
    color: #94a3b8;
    margin: 0 0 0.2rem 0;
    font-family: 'Inter', sans-serif;
    text-align: center;
  }
  .ai-welcome-title {
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin: 0 !important;
    font-family: 'Inter', sans-serif;
    letter-spacing: -0.5px;
    text-align: center;
  }

  /* Input area at Bottom / Center */
  .ai-input-area {
    width: 100%;
    padding: 1rem 2rem 2rem 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #0b0f19;
    z-index: 10;
    box-sizing: border-box;
    position: sticky;
    bottom: 0;
    margin-top: auto;
    transition: all 0.3s;
  }
  .ai-main-wrapper.empty-state .ai-input-area {
    margin-top: 0;
    padding-top: 0;
  }
  
  .ai-input-container {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    background: #181c26;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1.2rem 1.2rem 0.8rem 1.2rem;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    box-sizing: border-box;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  .ai-input-container:focus-within {
    border-color: #3b82f6;
  }
  
  .ai-input {
    width: 100%;
    background: transparent;
    border: none;
    color: #f8fafc;
    font-size: 1rem;
    outline: none;
    resize: none;
    font-family: 'Inter', sans-serif;
    min-height: 48px;
    max-height: 150px;
    overflow-y: auto;
    line-height: 1.5;
    margin-bottom: 0.5rem;
  }
  .ai-input::placeholder { color: #64748b; }
  
  .ai-input-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
  }
  .ai-input-tools {
    display: flex;
    gap: 0.8rem;
    color: #64748b;
  }
  .ai-input-tools svg {
    cursor: pointer;
  }
  
  .ai-send-btn-new {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #334155;
    border: none;
    color: #f8fafc;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
  }
  .ai-send-btn-new:hover {
    background: #475569;
  }
  .ai-send-btn-new.active {
    background: #3b82f6;
  }

  /* Shortcut Pills */
  .ai-suggestion-grid {
    display: none;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.6rem;
    width: 100%;
    max-width: 800px;
    margin: 1rem auto 0 auto;
    animation: fadeIn 0.4s ease;
  }
  .ai-main-wrapper.empty-state .ai-suggestion-grid {
    display: flex;
  }
  
  .ai-suggestion-card {
    background: transparent;
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: 0.5rem 1rem;
    color: #94a3b8;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
  }
  .ai-suggestion-card:hover {
    background: rgba(255,255,255,0.05);
    color: #e2e8f0;
    border-color: rgba(255,255,255,0.3);
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
      left: 0 !important;
      width: 100% !important;
      top: 48px !important; /* height of mobile mkdocs header */
      height: calc(100vh - 48px) !important;
      grid-template-columns: 1fr !important;
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
      transform: translateX(-100%);
      transition: transform 0.3s ease;
    }
    
    .ai-sidebar.active {
      transform: translateX(0);
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

<div class="dashboard-container">
  <!-- Painel Lateral Esquerdo -->
  <aside class="ai-sidebar" id="ai-sidebar-element">
    <div class="ai-sidebar-mobile-close" id="mobile-close-sidebar">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
    </div>
    <div class="ai-sidebar-logo">
      <div class="ai-sidebar-logo-icon"></div>
      <div class="ai-sidebar-logo-text">
        <strong>Assistente</strong>
        <span>Inteligência de Dados</span>
      </div>
    </div>
    
    <button class="ai-new-chat-btn">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
      Nova Conversa
    </button>
    <button class="ai-sidebar-btn">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="3" x2="9" y2="21"></line></svg>
      Todos os Paineis
    </button>
    
    <div class="ai-history-title">Conversas Recentes</div>
    <div class="ai-history-list">
      <div class="ai-history-item">
        <span>Qual é a situação atual da saúde?</span>
      </div>
      <div class="ai-history-item">
        <span>Compare os indicadores de educação</span>
      </div>
      <div class="ai-history-item">
        <span>Resumo do investimento em 2024</span>
      </div>
      <div class="ai-history-item">
        <span>Alertas da Segurança Pública</span>
      </div>
      <div class="ai-history-item">
        <span>Diretrizes do Planejamento</span>
      </div>
    </div>
  </aside>

  <!-- Área Central do Chat -->
  <main class="ai-main-wrapper empty-state">
    
    <!-- Top Header -->
    <div class="ai-top-header">
      <div class="ai-breadcrumb">
        <span id="mobile-open-sidebar" style="display:none; cursor:pointer; margin-right:12px;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        </span>
        <span>Assistente</span> > <strong>Nova Conversa</strong>
      </div>
      <div class="ai-top-actions">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
      </div>
    </div>

    <div class="ai-main-scroll">
      <!-- Welcome Header (only visible in empty-state) -->
      <div class="ai-welcome-header">
        <div class="ai-welcome-icon"></div>
        <p class="ai-welcome-subtitle">Olá! Sou o Assistente, inteligência artificial do MT 360.</p>
        <h1 class="ai-welcome-title">Como posso ajudar você hoje?</h1>
      </div>

      <!-- Container de Mensagens Ativas -->
      <div id="ai-chat-messages" class="ai-chat-messages"></div>
    </div>

    <!-- Barra de Digitação (Chat Input) Fixada na Base -->
    <div class="ai-input-area">
      <div class="ai-input-container">
        <!-- Textarea -->
        <textarea class="ai-input" placeholder="Pergunte ao Assistente..." rows="1"></textarea>
        
        <div class="ai-input-actions">
          <div class="ai-input-tools">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path></svg>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>
          </div>
          <!-- Send button -->
          <button class="ai-send-btn-new" title="Enviar mensagem">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
          </button>
        </div>
      </div>

      <!-- Action Pills (only visible in empty-state) -->
      <div class="ai-suggestion-grid">
        <button class="ai-suggestion-card" data-query="saude">Ver todas as obras</button>
        <button class="ai-suggestion-card" data-query="evasao">Resumo de conversas</button>
        <button class="ai-suggestion-card" data-query="seguranca">Obras em atraso</button>
        <button class="ai-suggestion-card" data-query="infraestrutura">Total gasto no mês</button>
      </div>
    </div>

<script>
document.addEventListener("DOMContentLoaded", function() {
  const newChatBtn = document.querySelector('.ai-new-chat-btn');
  const historyItems = document.querySelectorAll('.ai-history-item');
  const chatMessages = document.getElementById('ai-chat-messages');
  const welcomeHeader = document.querySelector('.ai-welcome-header');
  const chatInput = document.querySelector('.ai-input');
  const sendBtn = document.querySelector('.ai-send-btn-new');
  const mainScroll = document.querySelector('.ai-main-scroll');
  const mainWrapper = document.querySelector('.ai-main-wrapper');
  
  const sidebar = document.getElementById('ai-sidebar-element');
  const openSidebarBtn = document.getElementById('mobile-open-sidebar');
  const closeSidebarBtn = document.getElementById('mobile-close-sidebar');

  // Sidebar toggles for mobile
  if (openSidebarBtn && closeSidebarBtn && sidebar) {
    openSidebarBtn.addEventListener('click', () => {
      sidebar.classList.add('active');
    });
    closeSidebarBtn.addEventListener('click', () => {
      sidebar.classList.remove('active');
    });
    // Ensure button is visible only on mobile
    function checkMobile() {
      if (window.innerWidth <= 768) {
        openSidebarBtn.style.display = 'inline-flex';
      } else {
        openSidebarBtn.style.display = 'none';
        sidebar.classList.remove('active');
      }
    }
    window.addEventListener('resize', checkMobile);
    checkMobile();
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
  if (newChatBtn) {
    newChatBtn.addEventListener('click', function() {
      chatMessages.innerHTML = '';
      chatMessages.style.display = 'none';
      mainWrapper.classList.add('empty-state');
      chatInput.value = '';
      chatInput.style.height = '48px'; // Reset height
      document.querySelectorAll('.ai-history-item').forEach(i => i.classList.remove('active'));
    });
  }

  // History items click
  historyItems.forEach(item => {
    item.addEventListener('click', function() {
      document.querySelectorAll('.ai-history-item').forEach(i => i.classList.remove('active'));
      this.classList.add('active');
      
      const queryText = this.querySelector('span').textContent.trim();
      chatMessages.innerHTML = '';
      addMessage(queryText, 'user');
      chatInput.value = '';
      chatInput.style.height = '48px'; // Reset height
      handleBotResponse(queryText);
    });
  });

  // Suggestion Cards click
  document.querySelectorAll('.ai-suggestion-card').forEach(btn => {
    btn.addEventListener('click', function() {
      const queryType = this.getAttribute('data-query');
      let queryText = "";
      if (queryType === 'saude') queryText = "Qual é a situação atual da saúde no estado?";
      else if (queryType === 'evasao') queryText = "Como está a taxa de evasão escolar?";
      else if (queryType === 'seguranca') queryText = "Quais indicadores de segurança estão abaixo da meta?";
      else if (queryType === 'infraestrutura') queryText = "Resumo do investimento em infraestrutura em 2024";
      else if (queryType === 'comparar') queryText = "Compare os indicadores de educação com as metas";
      else if (queryType === 'alertas') queryText = "Quais alertas críticos existem no painel?";
      
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

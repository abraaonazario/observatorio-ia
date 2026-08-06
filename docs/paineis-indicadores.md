---
hide:
  - navigation
  - toc
---

<style>
  /* HIDE MKDOCS DEFAULTS COMPLETELY */
  h1 { display: none !important; } 
  .md-main__inner { margin: 0 !important; max-width: 100% !important; }
  .md-content { padding: 0 !important; }
  .md-grid { max-width: 100% !important; padding: 0 !important; margin: 0 !important; }
  .md-content__inner { margin: 0 !important; padding: 0 !important; }
  body, html { margin: 0; padding: 0; min-height: 100vh; font-family: 'Segoe UI', system-ui, sans-serif; }
  
  :root {
    --bg-color: #eef1f6;
    --panel-bg: rgba(255, 255, 255, 0.85);
    --panel-border: rgba(255, 255, 255, 0.5);
    --text-main: #212121;
    --text-muted: #555555;
    
    /* Theme Colors */
    --c-saude: #22d3ee;
    --c-edu: #a78bfa;
    --c-seg: #fb923c;
    --c-inf: #facc15;
    --c-soc: #f472b6;
    --c-fin: #4ade80;
  }

  /* FULL PAGE WRAPPER */
  .hub-wrapper {
    width: 100%;
    min-height: calc(100vh - 70px); /* Adjusting for standard header */
    background-color: var(--bg-color);
    /* Subtle map background pattern */
    background-image: radial-gradient(#d1d5db 1px, transparent 1px);
    background-size: 20px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px;
    box-sizing: border-box;
  }

  /* TOP BAR LOGO */
  .hub-top-bar {
    position: absolute;
    top: 20px;
    left: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 800;
    color: #112d7b;
    font-size: 16px;
    letter-spacing: -0.5px;
    cursor: pointer;
    background: #ffffff;
    padding: 8px 16px;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    text-decoration: none;
    z-index: 10;
  }
  .hub-top-bar svg { fill: #112d7b; }
  
  .hub-top-right {
    position: absolute;
    top: 20px;
    right: 20px;
    font-size: 12px;
    font-weight: 600;
    color: #777;
  }
  .hub-top-right span {
    font-weight: 800;
    color: #5b21b6;
  }

  /* MAIN PANEL */
  .hub-panel {
    background: var(--panel-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--panel-border);
    border-radius: 24px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.08), 
                inset 0 2px 0 rgba(255,255,255,0.7);
    padding: 50px 40px;
    max-width: 1000px;
    width: 100%;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
  }

  .hub-title {
    font-size: 32px;
    font-weight: 900;
    color: var(--text-main);
    letter-spacing: -0.5px;
    margin: 0;
    text-transform: uppercase;
  }
  
  .hub-subtitle {
    font-size: 16px;
    font-weight: 700;
    color: var(--text-muted);
    margin: 10px 0 40px 0;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }

  /* GRID CARDS */
  .hub-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    width: 100%;
    margin-bottom: 30px;
  }

  .hub-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 30px 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.04);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    position: relative;
    border: 1px solid rgba(0,0,0,0.03);
    overflow: hidden;
    cursor: pointer;
  }
  
  .hub-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; width: 100%; height: 4px;
    background: transparent;
    transition: all 0.3s;
  }

  .hub-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.08);
  }
  
  /* Color specific hovers */
  .hub-card.saude:hover::before { background: var(--c-saude); }
  .hub-card.edu:hover::before { background: var(--c-edu); }
  .hub-card.seg:hover::before { background: var(--c-seg); }
  .hub-card.inf:hover::before { background: var(--c-inf); }
  .hub-card.soc:hover::before { background: var(--c-soc); }
  .hub-card.fin:hover::before { background: var(--c-fin); }

  .hub-icon-wrap {
    width: 64px;
    height: 64px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
    transition: transform 0.3s;
  }
  
  .hub-card:hover .hub-icon-wrap {
    transform: scale(1.1);
  }

  .hub-card.saude .hub-icon-wrap { background: rgba(34, 211, 238, 0.15); color: #0891b2; }
  .hub-card.edu .hub-icon-wrap { background: rgba(167, 139, 250, 0.15); color: #7c3aed; }
  .hub-card.seg .hub-icon-wrap { background: rgba(251, 146, 60, 0.15); color: #ea580c; }
  .hub-card.inf .hub-icon-wrap { background: rgba(250, 204, 21, 0.15); color: #ca8a04; }
  .hub-card.soc .hub-icon-wrap { background: rgba(244, 114, 182, 0.15); color: #db2777; }
  .hub-card.fin .hub-icon-wrap { background: rgba(74, 222, 128, 0.15); color: #16a34a; }

  .hub-card-label {
    font-size: 10px;
    font-weight: 700;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }

  .hub-card-title {
    font-size: 18px;
    font-weight: 800;
    color: var(--text-main) !important;
    text-transform: uppercase;
    margin: 0;
  }

  .hub-footer {
    font-size: 10px;
    font-weight: 700;
    color: #999;
    text-transform: uppercase;
    margin-top: 10px;
  }

  @media(max-width: 900px) {
    .hub-grid { grid-template-columns: repeat(2, 1fr); }
  }
  @media(max-width: 600px) {
    .hub-grid { grid-template-columns: 1fr; }
    .hub-panel { padding: 30px 20px; }
  }

  /* DARK MODE */
  body.dark-mode .hub-wrapper {
    --bg-color: #0d1117;
    --panel-bg: rgba(22, 27, 34, 0.85);
    --panel-border: rgba(48, 54, 61, 0.5);
    --text-main: #ffffff;
    --text-muted: #cccccc;
    background-image: radial-gradient(#30363d 1px, transparent 1px);
  }
  body.dark-mode .hub-card {
    background: #161b22;
    border-color: #30363d;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
  }
  body.dark-mode .hub-top-bar {
    background: #1c2128;
    color: #ffffff;
    border: 1px solid #30363d;
  }
  body.dark-mode .hub-top-bar svg {
    fill: #58a6ff;
  }
  body.dark-mode .hub-card-label {
    color: #aaaaaa;
  }
  body.dark-mode .hub-footer {
    color: #aaaaaa;
  }
  body.dark-mode .hub-top-right {
    color: #cccccc;
  }
  body.dark-mode .hub-top-right span {
    color: #ffffff;
  }
  body.dark-mode .hub-card-title {
    color: #ffffff !important;
  }
  .theme-toggle-btn {
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 6px 12px;
    border-radius: 12px;
    background: var(--panel-bg);
    border: 1px solid var(--panel-border);
    font-size: 11px;
    font-weight: 700;
    color: var(--text-main);
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    user-select: none;
    margin-left: 14px;
    transition: all 0.2s;
  }
  .theme-toggle-btn:hover {
    background: rgba(0,0,0,0.05);
  }
  body.dark-mode .theme-toggle-btn:hover {
    background: rgba(255,255,255,0.05);
  }

</style>

<div class="hub-wrapper">

  <div class="hub-panel">
    
    <h1 class="hub-title">MT 360º</h1>
    <div class="hub-subtitle">ANÁLISE DETALHADA DOS PAINÉIS DE INDICADORES DO ESTADO</div>

    <div class="hub-grid">
      
      <!-- SAÚDE -->
      <a href="../saude/" class="hub-card saude">
        <div class="hub-icon-wrap">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>
        </div>
        <h2 class="hub-card-title">SAÚDE</h2>
      </a>

      <!-- EDUCAÇÃO -->
      <a href="../educacao/" class="hub-card edu">
        <div class="hub-icon-wrap">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
        </div>
        <h2 class="hub-card-title">EDUCAÇÃO</h2>
      </a>

      <!-- SEGURANÇA -->
      <a href="../seguranca/" class="hub-card seg">
        <div class="hub-icon-wrap">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
        </div>
        <h2 class="hub-card-title">SEGURANÇA</h2>
      </a>

      <!-- INFRAESTRUTURA -->
      <a href="../infraestrutura/" class="hub-card inf">
        <div class="hub-icon-wrap">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
        </div>
        <h2 class="hub-card-title">INFRAESTRUTURA</h2>
      </a>

      <!-- ASSISTÊNCIA SOCIAL -->
      <a href="../assistencia/" class="hub-card soc">
        <div class="hub-icon-wrap">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
        </div>
        <h2 class="hub-card-title">SOCIAL</h2>
      </a>

      <!-- FINANÇAS / FIPLAN -->
      <a href="../financas/" class="hub-card fin">
        <div class="hub-icon-wrap">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
        </div>
        <h2 class="hub-card-title">FIPLAN</h2>
      </a>

      <!-- TRANSPORTES -->
      <a href="../transportes/" class="hub-card inf">
        <div class="hub-icon-wrap">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="10" rx="2" ry="2"></rect><circle cx="6" cy="19" r="2"></circle><circle cx="18" cy="19" r="2"></circle><path d="M22 17v-4l-4-4H6"></path></svg>
        </div>
        <h2 class="hub-card-title">TRANSPORTES</h2>
      </a>

    </div>

    <div class="hub-footer">
      OS DADOS DESTA SEÇÃO SÃO FORNECIDOS E CONSOLIDADOS PELAS RESPECTIVAS SECRETARIAS. <br/>
      O MT 360º ATUA COMO PLATAFORMA DE INTEGRAÇÃO.
    </div>

  </div>
</div>

<script>
  function applyHubTheme(theme) {
    if (theme === 'dark') {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    // 1. Carregar o tema salvo
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      applyHubTheme('dark');
      const btn = document.getElementById('theme-toggle');
      if(btn) btn.innerHTML = 'Light'; // Just an example, maybe with SVG
    }

    // 2. Ouvir o botão padrão do menu superior
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        // Toggle the body class
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
      });
    }
  });
</script>

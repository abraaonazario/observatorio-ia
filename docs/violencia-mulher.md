---
hide:
  - navigation
  - toc
  - header
---

<script>document.body.classList.add('dashboard-page');</script>

<style>
  /* HIDE MKDOCS DEFAULTS COMPLETELY */
  .custom-top-nav, .md-header { display: none !important; }
  h1 { display: none !important; } 
  .md-main__inner { margin: 0 !important; max-width: 100% !important; }
  .md-content { padding: 0 !important; }
  .md-grid { max-width: 100% !important; padding: 0 !important; margin: 0 !important; }
  .md-content__inner { margin: 0 !important; padding: 0 !important; }
  body, html { margin: 0; padding: 0; overflow: hidden; background-color: #222; }
  
  :root {
    --pbi-bg: #f3f2f7; 
    --pbi-card: #ffffff;
    --pbi-pink: #d927a7; 
    --pbi-navy: #1e1b4b; 
    --pbi-title-purple: #4b2675;
    --pbi-text-dark: #333333;
    --pbi-text-muted: #888888;
    --pbi-border: #e2e8f0;
    --pbi-card-shadow: 0 2px 6px rgba(0,0,0,0.06);
  }
  
  /* SCALING WRAPPER - Full Width Responsive */
  .pbi-scale-wrapper {
    position: fixed;
    top: 0; left: 0;
    width: 100vw;
    height: 100vh;
    background-color: var(--pbi-bg); 
    display: flex;
    overflow-x: hidden;
    overflow-y: auto;
    z-index: 99999;
  }

  .pbi-dashboard {
    width: 100%;
    min-width: 1200px;
    height: 100%;
    min-height: 800px;
    background-color: var(--pbi-bg);
    display: flex;
    font-family: 'Segoe UI', Arial, sans-serif;
    overflow: hidden;
  }

  /* Sidebar */
  .pbi-sidebar {
    width: 78px;
    background-color: #4b2675;
    background-image: radial-gradient(circle at 50% 100%, rgba(217,39,167,0.4) 0%, transparent 60%);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 12px 0;
    gap: 8px;
    flex-shrink: 0;
  }
  
  .pbi-nav-btn {
    width: 62px;
    height: 56px;
    background: rgba(255,255,255,0.12);
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    color: rgba(255,255,255,0.7);
    cursor: pointer;
    position: relative;
    flex-shrink: 0;
    transition: all 0.2s;
    border: 1px solid transparent;
  }
  .pbi-nav-btn:hover {
    background: rgba(255,255,255,0.2);
    color: #ffffff;
    border-color: rgba(255,255,255,0.2);
  }
  .pbi-nav-btn span.nav-label {
    font-size: 8px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    line-height: 1;
    text-align: center;
    max-width: 60px;
  }
  .pbi-nav-btn::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0; width: 3px;
    background: transparent;
    border-radius: 10px 0 0 10px;
  }
  .pbi-nav-btn.active {
    background: rgba(255,255,255,0.22);
    color: #ffffff;
    border-color: rgba(255,255,255,0.3);
  }
  .pbi-nav-btn.active::before { background: #ffffff; }
  /* Theme color accents */
  .pbi-nav-btn.theme-saude.active   { border-color: #22d3ee; }
  .pbi-nav-btn.theme-saude.active::before { background: #22d3ee; }
  .pbi-nav-btn.theme-edu.active     { border-color: #a78bfa; }
  .pbi-nav-btn.theme-edu.active::before { background: #a78bfa; }
  .pbi-nav-btn.theme-seg.active     { border-color: #fb923c; }
  .pbi-nav-btn.theme-seg.active::before { background: #fb923c; }
  .pbi-nav-btn.theme-inf.active     { border-color: #facc15; }
  .pbi-nav-btn.theme-inf.active::before { background: #facc15; }
  .pbi-nav-btn.theme-fin.active     { border-color: #4ade80; }
  .pbi-nav-btn.theme-fin.active::before { background: #4ade80; }
  .pbi-nav-btn.theme-soc.active     { border-color: #f472b6; }
  .pbi-nav-btn.theme-soc.active::before { background: #f472b6; }

  /* Main Column */
  .pbi-main-col {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 8px 12px;
    gap: 10px;
    overflow: hidden;
  }

  /* Top Header */
  .pbi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 40px;
    flex-shrink: 0;
  }
  .pbi-header-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .pbi-logo-mt {
    display: flex;
    align-items: center;
    background: #ffffff;
    color: #112d7b;
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 800;
    line-height: 1;
    height: 36px;
    letter-spacing: -0.2px;
    border: 1px solid var(--pbi-border);
    box-shadow: var(--pbi-card-shadow);
  }
  .pbi-logo-mt svg {
    margin-right: 6px;
    fill: #112d7b;
  }
  .pbi-titles {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .pbi-title-main {
    font-size: 20px;
    font-weight: 800;
    color: var(--pbi-navy);
    letter-spacing: -0.3px;
    text-transform: uppercase;
    line-height: 1.1;
  }
  .pbi-title-sub {
    font-size: 12px;
    color: #888;
    font-weight: 600;
    text-transform: uppercase;
    line-height: 1.1;
  }

  /* Filters Row */
  .pbi-filters-row {
    display: flex;
    align-items: center;
    height: 40px;
    gap: 16px;
    flex-shrink: 0;
    background: var(--pbi-card);
    border-radius: 8px;
    padding: 0 14px;
    box-shadow: var(--pbi-card-shadow);
    border: 1px solid var(--pbi-border);
  }
  .pbi-filter-label {
    font-size: 13px;
    font-weight: 800;
    color: var(--pbi-text-dark);
  }
  .pbi-filter-box {
    display: flex;
    border: 1.5px solid var(--pbi-pink);
    border-radius: 6px;
    overflow: hidden;
    background: var(--pbi-card);
  }
  .pbi-filter-btn {
    padding: 6px 16px;
    font-size: 11px;
    font-weight: 800;
    color: var(--pbi-text-muted);
    cursor: pointer;
  }
  .pbi-filter-btn.active {
    background: rgba(217,39,167,0.1);
    color: var(--pbi-pink);
  }
  
  .pbi-dropdown-group {
    display: flex;
    flex: 1;
    justify-content: space-between;
    align-items: center;
    padding: 0 10px;
  }
  .pbi-dropdown {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .pbi-dropdown label {
    font-size: 9px;
    font-weight: 700;
    color: var(--pbi-text-dark);
  }
  .pbi-select {
    border: none;
    border-bottom: 2px solid #ccc;
    background: transparent;
    font-size: 12px;
    font-weight: 600;
    color: var(--pbi-text-muted);
    padding: 2px 16px 2px 0;
    outline: none;
    cursor: pointer;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23888' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right center;
  }
  .pbi-eraser {
    width: 32px;
    height: 32px;
    background: var(--pbi-card);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #444;
    border: 1px solid var(--pbi-border);
    cursor: pointer;
    box-shadow: var(--pbi-card-shadow);
  }

  /* Center Title */
  .pbi-main-title {
    text-align: center;
    font-size: 16px;
    font-weight: 800;
    color: var(--pbi-title-purple);
    flex-shrink: 0;
  }
  .pbi-main-title span {
    color: #8c8c8c;
    font-weight: 600;
    font-size: 13px;
  }

  /* KPIs */
  .pbi-kpis {
    flex-shrink: 0;
    height: 130px; 
    display: grid;
    grid-template-columns: 1fr 1fr 1.3fr 1fr 1fr 1fr 1fr;
    gap: 10px;
  }
  .pbi-kpi-card {
    background: var(--pbi-card);
    border-radius: 8px;
    box-shadow: var(--pbi-card-shadow);
    padding: 10px 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    border: 1px solid var(--pbi-border);
    overflow: hidden;
  }
  .pbi-kpi-val {
    font-size: 38px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 6px;
    letter-spacing: -1px;
  }
  .pbi-kpi-val.navy { color: var(--pbi-navy); }
  .pbi-kpi-val.pink { color: var(--pbi-pink); }
  .pbi-kpi-lbl {
    font-size: 13px;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 8px;
    letter-spacing: -0.2px;
  }
  .pbi-kpi-lbl.navy { color: var(--pbi-navy); }
  .pbi-kpi-lbl.pink { color: var(--pbi-pink); }
  
  .pbi-kpi-badge {
    background: transparent;
    color: #15803d;
    font-size: 11px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 3px;
  }
  
  .pbi-kpi-sub {
    font-size: 10px;
    color: var(--pbi-text-dark);
    font-weight: 700;
    text-transform: uppercase;
  }
  .pbi-kpi-lbl-text {
    color: var(--pbi-pink);
    font-size: 13px;
    font-weight: 800;
    margin: 6px 0 8px 0;
    line-height: 1.1;
  }
  .pbi-kpi-val-text {
    font-size: 24px;
    font-weight: 800;
    color: var(--pbi-text-dark);
    display: flex;
    align-items: baseline;
    justify-content: center;
    gap: 6px;
  }

  /* Grid Layout - USING FRACTIONS TO PREVENT OVERFLOW */
  .pbi-chart-grid {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-template-rows: 1fr 1fr 1.15fr;
    gap: 10px;
    min-height: 0;
  }
  
  .pbi-chart-card {
    background: var(--pbi-card);
    border-radius: 8px;
    box-shadow: var(--pbi-card-shadow);
    padding: 8px 10px;
    display: flex;
    flex-direction: column;
    position: relative;
    border: 1px solid var(--pbi-border);
    min-height: 0;
  }
  
  /* Area Assignments */
  #card-regiao { grid-area: 1 / 1 / 2 / 2; }
  #card-ano { grid-area: 1 / 2 / 2 / 4; }
  #card-mapa { grid-area: 1 / 4 / 2 / 6; padding: 0; overflow: hidden; }
  
  #card-municipio { grid-area: 2 / 1 / 4 / 2; }
  #card-mes { grid-area: 2 / 2 / 3 / 4; }
  #card-dia { grid-area: 2 / 4 / 3 / 6; }
  
  #card-local { grid-area: 3 / 2 / 4 / 3; }
  #card-motivo { grid-area: 3 / 3 / 4 / 4; }
  #card-meio { grid-area: 3 / 4 / 4 / 5; }
  #card-idade { grid-area: 3 / 5 / 4 / 6; }

  .pbi-chart-title {
    font-size: 12px;
    font-weight: 800;
    color: var(--pbi-text-dark);
    text-transform: uppercase;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    flex-shrink: 0;
  }
  .pbi-chart-subtitle {
    text-transform: none;
    font-weight: 400;
    color: #999;
    margin-left: 4px;
    font-size: 9px;
  }
  .pbi-chart-legend {
    font-size: 9px;
    color: var(--pbi-text-dark);
    display: flex;
    gap: 6px;
    position: absolute;
    top: 8px;
    right: 12px;
    z-index: 10;
  }
  .pbi-chart-legend-item {
    display: flex;
    align-items: center;
    gap: 4px;
    font-weight: 700;
  }
  .pbi-legend-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }
  .pbi-chart-container {
    flex: 1;
    position: relative;
    width: 100%;
    min-height: 0;
  }

  #pbi-map {
    width: 100%;
    height: 100%;
    background: #e2e8f0;
    filter: grayscale(1) opacity(0.7); 
  }
  
  .scrollable-chart::-webkit-scrollbar { width: 5px; }
  .scrollable-chart::-webkit-scrollbar-track { background: transparent; }
  .scrollable-chart::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 5px; }
  .scrollable-chart::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

  /* =========================================
     DARK MODE — Estilo MT 360
     Premium dark: fundo #0d1117, cards #161b22
     ========================================= */

  .pbi-scale-wrapper.dark-mode-wrapper {
    background-color: #0d1117;
  }

  .pbi-dashboard.dark-mode {
    --pbi-bg: #0d1117;
    --pbi-card: #161b22;
    --pbi-text-dark: #e6edf3;
    --pbi-title-purple: #79c0ff;
    --pbi-text-muted: #8b949e;
    --pbi-border: #30363d;
    --pbi-card-shadow: 0 0 0 1px #30363d, 0 4px 20px rgba(0,0,0,0.5);
  }

  /* Wrapper background */
  .pbi-dashboard.dark-mode { background-color: #0d1117; }

  /* Sidebar stays dark purple — fica bonito */
  .pbi-dashboard.dark-mode .pbi-sidebar {
    background-color: #13111c;
    background-image: radial-gradient(circle at 50% 100%, rgba(139,92,246,0.35) 0%, transparent 65%);
  }
  .pbi-dashboard.dark-mode .pbi-nav-btn {
    background: #21262d;
    color: #79c0ff;
    box-shadow: none;
    border: 1px solid #30363d;
  }
  .pbi-dashboard.dark-mode .pbi-nav-btn::before { background: rgba(121,192,255,0.2); }
  .pbi-dashboard.dark-mode .pbi-nav-btn.active { color: #58a6ff; }
  .pbi-dashboard.dark-mode .pbi-nav-btn.active::before { background: #58a6ff; }

  /* Header */
  .pbi-dashboard.dark-mode .pbi-logo-mt {
    background: #1c2128;
    color: #e6edf3;
    border-color: #30363d;
  }
  .pbi-dashboard.dark-mode .pbi-logo-mt svg { fill: #58a6ff; }
  .pbi-dashboard.dark-mode .pbi-title-main { color: #e6edf3; }
  .pbi-dashboard.dark-mode .pbi-title-sub { color: #8b949e; }
  .pbi-dashboard.dark-mode .pbi-header-right { color: #8b949e; }
  .pbi-dashboard.dark-mode .pbi-header-right span { color: #f472b6; }

  /* Center Title */
  .pbi-dashboard.dark-mode .pbi-main-title { color: #79c0ff; }
  .pbi-dashboard.dark-mode .pbi-main-title span { color: #6e7681; }

  /* Filter Row */
  .pbi-dashboard.dark-mode .pbi-filters-row {
    background: #161b22;
    border-color: #30363d;
  }
  .pbi-dashboard.dark-mode .pbi-filter-label { color: #e6edf3; }
  .pbi-dashboard.dark-mode .pbi-filter-box {
    background: #21262d;
    border-color: #8957e5;
  }
  .pbi-dashboard.dark-mode .pbi-filter-btn { color: #8b949e; }
  .pbi-dashboard.dark-mode .pbi-filter-btn.active {
    color: #f0abfc;
    background: rgba(139,92,246,0.2);
  }
  .pbi-dashboard.dark-mode .pbi-dropdown label { color: #8b949e; }
  .pbi-dashboard.dark-mode .pbi-select { color: #e6edf3; }
  .pbi-dashboard.dark-mode .pbi-eraser {
    background: #21262d;
    border-color: #30363d;
    color: #8b949e;
  }

  /* KPI Cards */
  .pbi-dashboard.dark-mode .pbi-kpi-card {
    background: #161b22;
    border-color: #30363d;
    box-shadow: 0 0 0 1px #21262d;
  }
  .pbi-dashboard.dark-mode .pbi-kpi-val.navy { color: #79c0ff; }
  .pbi-dashboard.dark-mode .pbi-kpi-val.pink { color: #f9a8d4; }
  .pbi-dashboard.dark-mode .pbi-kpi-lbl.navy { color: #79c0ff; }
  .pbi-dashboard.dark-mode .pbi-kpi-lbl.pink { color: #f9a8d4; }
  .pbi-dashboard.dark-mode .pbi-kpi-sub { color: #8b949e; }
  .pbi-dashboard.dark-mode .pbi-kpi-lbl-text { color: #f0abfc; }
  .pbi-dashboard.dark-mode .pbi-kpi-val-text { color: #e6edf3; }
  .pbi-dashboard.dark-mode .pbi-kpi-badge { color: #3fb950; }

  /* Chart Cards */
  .pbi-dashboard.dark-mode .pbi-chart-card {
    background: #161b22;
    border-color: #30363d;
  }
  .pbi-dashboard.dark-mode .pbi-chart-title { color: #e6edf3; }
  .pbi-dashboard.dark-mode .pbi-chart-subtitle { color: #6e7681; }
  .pbi-dashboard.dark-mode .pbi-chart-legend { color: #8b949e; }
  .pbi-dashboard.dark-mode .pbi-chart-legend-item { color: #8b949e; }

  /* Map */
  .pbi-dashboard.dark-mode #pbi-map {
    filter: invert(1) hue-rotate(200deg) brightness(0.75) saturate(0.6);
  }

  /* Scrollbars */
  .pbi-dashboard.dark-mode .scrollable-chart::-webkit-scrollbar-thumb {
    background: #30363d;
  }
  .pbi-dashboard.dark-mode .scrollable-chart::-webkit-scrollbar-thumb:hover {
    background: #484f58;
  }

  /* Cards */

</style>

<!-- Chart.js & Plugins -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0"></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<div class="pbi-scale-wrapper">
  <div class="pbi-dashboard">
    
    <!-- Sidebar MT 360 -->
    <aside class="pbi-sidebar">
      <!-- Home -->
      <div class="pbi-nav-btn active" title="Início" onclick="window.location.href='/'" style="cursor:pointer;">
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

      <!-- Settings at bottom -->
      <div class="pbi-nav-btn" style="margin-top:auto; margin-bottom:6px;" title="Configurações">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
        <span class="nav-label">Config.</span>
      </div>
    </aside>

    <div class="pbi-main-col">
      <!-- Header -->
      <header class="pbi-header">
        <div class="pbi-header-left">
          <div class="pbi-logo-mt" onclick="openObsModal()" style="cursor:pointer; user-select:none;" title="Abrir MT 360º">
            <svg width="18" height="18" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
            Mato Grosso
          </div>
          <div class="pbi-titles">
            <div class="pbi-title-main">MONITORAMENTO DA VIOLÊNCIA CONTRA A MULHER EM MT</div>
            <div class="pbi-title-sub">REGISTRO DE FEMINICÍDIOS E TENTATIVAS NO ESTADO DE MATO GROSSO</div>
          </div>
        </div>
        <div class="pbi-header-right" style="display:flex; align-items:center; gap: 14px;">
          <span style="font-size:12px; font-weight:600; color:#777;">FONTE DE DADOS: <span style="font-size:13px; color:var(--pbi-pink); font-weight:800;">SESP/MT</span></span>
          <div id="themeToggle" onclick="toggleDarkMode()" style="cursor:pointer; display:flex; align-items:center; justify-content:center; padding: 4px 10px; border-radius: 12px; background:var(--pbi-card); border: 1px solid var(--pbi-border); font-size: 11px; font-weight:700; user-select:none; box-shadow: var(--pbi-card-shadow);">
            🌙 Escuro
          </div>
        </div>
      </header>

      <!-- Filters Row -->
      <div class="pbi-filters-row">
        <span class="pbi-filter-label">FILTROS</span>
        <div class="pbi-filter-box">
          <div class="pbi-filter-btn active">FEMINICÍDIO</div>
          <div class="pbi-filter-btn">TENTATIVA</div>
        </div>
        <div class="pbi-dropdown-group">
          <div class="pbi-dropdown"><label>ANO</label><select class="pbi-select"><option>2026</option></select></div>
          <div class="pbi-dropdown"><label>REGIÃO</label><select class="pbi-select"><option>Todos</option></select></div>
          <div class="pbi-dropdown"><label>MUNICÍPIO</label><select class="pbi-select"><option>Todos</option></select></div>
          <div class="pbi-dropdown"><label>MOTIVAÇÃO</label><select class="pbi-select"><option>Todos</option></select></div>
          <div class="pbi-dropdown"><label>MEIO EMPREGADO</label><select class="pbi-select"><option>Todos</option></select></div>
          <div class="pbi-dropdown"><label>LOCAL DOS FATOS</label><select class="pbi-select"><option>Todos</option></select></div>
        </div>
        <div class="pbi-eraser">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 20H7L3 16C2.5 15.5 2.5 14.5 3 14L13 4C13.5 3.5 14.5 3.5 15 4L20 9C20.5 9.5 20.5 10.5 20 11L11 20H20V20Z"></path></svg>
        </div>
      </div>

      <div class="pbi-main-title">DADOS REFERENTES AO ANO DE 2026 <span>• Atualizado em 06/07/2026</span></div>

      <!-- KPIs (Fixed Height) -->
      <div class="pbi-kpis">
        <div class="pbi-kpi-card">
          <div class="pbi-kpi-val navy">104</div>
          <div class="pbi-kpi-lbl navy">TENTATIVAS</div>
          <div class="pbi-kpi-badge">▼ 11 casos (-9.6%) vs 2025</div>
        </div>
        <div class="pbi-kpi-card">
          <div class="pbi-kpi-val pink">26</div>
          <div class="pbi-kpi-lbl pink">FEMINICÍDIOS</div>
          <div class="pbi-kpi-badge">▼ 1 casos (-3.7%) vs 2025</div>
        </div>
        <div class="pbi-kpi-card" style="padding:4px;">
          <div class="pbi-chart-container"><canvas id="pbiPie"></canvas></div>
        </div>
        <div class="pbi-kpi-card">
          <div class="pbi-kpi-sub">PRINCIPAL MOTIVAÇÃO</div>
          <div class="pbi-kpi-lbl-text" style="color:var(--pbi-title-purple);">VIOLÊNCIA DOMÉSTICA</div>
          <div class="pbi-kpi-val-text">84,3% <span style="font-size:9px; font-weight:700; color:#888; text-transform:uppercase; max-width:50px; text-align:left; line-height:1.1; margin-left:6px;">DO TOTAL DE REGISTROS</span></div>
        </div>
        <div class="pbi-kpi-card">
          <div class="pbi-kpi-sub">LOCAL COM MAIS REGISTROS</div>
          <div class="pbi-kpi-lbl-text">RESIDÊNCIA PARTICULAR</div>
          <div class="pbi-kpi-val-text">90</div>
        </div>
        <div class="pbi-kpi-card">
          <div class="pbi-kpi-sub">FORMA MAIS UTILIZADA</div>
          <div class="pbi-kpi-lbl-text">ARMA CORTANTE OU PERFURANTE</div>
          <div class="pbi-kpi-val-text">69</div>
        </div>
        <div class="pbi-kpi-card">
          <div class="pbi-kpi-sub">FAIXA ETÁRIA COM MAIOR INCIDÊNCIA</div>
          <div class="pbi-kpi-lbl-text">36-45</div>
          <div class="pbi-kpi-val-text">40</div>
        </div>
      </div>

      <!-- Charts Grid -->
      <div class="pbi-chart-grid">
        
        <div class="pbi-chart-card" id="card-regiao">
          <div class="pbi-chart-title">POR REGIÃO</div>
          <div class="pbi-chart-legend"><div class="pbi-chart-legend-item"><div class="pbi-legend-dot" style="background:var(--pbi-pink);"></div>FEMIN.</div><div class="pbi-chart-legend-item"><div class="pbi-legend-dot" style="background:var(--pbi-navy);"></div>TENT.</div></div>
          <div class="pbi-chart-container"><canvas id="cRegion"></canvas></div>
        </div>
        
        <div class="pbi-chart-card" id="card-ano">
          <div class="pbi-chart-title">POR ANO</div>
          <div class="pbi-chart-legend" style="right:auto; left:50%; transform:translateX(-50%); top:4px;">
            <div class="pbi-chart-legend-item"><div class="pbi-legend-dot" style="background:#a1a1aa;"></div>DADOS HISTÓRICOS</div>
            <div class="pbi-chart-legend-item"><div class="pbi-legend-dot" style="background:var(--pbi-navy);"></div>ANO ATUAL</div>
          </div>
          <div class="pbi-chart-container"><canvas id="cYear"></canvas></div>
        </div>
        
        <div class="pbi-chart-card" id="card-mapa">
          <div class="pbi-chart-title" style="position:absolute; top:8px; left:12px; z-index:1000; background:rgba(255,255,255,0.85); padding:2px 6px; border-radius:4px; box-shadow:0 1px 3px rgba(0,0,0,0.1);">ESTADO DE MATO GROSSO</div>
          <div id="pbi-map"></div>
        </div>
        
        <div class="pbi-chart-card" id="card-municipio">
          <div class="pbi-chart-title">POR MUNICÍPIO</div>
          <div class="pbi-chart-legend"><div class="pbi-chart-legend-item"><div class="pbi-legend-dot" style="background:var(--pbi-pink);"></div>FEMIN.</div><div class="pbi-chart-legend-item"><div class="pbi-legend-dot" style="background:var(--pbi-navy);"></div>TENT.</div></div>
          <div class="pbi-chart-container scrollable-chart" style="padding-left:0px; overflow-y: auto; overflow-x: hidden;">
            <div style="height: 600px; position: relative; width: 100%;">
              <canvas id="cCity"></canvas>
            </div>
          </div>
        </div>

        <div class="pbi-chart-card" id="card-mes">
          <div class="pbi-chart-title">POR MÊS</div>
          <div class="pbi-chart-legend" style="right:auto; left:50%; transform:translateX(-50%); top:4px;"><div class="pbi-chart-legend-item"><div class="pbi-legend-dot" style="background:var(--pbi-pink);"></div>FEMIN.</div><div class="pbi-chart-legend-item"><div class="pbi-legend-dot" style="background:var(--pbi-navy);"></div>TENT.</div></div>
          <div class="pbi-chart-container"><canvas id="cMonth"></canvas></div>
        </div>

        <div class="pbi-chart-card" id="card-dia">
          <div class="pbi-chart-title">POR DIA DA SEMANA</div>
          <div class="pbi-chart-legend" style="right:auto; left:50%; transform:translateX(-50%); top:4px;"><div class="pbi-chart-legend-item"><div class="pbi-legend-dot" style="background:var(--pbi-pink);"></div>FEMIN.</div><div class="pbi-chart-legend-item"><div class="pbi-legend-dot" style="background:var(--pbi-navy);"></div>TENT.</div></div>
          <div class="pbi-chart-container"><canvas id="cDay"></canvas></div>
        </div>

        <div class="pbi-chart-card" id="card-local">
          <div class="pbi-chart-title">LOCAL DOS FATOS <span class="pbi-chart-subtitle">(ONDE?)</span></div>
          <div class="pbi-chart-container scrollable-chart" style="overflow-y:auto; overflow-x:hidden;">
            <div style="height:320px; position:relative; width:100%;">
              <canvas id="cLocal"></canvas>
            </div>
          </div>
        </div>

        <div class="pbi-chart-card" id="card-motivo">
          <div class="pbi-chart-title">MOTIVAÇÃO <span class="pbi-chart-subtitle">(POR QUE?)</span></div>
          <div class="pbi-chart-container scrollable-chart" style="overflow-y:auto; overflow-x:hidden;">
            <div style="height:280px; position:relative; width:100%;">
              <canvas id="cMotive"></canvas>
            </div>
          </div>
        </div>

        <div class="pbi-chart-card" id="card-meio">
          <div class="pbi-chart-title">MEIOS EMPREGADOS <span class="pbi-chart-subtitle">(COMO?)</span></div>
          <div class="pbi-chart-container scrollable-chart" style="overflow-y:auto; overflow-x:hidden;">
            <div style="height:240px; position:relative; width:100%;">
              <canvas id="cWeapon"></canvas>
            </div>
          </div>
        </div>

        <div class="pbi-chart-card" id="card-idade">
          <div class="pbi-chart-title">POR FAIXA ETÁRIA</div>
          <div class="pbi-chart-legend" style="right:auto; left:50%; transform:translateX(-50%); top:4px;"><div class="pbi-chart-legend-item"><div class="pbi-legend-dot" style="background:var(--pbi-pink);"></div>FEM.</div><div class="pbi-chart-legend-item"><div class="pbi-legend-dot" style="background:var(--pbi-navy);"></div>TEN.</div></div>
          <div class="pbi-chart-container"><canvas id="cAge"></canvas></div>
        </div>

      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener("DOMContentLoaded", function() {
  Chart.register(ChartDataLabels);
  
  Chart.defaults.color = '#555';
  Chart.defaults.font.family = 'Segoe UI, Arial, sans-serif';
  Chart.defaults.font.size = 10;
  Chart.defaults.scale.grid.color = 'rgba(0,0,0,0.04)';
  
  const cPink = '#d927a7';
  const cNavy = '#1e1b4b';
  const cGray = '#a1a1aa';
  const cDarkGray = '#6b7280';

  const hBarOpts = {
    responsive: true, maintainAspectRatio: false,
    indexAxis: 'y',
    scales: { 
      x: { display: false, stacked: true }, 
      y: { 
        stacked: true,
        grid: { display: false }, 
        ticks: { 
          font: { weight: '700', size: 9 },
          autoSkip: false,
          maxRotation: 0,
          crossAlign: 'near'
        } 
      } 
    },
    plugins: {
      legend: { display: false },
      datalabels: { 
        anchor: 'end', align: 'right', 
        color: '#222', font: { size: 10, weight: 'bold' },
        padding: { left: 4 }
      }
    },
    categoryPercentage: 0.8,
    barPercentage: 0.85,
    layout: { padding: { right: 25, left: -5 } }
  };

  const vBarOpts = {
    responsive: true, maintainAspectRatio: false,
    scales: { 
      x: { grid: { display: false }, ticks: { font: { weight: '700', size: 10 } } }, 
      y: { display: false } 
    },
    plugins: {
      legend: { display: false },
      datalabels: { anchor: 'end', align: 'top', color: '#222', font: { size: 10, weight: 'bold' } }
    },
    categoryPercentage: 0.8,
    barPercentage: 0.85,
    layout: { padding: { top: 15 } }
  };

  // Pie
  new Chart(document.getElementById('pbiPie'), {
    type: 'doughnut',
    data: {
      labels: ['Feminicídio', 'Outros'],
      datasets: [{ data: [20, 80], backgroundColor: [cPink, '#e2e8f0'], borderWidth: 0 }]
    },
    options: { 
      responsive: true, maintainAspectRatio: false, cutout: '75%', 
      plugins: { legend: { display: false }, datalabels: { display: false } },
      layout: { padding: 4 }
    },
    plugins: [{
      id: 'textCenter',
      beforeDraw: function(chart) {
        var width = chart.width, height = chart.height, ctx = chart.ctx;
        ctx.restore();
        ctx.font = "800 24px Segoe UI";
        ctx.textBaseline = "middle";
        ctx.fillStyle = window.pbiDarkTheme ? "#f5f5f5" : "#222222";
        var text = "20%", textX = Math.round((width - ctx.measureText(text).width) / 2), textY = height / 2 - 6;
        ctx.fillText(text, textX, textY);
        
        ctx.font = "700 8px Segoe UI";
        ctx.fillStyle = window.pbiDarkTheme ? "#aaaaaa" : "#777777";
        var t2 = "DOS CASOS RESULTARAM EM", t2X = Math.round((width - ctx.measureText(t2).width) / 2);
        ctx.fillText(t2, t2X, height / 2 + 10);
        var t3 = "FEMINICÍDIO", t3X = Math.round((width - ctx.measureText(t3).width) / 2);
        ctx.fillText(t3, t3X, height / 2 + 20);
        ctx.save();
      }
    }]
  });

  // Region
  new Chart(document.getElementById('cRegion'), {
    type: 'bar',
    data: {
      labels: ['CENTRO-SUL', 'NORTE', 'NORDESTE', 'SUDESTE', 'OESTE'],
      datasets: [
        { label: 'Feminicídio', data: [9, 11, 2, 2, 2], backgroundColor: cPink },
        { label: 'Tentativa', data: [38, 33, 13, 13, 7], backgroundColor: cNavy }
      ]
    }, options: { ...hBarOpts, scales: { x: { display: false }, y: { grid: { display: false }, ticks: { font: { weight: '700', size: 10 } } } } }
  });

  // Year Combo
  new Chart(document.getElementById('cYear'), {
    type: 'bar',
    data: {
      labels: ['2019','2020','2021','2022','2023','2024','2025','2026'],
      datasets: [
        { 
          type: 'line', label: '% Var', data: [15, 64, -13, 4, -4, -7, 34, -20], 
          borderColor: '#222', borderWidth: 1.5, borderDash: [4, 4], pointBackgroundColor: '#222', 
          datalabels: { 
            anchor: 'center', align: 'center', color: '#fff', 
            backgroundColor: '#222', borderRadius: 4, padding: 2, font: {size: 9, weight: 'bold'},
            formatter: (val) => val+'%' 
          }, 
          yAxisID: 'y1' 
        },
        { type: 'bar', label: 'Hist. Tentativa', data: [114, 190, 175, 201, 190, 171, 240, 0], backgroundColor: cGray, datalabels: { anchor: 'center', align: 'center', color: '#fff', font: {size: 9} }, yAxisID: 'y', stack: 's1' },
        { type: 'bar', label: 'Hist. Feminicídio', data: [39, 62, 43, 47, 46, 47, 53, 0], backgroundColor: cDarkGray, datalabels: { anchor: 'center', align: 'center', color: '#fff', font: {size: 9} }, yAxisID: 'y', stack: 's1' },
        { type: 'bar', label: 'Tentativa 2026', data: [0,0,0,0,0,0,0,104], backgroundColor: cNavy, datalabels: { anchor: 'center', align: 'center', color: '#fff', font: {size: 9} }, yAxisID: 'y', stack: 's1' },
        { type: 'bar', label: 'Feminicídio 2026', data: [0,0,0,0,0,0,0,26], backgroundColor: cPink, datalabels: { anchor: 'center', align: 'center', color: '#fff', font: {size: 9} }, yAxisID: 'y', stack: 's1' }
      ]
    },
    options: { 
      responsive: true, maintainAspectRatio: false, 
      scales: { x: { grid: { display: false }, ticks: {font: {size: 10, weight: 'bold'}} }, y: { stacked: true, display: false }, y1: { display: false } },
      plugins: { legend: { display: false } },
      categoryPercentage: 0.6, barPercentage: 0.8,
      layout: { padding: { top: 15 } }
    }
  });

  // City FULL LIST
  new Chart(document.getElementById('cCity'), {
    type: 'bar',
    data: {
      labels: ['CUIABÁ', 'RONDONÓPOLIS', 'VARZEA GRANDE', 'BARRA DO GARÇAS', 'SINOP', 'SORRISO', 'CAMPO NOVO DO PARECIS', 'VILA BELA DA SANTÍSSIMA TRIND...', 'BRASNORTE', 'CÁCERES', 'ITAÚBA', 'ALTA FLORESTA', 'CANARANA', 'CONFRESA', 'JUARA', 'JURUENA', 'LUCAS DO RIO VERDE', 'PARANATINGA', 'TANGARÁ DA SERRA', 'VERA', 'ACORIZAL', 'ALTO TAQUARI', 'APIACAS', 'ARENÁPOLIS', 'ARIPUANÃ', 'CASTANHEIRA', 'CHAPADA DOS GUIMARÃES', 'CLÁUDIA', 'COLÍDER', 'CURVELÂNDIA', 'DOM AQUINO', 'GAÚCHA DO NORTE', 'GUARANTÃ DO NORTE', 'ITIQUIRA', 'LUCIARA'],
      datasets: [
        { label: 'Tentativa', data: [30, 10, 9, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], backgroundColor: cNavy }
      ]
    }, 
    options: {
      ...hBarOpts,
      plugins: { datalabels: { anchor: 'end', align: 'right', color: '#222', font: { size: 9, weight: 'bold' }, padding: { left: 4 } } },
      scales: { y: { ticks: { font: { size: 9, weight: '600' }, autoSkip: false }, grid: { display: false } }, x: { display: false } },
      layout: { padding: { right: 20, left: -5 } }
    }
  });

  // Month
  new Chart(document.getElementById('cMonth'), {
    type: 'line',
    data: {
      labels: ['JAN','FEV','MAR','ABR','MAI','JUN','JUL'],
      datasets: [
        { label: 'Tentativa', data: [18, 18, 24, 16, 18, 10, 1], borderColor: cNavy, fill: false, borderWidth: 3, pointBackgroundColor: cNavy, pointRadius: 4 },
        { label: 'Feminicídio', data: [3, 4, 3, 3, 4, 3, 1], borderColor: cPink, fill: false, borderWidth: 3, pointBackgroundColor: cPink, pointRadius: 4 }
      ]
    }, options: { 
      responsive: true, maintainAspectRatio: false,
      scales: { x: { grid: { display: false }, ticks: { font: { weight: 'bold', size: 10} } }, y: { display: false } },
      plugins: { legend: { display: false }, datalabels: { anchor: 'end', align: 'top', color: '#222', font: { weight: 'bold', size: 10 } } },
      layout: { padding: { top: 15, right: 10, left: 10 } }
    }
  });

  // Day
  new Chart(document.getElementById('cDay'), {
    type: 'bar',
    data: {
      labels: ['SEG','TER','QUA','QUI','SEX','SÁB','DOM'],
      datasets: [
        { label: 'Feminicídio', data: [2, 3, 2, 4, 3, 6, 8], backgroundColor: cPink },
        { label: 'Tentativa', data: [11, 15, 10, 12, 23, 35, 40], backgroundColor: cNavy }
      ]
    }, options: vBarOpts
  });

  // Local FULL LIST
  new Chart(document.getElementById('cLocal'), { 
    type: 'bar', 
    data: { 
      labels: ['RESIDÊNCIA PARTICULAR', 'VIA PÚBLICA', 'OUTROS', 'PROPRIEDADE RURAL', 'HOSPITAL', 'OUTRO', 'HABITAÇÃO COLETIVA', 'BAR/BOATE', 'CLÍNICA MÉDICA', 'EDIFÍCIO PÚBLICO E DEPENDÊNCIAS', 'PRAÇA PÚBLICA', 'VIA PÚBLICA (TRANSEUNTE)'], 
      datasets: [{ data: [90, 10, 9, 8, 3, 3, 2, 1, 1, 1, 1, 1], backgroundColor: cNavy }] 
    }, 
    options: hBarOpts 
  });
  
  // Motive FULL LIST
  new Chart(document.getElementById('cMotive'), { 
    type: 'bar', 
    data: { 
      labels: ['VIOLÊNCIA DOMÉSTICA', 'SEXUAL', 'A APURAR', 'ÁLCOOL', 'ÁLCOOL ', 'ÁLCOOL/VIOLÊNCIA DOMÉSTICA', 'ÁLCOOL; VIOLÊNCIA DOMÉSTICA', 'AMBIÇÃO', 'OUTROS', 'SEXISTA'], 
      datasets: [
        { label: 'Tentativa', data: [40, 3, 1, 0, 1, 1, 1, 1, 1, 1], backgroundColor: cNavy, stack: 's1' },
        { label: 'Feminicídio', data: [19, 0, 0, 1, 0, 0, 0, 0, 0, 0], backgroundColor: cPink, stack: 's1' }
      ] 
    }, 
    options: hBarOpts 
  });
  
  // Weapon FULL LIST
  new Chart(document.getElementById('cWeapon'), { 
    type: 'bar', 
    data: { 
      labels: ['ARMA CORTANTE OU PERFURANTE', 'FORÇA MUSCULAR', 'ARMA CONTUNDENTE', 'OUTROS', 'ARMA DE FOGO', 'VEÍCULO', 'OUTRO(S)', 'FOGO'], 
      datasets: [
        { label: 'Feminicídio', data: [12, 5, 0, 0, 0, 0, 0, 0], backgroundColor: cPink, stack: 's1' },
        { label: 'Tentativa', data: [57, 19, 10, 8, 7, 6, 3, 1], backgroundColor: cNavy, stack: 's1' }
      ] 
    }, 
    options: hBarOpts 
  });
  
  // Age Stacked — Tentativa on bottom, Feminicídio on top (matches PBI model)
  new Chart(document.getElementById('cAge'), { 
    type: 'bar', 
    data: { 
      labels: ['12-17','18-24','25-29','30-35','36-45','46-59','60+'], 
      datasets: [
        { label: 'Tentativa', data: [3,19,16,20,40,15,4], backgroundColor: cNavy, stack: 's1' },
        { label: 'Feminicídio', data: [1,5,4,6,8,5,1], backgroundColor: cPink, stack: 's1' }
      ] 
    }, 
    options: { 
      responsive: true, maintainAspectRatio: false,
      scales: { 
        x: { stacked: true, grid: { display: false }, ticks: { font: { weight: 'bold', size: 10 } } }, 
        y: { stacked: true, display: false } 
      }, 
      plugins: { 
        legend: { display: false }, 
        datalabels: { 
          anchor: 'center', align: 'center', color: 'white', 
          font: {size: 9, weight: 'bold'},
          formatter: (val) => val > 1 ? val : ''
        } 
      },
      categoryPercentage: 0.8,
      barPercentage: 0.85,
      layout: { padding: { top: 15 } }
    } 
  });

  // Map
  if (document.getElementById('pbi-map') && typeof L !== 'undefined') {
    var map = L.map('pbi-map', { zoomControl: false, attributionControl: false }).setView([-12.68, -55.92], 5);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png').addTo(map);
    
    setTimeout(() => { map.invalidateSize(); }, 500);

    var bubbles = [
      { lat: -15.6, lng: -56.1, size: 22, col: cNavy },
      { lat: -16.4, lng: -54.6, size: 16, col: cPink },
      { lat: -11.8, lng: -55.5, size: 12, col: cNavy },
      { lat: -14.6, lng: -57.5, size: 14, col: cPink },
      { lat: -12.5, lng: -51.5, size: 10, col: cNavy },
      { lat: -10.0, lng: -53.0, size: 8, col: cPink }
    ];
    bubbles.forEach(b => {
      L.circleMarker([b.lat, b.lng], { color: b.col, fillColor: b.col, fillOpacity: 0.6, weight: 1, radius: b.size }).addTo(map);
    });
  }
});

// Dark mode toggle function
window.pbiDarkTheme = false;
window.toggleDarkMode = function() {
  const db = document.querySelector('.pbi-dashboard');
  const wrapper = document.querySelector('.pbi-scale-wrapper');
  db.classList.toggle('dark-mode');
  wrapper.classList.toggle('dark-mode-wrapper');
  const isDark = db.classList.contains('dark-mode');
  window.pbiDarkTheme = isDark;
  
  document.getElementById('themeToggle').innerHTML = isDark ? '☀️ Claro' : '🌙 Escuro';
  document.getElementById('themeToggle').style.background = isDark ? '#161b22' : '';
  document.getElementById('themeToggle').style.color = isDark ? '#e6edf3' : '';
  document.getElementById('themeToggle').style.borderColor = isDark ? '#30363d' : '';
  
  // GitHub dark palette
  const labelColor = isDark ? '#e6edf3' : '#222222';
  const axisColor  = isDark ? '#8b949e' : '#555555';
  const gridColor  = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.04)';
  
  Chart.defaults.color = axisColor;
  Chart.defaults.scale.grid.color = gridColor;
  
  for (let id in Chart.instances) {
    let chart = Chart.instances[id];
    
    // Top-level datalabels
    if (chart.options.plugins && chart.options.plugins.datalabels) {
      const dl = chart.options.plugins.datalabels;
      if (dl.color && dl.color !== 'white' && dl.color !== '#ffffff') {
        dl.color = labelColor;
      }
    }
    
    // Scales ticks
    if (chart.options.scales) {
      for (let axis in chart.options.scales) {
        if (!chart.options.scales[axis].ticks) chart.options.scales[axis].ticks = {};
        chart.options.scales[axis].ticks.color = axisColor;
      }
    }

    // Per-dataset datalabels
    chart.data.datasets.forEach(ds => {
      if (!ds.datalabels) return;
      if (ds.type === 'line' && ds.datalabels && ds.datalabels.formatter) {
        // Year combo line badges — use purple in dark
        ds.borderColor = isDark ? '#79c0ff' : '#222';
        ds.pointBackgroundColor = isDark ? '#79c0ff' : '#222';
        ds.datalabels.backgroundColor = isDark ? '#1f6feb' : '#222';
        ds.datalabels.color = '#ffffff';
      } else if (ds.datalabels.color && ds.datalabels.color !== 'white' && ds.datalabels.color !== '#ffffff') {
        ds.datalabels.color = labelColor;
      }
    });
    
    chart.update();
  }
};
</script>

<!-- OBSERVATORIO MT MODAL -->
<style>
  .obs-overlay {
    display: none; position: fixed; inset: 0; z-index: 999999;
    background: rgba(0,0,0,0.8); backdrop-filter: blur(8px);
    align-items: center; justify-content: center;
  }
  .obs-overlay.open { display: flex; animation: obsIn 0.2s ease; }
  @keyframes obsIn { from { opacity:0; } to { opacity:1; } }
  .obs-box {
    width: min(920px, 96vw); max-height: 92vh; overflow: hidden;
    background: #0d1117; border-radius: 16px; border: 1px solid #30363d;
    box-shadow: 0 32px 80px rgba(0,0,0,0.8);
    display: flex; flex-direction: column;
    animation: obsUp 0.3s cubic-bezier(0.34,1.56,0.64,1);
  }
  @keyframes obsUp { from { transform: translateY(24px) scale(0.97); opacity:0; } to { transform: none; opacity:1; } }
  .obs-head {
    display: flex; align-items: center; justify-content: space-between;
    padding: 20px 28px 18px; border-bottom: 1px solid #21262d; flex-shrink: 0;
  }
  .obs-brand { display: flex; align-items: center; gap: 12px; }
  .obs-brand-icon {
    width: 44px; height: 44px; border-radius: 10px;
    background: linear-gradient(135deg,#1f6feb,#388bfd);
    display: flex; align-items: center; justify-content: center;
  }
  .obs-brand-title { font-size: 18px; font-weight: 800; color: #e6edf3; letter-spacing: -0.3px; margin: 0; }
  .obs-brand-sub { font-size: 11px; color: #8b949e; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin: 2px 0 0; }
  .obs-close-btn {
    width: 34px; height: 34px; background: #21262d; border: 1px solid #30363d;
    border-radius: 8px; display: flex; align-items: center; justify-content: center;
    color: #8b949e; cursor: pointer; font-size: 18px; transition: all 0.15s;
  }
  .obs-close-btn:hover { background: #30363d; color: #e6edf3; }
  .obs-body { padding: 22px 28px 20px; overflow-y: auto; }
  .obs-section-lbl {
    font-size: 11px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1px; color: #6e7681; margin-bottom: 16px;
  }
  .obs-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 14px; }
  .obs-card {
    background: #161b22; border: 1px solid #30363d; border-radius: 12px;
    padding: 18px 16px; cursor: pointer; display: flex; align-items: flex-start;
    gap: 14px; transition: all 0.2s; position: relative; overflow: hidden;
  }
  .obs-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.4); border-color: var(--cc); }
  .obs-card.is-current { border-color: var(--cc); background: #1c2128; }
  .obs-card.is-current::after {
    content: 'ATUAL'; position: absolute; top: 10px; right: 10px;
    font-size: 9px; font-weight: 800; color: var(--cc); letter-spacing: 0.8px;
    padding: 2px 6px; border: 1px solid var(--cc); border-radius: 4px;
  }
  .obs-icon {
    width: 44px; height: 44px; border-radius: 10px; display: flex;
    align-items: center; justify-content: center; flex-shrink: 0;
    background: var(--ic);
  }
  .obs-name { font-size: 14px; font-weight: 800; color: #e6edf3; margin-bottom: 4px; }
  .obs-desc { font-size: 11px; color: #8b949e; line-height: 1.4; }
  .obs-arrow { font-size: 20px; color: #484f58; align-self: center; flex-shrink: 0; transition: all 0.2s; }
  .obs-card:hover .obs-arrow { transform: translateX(4px); color: var(--cc); }
  .obs-foot {
    padding: 14px 28px; border-top: 1px solid #21262d; flex-shrink: 0;
    display: flex; align-items: center; justify-content: space-between;
  }
  .obs-foot span { font-size: 11px; color: #6e7681; font-weight: 600; }
  .obs-foot a { font-size: 11px; font-weight: 700; color: #388bfd; cursor: pointer; text-decoration: none; }
  .obs-foot a:hover { text-decoration: underline; }
</style>

<div class="obs-overlay" id="obsOverlay" onclick="if(event.target===this)closeObsModal()">
  <div class="obs-box">
    <div class="obs-head">
      <div class="obs-brand">
        <div class="obs-brand-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
        </div>
        <div>
          <div class="obs-brand-title">MT 360º</div>
          <div class="obs-brand-sub">Painel de Indicadores · Est. 2024</div>
        </div>
      </div>
      <div class="obs-close-btn" onclick="closeObsModal()">✕</div>
    </div>
    <div class="obs-body">
      <div class="obs-section-lbl">Selecione um tema para explorar os indicadores</div>
      <div class="obs-grid">

        <div class="obs-card" style="--cc:#22d3ee;--ic:rgba(34,211,238,0.12);" onclick="window.location.href='/saude/'">
          <div class="obs-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#22d3ee" stroke-width="2.5"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg></div>
          <div style="flex:1;">
            <div class="obs-name">Saúde</div>
            <div class="obs-desc">Leitos, atendimentos, cobertura vacinal e indicadores hospitalares</div>
          </div>
          <div class="obs-arrow">›</div>
        </div>

        <div class="obs-card" style="--cc:#a78bfa;--ic:rgba(167,139,250,0.12);" onclick="window.location.href='/educacao/'">
          <div class="obs-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2.5"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg></div>
          <div style="flex:1;">
            <div class="obs-name">Educação</div>
            <div class="obs-desc">Matrículas, IDEB, evasão escolar e infraestrutura de ensino</div>
          </div>
          <div class="obs-arrow">›</div>
        </div>

        <div class="obs-card" style="--cc:#fb923c;--ic:rgba(251,146,60,0.12);" onclick="window.location.href='/seguranca/'">
          <div class="obs-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fb923c" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg></div>
          <div style="flex:1;">
            <div class="obs-name">Segurança</div>
            <div class="obs-desc">Ocorrências, homicídios, furtos e indicadores de segurança pública</div>
          </div>
          <div class="obs-arrow">›</div>
        </div>

        <div class="obs-card" style="--cc:#facc15;--ic:rgba(250,204,21,0.12);" onclick="window.location.href='/infraestrutura/'">
          <div class="obs-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#facc15" stroke-width="2.5"><rect x="2" y="3" width="20" height="14" rx="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg></div>
          <div style="flex:1;">
            <div class="obs-name">Infraestrutura</div>
            <div class="obs-desc">Rodovias, saneamento, energia elétrica e obras públicas</div>
          </div>
          <div class="obs-arrow">›</div>
        </div>

        <div class="obs-card" style="--cc:#4ade80;--ic:rgba(74,222,128,0.12);" onclick="window.location.href='/financas/'">
          <div class="obs-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2.5"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg></div>
          <div style="flex:1;">
            <div class="obs-name">Finanças / Tributação</div>
            <div class="obs-desc">Receita, despesa, arrecadação e execução orçamentária do Estado</div>
          </div>
          <div class="obs-arrow">›</div>
        </div>

        <div class="obs-card" style="--cc:#38bdf8;--ic:rgba(56,189,248,0.12);" onclick="window.location.href='/assistencia-social/'">
          <div class="obs-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg></div>
          <div style="flex:1;">
            <div class="obs-name">Assistência Social</div>
            <div class="obs-desc">Programas sociais, beneficiários, CRAS/CREAS e vulnerabilidade</div>
          </div>
          <div class="obs-arrow">›</div>
        </div>

        <div class="obs-card is-current" style="--cc:#f472b6;--ic:rgba(244,114,182,0.12);" onclick="closeObsModal()">
          <div class="obs-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#f472b6" stroke-width="2.5"><path d="M14.5 10c-.83 0-1.5-.67-1.5-1.5v-5c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v4h-2v-3c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v3h-2v-2c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v7c0 3.87 3.13 7 7 7s7-3.13 7-7v-3.5c0-.83-.67-1.5-1.5-1.5h-1.5z"></path></svg></div>
          <div style="flex:1;">
            <div class="obs-name">Violência Mulher</div>
            <div class="obs-desc">Feminicídios, tentativas, motivações e monitoramento SESP/MT</div>
          </div>
          <div class="obs-arrow">›</div>
        </div>

      </div>
    </div>
    <div class="obs-foot">
      <span>🌐 MT 360 · Estado de Mato Grosso</span>
      <a onclick="window.location.href='/'">← Voltar ao início</a>
    </div>
  </div>
</div>

<script>
function openObsModal() {
  document.getElementById('obsOverlay').classList.add('open');
}
function closeObsModal() {
  document.getElementById('obsOverlay').classList.remove('open');
}
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeObsModal();
});
</script>

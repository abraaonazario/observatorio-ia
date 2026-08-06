---
hide:
  - navigation
  - toc
---

<script>document.body.classList.add('dashboard-page');</script>

<style>
  :root {
    --theme-color: #3b82f6; /* Azul do Mapa */
  }
  
  /* Layout do mapa ocupando a tela inteira abaixo do menu e respeitando a barra lateral */
  .dashboard-container {
    padding: 0 !important;
    margin: 90px 0 0 78px !important;
    display: flex;
    flex-direction: column;
    height: calc(100vh - 90px); 
    width: calc(100% - 78px);
    overflow: hidden;
    position: relative; /* Importante para a sidebar absoluta */
  }
  
  #map {
    flex: 1;
    width: 100%;
    background-color: #1e293b; 
    z-index: 1; 
  }

  /* Filtro Dark Mode no Leaflet */
  .leaflet-layer,
  .leaflet-control-zoom-in,
  .leaflet-control-zoom-out,
  .leaflet-control-attribution {
    filter: invert(100%) hue-rotate(180deg) brightness(95%) contrast(90%);
  }
  
  /* Estilização da Sidebar Analítica Flutuante */
  .map-sidebar {
    position: absolute;
    top: 20px;
    left: 20px;
    width: 320px;
    background: rgba(15, 23, 42, 0.75);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    z-index: 1000;
    padding: 1.5rem;
    color: white;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
  }

  .sidebar-header h2 {
    margin: 0;
    font-size: 1.2rem;
    font-weight: 700;
    color: #f8fafc;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .sidebar-header p {
    margin: 5px 0 0 0;
    font-size: 0.8rem;
    color: #94a3b8;
  }

  /* Botões de Tema */
  .theme-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
  }
  .theme-btn {
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid transparent;
    padding: 0.6rem;
    border-radius: 8px;
    color: #cbd5e1;
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    text-align: left;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    transition: all 0.2s;
  }
  .theme-btn:hover {
    background: rgba(51, 65, 85, 0.8);
  }
  /* Cores Ativas por Tema */
  .theme-btn.active[data-theme="geral"] { background: rgba(59, 130, 246, 0.2); border-color: #3b82f6; color: #3b82f6; }
  .theme-btn.active[data-theme="saude"] { background: rgba(56, 189, 248, 0.2); border-color: #38bdf8; color: #38bdf8; }
  .theme-btn.active[data-theme="educacao"] { background: rgba(167, 139, 250, 0.2); border-color: #a78bfa; color: #a78bfa; }
  .theme-btn.active[data-theme="seguranca"] { background: rgba(239, 68, 68, 0.2); border-color: #ef4444; color: #ef4444; }
  .theme-btn.active[data-theme="infraestrutura"] { background: rgba(245, 158, 11, 0.2); border-color: #f59e0b; color: #f59e0b; }
  .theme-btn.active[data-theme="financas"] { background: rgba(16, 185, 129, 0.2); border-color: #10b981; color: #10b981; }
  .theme-btn.active[data-theme="assistencia"] { background: rgba(236, 72, 153, 0.2); border-color: #ec4899; color: #ec4899; }

  /* Caixa de Estatísticas Analíticas */
  .stats-box {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 10px;
    padding: 1rem;
    border: 1px solid rgba(255,255,255,0.05);
  }
  .stats-title {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #94a3b8;
    margin-bottom: 0.8rem;
  }
  .stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }
  .stat-row:last-child { margin-bottom: 0; }
  .stat-label { font-size: 0.85rem; color: #cbd5e1; }
  .stat-value { font-size: 1rem; font-weight: 700; color: white; }

  /* Estilização dos Popups do mapa */
  .leaflet-popup-content-wrapper, .leaflet-popup-tip {
    background: #0f172a !important;
    color: #f8fafc !important;
    border: 1px solid #1e293b;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5) !important;
  }
  .leaflet-popup-content h3 { margin: 0 0 5px 0 !important; font-size: 14px; font-weight: 700; }
  .leaflet-popup-content p { margin: 0 !important; font-size: 12px; color: #94a3b8 !important; }
</style>

<!-- Leaflet CSS & JS via CDN -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

<!-- MENU PADRÃO DO DASHBOARD -->
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
  <div class="pbi-nav-btn theme-saude" title="Assistente IA" onclick="window.location.href='../assistente-ia/'" style="cursor:pointer; margin-top: auto;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#22d3ee" stroke-width="2.5"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
    <span class="nav-label" style="color:#22d3ee;">Assis. IA</span>
  </div>
  
  <!-- Mapa -->
  <div class="pbi-nav-btn theme-fin active" title="Mapa de Ativos" onclick="window.location.href='../mapa-ativos/'" style="cursor:pointer;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
    <span class="nav-label" style="color:#4ade80;">Mapa</span>
  </div>
  
  <!-- Settings at bottom -->
  <div class="pbi-nav-btn" style="margin-bottom:6px;" title="Configurações">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
    <span class="nav-label">Config.</span>
  </div>
</aside>

<!-- Container Principal do Mapa -->
<div class="dashboard-container">
  
  <!-- Sidebar Flutuante -->
  <div class="map-sidebar">
    <div class="sidebar-header">
      <h2>🗺️ Camadas de Dados</h2>
      <p>Filtre os ativos no estado do MT</p>
    </div>

    <!-- Botões de Tema -->
    <div class="theme-grid" id="theme-controls">
      <button class="theme-btn active" data-theme="geral" style="grid-column: span 2;">🌐 Visão Geral</button>
      <button class="theme-btn" data-theme="saude">⚕️ Saúde</button>
      <button class="theme-btn" data-theme="educacao">📚 Educação</button>
      <button class="theme-btn" data-theme="seguranca">🛡️ Segurança</button>
      <button class="theme-btn" data-theme="infraestrutura">🏗️ Infraestrutura</button>
      <button class="theme-btn" data-theme="financas">💲 Finanças</button>
      <button class="theme-btn" data-theme="assistencia">🤝 Social</button>
    </div>

    <!-- Filtro de Município -->
    <div class="filter-box" style="margin-top: 0.5rem;">
      <label for="cityFilter" style="font-size: 0.75rem; color: #94a3b8; font-weight: bold; margin-bottom: 0.3rem; display: block;">FILTRAR POR MUNICÍPIO</label>
      <select id="cityFilter" style="width: 100%; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); color: white; padding: 0.6rem; border-radius: 8px; font-size: 0.85rem; outline: none; cursor: pointer;">
        <option value="todos">Todos os Municípios</option>
        <option value="Cuiabá">Cuiabá</option>
        <option value="Várzea Grande">Várzea Grande</option>
        <option value="Rondonópolis">Rondonópolis</option>
        <option value="Sinop">Sinop</option>
        <option value="Sorriso">Sorriso</option>
        <option value="Tangará da Serra">Tangará da Serra</option>
        <option value="Cáceres">Cáceres</option>
        <option value="Alta Floresta">Alta Floresta</option>
        <option value="Barra do Garças">Barra do Garças</option>
      </select>
    </div>

    <!-- Caixa de Estatísticas -->
    <div class="stats-box">
      <div class="stats-title" id="stats-title">ESTATÍSTICAS GERAIS</div>
      <div id="stats-content">
        <div class="stat-row"><span class="stat-label">Total de Ativos:</span> <span class="stat-value">5</span></div>
        <div class="stat-row"><span class="stat-label">Conexões Ativas:</span> <span class="stat-value">365</span></div>
        <div class="stat-row"><span class="stat-label">Status Regional:</span> <span class="stat-value" style="color:#10b981;">Estável</span></div>
      </div>
    </div>
  </div>

  <!-- DIV ONDE O MAPA RENDERIZA -->
  <div id="map"></div>
</div>

<script>
  document.addEventListener("DOMContentLoaded", function() {
    if (document.getElementById('map') && typeof L !== 'undefined') {
      
      var map = L.map('map', { zoomControl: false }).setView([-13.0, -56.0], 6);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '© OpenStreetMap - Observatório IA MT'
      }).addTo(map);

      L.control.zoom({ position: 'bottomright' }).addTo(map);

      // Definição de Cores
      const colors = {
        geral: "#3b82f6", saude: "#38bdf8", educacao: "#a78bfa", 
        seguranca: "#ef4444", infraestrutura: "#f59e0b", financas: "#10b981", assistencia: "#ec4899"
      };

      // Banco de Dados Expandido dos Ativos do MT por Tema
      var markersData = {
        geral: [
          { nome: "Palácio Paiaguás", lat: -15.5786, lng: -56.0970, tipo: "Sede Governo", extra: "Cuiabá - Status: Operacional", municipio: "Cuiabá" },
          { nome: "Data Center MT", lat: -15.6014, lng: -56.0979, tipo: "Infraestrutura Core", extra: "Cuiabá - Status: Operacional", municipio: "Cuiabá" },
          { nome: "Hub Tecnológico do Agro", lat: -11.8643, lng: -55.5036, tipo: "Inovação", extra: "Sinop - Status: Em Expansão", municipio: "Sinop" },
          { nome: "Complexo de Monitoramento Ambiental", lat: -12.5458, lng: -55.7139, tipo: "Meio Ambiente", extra: "Sorriso - Status: Operacional", municipio: "Sorriso" },
          { nome: "Polo Logístico do Araguaia", lat: -15.8942, lng: -52.2564, tipo: "Logística", extra: "Barra do Garças - Status: Em Construção", municipio: "Barra do Garças" },
          { nome: "Centro de Distribuição Integrado", lat: -16.4716, lng: -54.6366, tipo: "Logística", extra: "Rondonópolis - Status: Operacional", municipio: "Rondonópolis" },
          { nome: "Nó de Conectividade Regional", lat: -14.6186, lng: -57.5135, tipo: "Infraestrutura", extra: "Tangará da Serra - Status: Operacional", municipio: "Tangará da Serra" },
          { nome: "Estação de Observação", lat: -9.8767, lng: -56.0825, tipo: "Pesquisa", extra: "Alta Floresta - Status: Operacional", municipio: "Alta Floresta" }
        ],
        saude: [
          { nome: "Hospital Estadual Santa Casa", lat: -15.60, lng: -56.10, tipo: "Alta Complexidade", extra: "Cuiabá - Leitos Ocupados: 85%", municipio: "Cuiabá" },
          { nome: "Hospital Regional de Rondonópolis", lat: -16.48, lng: -54.64, tipo: "Pronto Atendimento", extra: "Rondonópolis - Atendimentos/dia: 420", municipio: "Rondonópolis" },
          { nome: "Hospital Regional de Sinop", lat: -11.85, lng: -55.50, tipo: "Pronto Atendimento", extra: "Sinop - Leitos Ocupados: 78%", municipio: "Sinop" },
          { nome: "Hospital Regional de Cáceres", lat: -16.07, lng: -57.68, tipo: "Pronto Atendimento", extra: "Cáceres - Fronteira", municipio: "Cáceres" },
          { nome: "Hospital Regional de Sorriso", lat: -12.55, lng: -55.71, tipo: "Pronto Atendimento", extra: "Sorriso - Leitos Ocupados: 90%", municipio: "Sorriso" },
          { nome: "UPA Morada do Ouro", lat: -15.57, lng: -56.07, tipo: "Urgência", extra: "Cuiabá - Operacional", municipio: "Cuiabá" },
          { nome: "Centro de Reabilitação Dom Aquino", lat: -15.61, lng: -56.09, tipo: "Reabilitação", extra: "Cuiabá - Operacional", municipio: "Cuiabá" },
          { nome: "Hospital Regional de Alta Floresta", lat: -9.87, lng: -56.08, tipo: "Pronto Atendimento", extra: "Alta Floresta - Leitos Ocupados: 65%", municipio: "Alta Floresta" }
        ],
        educacao: [
          { nome: "Unemat Sede Sump", lat: -16.06, lng: -57.68, tipo: "Ensino Superior", extra: "Cáceres - Cursos Ativos: 25", municipio: "Cáceres" },
          { nome: "Polo Tecnológico IFMT", lat: -15.61, lng: -56.06, tipo: "Técnico e Superior", extra: "Cuiabá - Inovação", municipio: "Cuiabá" },
          { nome: "Escola Estadual Liceu Cuiabano", lat: -15.59, lng: -56.10, tipo: "Ensino Médio", extra: "Cuiabá - Referência", municipio: "Cuiabá" },
          { nome: "Centro de Formação de Professores", lat: -16.46, lng: -54.65, tipo: "Capacitação", extra: "Rondonópolis - EAD", municipio: "Rondonópolis" },
          { nome: "Campus Unemat Sinop", lat: -11.85, lng: -55.51, tipo: "Ensino Superior", extra: "Sinop - Alunos: 3000", municipio: "Sinop" },
          { nome: "Escola Estadual Militar Tiradentes", lat: -12.54, lng: -55.71, tipo: "Ensino Médio", extra: "Sorriso - Destaque IDEB", municipio: "Sorriso" },
          { nome: "Campus IFMT Barra do Garças", lat: -15.89, lng: -52.26, tipo: "Técnico", extra: "Barra do Garças - Operacional", municipio: "Barra do Garças" },
          { nome: "Centro de Capacitação Tecnológica", lat: -14.62, lng: -57.50, tipo: "Técnico", extra: "Tangará da Serra - Cursos Ativos: 8", municipio: "Tangará da Serra" }
        ],
        seguranca: [
          { nome: "CIOSP (Centro de Operações)", lat: -15.58, lng: -56.10, tipo: "Comando Central", extra: "Cuiabá - Câmeras Monitoradas: 2.150", municipio: "Cuiabá" },
          { nome: "Base GEFRON", lat: -16.09, lng: -57.69, tipo: "Fronteira", extra: "Cáceres - Drones Ativos: 8", municipio: "Cáceres" },
          { nome: "Delegacia Especializada Roubos e Furtos", lat: -16.47, lng: -54.63, tipo: "Polícia Civil", extra: "Rondonópolis - Resolutividade: Alta", municipio: "Rondonópolis" },
          { nome: "Batalhão de Operações Especiais (BOPE)", lat: -15.59, lng: -56.08, tipo: "Tático", extra: "Cuiabá - Operacional", municipio: "Cuiabá" },
          { nome: "Base Integrada de Segurança", lat: -11.86, lng: -55.50, tipo: "Polícia Militar", extra: "Sinop - Patrulhas: 15", municipio: "Sinop" },
          { nome: "Delegacia da Mulher", lat: -12.55, lng: -55.72, tipo: "Especializada", extra: "Sorriso - Casos Acompanhados: 120", municipio: "Sorriso" },
          { nome: "Centro de Detenção Provisória", lat: -15.90, lng: -52.25, tipo: "Sistema Prisional", extra: "Barra do Garças - Capacidade: 80%", municipio: "Barra do Garças" }
        ],
        infraestrutura: [
          { nome: "Rodovia MT-251 (Cuiabá-Chapada)", lat: -15.46, lng: -55.75, tipo: "Rodoviária", extra: "Obras de Manutenção - 60% Concluído", municipio: "Cuiabá" },
          { nome: "Ponte sobre o Rio Paraguai", lat: -16.08, lng: -57.66, tipo: "Rodoviária", extra: "Cáceres - Tráfego: Alto", municipio: "Cáceres" },
          { nome: "Usina Hidrelétrica de Teles Pires", lat: -9.42, lng: -56.01, tipo: "Energia", extra: "Alta Floresta - Geração: 1820 MW", municipio: "Alta Floresta" },
          { nome: "Ferrovia de Integração Estadual", lat: -16.48, lng: -54.60, tipo: "Ferroviária", extra: "Rondonópolis - Expansão Norte", municipio: "Rondonópolis" },
          { nome: "Aeroporto Internacional Marechal Rondon", lat: -15.65, lng: -56.11, tipo: "Aeroportuária", extra: "Várzea Grande - Movimento: Alto", municipio: "Várzea Grande" },
          { nome: "Aeroporto Presidente João Batista Figueiredo", lat: -11.88, lng: -55.53, tipo: "Aeroportuária", extra: "Sinop - Movimento: Médio", municipio: "Sinop" },
          { nome: "Rodovia BR-163", lat: -13.00, lng: -55.90, tipo: "Rodoviária", extra: "Lucas do Rio Verde - Concessão Ativa", municipio: "Outros" }
        ],
        financas: [
          { nome: "Sefaz Sede", lat: -15.58, lng: -56.09, tipo: "Gestão Central", extra: "Cuiabá - Operacional", municipio: "Cuiabá" },
          { nome: "Agência Fazendária Norte", lat: -11.87, lng: -55.51, tipo: "Arrecadação", extra: "Sinop - Crescimento: +15%", municipio: "Sinop" },
          { nome: "Posto Fiscal Correntes", lat: -17.58, lng: -54.73, tipo: "Fiscalização de Fronteira", extra: "Itiquira/MS - Operacional", municipio: "Outros" },
          { nome: "Agência Fazendária Sul", lat: -16.47, lng: -54.64, tipo: "Arrecadação", extra: "Rondonópolis - Operacional", municipio: "Rondonópolis" },
          { nome: "Agência Fazendária Araguaia", lat: -15.89, lng: -52.26, tipo: "Arrecadação", extra: "Barra do Garças - Crescimento: +8%", municipio: "Barra do Garças" },
          { nome: "Agência Fazendária Oeste", lat: -16.07, lng: -57.68, tipo: "Arrecadação", extra: "Cáceres - Operacional", municipio: "Cáceres" }
        ],
        assistencia: [
          { nome: "CRAS Dom Aquino", lat: -15.61, lng: -56.08, tipo: "Assistência Social", extra: "Cuiabá - Famílias Atendidas: 4.200", municipio: "Cuiabá" },
          { nome: "Centro de Convivência de Idosos", lat: -15.65, lng: -56.13, tipo: "Terceira Idade", extra: "Várzea Grande - Vagas Preenchidas: 100%", municipio: "Várzea Grande" },
          { nome: "CRAS Central Rondonópolis", lat: -16.48, lng: -54.63, tipo: "Assistência Social", extra: "Rondonópolis - Famílias Atendidas: 2.800", municipio: "Rondonópolis" },
          { nome: "Restaurante Popular Sede", lat: -15.60, lng: -56.09, tipo: "Segurança Alimentar", extra: "Cuiabá - Refeições/dia: 1.500", municipio: "Cuiabá" },
          { nome: "Centro de Acolhimento Sinop", lat: -11.86, lng: -55.49, tipo: "Moradia Provisória", extra: "Sinop - Ocupação: 95%", municipio: "Sinop" },
          { nome: "CRAS Jardim Primavera", lat: -12.54, lng: -55.70, tipo: "Assistência Social", extra: "Sorriso - Famílias Atendidas: 1.100", municipio: "Sorriso" },
          { nome: "Centro de Reabilitação para Dependentes", lat: -14.63, lng: -57.49, tipo: "Saúde Mental", extra: "Tangará da Serra - Ativos: 85", municipio: "Tangará da Serra" }
        ]
      };

      // Estatísticas Analíticas por Tema Expandidas
      var statsData = {
        geral: { title: "ESTATÍSTICAS GERAIS (MT)", stats: [ {l: "Total de Ativos Mapeados:", v: "51"}, {l: "Conexões IoT Ativas:", v: "12.450"}, {l: "Status da Rede Estadual:", v: "Estável", c: "#10b981"} ] },
        saude: { title: "DADOS DA SAÚDE (MT)", stats: [ {l: "Unidades de Saúde (Total):", v: "900"}, {l: "Leitos UTI Ocupados:", v: "82%", c: "#ef4444"}, {l: "Atendimentos Mês (Est.):", v: "185 Mil"} ] },
        educacao: { title: "DADOS DA EDUCAÇÃO (MT)", stats: [ {l: "Escolas Estaduais (Total):", v: "727"}, {l: "Alunos Rede Estadual:", v: "385.000"}, {l: "Conectividade Escolar:", v: "94%", c: "#10b981"} ] },
        seguranca: { title: "DADOS DA SEGURANÇA (MT)", stats: [ {l: "Bases e Delegacias (Total):", v: "300"}, {l: "Câmeras Integradas:", v: "4.850"}, {l: "Índice de Criminalidade:", v: "-8%", c: "#10b981"} ] },
        infraestrutura: { title: "INFRAESTRUTURA (MT)", stats: [ {l: "Obras e Ativos (Total):", v: "250"}, {l: "Manutenção Rodovias:", v: "72% Concluído", c: "#f59e0b"}, {l: "Energia (Renovável):", v: "85%", c: "#10b981"} ] },
        financas: { title: "DADOS TRIBUTÁRIOS (MT)", stats: [ {l: "Postos Fiscais:", v: "6"}, {l: "Arrecadação Prevista:", v: "R$ 38.5 Bi", c: "#10b981"}, {l: "Crescimento Anual:", v: "+14%"} ] },
        assistencia: { title: "ASSISTÊNCIA SOCIAL (MT)", stats: [ {l: "Equipamentos Sociais (Total):", v: "180"}, {l: "Famílias SER Família:", v: "350.000"}, {l: "Segurança Alimentar:", v: "Alta Cobertura", c: "#38bdf8"} ] }
      };

      const randomCities = ["Cuiabá", "Várzea Grande", "Rondonópolis", "Sinop", "Sorriso", "Tangará da Serra", "Cáceres", "Alta Floresta", "Barra do Garças"];
      function getRandomCity() { return randomCities[Math.floor(Math.random() * randomCities.length)]; }

      // Gerador dinâmico de escolas para totalizar as 727 unidades estaduais
      for(let i = 1; i <= 719; i++) {
        let lat = -17.5 + Math.random() * 8.0; // bounding box aproximado de MT
        let lng = -61.0 + Math.random() * 10.5;
        markersData.educacao.push({
          nome: "Escola Estadual Unidade " + (i + 8),
          lat: lat,
          lng: lng,
          tipo: "Ensino Básico",
          extra: "MT - Status: Operacional",
          municipio: getRandomCity()
        });
      }

      // Gerador dinâmico de unidades de saúde (UBS e Clínicas) para totalizar 900 unidades
      for(let j = 1; j <= 892; j++) {
        let lat = -17.5 + Math.random() * 8.0; 
        let lng = -61.0 + Math.random() * 10.5;
        markersData.saude.push({
          nome: "Unidade Básica de Saúde (UBS) #" + j,
          lat: lat,
          lng: lng,
          tipo: "Atenção Básica",
          extra: "MT - Atendimento SUS",
          municipio: getRandomCity()
        });
      }

      // Gerador dinâmico de segurança (Delegacias e BPMs) para totalizar 300 unidades
      for(let k = 1; k <= 293; k++) {
        let lat = -17.5 + Math.random() * 8.0; 
        let lng = -61.0 + Math.random() * 10.5;
        markersData.seguranca.push({
          nome: k % 2 === 0 ? "Batalhão PM #" + k : "Delegacia PJC #" + k,
          lat: lat,
          lng: lng,
          tipo: k % 2 === 0 ? "Policiamento Ostensivo" : "Polícia Judiciária",
          extra: "MT - Operacional",
          municipio: getRandomCity()
        });
      }

      // Gerador dinâmico de infraestrutura (Obras e Rodovias) para totalizar 250 unidades
      for(let w = 1; w <= 243; w++) {
        let lat = -17.5 + Math.random() * 8.0; 
        let lng = -61.0 + Math.random() * 10.5;
        let tipoObra = w % 3 === 0 ? "Usina / Energia" : (w % 3 === 1 ? "Manutenção Rodoviária" : "Ponte / Viaduto");
        markersData.infraestrutura.push({
          nome: "Obra de Infraestrutura #" + w,
          lat: lat,
          lng: lng,
          tipo: tipoObra,
          extra: "MT - Status: Em Andamento",
          municipio: getRandomCity()
        });
      }

      // Gerador dinâmico de assistência social (CRAS/CREAS) para totalizar 180 unidades
      for(let s = 1; s <= 173; s++) {
        let lat = -17.5 + Math.random() * 8.0; 
        let lng = -61.0 + Math.random() * 10.5;
        let tipoSocial = s % 3 === 0 ? "CREAS" : (s % 3 === 1 ? "Restaurante Popular" : "CRAS");
        markersData.assistencia.push({
          nome: "Unidade " + tipoSocial + " #" + s,
          lat: lat,
          lng: lng,
          tipo: "Atenção Social",
          extra: "MT - Atendimento à População",
          municipio: getRandomCity()
        });
      }

      var currentMarkers = [];
      var activeTheme = 'geral';

      function updateMap(theme) {
        if(theme) activeTheme = theme;
        
        // Remover marcadores antigos
        currentMarkers.forEach(m => map.removeLayer(m));
        currentMarkers = [];

        var color = colors[activeTheme];
        var data = markersData[activeTheme] || [];
        var selectedCity = document.getElementById('cityFilter') ? document.getElementById('cityFilter').value : 'todos';

        // Filtrar por município, se selecionado
        if(selectedCity !== 'todos') {
          data = data.filter(item => item.municipio === selectedCity);
        }

        // Adicionar novos marcadores com cor do tema (usando SVG icon para cor customizada)
        data.forEach(function(ativo) {
          var customIcon = L.divIcon({
            className: 'custom-icon',
            html: `<div style="background-color: ${color}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 5px ${color};"></div>`,
            iconSize: [14, 14],
            iconAnchor: [7, 7]
          });

          var marker = L.marker([ativo.lat, ativo.lng], {icon: customIcon}).addTo(map);
          
          var popupHTML = `
            <h3 style="color: ${color} !important;">${ativo.nome}</h3>
            <p><strong>Tipo:</strong> ${ativo.tipo}</p>
            <p>${ativo.extra}</p>
          `;
          marker.bindPopup(popupHTML);
          currentMarkers.push(marker);
        });

        // Ajustar visualização do mapa para focar nos pontos
        if(data.length > 0) {
          var group = new L.featureGroup(currentMarkers);
          map.flyToBounds(group.getBounds().pad(0.5), {duration: 1.5});
        }

        // Atualizar Sidebar Analítica
        var stats = statsData[activeTheme];
        document.getElementById('stats-title').innerText = stats.title + (selectedCity !== 'todos' ? ` - ${selectedCity}` : '');
        
        var statsHtml = '';
        stats.stats.forEach(s => {
          var valStyle = s.c ? `color: ${s.c};` : '';
          statsHtml += `<div class="stat-row"><span class="stat-label">${s.l}</span> <span class="stat-value" style="${valStyle}">${s.v}</span></div>`;
        });
        document.getElementById('stats-content').innerHTML = statsHtml;
      }

      // Evento do Filtro de Cidade
      document.getElementById('cityFilter').addEventListener('change', function() {
        updateMap();
      });

      // Interação de Clique nos Botões
      var buttons = document.querySelectorAll('.theme-btn');
      buttons.forEach(btn => {
        btn.addEventListener('click', function() {
          // Remove active class de todos
          buttons.forEach(b => b.classList.remove('active'));
          // Adiciona no clicado
          this.classList.add('active');
          
          // Roda a atualização do mapa
          var theme = this.getAttribute('data-theme');
          updateMap(theme);
        });
      });

      // Init inicial
      updateMap('geral');
    }
  });
</script>

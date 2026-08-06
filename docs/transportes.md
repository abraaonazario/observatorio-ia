---
hide:
  - navigation
  - toc
---

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>document.body.classList.add('dashboard-page');</script>

<style>
  :root {
    --theme-color: #ef4444; /* Red for fuel/energy */
    --bg-dark: #0b0f19;
    --panel-bg: #0f172a;
    --border-color: #1e293b;
  }
  
  .dashboard-container {
    padding: 0 2rem 2rem calc(78px + 2rem) !important;
    margin-top: 90px !important;
    min-height: calc(100vh - 90px);
    background: var(--bg-dark);
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
    box-sizing: border-box;
  }
  
  .dash-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    padding-top: 1.5rem;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 1.5rem;
  }
  
  .dash-title-group h1 {
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    margin: 0 0 0.4rem 0 !important;
  }
  
  .dash-title-group p {
    font-size: 0.95rem;
    color: #64748b;
    margin: 0;
  }
  
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .kpi-card {
    background: rgba(30, 41, 59, 0.45);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  }
  
  .kpi-icon-box {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
  }
  
  .kpi-info {
    display: flex;
    flex-direction: column;
  }
  
  .kpi-num {
    font-size: 1.6rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
  }
  
  .kpi-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #64748b;
    margin-top: 0.2rem;
  }
  
  .charts-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  @media (max-width: 992px) {
    .charts-grid {
      grid-template-columns: 1fr;
    }
  }
  
  .chart-card {
    background: rgba(30, 41, 59, 0.3);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    display: flex;
    flex-direction: column;
  }
  
  .chart-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.5rem;
  }
  
  .chart-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #ffffff;
  }
  
  .chart-subtitle {
    font-size: 0.8rem;
    color: #64748b;
    margin-top: 0.2rem;
  }
  
  .chart-body {
    position: relative;
    min-height: 300px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem;
    color: #94a3b8;
  }
  
  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(255, 255, 255, 0.1);
    border-left-color: var(--theme-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>

<!-- Sidebar -->
<aside class="pbi-sidebar">
  <div class="pbi-nav-btn" title="Início" onclick="window.location.href='../'" style="cursor:pointer;">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
    <span class="nav-label">Início</span>
  </div>
  <div style="width:52px; height:1px; background:rgba(255,255,255,0.15); margin: 2px 0;"></div>
  
  <div class="pbi-nav-btn theme-saude" title="Saúde" onclick="window.location.href='../saude/'" style="cursor:pointer;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#22d3ee" stroke-width="2.5"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>
    <span class="nav-label" style="color:#22d3ee;">Saúde</span>
  </div>
  
  <div class="pbi-nav-btn theme-edu" title="Educação" onclick="window.location.href='../educacao/'" style="cursor:pointer;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2.5"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
    <span class="nav-label" style="color:#a78bfa;">Educação</span>
  </div>
  
  <div class="pbi-nav-btn theme-seg" title="Segurança" onclick="window.location.href='../seguranca/'" style="cursor:pointer;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fb923c" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
    <span class="nav-label" style="color:#fb923c;">Segurança</span>
  </div>
  
  <div class="pbi-nav-btn theme-inf" title="Transportes" style="cursor:pointer; background: rgba(250, 204, 21, 0.15);">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ca8a04" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><polygon points="10 8 16 12 10 16 10 8"></polygon></svg>
    <span class="nav-label" style="color:#ca8a04;">Transportes</span>
  </div>
</aside>

<div class="dashboard-container">
  
  <div class="dash-header">
    <div class="dash-title-group">
      <h1>Painel de Transportes (Combustíveis)</h1>
      <p>Dados oficiais de revendedores autorizados no estado de Mato Grosso</p>
    </div>
    <div style="text-align: right;">
      <span style="font-size: 0.75rem; color: #64748b; text-transform: uppercase;">Fonte de Dados</span><br>
      <strong style="color: var(--theme-color); font-weight: 700;">API Pública ANP</strong>
    </div>
  </div>
  
  <div id="loading-state" class="loading-container">
    <div class="spinner"></div>
    <p>Conectando à ANP e processando dados do Mato Grosso...</p>
  </div>

  <div id="dashboard-content" style="display: none;">
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-icon-box" style="background: rgba(239, 68, 68, 0.15); color: #ef4444;">⛽</div>
        <div class="kpi-info">
          <span class="kpi-num" id="kpi-postos">0</span>
          <span class="kpi-label">Postos Ativos (MT)</span>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon-box" style="background: rgba(139, 92, 246, 0.15); color: #8b5cf6;">🏢</div>
        <div class="kpi-info">
          <span class="kpi-num" id="kpi-distribuidoras">0</span>
          <span class="kpi-label">Distribuidoras</span>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon-box" style="background: rgba(74, 222, 128, 0.15); color: #4ade80;">🗺️</div>
        <div class="kpi-info">
          <span class="kpi-num" id="kpi-municipios">0</span>
          <span class="kpi-label">Municípios Atendidos</span>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon-box" style="background: rgba(34, 211, 238, 0.15); color: #22d3ee;">🛢️</div>
        <div class="kpi-info">
          <span class="kpi-num" id="kpi-tancagem">0</span>
          <span class="kpi-label">Tancagem Total (m³)</span>
        </div>
      </div>
    </div>
    
    <div class="charts-grid">
      <div class="chart-card">
        <div class="chart-header">
          <div>
            <div class="chart-title">Postos por Distribuidora</div>
            <div class="chart-subtitle">Top 10 Bandeiras presentes no estado</div>
          </div>
        </div>
        <div class="chart-body">
          <canvas id="chartDistribuidoras"></canvas>
        </div>
      </div>
      
      <div class="chart-card">
        <div class="chart-header">
          <div>
            <div class="chart-title">Concentração por Município</div>
            <div class="chart-subtitle">Top 10 cidades com mais postos registrados</div>
          </div>
        </div>
        <div class="chart-body">
          <canvas id="chartMunicipios"></canvas>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', async () => {
  try {
    // Usando dados processados localmente devido a bloqueios na API
    const targetUrl = '../data/combustiveis_mt.json';
    const response = await fetch(targetUrl);
    const result = await response.json();
    
    if (result.status === 200 && result.data) {
      // 1. Filtrar dados do Mato Grosso (MT)
      const dataMT = result.data.filter(item => item.uf === 'MT');
      
      // 2. Processar KPIs
      const distribuidoras = new Set();
      const municipios = new Set();
      let totalTancagem = 0;
      
      const distribuidorasCount = {};
      const municipiosCount = {};
      
      dataMT.forEach(posto => {
        distribuidoras.add(posto.distribuidora);
        municipios.add(posto.municipio);
        
        // Sum tancagem from products
        if (posto.produtos && posto.produtos.length > 0) {
          posto.produtos.forEach(prod => {
            if (prod.tancagem) {
              totalTancagem += Number(prod.tancagem);
            }
          });
        }
        
        // Count for charts
        distribuidorasCount[posto.distribuidora] = (distribuidorasCount[posto.distribuidora] || 0) + 1;
        municipiosCount[posto.municipio] = (municipiosCount[posto.municipio] || 0) + 1;
      });
      
      // Update DOM
      document.getElementById('kpi-postos').innerText = dataMT.length.toLocaleString('pt-BR');
      document.getElementById('kpi-distribuidoras').innerText = distribuidoras.size.toLocaleString('pt-BR');
      document.getElementById('kpi-municipios').innerText = municipios.size.toLocaleString('pt-BR');
      document.getElementById('kpi-tancagem').innerText = Math.round(totalTancagem).toLocaleString('pt-BR');
      
      // Process Data for Charts (Top 10)
      const topDistribuidoras = Object.entries(distribuidorasCount)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);
        
      const topMunicipios = Object.entries(municipiosCount)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);

      // Hide loading, show content
      document.getElementById('loading-state').style.display = 'none';
      document.getElementById('dashboard-content').style.display = 'block';
      
      // Draw Charts
      Chart.defaults.color = '#94a3b8';
      Chart.defaults.font.family = 'Inter';
      
      // Pie Chart: Distribuidoras
      new Chart(document.getElementById('chartDistribuidoras'), {
        type: 'doughnut',
        data: {
          labels: topDistribuidoras.map(d => d[0]),
          datasets: [{
            data: topDistribuidoras.map(d => d[1]),
            backgroundColor: [
              '#ef4444', '#f97316', '#f59e0b', '#84cc16', '#22c55e',
              '#14b8a6', '#06b6d4', '#3b82f6', '#8b5cf6', '#d946ef'
            ],
            borderWidth: 0,
            hoverOffset: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'right', labels: { color: '#cbd5e1' } }
          }
        }
      });
      
      // Bar Chart: Municipios
      new Chart(document.getElementById('chartMunicipios'), {
        type: 'bar',
        data: {
          labels: topMunicipios.map(m => m[0]),
          datasets: [{
            label: 'Número de Postos',
            data: topMunicipios.map(m => m[1]),
            backgroundColor: 'rgba(239, 68, 68, 0.8)',
            borderRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            y: { grid: { color: 'rgba(255,255,255,0.05)' }, beginAtZero: true },
            x: { grid: { display: false } }
          }
        }
      });
      
    }
  } catch (error) {
    document.getElementById('loading-state').innerHTML = `<p style="color: #ef4444;">Erro ao carregar dados da ANP.</p>`;
    console.error('Error fetching ANP data:', error);
  }
});
</script>

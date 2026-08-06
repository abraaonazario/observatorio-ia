---
hide:
  - navigation
  - toc
---

<script>document.body.classList.add('dashboard-page');</script>

<style>
  :root {
    --theme-color: #10b981; /* Verde das Finanças */
  }
</style>

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
  <div class="pbi-nav-btn theme-fin active" title="Finanças" onclick="window.location.href='../financas/'" style="cursor:pointer;">
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
  
  <div class="dash-header">
    <div class="dash-title-group">
      <h1>Indicadores de Finanças e Tributação</h1>
      <p>Agosto 2024 · Estado de MT</p>
    </div>
    <div class="dash-actions">
      <div class="dash-nav-time">
      <span>Última atualização</span>
      <strong>06/07/2026 - 20:24</strong>
    </div>
      <button class="dash-btn">📅 Período</button>
      <button class="dash-btn">↻ Atualizar</button>
    </div>
  </div>

  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-icon">💰</div>
      <span class="kpi-title">ARRECADAÇÃO TOTAL</span>
      <h3 class="kpi-value">R$ 3.2B</h3>
      <span class="kpi-trend">+4,5% vs. mês anterior</span>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon">🧾</div>
      <span class="kpi-title">RECEITA TRIBUTÁRIA</span>
      <h3 class="kpi-value">R$ 2.5B</h3>
      <span class="kpi-trend">+5,1% vs. mês anterior</span>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon">📉</div>
      <span class="kpi-title">INADIMPLÊNCIA</span>
      <h3 class="kpi-value">6,4%</h3>
      <span class="kpi-trend negative">-1,2% vs. mês anterior</span>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon">💸</div>
      <span class="kpi-title">DESPESA EMPENHADA</span>
      <h3 class="kpi-value">R$ 1.8B</h3>
      <span class="kpi-trend">+2,4% vs. mês anterior</span>
    </div>
  </div>

  <div class="charts-grid">
    <div class="chart-card">
      <div class="chart-header">
        <div>
          <div class="chart-title">Receitas vs. Despesas</div>
          <div class="chart-subtitle">Evolução mensal — Jan a Ago 2024</div>
        </div>
        <span class="chart-badge">Acumulado 2024</span>
      </div>
      <div class="chart-body">
        <canvas id="lineChartFinancas"></canvas>
      </div>
    </div>
    <div class="chart-card">
      <div class="chart-header">
        <div>
          <div class="chart-title">Fontes de Arrecadação</div>
          <div class="chart-subtitle">Composição percentual</div>
        </div>
      </div>
      <div class="chart-body" style="display: flex; align-items: center; justify-content: center;">
        <canvas id="donutChartFinancas"></canvas>
      </div>
    </div>
  </div>

  <div class="charts-grid">
    <div class="chart-card">
      <div class="chart-header">
        <div>
          <div class="chart-title">Execução Orçamentária (%)</div>
          <div class="chart-subtitle">Jan - Ago 2024</div>
        </div>
      </div>
      <div class="chart-body">
        <canvas id="barChartFinancas"></canvas>
      </div>
    </div>
    <div class="chart-card">
      <div class="chart-header">
        <div>
          <div class="chart-title">Status & Alertas</div>
          <div class="chart-subtitle">Indicadores críticos</div>
        </div>
      </div>
      <div class="alert-list">
        <div class="alert-item">
          <div class="alert-label"><span class="alert-icon ok">✓</span> Limite de Gastos com Pessoal</div>
          <div class="alert-meta">Max: 49% <span class="alert-value">42%</span></div>
        </div>
        <div class="alert-item">
          <div class="alert-label"><span class="alert-icon ok">✓</span> Dívida Consolidada</div>
          <div class="alert-meta">Livre <span class="alert-value">Controlada</span></div>
        </div>
        <div class="alert-item">
          <div class="alert-label"><span class="alert-icon warn">⚠</span> Arrecadação IPVA</div>
          <div class="alert-meta">Meta: 95% <span class="alert-value" style="color:#f59e0b">88%</span></div>
        </div>
      </div>
    </div>
  </div>

</div>

<script>
  document.addEventListener("DOMContentLoaded", function() {
    Chart.defaults.color = '#94a3b8'; Chart.defaults.font.family = 'Inter';
    
    new Chart(document.getElementById('lineChartFinancas'), {
      type: 'line',
      data: {
        labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago'],
        datasets: [{
          label: 'Receitas', data: [2.8, 2.9, 3.1, 3.0, 3.2, 3.3, 3.2, 3.4], borderColor: '#10b981', tension: 0.4
        }, {
          label: 'Despesas', data: [1.5, 1.6, 1.6, 1.7, 1.8, 1.9, 1.8, 1.8], borderColor: '#f43f5e', tension: 0.4
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { grid: { color: '#1e293b' } }, x: { grid: { display: false } } } }
    });

    new Chart(document.getElementById('donutChartFinancas'), {
      type: 'doughnut',
      data: {
        labels: ['ICMS', 'IPVA', 'FPE', 'Outros'],
        datasets: [{ data: [60, 15, 15, 10], backgroundColor: ['#10b981', '#38bdf8', '#f59e0b', '#8b5cf6'], borderWidth: 0 }]
      },
      options: { responsive: true, maintainAspectRatio: false, cutout: '70%', plugins: { legend: { position: 'right' } } }
    });

    new Chart(document.getElementById('barChartFinancas'), {
      type: 'bar',
      data: {
        labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago'],
        datasets: [{ data: [12, 24, 36, 48, 60, 72, 84, 95], backgroundColor: '#10b981', borderRadius: 4 }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { max: 100, grid: { color: '#1e293b' } }, x: { grid: { display: false } } } }
    });
  });
</script>

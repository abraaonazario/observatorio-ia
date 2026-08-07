---
hide:
  - navigation
  - toc
  - header
---

<script>document.body.classList.add('dashboard-page');</script>

<style>
  :root {
    --theme-color: #0ea5e9;
  }

  .dash-nav-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    padding: 1rem 2rem;
    background: rgba(15, 23, 42, 0.95);
    border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    position: sticky;
    top: 0;
    z-index: 10;
  }

  .dash-nav-left {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .dash-nav-back {
    color: #cbd5e1;
    text-decoration: none;
    font-weight: 600;
  }

  .dash-nav-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .dash-nav-logo {
    width: 40px;
    height: 40px;
    display: grid;
    place-items: center;
    border-radius: 12px;
    background: linear-gradient(135deg, #0ea5e9, #3b82f6);
    color: white;
  }

  .dash-nav-titles {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
  }

  .dash-nav-main-title {
    font-weight: 800;
    color: #f8fafc;
  }

  .dash-nav-sub-title {
    color: #94a3b8;
    font-size: 0.85rem;
  }

  .dash-nav-tabs {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    align-items: center;
  }

  .dash-tab {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.75rem 1rem;
    border-radius: 999px;
    border: 1px solid rgba(148, 163, 184, 0.18);
    color: #cbd5e1;
    background: rgba(15, 23, 42, 0.85);
    text-decoration: none;
    font-weight: 600;
    transition: all 0.2s;
  }

  .dash-tab.active,
  .dash-tab:hover {
    border-color: rgba(14, 165, 233, 0.65);
    background: rgba(14, 165, 233, 0.12);
    color: #ffffff;
  }

  .dash-nav-right {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
  }

  .dash-btn-icon {
    display: inline-flex;
    align-items: center;
    padding: 0.65rem 1rem;
    border-radius: 999px;
    border: 1px solid rgba(148, 163, 184, 0.18);
    background: rgba(15, 23, 42, 0.85);
    color: #cbd5e1;
    text-decoration: none;
    font-size: 0.9rem;
    transition: all 0.2s;
  }

  .dash-btn-icon:hover {
    border-color: rgba(16, 185, 129, 0.6);
    color: #ffffff;
  }

  .dash-nav-time {
    text-align: right;
    color: #94a3b8;
    font-size: 0.8rem;
  }

  .dash-nav-time strong {
    display: block;
    margin-top: 0.25rem;
    color: #ffffff;
  }

  .dashboard-container {
    padding: 2rem;
    min-height: calc(100vh - 100px);
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, #090a11 100%);
    color: #e2e8f0;
  }

  .dash-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
  }

  .dash-title-group h1 {
    margin: 0;
    font-size: 2.2rem;
    letter-spacing: -0.03em;
  }

  .dash-title-group p {
    margin: 0.5rem 0 0;
    color: #94a3b8;
  }

  .dash-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .dash-btn {
    background: rgba(14, 165, 233, 0.08);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 999px;
    color: #ffffff;
    padding: 0.9rem 1.4rem;
    font-weight: 700;
    cursor: pointer;
  }

  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .kpi-card {
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 18px;
    padding: 1.2rem;
    min-height: 160px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .kpi-icon {
    width: 44px;
    height: 44px;
    display: grid;
    place-items: center;
    border-radius: 14px;
    background: rgba(14, 165, 233, 0.14);
    color: #38bdf8;
    font-size: 1.2rem;
  }

  .kpi-title {
    display: block;
    margin-top: 1rem;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    color: #94a3b8;
  }

  .kpi-value {
    margin: 0.8rem 0 0;
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
  }

  .kpi-trend {
    color: #6ee7b7;
    font-size: 0.9rem;
    margin-top: 0.5rem;
  }

  .charts-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .chart-card {
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 18px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    min-height: 360px;
  }

  .chart-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 1.2rem 1.5rem 0 1.5rem;
    gap: 1rem;
  }

  .chart-title {
    font-size: 1rem;
    font-weight: 700;
    color: #f8fafc;
  }

  .chart-subtitle {
    color: #94a3b8;
    font-size: 0.9rem;
    margin-top: 0.25rem;
  }

  .chart-badge {
    background: rgba(14, 165, 233, 0.12);
    color: #38bdf8;
    padding: 0.45rem 0.8rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    align-self: flex-start;
  }

  .chart-body {
    flex: 1;
    padding: 1rem 1.5rem 1.5rem;
    min-height: 260px;
  }

  canvas {
    width: 100% !important;
    height: 100% !important;
  }

  .alert-list {
    display: grid;
    gap: 0.85rem;
    padding: 0 1.5rem 1.5rem;
  }

  .alert-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(148, 163, 184, 0.08);
    border-radius: 14px;
    padding: 1rem;
  }

  .alert-label {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-weight: 700;
    color: #f8fafc;
  }

  .alert-icon {
    width: 28px;
    height: 28px;
    display: grid;
    place-items: center;
    border-radius: 8px;
    background: rgba(56, 189, 248, 0.15);
  }

  .alert-meta {
    margin-top: 0.5rem;
    color: #94a3b8;
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .alert-value {
    font-weight: 700;
    color: #ffffff;
  }

  .alert-icon.ok { background: rgba(16, 185, 129, 0.18); }
  .alert-icon.warn { background: rgba(251, 191, 36, 0.18); }

  @media (max-width: 1100px) {
    .charts-grid { grid-template-columns: 1fr; }
    .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  }

  @media (max-width: 680px) {
    .dash-nav-header { flex-direction: column; align-items: stretch; }
    .dash-nav-right { justify-content: flex-start; }
    .kpi-grid { grid-template-columns: 1fr; }
  }
</style>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

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
      <h1>Dashboard MT 360</h1>
      <p>Indicadores de execução e desempenho - RAG 2025 Mato Grosso</p>
    </div>
    <div class="dash-actions">
      <button class="dash-btn">📅 2025</button>
      <button class="dash-btn">↻ Atualizar</button>
    </div>
  </div>

  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-icon">📊</div>
      <span class="kpi-title">Desempenho Indicadores</span>
      <h3 class="kpi-value">97%</h3>
      <span class="kpi-trend">RAG 2025 - Meta atingida</span>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon">💰</div>
      <span class="kpi-title">Execução Financeira</span>
      <h3 class="kpi-value">R$ 35,79B</h3>
      <span class="kpi-trend">De R$ 38,94B alocados</span>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon">🎯</div>
      <span class="kpi-title">Eixo Social</span>
      <h3 class="kpi-value">100%</h3>
      <span class="kpi-trend">R$ 11,23B mobilizado</span>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon">⚙️</div>
      <span class="kpi-title">Eixo Institucional</span>
      <h3 class="kpi-value">109%</h3>
      <span class="kpi-trend">Acima da meta planejada</span>
    </div>
  </div>

  <div class="charts-grid">
    <div class="chart-card">
      <div class="chart-header">
        <div>
          <div class="chart-title">Execução Mensal (2025)</div>
          <div class="chart-subtitle">Desempenho acumulado de indicadores e orçamento</div>
        </div>
        <span class="chart-badge">RAG 2025</span>
      </div>
      <div class="chart-body">
        <canvas id="lineChartObsIA"></canvas>
      </div>
    </div>

    <div class="chart-card">
      <div class="chart-header">
        <div>
          <div class="chart-title">Desempenho por Eixo</div>
          <div class="chart-subtitle">% atingido em relação à meta - 2025</div>
        </div>
      </div>
      <div class="chart-body" style="display:flex;align-items:center;justify-content:center;">
        <canvas id="donutChartObsIA"></canvas>
      </div>
    </div>
  </div>

  <div class="charts-grid">
    <div class="chart-card">
      <div class="chart-header">
        <div>
          <div class="chart-title">Execução por Eixo (RAG 2025)</div>
          <div class="chart-subtitle">Percentual de atingimento de metas por eixo estratégico</div>
        </div>
      </div>
      <div class="chart-body">
        <canvas id="barChartObsIA"></canvas>
      </div>
    </div>

    <div class="chart-card">
      <div class="chart-header">
        <div>
          <div class="chart-title">Status de Execução</div>
          <div class="chart-subtitle">Indicadores críticos - 2025</div>
        </div>
      </div>
      <div class="alert-list">
        <div class="alert-item">
          <div class="alert-label"><span class="alert-icon ok">✓</span> Desempenho Indicadores</div>
          <div class="alert-meta">RAG 2025 Meta <span class="alert-value">97%</span></div>
        </div>
        <div class="alert-item">
          <div class="alert-label"><span class="alert-icon ok">✓</span> Eixo Social</div>
          <div class="alert-meta">R$ 11,23B mobilizado <span class="alert-value">100%</span></div>
        </div>
        <div class="alert-item">
          <div class="alert-label"><span class="alert-icon ok">✓</span> Execução Financeira</div>
          <div class="alert-meta">R$ 35,79B executado <span class="alert-value">97%</span></div>
        </div>
        <div class="alert-item">
          <div class="alert-label"><span class="alert-icon ok">✓</span> Eixo Institucional</div>
          <div class="alert-meta">Desempenho acima da meta <span class="alert-value">109%</span></div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
  document.addEventListener('DOMContentLoaded', function() {
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = 'Inter, Roboto, sans-serif';

    new Chart(document.getElementById('lineChartObsIA'), {
      type: 'line',
      data: {
        labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
        datasets: [
          {
            label: 'Desempenho (% meta atingida)',
            data: [82, 85, 88, 90, 92, 94, 95, 96, 96, 97, 97, 97],
            borderColor: '#0ea5e9',
            backgroundColor: 'rgba(14, 165, 233, 0.18)',
            fill: true,
            tension: 0.35
          },
          {
            label: 'Execução Financeira (%)',
            data: [75, 78, 81, 84, 87, 90, 92, 94, 95, 96, 96, 97],
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.12)',
            fill: true,
            tension: 0.35
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'bottom', labels: { color: '#cbd5e1' } } },
        scales: {
          y: { beginAtZero: false, grid: { color: 'rgba(148, 163, 184, 0.15)' } },
          x: { grid: { display: false } }
        }
      }
    });

    new Chart(document.getElementById('donutChartObsIA'), {
      type: 'doughnut',
      data: {
        labels: ['Social', 'Econômico', 'Ambiental', 'Infraestrutura', 'Digital', 'Institucional', 'Trabalho'],
        datasets: [{
          data: [100, 96, 98, 87, 90, 97, 90],
          backgroundColor: ['#0ea5e9', '#8b5cf6', '#10b981', '#f59e0b', '#06b6d4', '#3b82f6', '#ec4899'],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '72%',
        plugins: { legend: { position: 'right', labels: { color: '#cbd5e1' } } }
      }
    });

    new Chart(document.getElementById('barChartObsIA'), {
      type: 'bar',
      data: {
        labels: ['Social', 'Econômico', 'Ambiental', 'Infraestrutura', 'Digital', 'Institucional', 'Trabalho', 'Outros'],
        datasets: [{
          data: [100, 96, 98, 87, 90, 97, 90, 97],
          backgroundColor: '#0ea5e9',
          borderRadius: 8,
          maxBarThickness: 32
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, max: 110, grid: { color: 'rgba(148, 163, 184, 0.15)' }, ticks: { color: '#cbd5e1' } },
          x: { grid: { display: false }, ticks: { color: '#cbd5e1' } }
        }
      }
    });
  });
</script>

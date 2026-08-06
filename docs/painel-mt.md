---
hide:
  - navigation
  - toc
  - header
---

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">

<style>
  body, html {
    background-color: #09090b !important;
    margin: 0; padding: 0;
  }
  .md-main__inner { margin: 0; padding: 0; max-width: 100%; }
  .md-content { padding: 0; }
  
  .mt-container {
    font-family: 'Inter', sans-serif;
    color: #ffffff;
    padding: 2rem;
    min-height: 100vh;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    background: #09090b;
    box-shadow: inset 0 0 100px rgba(0,0,0,0.5);
  }

  .mt-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 2rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 1.5rem;
  }

  .mt-title { margin: 0; font-size: 2.2rem; font-weight: 800; color: #fff; display: flex; align-items: center; gap: 12px; }
  .mt-title span {
    background: linear-gradient(90deg, #a78bfa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .mt-subtitle { color: #9ca3af; font-size: 0.95rem; margin-top: 5px; }

  .badge-api {
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(52, 211, 153, 0.3);
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    letter-spacing: 0.05em;
  }
  
  .badge-api::before {
    content: ''; width: 8px; height: 8px; background-color: #34d399; border-radius: 50%; box-shadow: 0 0 8px #34d399;
  }

  /* Grid Layout */
  .grid-layout {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 1.5rem;
  }

  /* Cards */
  .kpi-col { display: flex; flex-direction: column; gap: 1.5rem; }
  
  .card {
    background: linear-gradient(145deg, #13141a, #0c0d11);
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
  }

  .card-val { font-size: 2.5rem; font-weight: 800; color: #fff; margin: 10px 0; }
  .card-label { font-size: 0.8rem; color: #9ca3af; text-transform: uppercase; font-weight: 600; letter-spacing: 1px;}
  
  .border-purple { box-shadow: inset 0px 40px 50px -40px rgba(167, 139, 250, 0.15); border-top: 1px solid rgba(167, 139, 250, 0.4); }
  .border-green { box-shadow: inset 0px 40px 50px -40px rgba(16, 185, 129, 0.15); border-top: 1px solid rgba(16, 185, 129, 0.4); }
  
  /* Estilos do cabeçalho do gráfico copiando a imagem */
  .chart-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.5rem;
  }
  .chart-title {
    margin: 0; color: #e5e7eb; font-size: 1rem; font-weight: 600;
  }
  .chart-subtitle {
    font-size: 0.75rem; color: #9ca3af; margin-top: 0.25rem;
  }
  .chart-badge {
    font-size: 0.65rem; background: #1f2937; color: #9ca3af; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.05em; font-weight: bold;
  }

  @media (max-width: 900px) {
    .grid-layout { grid-template-columns: 1fr; }
  }
</style>

<div class="mt-container">
  
  <div class="mt-header">
    <div>
      <h1 class="mt-title">Dashboard <span>Portal de Dados MT</span></h1>
      <div class="mt-subtitle">Nov/2025 — Abr/2026 • 6 meses (Simulação da API)</div>
    </div>
    <div class="badge-api">LIVE DATA</div>
  </div>

  <div class="grid-layout">
    
    <!-- Coluna de KPIs -->
    <div class="kpi-col">
      <div class="card border-purple">
        <div class="card-label" style="color: #a78bfa;"><i class="fa-solid fa-database"></i> Bases Catalogadas</div>
        <div class="card-val">1.248</div>
        <div style="font-size: 0.8rem; color: #34d399; font-weight:bold; background: rgba(16, 185, 129, 0.15); padding: 4px; border-radius:4px; display:inline-block;">↑ +11,3% vs 6 meses anteriores</div>
      </div>
      
      <div class="card border-green">
        <div class="card-label" style="color: #34d399;"><i class="fa-solid fa-download"></i> Volume de Downloads</div>
        <div class="card-val">84.512</div>
        <div style="font-size: 0.8rem; color: #34d399; font-weight:bold; background: rgba(16, 185, 129, 0.15); padding: 4px; border-radius:4px; display:inline-block;">↑ +6,7% vs 6 meses anteriores</div>
      </div>
    </div>

    <!-- Coluna de Gráficos -->
    <div class="kpi-col">
      
      <!-- Gráfico de Linha Duplo Estilo TechStore -->
      <div class="card">
        <div class="chart-header">
          <div>
            <h4 class="chart-title">Evolução Mensal • Downloads vs Novos Datasets</h4>
            <div class="chart-subtitle">Pico de acessos em Dez/25 • Total acumulado 84.5K downloads, 1.2K datasets.</div>
          </div>
          <div class="chart-badge">Eixo Duplo</div>
        </div>
        <canvas id="neonAreaChart" height="130"></canvas>
      </div>

      <!-- Gráfico de Rosca Estilo TechStore -->
      <div class="card">
        <div class="chart-header">
          <div>
            <h4 class="chart-title">Downloads por Categoria</h4>
            <div class="chart-subtitle">Saúde lidera com 29.3% dos acessos (24.7K downloads).</div>
          </div>
        </div>
        <canvas id="neonDonutChart" height="100"></canvas>
      </div>

    </div>

  </div>
</div>

<script>
  Chart.defaults.color = '#9ca3af';
  Chart.defaults.font.family = "'Inter', sans-serif";

  document.addEventListener("DOMContentLoaded", function() {
    
    // Gráfico de Linha Neon (Duplo Eixo) igual à imagem de referência
    const ctxArea = document.getElementById('neonAreaChart').getContext('2d');
    
    // Gradiente Roxo para a área principal
    let gradientPurple = ctxArea.createLinearGradient(0, 0, 0, 400);
    gradientPurple.addColorStop(0, 'rgba(167, 139, 250, 0.5)'); // Roxo intenso no topo
    gradientPurple.addColorStop(1, 'rgba(167, 139, 250, 0.0)'); // Transparente na base

    // Gradiente Verde (opcional, na imagem original a linha verde parece não ter preenchimento, mas vamos manter sutil)
    let gradientGreen = ctxArea.createLinearGradient(0, 0, 0, 400);
    gradientGreen.addColorStop(0, 'rgba(52, 211, 153, 0.1)');
    gradientGreen.addColorStop(1, 'rgba(52, 211, 153, 0.0)');

    new Chart(ctxArea, {
      type: 'line',
      data: {
        labels: ['Nov', 'Dez', 'Jan', 'Fev', 'Mar', 'Abr'],
        datasets: [
          {
            label: 'Downloads',
            data: [8.2, 9.3, 6.0, 4.5, 6.5, 6.2],
            borderColor: '#a78bfa', // Roxo Neon
            backgroundColor: gradientPurple,
            borderWidth: 3,
            tension: 0.4,
            fill: true,
            pointBackgroundColor: '#a78bfa',
            pointBorderColor: '#111217',
            pointBorderWidth: 2,
            pointRadius: 0,
            pointHoverRadius: 6,
            yAxisID: 'y'
          },
          {
            label: 'Novos Datasets',
            data: [1.2, 1.8, 1.0, 0.8, 1.3, 1.2],
            borderColor: '#34d399', // Verde Neon
            backgroundColor: 'transparent', // Sem preenchimento, apenas a linha como na ref
            borderWidth: 3,
            tension: 0.4,
            fill: false,
            pointBackgroundColor: '#34d399',
            pointBorderColor: '#111217',
            pointBorderWidth: 2,
            pointRadius: 0,
            pointHoverRadius: 6,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        interaction: { mode: 'index', intersect: false },
        plugins: { 
          legend: { position: 'top', align: 'end', labels: { boxWidth: 10, usePointStyle: true, padding: 20 } },
          tooltip: { backgroundColor: 'rgba(17, 18, 23, 0.95)', titleColor: '#fff', bodyColor: '#cbd5e1', borderColor: '#1f2937', borderWidth: 1, padding: 12 }
        },
        scales: {
          x: { 
            grid: { color: 'rgba(255, 255, 255, 0.05)', borderColor: 'transparent', drawTicks: false },
            ticks: { color: '#6b7280', padding: 10 }
          },
          y: { 
            type: 'linear', display: true, position: 'left',
            grid: { color: 'rgba(255, 255, 255, 0.05)', borderColor: 'transparent', drawTicks: false },
            ticks: { color: '#a78bfa', callback: function(value) { return value + 'K'; }, stepSize: 1, padding: 10 },
            min: 4.0
          },
          y1: { 
            type: 'linear', display: true, position: 'right',
            grid: { drawOnChartArea: false, borderColor: 'transparent', drawTicks: false },
            ticks: { color: '#34d399', callback: function(value) { return value; }, stepSize: 0.2, padding: 10 },
            min: 0.6
          }
        }
      }
    });

    // Gráfico de Rosca Neon com as exatas 4 cores da imagem de referência (Rosa, Amarelo, Verde, Ciano)
    const ctxDonut = document.getElementById('neonDonutChart').getContext('2d');
    new Chart(ctxDonut, {
      type: 'doughnut',
      data: {
        labels: ['Saúde (SES)', 'Educação (SEDUC)', 'Segurança (SESP)', 'Fazenda (SEFAZ)'],
        datasets: [{
          data: [29.3, 25.5, 25.2, 20.0],
          backgroundColor: [
            '#f472b6', // Rosa Neon
            '#fcd34d', // Amarelo
            '#34d399', // Verde Claro
            '#22d3ee'  // Ciano
          ],
          borderColor: '#111217', // Cor de fundo do card para dar o espaçamento grosso
          borderWidth: 4,
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '75%', // Buraco grande no meio
        plugins: { 
          legend: { position: 'right', labels: { color: '#9ca3af', usePointStyle: true, padding: 20 } },
          tooltip: { backgroundColor: 'rgba(17, 18, 23, 0.9)', borderColor: '#1f2937', borderWidth: 1 }
        }
      }
    });
    
  });
</script>

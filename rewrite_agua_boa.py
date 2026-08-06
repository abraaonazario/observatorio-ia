import re

def rewrite_agua_boa():
    path = r"c:\Users\nazap\OneDrive\Área de Trabalho\projeto\Data Lake\Data Lake\docs\cidade-agua-boa.md"
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split before the dash-header
    # We will replace from <div class="cidade-header"> down to the end of the file.
    
    new_content = """      <!-- Cabeçalho Padrão do Dashboard -->
      <div class="dash-header">
        <div class="dash-title-group">
          <h1>Água Boa</h1>
          <p>51 Anos · 09/07 · Perfil Municipal</p>
        </div>
        <div class="dash-actions">
          <div class="dash-nav-time">
            <span>Última atualização</span>
            <strong>16/07/2026 - 15:00</strong>
          </div>
          <button class="dash-btn" onclick="window.location.href='../perfil-municipios/'">↻ Voltar para Municípios</button>
        </div>
      </div>

      <!-- Top 4 KPIs -->
      <div class="kpi-grid">
          <div class="kpi-card">
              <div class="kpi-icon" style="color: #38bdf8;">💰</div>
              <span class="kpi-title">PIB - 2023</span>
              <h3 class="kpi-value">R$ 2,4 bi</h3>
              <span class="kpi-trend" style="color: #cbd5e1;">24º de 142º</span>
          </div>
          <div class="kpi-card">
              <div class="kpi-icon" style="color: #f472b6;">👥</div>
              <span class="kpi-title">POPULAÇÃO</span>
              <h3 class="kpi-value">31.314</h3>
              <span class="kpi-trend" style="color: #cbd5e1;">Habitantes</span>
          </div>
          <div class="kpi-card">
              <div class="kpi-icon" style="color: #4ade80;">🗺️</div>
              <span class="kpi-title">ÁREA TOTAL</span>
              <h3 class="kpi-value">7,5 mil</h3>
              <span class="kpi-trend" style="color: #cbd5e1;">Km²</span>
          </div>
          <div class="kpi-card">
              <div class="kpi-icon" style="color: #a855f7;">💵</div>
              <span class="kpi-title">SALÁRIO MÉDIO (2024)</span>
              <h3 class="kpi-value">2,2 SM</h3>
              <span class="kpi-trend" style="color: #cbd5e1;">76º de 142º</span>
          </div>
      </div>

      <!-- Seção de Gráficos e Status -->
      <div class="charts-grid">
        <!-- Gráfico de Rosca: Gênero -->
        <div class="chart-card">
          <div class="chart-header">
            <div>
              <div class="chart-title">Distribuição por Gênero</div>
              <div class="chart-subtitle">Composição da população</div>
            </div>
          </div>
          <div class="chart-body" style="height: 250px;">
            <canvas id="generoChart"></canvas>
          </div>
        </div>

        <!-- Gráfico de Barras: Raça/Cor -->
        <div class="chart-card">
          <div class="chart-header">
            <div>
              <div class="chart-title">Cor ou Raça (%)</div>
              <div class="chart-subtitle">Perfil demográfico</div>
            </div>
          </div>
          <div class="chart-body" style="height: 250px;">
            <canvas id="racaChart"></canvas>
          </div>
        </div>
        
        <!-- Lista de Indicadores Secundários -->
        <div class="chart-card">
          <div class="chart-header">
            <div>
              <div class="chart-title">Indicadores Regionais</div>
              <div class="chart-subtitle">Saneamento e Emprego</div>
            </div>
          </div>
          <div class="alert-list">
            <div class="alert-item">
              <div class="alert-label"><span class="alert-icon ok">✓</span> Atendimento de Água (2022)</div>
              <div class="alert-meta">Pop. atendida: <span class="alert-value">84,69%</span></div>
            </div>
            <div class="alert-item">
              <div class="alert-label"><span class="alert-icon warn">⚠️</span> Esgotamento Sanitário (2022)</div>
              <div class="alert-meta">Pop. atendida: <span class="alert-value" style="color:#f59e0b">1,54%</span></div>
            </div>
            <div class="alert-item">
              <div class="alert-label"><span class="alert-icon ok">✓</span> Coleta de Resíduos (2022)</div>
              <div class="alert-meta">Pop. atendida: <span class="alert-value">100%</span></div>
            </div>
            <div class="alert-item">
              <div class="alert-label"><span class="alert-icon ok">✓</span> População Ocupada (2024)</div>
              <div class="alert-meta">Formal: <span class="alert-value">24,78%</span></div>
            </div>
            <div class="alert-item">
              <div class="alert-label"><span class="alert-icon ok">✓</span> Bioma Predominante</div>
              <div class="alert-meta"><span class="alert-value">Cerrado</span></div>
            </div>
          </div>
        </div>
      </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
  document.addEventListener("DOMContentLoaded", function() {
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = 'Inter';
    
    // Gráfico Donut (Gênero)
    new Chart(document.getElementById('generoChart'), {
      type: 'doughnut',
      data: {
        labels: ['Homens', 'Mulheres'],
        datasets: [{
          data: [52.2, 47.8],
          backgroundColor: ['#38bdf8', '#ec4899'],
          borderWidth: 0
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, cutout: '70%', plugins: { legend: { position: 'bottom' } } }
    });

    // Gráfico Bar (Raça)
    new Chart(document.getElementById('racaChart'), {
      type: 'bar',
      data: {
        labels: ['Parda', 'Branca', 'Preta', 'Indígena', 'Amarela'],
        datasets: [{
          label: 'Percentual',
          data: [54.4, 36.4, 7.8, 1.2, 0.2],
          backgroundColor: '#8b5cf6',
          borderRadius: 4
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { grid: { color: '#1e293b' } }, x: { grid: { display: false } } } }
    });
  });
</script>
"""

    start_str = '      <!-- Cabeçalho -->'
    parts = content.split(start_str)
    
    final_content = parts[0] + new_content
    with open(path, "w", encoding="utf-8") as f:
        f.write(final_content)

rewrite_agua_boa()

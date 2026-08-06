---
hide:
  - navigation
  - toc
  - header
---

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">

<style>
  /* Base - Tela Cheia e Dark Mode */
  body, html {
    background-color: #09090b !important;
    margin: 0; padding: 0;
  }
  .md-main__inner { margin: 0; padding: 0; max-width: 100%; }
  .md-content { padding: 0; }
  
  .bi-container {
    font-family: 'Inter', Roboto, sans-serif;
    color: #ffffff;
    padding: 2rem;
    min-height: 100vh;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  /* Header do BI */
  .bi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 1rem;
  }
  .bi-title h1 {
    margin: 0; font-size: 2rem; font-weight: 800;
    background: linear-gradient(90deg, #3b82f6, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .bi-title p { margin: 0; color: #9ca3af; font-size: 0.9rem; }
  
  /* Layout da Cadeia de Valor */
  .value-chain {
    display: flex;
    gap: 1rem;
    flex: 1;
  }

  /* Setas Laterais */
  .side-arrow {
    width: 60px;
    background: linear-gradient(180deg, rgba(16,185,129,0.1) 0%, rgba(16,185,129,0.4) 50%, rgba(16,185,129,0.1) 100%);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    writing-mode: vertical-rl;
    text-orientation: mixed;
    transform: rotate(180deg);
    font-weight: 700;
    color: #34d399;
    letter-spacing: 4px;
    text-transform: uppercase;
    box-shadow: 0 0 20px rgba(16,185,129,0.1);
  }
  .side-arrow-right {
    transform: none;
  }

  /* Centro da Cadeia */
  .chain-center {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  /* Seções (Gerencial, Finalístico, Suporte) */
  .section-label {
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    font-size: 0.75rem;
    color: #6b7280;
    letter-spacing: 2px;
    text-transform: uppercase;
    text-align: center;
    margin-right: 0.5rem;
  }
  .section-row {
    display: flex;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 1rem;
    position: relative;
  }
  
  .cards-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    flex: 1;
    justify-content: center;
  }
  
  /* Específico para o meio (Finalístico) que é um grid */
  .grid-finalistico {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    width: 100%;
  }

  /* Cards (Blocos de Assunto) */
  .process-card {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 0.75rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.2s;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    min-height: 80px;
  }
  .process-card:hover {
    transform: translateY(-2px);
    border-color: #3b82f6;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
  }
  .card-title {
    font-size: 0.75rem;
    font-weight: 600;
    color: #e2e8f0;
    line-height: 1.2;
    margin-bottom: 0.5rem;
    z-index: 2;
  }
  
  /* Indicadores nos Cards (Simulando BI) */
  .card-kpi {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    z-index: 2;
  }
  .kpi-val { font-size: 1.1rem; font-weight: 800; color: #34d399; }
  .kpi-trend { font-size: 0.65rem; color: #9ca3af; }
  
  /* Cores por macro-processo */
  .gerencial .process-card { border-top: 3px solid #f59e0b; }
  .finalistico .process-card { border-top: 3px solid #3b82f6; }
  .suporte .process-card { border-top: 3px solid #8b5cf6; }

  /* Glow separators (Setas amarelas do diagrama original) */
  .glow-divider {
    height: 10px;
    background: linear-gradient(90deg, transparent 0%, rgba(245, 158, 11, 0.2) 20%, rgba(245, 158, 11, 0.5) 50%, rgba(245, 158, 11, 0.2) 80%, transparent 100%);
    clip-path: polygon(0 0, 100% 0, 98% 100%, 2% 100%);
  }
  .glow-divider.bottom {
    clip-path: polygon(2% 0, 98% 0, 100% 100%, 0 100%);
  }

  @media (max-width: 1200px) {
    .grid-finalistico { grid-template-columns: repeat(3, 1fr); }
  }
  @media (max-width: 900px) {
    .grid-finalistico { grid-template-columns: repeat(2, 1fr); }
    .side-arrow { display: none; }
  }
</style>

<div class="bi-container">
  
  <div class="bi-header">
    <div class="bi-title">
      <h1>BI • Cadeia de Valor Integrada</h1>
      <p>Observatório Governamental - Estado de Mato Grosso</p>
    </div>
    <div style="text-align:right;">
      <div style="font-size:0.75rem; color:#9ca3af;">Índice Geral de Eficiência</div>
      <div style="font-size:1.8rem; font-weight:800; color:#34d399;">87,4% ▲</div>
    </div>
  </div>

  <div class="value-chain">
    
    <!-- Seta Esquerda -->
    <div class="side-arrow">
      Demandas da Sociedade
    </div>

    <!-- Centro -->
    <div class="chain-center">
      
      <!-- GERENCIAL -->
      <div class="section-row gerencial">
        <div class="section-label">Gerencial</div>
        <div class="cards-container">
          <div class="process-card" style="flex:1;"><div class="card-title">Governança Estratégia Organizacional</div><div class="card-kpi"><span class="kpi-val">98%</span><span class="kpi-trend">Concluído</span></div></div>
          <div class="process-card" style="flex:1;"><div class="card-title">Gestão de Iniciativas Estratégicas</div><div class="card-kpi"><span class="kpi-val">124</span><span class="kpi-trend">Projetos Ativos</span></div></div>
          <div class="process-card" style="flex:1;"><div class="card-title">Gestão de Governança, Risco e Conformidade</div><div class="card-kpi"><span class="kpi-val" style="color:#f59e0b;">Baixo</span><span class="kpi-trend">Nível de Risco</span></div></div>
          <div class="process-card" style="flex:1;"><div class="card-title">Monitoramento e Avaliação de Resultados</div><div class="card-kpi"><span class="kpi-val">92%</span><span class="kpi-trend">Metas Atingidas</span></div></div>
          <div class="process-card" style="flex:1;"><div class="card-title">Relacionamento com Sociedade e Governo</div><div class="card-kpi"><span class="kpi-val">4.5/5</span><span class="kpi-trend">Satisfação</span></div></div>
        </div>
      </div>

      <div class="glow-divider"></div>

      <!-- FINALÍSTICO -->
      <div class="section-row finalistico">
        <div class="section-label">Finalístico</div>
        <div class="grid-finalistico">
          <!-- Coluna 1 -->
          <div class="process-card"><div class="card-title">Agricultura e Pecuária</div><div class="card-kpi"><span class="kpi-val">R$ 4B</span><span class="kpi-trend">Fomento</span></div></div>
          <div class="process-card"><div class="card-title">Assistência Social e Cidadania</div><div class="card-kpi"><span class="kpi-val">450K</span><span class="kpi-trend">Famílias</span></div></div>
          <div class="process-card"><div class="card-title">Ciência, Tecnologia e Inovação</div><div class="card-kpi"><span class="kpi-val">85</span><span class="kpi-trend">Editais</span></div></div>
          <div class="process-card"><div class="card-title">Desenvolvimento, Comércio e Indústria</div><div class="card-kpi"><span class="kpi-val">▲ 4%</span><span class="kpi-trend">PIB Est.</span></div></div>
          <div class="process-card"><div class="card-title">Ordenamento Territorial</div><div class="card-kpi"><span class="kpi-val">95%</span><span class="kpi-trend">Mapeado</span></div></div>
          
          <!-- Coluna 2 -->
          <div class="process-card"><div class="card-title">Cultura e Artes</div><div class="card-kpi"><span class="kpi-val">210</span><span class="kpi-trend">Eventos</span></div></div>
          <div class="process-card"><div class="card-title">Educação e Pesquisa</div><div class="card-kpi"><span class="kpi-val">452K</span><span class="kpi-trend">Alunos</span></div></div>
          <div class="process-card"><div class="card-title">Energia, Minerais, Combustíveis e Gás</div><div class="card-kpi"><span class="kpi-val">1.2GW</span><span class="kpi-trend">Renovável</span></div></div>
          <div class="process-card"><div class="card-title">Esporte e Lazer</div><div class="card-kpi"><span class="kpi-val">54</span><span class="kpi-trend">Complexos</span></div></div>
          <div class="process-card"><div class="card-title">Comunicação e Transparência</div><div class="card-kpi"><span class="kpi-val">100%</span><span class="kpi-trend">LAI Cump.</span></div></div>
          
          <!-- Coluna 3 -->
          <div class="process-card"><div class="card-title">Infraestrutura e Habitação</div><div class="card-kpi"><span class="kpi-val">15K</span><span class="kpi-trend">Moradias</span></div></div>
          <div class="process-card"><div class="card-title">Meio Ambiente e Clima</div><div class="card-kpi"><span class="kpi-val" style="color:#ef4444;">-12%</span><span class="kpi-trend">Desmatamento</span></div></div>
          <div class="process-card"><div class="card-title">Trabalho e Emprego</div><div class="card-kpi"><span class="kpi-val">18K</span><span class="kpi-trend">Vagas Ger.</span></div></div>
          <div class="process-card"><div class="card-title">Saneamento</div><div class="card-kpi"><span class="kpi-val">68%</span><span class="kpi-trend">Cobertura</span></div></div>
          <div class="process-card"><div class="card-title">Finanças e Tributação</div><div class="card-kpi"><span class="kpi-val">R$ 42M</span><span class="kpi-trend">Arrecadação</span></div></div>

          <!-- Coluna 4 -->
          <div class="process-card"><div class="card-title">Segurança Pública</div><div class="card-kpi"><span class="kpi-val">12K</span><span class="kpi-trend">Ocorrências</span></div></div>
          <div class="process-card"><div class="card-title">Transportes e Rodovias</div><div class="card-kpi"><span class="kpi-val">850km</span><span class="kpi-trend">Pavimentação</span></div></div>
          <div class="process-card"><div class="card-title">Turismo</div><div class="card-kpi"><span class="kpi-val">1.1M</span><span class="kpi-trend">Visitantes</span></div></div>
          <div class="process-card"><div class="card-title">Trânsito, Veículos e Habilitação</div><div class="card-kpi"><span class="kpi-val">340K</span><span class="kpi-trend">CNHs</span></div></div>
          <div class="process-card"><div class="card-title">Saúde e Vigilância Sanitária</div><div class="card-kpi"><span class="kpi-val">78%</span><span class="kpi-trend">Ocup. UTI</span></div></div>
        </div>
      </div>

      <div class="glow-divider bottom"></div>

      <!-- SUPORTE -->
      <div class="section-row suporte">
        <div class="section-label">Suporte</div>
        <div class="cards-container">
          <div class="process-card" style="flex:1;"><div class="card-title">Gestão de Desenvolv. de Pessoas</div></div>
          <div class="process-card" style="flex:1;"><div class="card-title">Gestão Orçamentária e Financeira</div></div>
          <div class="process-card" style="flex:1;"><div class="card-title">Gestão de Bens e Serviços</div></div>
          <div class="process-card" style="flex:1;"><div class="card-title">Gestão de Tecnologia de Informação</div></div>
          <div class="process-card" style="flex:1;"><div class="card-title">Gestão da Comunicação</div></div>
          <div class="process-card" style="flex:1;"><div class="card-title">Gestão de Consultoria Jurídica</div></div>
        </div>
      </div>
      
    </div>

    <!-- Seta Direita -->
    <div class="side-arrow side-arrow-right">
      Valor Entregue à Sociedade
    </div>

  </div>
</div>

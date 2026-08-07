---
hide:
  - navigation
  - toc
---

<style>.md-header { display: none !important; } .md-main__inner { margin-top: 0 !important; } .md-content { padding-top: 0 !important; } .md-grid { max-width: 100% !important; padding: 0 !important; margin: 0 !important; } .md-content__inner { margin: 0 !important; } .hero-section { padding-top: 70px; margin-top: 0; } .custom-top-nav { padding-left: 2rem !important; } .nav-brand { display: flex; align-items: center; gap: 2rem; min-width: max-content; } .nav-logo { background: linear-gradient(135deg, #0ea5e9, #10b981); color: white; width: 35px; height: 35px; min-width: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1rem; box-shadow: 0 0 10px rgba(16, 185, 129, 0.3); } .nav-titles { display: flex; flex-direction: column; white-space: nowrap; } .nav-main-title { font-weight: 800; font-size: 0.95rem; letter-spacing: 0.5px; line-height: 1.2; } .nav-sub-title { font-size: 0.65rem; color: #94a3b8; letter-spacing: 0.5px; } .nav-links { display: flex; gap: 1.5rem; white-space: nowrap; } .nav-links a { color: #cbd5e1 !important; text-decoration: none !important; font-size: 0.85rem; font-weight: 500; transition: color 0.2s; padding-bottom: 5px; border-bottom: 2px solid transparent; } .nav-links a:hover, .nav-links a.active { color: white !important; border-bottom: 2px solid #55b44d; } .nav-actions { display: flex; align-items: center; gap: 1rem; min-width: max-content; } .nav-badge { font-size: 0.75rem; color: #94a3b8; display: flex; align-items: center; gap: 0.4rem; border: 1px solid #1e3a8a; padding: 0.3rem 0.6rem; border-radius: 15px; white-space: nowrap; } .btn-portal { background: #90d836; color: #0f172a !important; text-decoration: none !important; padding: 0.5rem 1.2rem; border-radius: 6px; font-weight: 700; font-size: 0.85rem; transition: transform 0.2s; white-space: nowrap; } .btn-portal:hover { transform: translateY(-2px); } @media screen and (max-width: 900px) { .nav-links, .nav-badge { display: none; } }</style>



<div class="hero-section">
  <div class="hero-badge">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" style="margin-right: 8px;"><path d="M12 2l3 6 6 3-6 3-3 6-3-6-6-3 6-3z"></path></svg> Transparência e Gestão Pública de Excelência
  </div>
  <h1 class="hero-title">INDICADORES ESTRATÉGICOS PARA UM ESTADO BRILHANTE</h1>
  <p class="hero-subtitle">
    Monitoramento em tempo real de Saúde, Educação, Segurança e Infraestrutura.
    Decisões baseadas em dados com transparência e excelência.
  </p>
  
  <div class="hero-actions">
    <a href="paineis-indicadores/" class="btn btn-primary">Acessar Painel &rarr;</a>
    <a href="http://167.114.5.193:8000/assistente-ia/" class="btn btn-secondary">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" style="margin-right: 8px;"><path d="M12 2l3 6 6 3-6 3-3 6-3-6-6-3 6-3z"></path></svg>
      Assistente IA
    </a>
  </div>

  <div class="hero-stats">
    <div class="stat-item">
      <h4>+39</h4>
      <p>Mapeados</p>
    </div>
    <div class="stat-item">
      <h4>4</h4>
      <p>Áreas Monitoradas</p>
    </div>
    <div class="stat-item">
      <h4>8</h4>
      <p>Meses de Dados</p>
    </div>
  </div>
</div>

<script>
  const toggleBtn = document.getElementById('theme-toggle');
  
  function applyTheme(theme) {
    if (theme === 'dark') {
      document.body.classList.add('dark-theme');
      toggleBtn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg> Light';
    } else {
      document.body.classList.remove('dark-theme');
      toggleBtn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg> Dark';
    }
  }

  // Initial check
  if (localStorage.getItem('theme') === 'dark') {
    applyTheme('dark');
  }

  toggleBtn.addEventListener('click', () => {
    const isDark = document.body.classList.contains('dark-theme');
    const newTheme = isDark ? 'light' : 'dark';
    localStorage.setItem('theme', newTheme);
    applyTheme(newTheme);
  });
</script>


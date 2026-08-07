document.addEventListener("DOMContentLoaded", function() {
    const months = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ];
    
    const now = new Date();
    const currentMonth = months[now.getMonth()];
    const currentYear = now.getFullYear();
    const newDateStr = currentMonth + " " + currentYear;
    
    // Procura os subtítulos no cabeçalho do dashboard
    const subtitleElements = document.querySelectorAll('.dash-title-group p');
    
    subtitleElements.forEach(function(el) {
        if (el.textContent.includes('Agosto 2024')) {
            el.textContent = el.textContent.replace('Agosto 2024', newDateStr);
        }
    });

    // Mobile Sidebar Toggle
    if (window.innerWidth <= 768) {
        const pbiSidebar = document.querySelector('.pbi-sidebar');
        const customTopNavBrand = document.querySelector('.custom-top-nav .nav-brand');
        
        if (pbiSidebar && customTopNavBrand && !document.querySelector('.pbi-mobile-toggle')) {
            const toggleBtn = document.createElement('div');
            toggleBtn.className = 'pbi-mobile-toggle';
            toggleBtn.style.cssText = 'margin-left: 15px; cursor: pointer; display: flex; align-items: center; color: white; z-index: 1001;';
            toggleBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>';
            
            customTopNavBrand.parentNode.insertBefore(toggleBtn, customTopNavBrand);
            
            toggleBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                pbiSidebar.classList.toggle('open-mobile');
            });
            
            document.addEventListener('click', function(e) {
                if (pbiSidebar.classList.contains('open-mobile') && !pbiSidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
                    pbiSidebar.classList.remove('open-mobile');
                }
            });
        }
    }
});

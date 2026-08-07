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
});

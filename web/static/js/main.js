document.addEventListener('DOMContentLoaded', () => {
    // 1. Inicializar Gráficos Chart.js usando os dados injetados pelo Flask
    try {
        initCharts();
    } catch (e) {
        console.error("Erro ao inicializar gráficos:", e);
    }

    // 2. Inicializar o Mapa do Leaflet
    try {
        initMap();
    } catch (e) {
        console.error("Erro ao inicializar mapa:", e);
        const mapContainer = document.getElementById('map');
        if (mapContainer) {
            mapContainer.innerHTML = `<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: #9ca3af; font-family: Inter; font-size: 14px; text-align: center; padding: 20px; background: rgba(0,0,0,0.2);">
                <i class="fa-solid fa-circle-exclamation" style="font-size: 24px; color: #f59e0b; margin-bottom: 10px;"></i>
                <span>Não foi possível carregar os elementos interativos do mapa.<br>Isso ocorre quando a conexão com o servidor de mapas (CartoDB/OpenStreetMap) falha.<br><strong style="color: #10b981;">O restante da aplicação continua 100% funcional offline!</strong></span>
            </div>`;
        }
    }

    // 3. Event Listener para Classificação de Texto
    try {
        initClassifierForm();
    } catch (e) {
        console.error("Erro ao inicializar formulário de classificação:", e);
    }

    // 4. Gerenciamento do Status de Treinamento
    try {
        initTrainingMonitor();
    } catch (e) {
        console.error("Erro ao inicializar monitor de treinamento:", e);
    }

    // 5. Inicializar Tabela de Notícias e Automação
    try {
        initNewsTable();
    } catch (e) {
        console.error("Erro ao inicializar tabela de notícias:", e);
    }
});

// ==========================================
// 1. INICIALIZAÇÃO DE GRÁFICOS (CHART.JS)
// ==========================================
function initCharts() {
    const data = window.statsData || { top_movimentos: {}, top_estados: {}, top_pautas: {} };

    // --- Gráfico de Movimentos (Doughnut) ---
    const ctxMov = document.getElementById('chart-movimentos');
    if (ctxMov) {
        const movLabels = Object.keys(data.top_movimentos);
        const movValues = Object.values(data.top_movimentos);
        
        new Chart(ctxMov, {
            type: 'doughnut',
            data: {
                labels: movLabels,
                datasets: [{
                    data: movValues,
                    backgroundColor: [
                        'rgba(16, 185, 129, 0.7)',  // Emerald
                        'rgba(245, 158, 11, 0.7)',  // Gold
                        'rgba(59, 130, 246, 0.7)',   // Blue
                        'rgba(139, 92, 246, 0.7)',  // Purple
                        'rgba(239, 68, 68, 0.7)'     // Red
                    ],
                    borderColor: 'rgba(255, 255, 255, 0.5)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#334155', font: { family: 'Inter', size: 11 } }
                    }
                }
            }
        });
    }

    // --- Gráfico de Estados (Barra Vertical) ---
    const ctxEst = document.getElementById('chart-estados');
    if (ctxEst) {
        const estLabels = Object.keys(data.top_estados);
        const estValues = Object.values(data.top_estados);

        new Chart(ctxEst, {
            type: 'bar',
            data: {
                labels: estLabels,
                datasets: [{
                    label: 'Número de Incidentes',
                    data: estValues,
                    backgroundColor: 'rgba(245, 158, 11, 0.65)',
                    borderColor: 'rgba(245, 158, 11, 1)',
                    borderWidth: 1,
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
                    y: {
                        grid: { color: 'rgba(15, 23, 42, 0.06)' },
                        ticks: { color: '#475569', font: { family: 'Inter' } }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#475569', font: { family: 'Inter' } }
                    }
                }
            }
        });
    }

    // --- Gráfico de Pautas (Barra Horizontal) ---
    const ctxPau = document.getElementById('chart-pautas');
    if (ctxPau) {
        // Remover ponto e vírgula extra no final da pauta
        const pauLabels = Object.keys(data.top_pautas).map(label => label.replace(';', '').trim());
        const pauValues = Object.values(data.top_pautas);

        new Chart(ctxPau, {
            type: 'bar',
            data: {
                labels: pauLabels,
                datasets: [{
                    label: 'Conflitos por Tema',
                    data: pauValues,
                    backgroundColor: 'rgba(16, 185, 129, 0.65)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(15, 23, 42, 0.06)' },
                        ticks: { color: '#475569', font: { family: 'Inter' } }
                    },
                    y: {
                        grid: { display: false },
                        ticks: { color: '#475569', font: { family: 'Inter' } }
                    }
                }
            }
        });
    }
}

// ==========================================
// 2. INICIALIZAÇÃO E PLOTAGEM DE MAPA GIS
// ==========================================
let map;
function initMap() {
    // Centralizar no centro geográfico do Brasil
    map = L.map('map').setView([-14.235, -51.925], 4);
    
    // Adicionar camada de mapa Light elegante do CartoDB
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    // Carregar dados de conflitos da API e plotar marcadores com cores diferenciadas
    fetch('/api/map-data')
        .then(response => response.json())
        .then(markersData => {
            markersData.forEach(m => {
                // Definir cor baseada no movimento social principal envolvido
                let markerColor = '#f59e0b'; // Gold padrão
                if (m.movimento.toLowerCase().includes('lcp')) {
                    markerColor = '#ef4444'; // Vermelho para a LCP
                } else if (m.movimento.toLowerCase().includes('mst')) {
                    markerColor = '#059669'; // Esmeralda para o MST
                } else if (m.movimento.toLowerCase().includes('cpt')) {
                    markerColor = '#3b82f6'; // Azul para a CPT
                } else if (m.movimento.toLowerCase().includes('quilombola') || m.movimento.toLowerCase().includes('indigena')) {
                    markerColor = '#8b5cf6'; // Roxo para tradicionais
                }

                // Criar marcador vetorial circular premium
                const circleMarker = L.circleMarker([m.lat, m.lng], {
                    radius: 7,
                    fillColor: markerColor,
                    color: '#475569',
                    weight: 1,
                    opacity: 0.8,
                    fillOpacity: 0.85
                }).addTo(map);

                // Popup com estilização premium e metadados detalhados
                const popupContent = `
                    <div class="map-popup-premium">
                        <h4 style="margin: 0 0 5px 0; font-family: Outfit; font-weight: 600; color: #0f172a;">
                            <i class="fa-solid fa-location-dot"></i> ${m.municipio} - ${m.estado}
                        </h4>
                        <div style="font-size: 11px; color: #475569; margin-bottom: 6px; border-bottom: 1px solid rgba(15,23,42,0.1); padding-bottom: 4px;">
                            <strong>Ação Derivada:</strong> <span style="color: #059669; font-weight: 600;">${m.acao_derivada}</span>
                        </div>
                        <div style="font-size: 11px; color: #1e293b;">
                            <p style="margin: 2px 0;"><strong>Movimento:</strong> ${m.movimento}</p>
                            <p style="margin: 2px 0;"><strong>Pauta:</strong> ${m.pauta.replace(';', '')}</p>
                        </div>
                    </div>
                `;

                circleMarker.bindPopup(popupContent);
            });
        })
        .catch(err => console.error("Erro ao carregar dados dos marcadores do mapa:", err));
}

// ==========================================
// 3. LOGICA DO FORMULARIO CLASSIFICADOR
// ==========================================
function initClassifierForm() {
    const form = document.getElementById('classify-form');
    const placeholder = document.querySelector('.placeholder-results');
    const loader = document.getElementById('loader');
    const resultsContent = document.getElementById('results-content');
    
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const newsText = document.getElementById('news-text').value;
        const estado = document.getElementById('meta-estado').value;
        const pauta = document.getElementById('meta-pauta').value;
        const movimento = document.getElementById('meta-movimento').value;

        // Mostrar Loader
        placeholder.classList.add('hidden');
        resultsContent.classList.add('hidden');
        loader.classList.remove('hidden');

        // Fazer requisição assíncrona ao servidor Flask
        fetch('/api/classify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: newsText,
                estado: estado,
                pauta: pauta,
                movimento: movimento
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error || "Erro na classificação"); });
            }
            return response.json();
        })
        .then(data => {
            loader.classList.add('hidden');
            resultsContent.classList.remove('hidden');

            // Renderizar resultados principais
            const res = data.classificacao_geral;
            
            document.getElementById('res-derivada').innerText = res.acao_derivada || "SEM CLASSIFICAÇÃO";
            document.getElementById('res-derivada-conf').innerText = `${(res.confianca_derivada * 100).toFixed(1)}%`;
            document.getElementById('res-derivada-conf-bar').style.width = `${res.confianca_derivada * 100}%`;

            document.getElementById('res-matriz').innerText = res.acao_matriz || "SEM CATEGORIA";
            document.getElementById('res-matriz-conf').innerText = `${(res.confianca_matriz * 100).toFixed(1)}%`;
            document.getElementById('res-matriz-conf-bar').style.width = `${res.confianca_matriz * 100}%`;

            // Detalhamento de Chunks
            const chunksList = document.getElementById('chunks-list');
            chunksList.innerHTML = ''; // Limpar anterior

            data.chunks.forEach((chunk, idx) => {
                const chunkItem = document.createElement('div');
                chunkItem.className = 'chunk-item';
                chunkItem.innerHTML = `
                    <p style="color: var(--text-secondary); margin-bottom: 4px;">"${chunk.texto.substring(0, 180)}..."</p>
                    <div class="chunk-meta">
                        <span><strong>Chunk #${idx + 1}</strong></span>
                        <span>Previsão: <strong style="color: #10b981;">${chunk.acao_derivada}</strong> (${(chunk.confianca_derivada * 100).toFixed(1)}%)</span>
                    </div>
                `;
                chunksList.appendChild(chunkItem);
            });
        })
        .catch(err => {
            loader.classList.add('hidden');
            placeholder.classList.remove('hidden');
            alert(`Erro ao classificar a notícia: ${err.message}`);
        });
    });
}

// ==========================================
// 4. MONITORAMENTO E DISPARO DE TREINAMENTO
// ==========================================
let statusPollInterval;
function initTrainingMonitor() {
    const btnTrain = document.getElementById('btn-train');
    const badge = document.getElementById('train-status-badge');
    
    if (!btnTrain) return;

    // Checar status inicial
    checkTrainingStatus();

    btnTrain.addEventListener('click', () => {
        if (btnTrain.disabled) return;

        if (confirm("Deseja mesmo disparar a ingestão dos dados, chunking semântico, extração de PDFs e retreinamento do classificador? Esta operação roda em background.")) {
            btnTrain.disabled = true;
            updateStatusBadge("Training");

            fetch('/api/train', { method: 'POST' })
                .then(res => res.json())
                .then(data => {
                    alert(data.message);
                    // Começar polling de status
                    startStatusPolling();
                })
                .catch(err => {
                    btnTrain.disabled = false;
                    updateStatusBadge("Error: " + err.message);
                });
        }
    });
}

function checkTrainingStatus() {
    fetch('/api/train/status')
        .then(res => res.json())
        .then(data => {
            updateStatusBadge(data.status);
            if (data.status === "Training") {
                document.getElementById('btn-train').disabled = true;
                startStatusPolling();
            }
        });
}

function startStatusPolling() {
    if (statusPollInterval) clearInterval(statusPollInterval);
    
    statusPollInterval = setInterval(() => {
        fetch('/api/train/status')
            .then(res => res.json())
            .then(data => {
                updateStatusBadge(data.status);
                if (data.status !== "Training") {
                    clearInterval(statusPollInterval);
                    document.getElementById('btn-train').disabled = false;
                    // Recarregar a página se terminou com sucesso para atualizar as estatísticas
                    if (data.status.startsWith("Success")) {
                        setTimeout(() => {
                            alert("Treinamento finalizado com sucesso! Atualizando dashboard.");
                            window.location.reload();
                        }, 500);
                    }
                }
            });
    }, 4000);
}

function updateStatusBadge(status) {
    const badge = document.getElementById('train-status-badge');
    if (!badge) return;

    badge.className = 'badge';

    if (status === "Idle" || status === "Ocioso") {
        badge.classList.add('bg-idle');
        badge.innerText = "Status: Ocioso";
    } else if (status === "Training") {
        badge.classList.add('bg-training');
        badge.innerText = "Status: Treinando...";
    } else if (status.startsWith("Success")) {
        badge.classList.add('bg-success');
        const parts = status.split('|');
        const accD = parts[1] ? parts[1].split(':')[1] : '';
        badge.innerText = `Status: Sucesso! ${accD ? 'F1-Derivada: ' + accD : ''}`;
    } else if (status.startsWith("Error")) {
        badge.classList.add('bg-error');
        badge.innerText = "Status: Erro!";
    }
}

// ==========================================
// 5. TABELA DE NOTÍCIAS E AUTOMAÇÃO
// ==========================================
let allNewsData = [];

function initNewsTable() {
    const tableBody = document.getElementById('news-table-body');
    const searchInput = document.getElementById('search-news');
    
    if (!tableBody) return;

    // Fetch news list from API
    fetch('/api/news-list')
        .then(res => res.json())
        .then(data => {
            allNewsData = data;
            renderNewsTable(data);
            
            // Setup Search filter
            if (searchInput) {
                searchInput.addEventListener('input', (e) => {
                    const query = e.target.value.toLowerCase().trim();
                    const filtered = allNewsData.filter(news => {
                        return news.codigo_noticia.toLowerCase().includes(query) ||
                               news.titulo_noticia.toLowerCase().includes(query) ||
                               news.estado.toLowerCase().includes(query) ||
                               news.nome_movimento.toLowerCase().includes(query) ||
                               news.pauta_acao.toLowerCase().includes(query);
                    });
                    renderNewsTable(filtered);
                });
            }
        })
        .catch(err => {
            console.error("Erro ao carregar banco de notícias:", err);
            tableBody.innerHTML = `
                <tr>
                    <td colspan="7" class="table-placeholder" style="color: #ef4444;">
                        <i class="fa-solid fa-circle-exclamation" style="margin-right: 0.5rem;"></i>
                        Erro ao carregar banco de notícias. Verifique a conexão com o backend.
                    </td>
                </tr>
            `;
        });
}

function renderNewsTable(newsItems) {
    const tableBody = document.getElementById('news-table-body');
    const showingCount = document.getElementById('table-showing-count');
    const totalCount = document.getElementById('table-total-count');
    
    if (!tableBody) return;

    tableBody.innerHTML = '';
    
    if (showingCount) showingCount.innerText = newsItems.length;
    if (totalCount) totalCount.innerText = allNewsData.length;

    if (newsItems.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="table-placeholder">
                    Nenhuma notícia encontrada correspondente aos critérios de busca.
                </td>
            </tr>
        `;
        return;
    }

    newsItems.forEach((news, idx) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="font-weight: 600; color: #6b7280; text-align: center;">${idx + 1}</td>
            <td style="font-weight: 600;">
                <a href="/pdf/${news.codigo_noticia}" target="_blank" class="pdf-link" title="Abrir PDF original da notícia">
                    <i class="fa-regular fa-file-pdf"></i> ${news.codigo_noticia}
                </a>
            </td>
            <td style="font-weight: 500; color: var(--text-primary);">${news.titulo_noticia}</td>
            <td>${news.estado !== 'N.I' ? news.estado : '<span style="color: #6b7280;">N.I</span>'}</td>
            <td>${news.nome_movimento !== 'N.I' ? news.nome_movimento.replace('Nome do movimento', '').trim() : '<span style="color: #6b7280;">N.I</span>'}</td>
            <td>${news.pauta_acao !== 'N.I' ? news.pauta_acao.replace(';', '').trim() : '<span style="color: #6b7280;">N.I</span>'}</td>
            <td style="text-align: center;">
                <button class="btn-table-action" onclick="autoClassifyNews('${news.codigo_noticia}', this)">
                    <i class="fa-solid fa-bolt"></i> Classificar
                </button>
            </td>
        `;
        tableBody.appendChild(tr);
    });
}

function autoClassifyNews(newsCode, buttonElement) {
    // Show spinner in button
    const originalContent = buttonElement.innerHTML;
    buttonElement.disabled = true;
    buttonElement.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Lendo...`;

    // Fetch full news details
    fetch(`/api/news/${newsCode}`)
        .then(res => {
            if (!res.ok) throw new Error("Erro ao buscar texto completo da notícia.");
            return res.json();
        })
        .then(data => {
            // Restore button
            buttonElement.disabled = false;
            buttonElement.innerHTML = originalContent;

            // Scroll down to classifier
            const classifierSection = document.getElementById('classify-form');
            if (classifierSection) {
                classifierSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }

            // Fill text area
            const textarea = document.getElementById('news-text');
            if (textarea) {
                textarea.value = data.texto_noticia || `${data.titulo_noticia}. Pauta: ${data.pauta_acao}.`;
            }

            // Automate dropdowns
            selectDropdownValue('meta-estado', data.estado);
            selectDropdownValue('meta-pauta', data.pauta_acao);
            selectDropdownValue('meta-movimento', data.nome_movimento);

            // Disparar o form submit
            const form = document.getElementById('classify-form');
            if (form) {
                // Dispatch event submit to run JS event listener
                form.dispatchEvent(new Event('submit', { cancelable: true }));
            }
        })
        .catch(err => {
            buttonElement.disabled = false;
            buttonElement.innerHTML = originalContent;
            alert("Erro ao recuperar os detalhes da notícia: " + err.message);
        });
}

function selectDropdownValue(elementId, value) {
    const select = document.getElementById(elementId);
    if (!select) return;
    
    if (!value || value === 'N.I') {
        select.value = 'N.I';
        return;
    }

    const valLower = value.toLowerCase().trim();
    let matchedValue = 'N.I'; // Fallback
    
    for (let i = 0; i < select.options.length; i++) {
        const optVal = select.options[i].value;
        const optText = select.options[i].text.toLowerCase().trim();
        
        // Exact matches
        if (optVal.toLowerCase().trim() === valLower || optText === valLower) {
            matchedValue = optVal;
            break;
        }
        
        // Substring matches
        if (optVal !== 'N.I') {
            const cleanOptVal = optVal.replace(/[;()]/g, '').toLowerCase().trim();
            const cleanVal = valLower.replace(/[;()]/g, '').trim();
            
            if (cleanVal.includes(cleanOptVal) || cleanOptVal.includes(cleanVal)) {
                matchedValue = optVal;
            }
        }
    }
    select.value = matchedValue;
}

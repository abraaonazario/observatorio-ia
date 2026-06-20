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

    // 6. Inicializar Grafo de Conhecimento
    try {
        initKnowledgeGraph();
    } catch (e) {
        console.error("Erro ao inicializar Grafo de Conhecimento:", e);
    }

    // 7. Inicializar Tabela de PDFs Brutos
    try {
        initRawPdfsTable();
    } catch (e) {
        console.error("Erro ao inicializar tabela de PDFs brutos:", e);
    }
});

// ==========================================
// 0. HELPER PARA CATEGORIA ATUAL E TEMAS
// ==========================================
function getCurrentCategory() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('category') || 'agrario';
}

function handleThemeChange(checkbox) {
    if (checkbox.checked) {
        // Uncheck all others
        const checkboxes = document.querySelectorAll('input[name="tema"]');
        checkboxes.forEach(cb => {
            if (cb !== checkbox) cb.checked = false;
        });
        
        // Redirect to new category
        window.location.href = '/?category=' + checkbox.value;
    } else {
        // Prevent unchecking the only checked box to ensure one is always selected
        checkbox.checked = true;
    }
}

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
window.allMapMarkers = [];
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
    const cat = getCurrentCategory();
    fetch(`/api/map-data?category=${cat}`)
        .then(response => response.json())
        .then(markersData => {
            window.allMapMarkers = []; // reset markers
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
                
                // Store marker for filtering
                window.allMapMarkers.push({ marker: circleMarker, data: m });
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
    
    // Configurar o upload de PDF
    const pdfInput = document.getElementById('pdf-upload-input');
    const pdfNameSpan = document.getElementById('pdf-upload-name');
    const pdfSpinner = document.getElementById('pdf-upload-spinner');
    
    if (pdfInput) {
        pdfInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (!file) {
                pdfNameSpan.innerText = 'Nenhum arquivo selecionado';
                return;
            }
            
            pdfNameSpan.innerText = file.name;
            pdfSpinner.classList.remove('hidden');
            
            const formData = new FormData();
            formData.append('file', file);
            
            fetch('/api/extract-pdf-text', {
                method: 'POST',
                body: formData
            })
            .then(res => {
                if (!res.ok) {
                    return res.json().then(err => { throw new Error(err.error || "Erro ao ler o PDF"); });
                }
                return res.json();
            })
            .then(data => {
                pdfSpinner.classList.add('hidden');
                
                // Preencher a textarea com o texto do PDF
                const textarea = document.getElementById('news-text');
                if (textarea) {
                    textarea.value = data.text;
                    
                    // Disparar a submissão do formulário para classificar
                    if (form) {
                        form.dispatchEvent(new Event('submit', { cancelable: true }));
                        // Limpar o input para permitir enviar o mesmo arquivo novamente se quiser
                        pdfInput.value = '';
                    }
                }
            })
            .catch(err => {
                pdfSpinner.classList.add('hidden');
                alert(`Erro ao processar PDF: ${err.message}`);
                pdfInput.value = '';
            });
        });
    }

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
        const cat = getCurrentCategory();
        fetch('/api/classify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                category: cat,
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

            const cat = getCurrentCategory();
            fetch('/api/train', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ category: cat })
            })
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
                if (!data.status.startsWith("Training")) {
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
    } else if (status.startsWith("Training")) {
        badge.classList.add('bg-training');
        const parts = status.split('|');
        const progressInfo = parts[1] || "Treinando...";
        badge.innerText = `Status: ${progressInfo}`;
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

function getMonthNumber(mesPasta) {
    if (!mesPasta || mesPasta === 'N.I') return 99;
    const match = mesPasta.match(/^(\d+)/);
    return match ? parseInt(match[1], 10) : 99;
}

function initNewsTable() {
    const tableBody = document.getElementById('news-table-body');
    const searchInput = document.getElementById('search-news');
    const filterMonth = document.getElementById('filter-month');
    
    if (!tableBody) return;

    // Fetch news list from API
    const cat = getCurrentCategory();
    fetch(`/api/news-list?category=${cat}`)
        .then(res => res.json())
        .then(data => {
            // Sort chronologically by month
            data.sort((a, b) => getMonthNumber(a.mes_pasta) - getMonthNumber(b.mes_pasta));
            
            allNewsData = data;
            renderNewsTable(data);
            
            // Setup Search & Month filter
            const applyFilters = () => {
                const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
                const selectedMonth = filterMonth ? filterMonth.value : 'ALL';
                
                const filtered = allNewsData.filter(news => {
                    const matchesSearch = !query || 
                           news.codigo_noticia.toLowerCase().includes(query) ||
                           news.titulo_noticia.toLowerCase().includes(query) ||
                           news.estado.toLowerCase().includes(query) ||
                           news.nome_movimento.toLowerCase().includes(query) ||
                           news.pauta_acao.toLowerCase().includes(query);
                    
                    const matchesMonth = selectedMonth === 'ALL' || news.mes_pasta === selectedMonth;
                    
                    return matchesSearch && matchesMonth;
                });
                
                // Update Top Stats Cards
                const cardConflitos = document.querySelector('#card-total-conflitos .stat-number');
                const cardNoticias = document.querySelector('#card-total-noticias .stat-number');
                
                if (cardConflitos) {
                    cardConflitos.innerText = filtered.reduce((acc, n) => acc + (parseInt(n.qtd_chunks) || 0), 0);
                }
                if (cardNoticias) {
                    cardNoticias.innerText = filtered.length;
                }
                
                // Update Map Markers
                if (window.allMapMarkers && map) {
                    window.allMapMarkers.forEach(item => {
                        const matchesMonth = selectedMonth === 'ALL' || item.data.mes_pasta === selectedMonth;
                        // Search query in map can be added later if needed, for now just month
                        if (matchesMonth) {
                            if (!map.hasLayer(item.marker)) {
                                item.marker.addTo(map);
                            }
                        } else {
                            if (map.hasLayer(item.marker)) {
                                item.marker.remove();
                            }
                        }
                    });
                }
                
                renderNewsTable(filtered);
            };

            if (searchInput) searchInput.addEventListener('input', applyFilters);
            if (filterMonth) filterMonth.addEventListener('change', applyFilters);
        })
        .catch(err => {
            console.error("Erro ao carregar banco de notícias:", err);
            tableBody.innerHTML = `
                <tr>
                    <td colspan="8" class="table-placeholder" style="color: #ef4444;">
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
                <td colspan="8" class="table-placeholder">
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
            <td style="font-weight: 500; color: var(--text-secondary);">${news.mes_pasta !== 'N.I' ? news.mes_pasta : '<span style="color: #6b7280;">N.I</span>'}</td>
            <td style="text-align: center; font-weight: 700; color: #059669;">${news.qtd_chunks || 0}</td>
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
    const cat = getCurrentCategory();
    fetch(`/api/news/${newsCode}?category=${cat}`)
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

// ==========================================
// 6. GRAFO DE CONHECIMENTO INTERATIVO
// ==========================================
function initKnowledgeGraph() {
    const container = document.getElementById('knowledge-graph');
    const loader = document.getElementById('graph-loader');
    const detailsEl = document.getElementById('graph-node-details');
    const nameEl = document.getElementById('graph-node-name');
    const typeEl = document.getElementById('graph-node-type');
    const freqEl = document.getElementById('graph-node-freq');
    const searchInput = document.getElementById('search-news');
    
    if (!container) return;

    const cat = getCurrentCategory();
    fetch(`/api/knowledge-graph?category=${cat}`)
        .then(response => {
            if (!response.ok) throw new Error("Erro ao carregar dados do grafo.");
            return response.json();
        })
        .then(data => {
            if (loader) loader.classList.add('hidden');

            if (!data.nodes || data.nodes.length === 0) {
                container.innerHTML = `<div style="display: flex; align-items: center; justify-content: center; height: 100%; color: var(--text-muted);">Grafo vazio. Adicione mais dados para gerar conexões.</div>`;
                return;
            }

            // Utilizar arrays puros ao invés de vis.DataSet para máxima compatibilidade offline
            const nodesArray = data.nodes;
            const edgesArray = data.edges;

            const graphData = { nodes: nodesArray, edges: edgesArray };
            
            console.log(`[Vis.js] Inicializando Grafo com ${nodesArray.length} nós e ${edgesArray.length} arestas.`);

            // Opções de configuração MINIMALISTAS para evitar bugs visuais ou falhas de renderização
            const options = {
                autoResize: false, // <-- ISTO DESLIGA O RESIZEOBSERVER QUE ESTAVA TRAVANDO A TELA EM LOOP!
                nodes: { shape: 'dot' },
                physics: { enabled: true, stabilization: false },
                groups: {
                    movimento: { color: { background: '#3b82f6' } },
                    estado: { color: { background: '#10b981' } },
                    pauta: { color: { background: '#f59e0b' } },
                    acao: { color: { background: '#ef4444' } }
                }
            };

            // Criar rede interativa
            const network = new vis.Network(container, graphData, options);

            // Ouvinte de clique em nó para exibir detalhes e aplicar filtro dinâmico
            network.on("selectNode", function (params) {
                if (params.nodes.length > 0) {
                    const selectedId = params.nodes[0];
                    const node = nodesArray.find(n => n.id === selectedId);
                    
                    if (node) {
                        // Atualizar painel de detalhes
                        if (nameEl) nameEl.innerText = node.label;
                        if (typeEl) {
                            let grp = node.group;
                            if (grp === 'movimento') grp = 'Movimento Social';
                            else if (grp === 'estado') grp = 'Território (Estado)';
                            else if (grp === 'pauta') grp = 'Demanda (Pauta)';
                            else if (grp === 'acao') grp = 'Ação de Conflito';
                            typeEl.innerText = grp;
                        }
                        if (freqEl) freqEl.innerText = `${node.value} coocorrências no dataset`;
                        
                        if (detailsEl) detailsEl.classList.remove('hidden');

                        // Aplicar filtro na tabela de notícias
                        if (searchInput) {
                            searchInput.value = node.label;
                            searchInput.dispatchEvent(new Event('input'));
                        }
                    }
                }
            });

            // Deseleção do nó: ocultar painel de detalhes e limpar filtro
            network.on("deselectNode", function (params) {
                if (detailsEl) detailsEl.classList.add('hidden');
                
                if (searchInput) {
                    searchInput.value = '';
                    searchInput.dispatchEvent(new Event('input'));
                }
            });
            
            // Ao terminar estabilização, desativar física para evitar consumo de CPU e estabilizar a visualização
            network.on("stabilizationIterationsDone", function () {
                network.setOptions({ physics: { enabled: false } });
            });
        })
        .catch(err => {
            console.error("Erro ao inicializar o Grafo de Conhecimento:", err);
            if (loader) loader.classList.add('hidden');
            container.innerHTML = `
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: #ef4444; font-size: 14px; text-align: center; padding: 20px;">
                    <i class="fa-solid fa-triangle-exclamation" style="font-size: 24px; margin-bottom: 10px;"></i>
                    <span>Erro ao carregar o Grafo de Conhecimento.<br>Verifique se os dados do pipeline estão prontos.</span>
                </div>
            `;
        });
}

// ==========================================
// 7. REPOSITÓRIO DE PDFs BRUTOS
// ==========================================
let allRawPdfs = [];

function initRawPdfsTable() {
    const tableBody = document.getElementById('raw-pdfs-table-body');
    const searchInput = document.getElementById('search-raw-pdfs');
    const totalCount = document.getElementById('raw-pdfs-total-count');
    
    if (!tableBody) return;

    const cat = getCurrentCategory();
    fetch(`/api/raw-pdfs?category=${cat}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) throw new Error(data.error);
            allRawPdfs = data;
            if (totalCount) totalCount.innerText = allRawPdfs.length;
            renderRawPdfsTable(allRawPdfs);

            if (searchInput) {
                searchInput.addEventListener('input', () => {
                    const query = searchInput.value.toLowerCase().trim();
                    const filtered = allRawPdfs.filter(pdf => 
                        pdf.filename.toLowerCase().includes(query)
                    );
                    renderRawPdfsTable(filtered);
                });
            }
        })
        .catch(err => {
            console.error("Erro ao carregar lista de PDFs brutos:", err);
            tableBody.innerHTML = `
                <tr>
                    <td colspan="4" class="table-placeholder" style="color: #ef4444;">
                        <i class="fa-solid fa-circle-exclamation" style="margin-right: 0.5rem;"></i>
                        Erro ao carregar lista de PDFs brutos. Verifique se o arquivo ZIP está disponível.
                    </td>
                </tr>
            `;
        });
}

function renderRawPdfsTable(pdfList) {
    const tableBody = document.getElementById('raw-pdfs-table-body');
    if (!tableBody) return;

    tableBody.innerHTML = '';

    if (pdfList.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="4" class="table-placeholder">
                    Nenhum PDF encontrado correspondente à busca.
                </td>
            </tr>
        `;
        return;
    }

    pdfList.forEach((pdf, idx) => {
        const tr = document.createElement('tr');
        // Usar encodeURIComponent ou escape simplificado para prevenir quebra de strings JS
        const safeFilepath = pdf.filepath.replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '\\"');
        tr.innerHTML = `
            <td style="font-weight: 600; color: #6b7280; text-align: center;">${idx + 1}</td>
            <td style="font-weight: 500; color: var(--text-primary);">
                <i class="fa-regular fa-file-pdf" style="color: #ef4444; margin-right: 0.5rem;"></i>
                <a href="/api/download-pdf?filepath=${encodeURIComponent(pdf.filepath)}&category=${getCurrentCategory()}" download style="color: var(--primary-color); text-decoration: none; cursor: pointer;">
                    ${pdf.filename}
                </a>
            </td>
            <td style="text-align: center; font-weight: 700; color: #059669;">${pdf.qtd_chunks || 0}</td>
            <td style="color: var(--text-secondary); font-size: 0.9em;">${pdf.justificativa || ''}</td>
            <td style="text-align: center; color: var(--text-primary); font-weight: 500;">${pdf.qtd_paginas !== undefined ? pdf.qtd_paginas : '?'}</td>
            <td style="text-align: center; color: var(--text-secondary);">${pdf.size}</td>
            <td style="text-align: center;">
                <button class="btn-table-action" onclick="processRawPdf('${safeFilepath}', \`${pdf.justificativa || ''}\`, this)" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">
                    <i class="fa-solid fa-microchip"></i> Processar IA
                </button>
            </td>
        `;
        tableBody.appendChild(tr);
    });
}

function processRawPdf(filepath, justificativa, buttonElement) {
    const originalContent = buttonElement.innerHTML;
    buttonElement.disabled = true;
    buttonElement.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Extraindo...`;

    fetch('/api/extract-pdf-from-zip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filepath: filepath })
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => { throw new Error(err.error || "Erro ao extrair PDF do ZIP."); });
        }
        return res.json();
    })
    .then(data => {
        buttonElement.disabled = false;
        buttonElement.innerHTML = originalContent;

        // Mostrar a justificativa
        const justContainer = document.getElementById('justificativa-container');
        const justText = document.getElementById('justificativa-text');
        if (justContainer && justText) {
            if (justificativa) {
                justText.innerText = justificativa;
                justContainer.style.display = 'block';
            } else {
                justContainer.style.display = 'none';
            }
        }
        buttonElement.innerHTML = originalContent;

        // Scroll down to classifier
        const classifierSection = document.getElementById('classify-form');
        if (classifierSection) {
            classifierSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        // Fill text area
        const textarea = document.getElementById('news-text');
        if (textarea) {
            textarea.value = data.text;
        }

        // Disparar o form submit
        const form = document.getElementById('classify-form');
        if (form) {
            form.dispatchEvent(new Event('submit', { cancelable: true }));
        }
    })
    .catch(err => {
        buttonElement.disabled = false;
        buttonElement.innerHTML = originalContent;
        alert("Erro ao extrair e processar o PDF: " + err.message);
    });
}

// ==========================================
// Chatbot Agent Logic (RAG Extrativo)
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    const chatbotBtn = document.querySelector('.bd-chatbot-btn');
    const chatbotSidebar = document.getElementById('chatbot-sidebar');
    const closeBtn = document.getElementById('chatbot-close-btn');
    const sendBtn = document.getElementById('chatbot-send-btn');
    const inputField = document.getElementById('chatbot-input');
    const messagesContainer = document.getElementById('chatbot-messages');

    if (!chatbotBtn || !chatbotSidebar) return;

    // Toggle Sidebar
    chatbotBtn.addEventListener('click', () => {
        chatbotSidebar.classList.add('active');
        inputField.focus();
    });

    closeBtn.addEventListener('click', () => {
        chatbotSidebar.classList.remove('active');
    });

    // Send Message
    const sendMessage = async () => {
        const query = inputField.value.trim();
        if (!query) return;

        // Add user message to UI
        const userMsg = document.createElement('div');
        userMsg.className = 'message user-message';
        userMsg.innerHTML = `<div class="message-content">${query.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</div>`;
        messagesContainer.appendChild(userMsg);
        
        // Clear input and scroll
        inputField.value = '';
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Add loading indicator
        const aiMsg = document.createElement('div');
        aiMsg.className = 'message ai-message loading-msg';
        aiMsg.innerHTML = `
            <div class="message-content">
                <div class="loader-dots"><span></span><span></span><span></span></div>
            </div>
        `;
        messagesContainer.appendChild(aiMsg);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        try {
            const urlParams = new URLSearchParams(window.location.search);
            const category = urlParams.get('category') || 'agrario';

            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query, category: category })
            });

            const data = await response.json();
            
            // Remove loading
            messagesContainer.removeChild(aiMsg);

            // Add real response
            const responseMsg = document.createElement('div');
            responseMsg.className = 'message ai-message';
            if (response.ok) {
                responseMsg.innerHTML = `<div class="message-content">${data.answer}</div>`;
            } else {
                responseMsg.innerHTML = `<div class="message-content" style="color: #ef4444;"><i class="fa-solid fa-triangle-exclamation"></i> ${data.error || "Erro ao consultar a base."}</div>`;
            }
            messagesContainer.appendChild(responseMsg);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;

        } catch (error) {
            messagesContainer.removeChild(aiMsg);
            const errorMsg = document.createElement('div');
            errorMsg.className = 'message ai-message';
            errorMsg.innerHTML = `<div class="message-content" style="color: #ef4444;"><i class="fa-solid fa-plug-circle-xmark"></i> Falha de conexão com o Agente de IA.</div>`;
            messagesContainer.appendChild(errorMsg);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    };

    sendBtn.addEventListener('click', sendMessage);
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});

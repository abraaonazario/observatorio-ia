import os
import sys
import pickle
import numpy as np
import pandas as pd
import torch
from flask import Flask, render_template, jsonify, request, send_file
import logging
from threading import Thread
import time
import io
import zipfile
import pdfplumber

# Adicionar raiz do projeto ao path para garantir que os módulos sejam encontrados
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
# Importações dos nossos módulos
from preprocessing.text_preprocessor import SemanticChunker
from embeddings.embedding_generator import EmbeddingManager
from training.classifier_trainer import ModelTrainer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, template_folder='templates', static_folder='static')

# Coordenadas geográficas das capitais dos estados brasileiros para geocodificação offline resiliente
ESTADO_COORDS = {
    'AC': (-9.9749, -67.8076), 'AL': (-9.6658, -35.7350), 'AM': (-3.1190, -60.0217),
    'AP': (0.0389, -51.0664), 'BA': (-12.9714, -38.5014), 'CE': (-3.7172, -38.5434),
    'DF': (-15.7801, -47.9292), 'ES': (-20.3155, -40.3128), 'GO': (-16.6869, -49.2648),
    'MA': (-2.5307, -44.3068), 'MG': (-19.9173, -43.9345), 'MS': (-20.4435, -54.6478),
    'MT': (-15.6010, -56.0974), 'PA': (-1.4558, -48.4902), 'PB': (-7.1153, -34.8610),
    'PE': (-8.0543, -34.8813), 'PI': (-5.0920, -42.8038), 'PR': (-25.4290, -49.2671),
    'RJ': (-22.9068, -43.1729), 'RN': (-5.7950, -35.2094), 'RO': (-8.7612, -63.9039),
    'RR': (2.8197, -60.6733), 'RS': (-30.0346, -51.2177), 'SC': (-27.5954, -48.5480),
    'SE': (-10.9111, -37.0717), 'SP': (-23.5505, -46.6333), 'TO': (-10.1844, -48.3336),
    'Acre': (-9.9749, -67.8076), 'Alagoas': (-9.6658, -35.7350), 'Amazonas': (-3.1190, -60.0217),
    'Amapá': (0.0389, -51.0664), 'Bahia': (-12.9714, -38.5014), 'Ceará': (-3.7172, -38.5434),
    'Distrito Federal': (-15.7801, -47.9292), 'Espírito Santo': (-20.3155, -40.3128), 'Goiás': (-16.6869, -49.2648),
    'Maranhão': (-2.5307, -44.3068), 'Minas Gerais': (-19.9173, -43.9345), 'Mato Grosso do Sul': (-20.4435, -54.6478),
    'Mato Grosso': (-15.6010, -56.0974), 'Pará': (-1.4558, -48.4902), 'Paraíba': (-7.1153, -34.8610),
    'Pernambuco': (-8.0543, -34.8813), 'Piauí': (-5.0920, -42.8038), 'Paraná': (-25.4290, -49.2671),
    'Rio de Janeiro': (-22.9068, -43.1729), 'Rio Grande do Norte': (-5.7950, -35.2094), 'Rondônia': (-8.7612, -63.9039),
    'Roraima': (2.8197, -60.6733), 'Rio Grande do Sul': (-30.0346, -51.2177), 'Santa Catarina': (-27.5954, -48.5480),
    'Sergipe': (-10.9111, -37.0717), 'São Paulo': (-23.5505, -46.6333), 'Tocantins': (-10.1844, -48.3336)
}

# Dicionário global para armazenar os recursos de cada categoria
CATEGORIAS = ['agrario', 'urbano', 'aguas', 'floresta']
MODELS = {cat: {
    'DATASET': None,
    'NN_MODEL': None,
    'NN_ENCODERS': None,
    'EMB_MANAGER': None,
    'CHUNKER': None,
    'MICRO_TO_MACRO_MAP': {},
    'MACRO_TO_MICROS_MAP': {}
} for cat in CATEGORIAS}

TRAINING_STATUS = "Idle"  # Idle, Training, Success, Error

def build_hierarchical_maps(category):
    """Dynamically builds hierarchical maps from the loaded dataset for a category."""
    mod = MODELS[category]
    mod['MICRO_TO_MACRO_MAP'] = {}
    mod['MACRO_TO_MICROS_MAP'] = {}
    if mod['DATASET'] is not None:
        try:
            df_clean = mod['DATASET'].dropna(subset=['acao_derivada', 'acao_matriz_derivada'])
            for idx, row in df_clean.iterrows():
                micro = str(row['acao_derivada']).strip()
                macro = str(row['acao_matriz_derivada']).strip()
                if micro and macro and micro != 'nan' and macro != 'nan':
                    mod['MICRO_TO_MACRO_MAP'][micro] = macro
                    if macro not in mod['MACRO_TO_MICROS_MAP']:
                        mod['MACRO_TO_MICROS_MAP'][macro] = set()
                    mod['MACRO_TO_MICROS_MAP'][macro].add(micro)
            
            for macro in mod['MACRO_TO_MICROS_MAP']:
                mod['MACRO_TO_MICROS_MAP'][macro] = list(mod['MACRO_TO_MICROS_MAP'][macro])
            
            logging.info(f"[{category}] Mapeamento hierárquico construído. Macros: {len(mod['MACRO_TO_MICROS_MAP'])} | Micros: {len(mod['MICRO_TO_MACRO_MAP'])}")
        except Exception as e:
            logging.error(f"Erro ao construir mapas hierárquicos para {category}: {e}")

def load_resources():
    for cat in CATEGORIAS:
        try:
            dataset_path = os.path.join(ROOT_DIR, f"data/processed/{cat}/dataset_with_similarities.csv")
            if os.path.exists(dataset_path):
                MODELS[cat]['DATASET'] = pd.read_csv(dataset_path)
                logging.info(f"[{cat}] Dataset carregado.")
                build_hierarchical_maps(cat)
            else:
                logging.warning(f"[{cat}] Dataset não encontrado.")
                
            nn_model_path = os.path.join(ROOT_DIR, f"models/{cat}/land_conflict_mt_dnn.pth")
            nn_encoders_path = os.path.join(ROOT_DIR, f"models/{cat}/nn_encoders.pkl")
            
            if os.path.exists(nn_model_path) and os.path.exists(nn_encoders_path):
                with open(nn_encoders_path, 'rb') as f:
                    MODELS[cat]['NN_ENCODERS'] = pickle.load(f)
                
                from training.neural_network_trainer import MultiTaskDNN
                sim_cols = [col for col in MODELS[cat]['DATASET'].columns if col.startswith('sim_score_')]
                input_dim = 384 + len(sim_cols) + 3 
                
                num_classes_derivada = len(MODELS[cat]['NN_ENCODERS']['acao_derivada'].classes_)
                num_classes_matriz = len(MODELS[cat]['NN_ENCODERS']['acao_matriz_derivada'].classes_)
                
                nn_model = MultiTaskDNN(input_dim, num_classes_derivada, num_classes_matriz)
                nn_model.load_state_dict(torch.load(nn_model_path, map_location='cpu'))
                nn_model.eval()
                MODELS[cat]['NN_MODEL'] = nn_model
                logging.info(f"[{cat}] Rede Neural PyTorch carregada.")
                
            # Somente inicializar EmbeddingManager se houver dados
            if MODELS[cat]['DATASET'] is not None:
                MODELS[cat]['EMB_MANAGER'] = EmbeddingManager(category=cat)
                MODELS[cat]['CHUNKER'] = SemanticChunker(chunk_size=350, overlap=100)
        except Exception as e:
            logging.error(f"Erro ao carregar recursos para {cat}: {e}")

@app.route('/')
def dashboard():
    cat = request.args.get('category', 'agrario')
    if cat not in CATEGORIAS:
        cat = 'agrario'
        
    # Prepara métricas rápidas para renderizar no dashboard
    unique_estados = []
    unique_movimentos = []
    unique_pautas = []
    unique_meses = []
    
    # Calculate counts and sources for all categories for the sidebar
    category_counts = {}
    category_sources = {}
    for c in CATEGORIAS:
        if MODELS[c]['DATASET'] is not None:
            category_counts[c] = len(MODELS[c]['DATASET']['codigo_noticia'].unique())
        else:
            category_counts[c] = 0
            
        # Determine source types
        c_raw_dir = os.path.join(ROOT_DIR, "data", "raw", c)
        has_pdf = False
        has_excel = False
        if os.path.exists(c_raw_dir):
            for root, _, files in os.walk(c_raw_dir):
                for f in files:
                    if f.lower().endswith('.pdf') or f.lower().endswith('.zip'):
                        has_pdf = True
                    if f.lower().endswith('.xlsx') or f.lower().endswith('.xls'):
                        has_excel = True
        
        if has_pdf and has_excel:
            category_sources[c] = "PDF + Planilha"
        elif has_pdf:
            category_sources[c] = "PDF"
        elif has_excel:
            category_sources[c] = "Planilha"
        else:
            category_sources[c] = ""
            
    # Contar total de PDFs na pasta raw (sem contar duas vezes)
    raw_dir = os.path.join(ROOT_DIR, "data", "raw", cat)
    total_pdfs = 0
    import glob
    # Contar PDFs soltos (arquivos fora do ZIP)
    pdfs_soltos = glob.glob(os.path.join(raw_dir, "*.pdf"))
    pdfs_soltos += glob.glob(os.path.join(raw_dir, "**", "*.pdf"), recursive=True)
    # Deduplicate
    pdfs_soltos = list(set(pdfs_soltos))
    
    zip_files = glob.glob(os.path.join(raw_dir, "*.zip"))
    if zip_files and not pdfs_soltos:
        # Só conta do ZIP se não há PDFs soltos (evita dupla contagem)
        try:
            with zipfile.ZipFile(zip_files[0], 'r') as z:
                total_pdfs = sum(1 for info in z.infolist() if info.filename.lower().endswith('.pdf') and not info.filename.startswith('__MACOSX'))
        except:
            pass
    else:
        total_pdfs = len(pdfs_soltos)
    
    mod = MODELS[cat]
    if mod['DATASET'] is not None:
        dataset = mod['DATASET']
        total_noticias = len(dataset['codigo_noticia'].unique())
        total_conflitos = len(dataset)
        
        # Obter top pautas e movimentos
        top_pautas = dataset['pauta_acao'].value_counts().head(5).to_dict()
        top_movimentos = dataset['nome_movimento'].value_counts().head(5).to_dict()
        top_estados = dataset['estado'].value_counts().head(5).to_dict()
        
        # Calcular Top 5 PDFs mais densos (com mais chunks)
        top_densos_series = dataset['codigo_noticia'].value_counts().head(5)
        top_densos = []
        for code, count in top_densos_series.items():
            if code and str(code).strip() not in ('nan', '', 'N.I'):
                title = dataset[dataset['codigo_noticia'] == code].iloc[0].get('titulo_noticia', 'N.I')
                top_densos.append({'codigo': str(code), 'titulo': str(title), 'chunks': int(count)})
        
        # Extrair valores únicos para os dropdowns dinâmicos
        unique_estados = sorted([str(x).strip() for x in dataset['estado'].dropna().unique() if str(x).strip() not in ('N.I', 'nan', '')])
        unique_movimentos = sorted([str(x).strip() for x in dataset['nome_movimento'].dropna().unique() if str(x).strip() not in ('N.I', 'nan', '')])
        unique_pautas = sorted([str(x).strip().replace(';', '') for x in dataset['pauta_acao'].dropna().unique() if str(x).strip() not in ('N.I', 'nan', '')])
        
        # Extrair meses dinâmicos e contar ocorrências
        if 'mes_pasta' in dataset.columns:
            import re
            # Mapa de exibição: normaliza nome interno para nome bonito com acento
            _DISPLAY_MAP = {
                '1. JANEIRO': '1. Janeiro', '2. FEVEREIRO': '2. Fevereiro',
                '3. MARCO': '3. Março', '3. MARÇO': '3. Março',
                '4. ABRIL': '4. Abril', '5. MAIO': '5. Maio',
                '6. JUNHO': '6. Junho', '7. JULHO': '7. Julho',
                '8. AGOSTO': '8. Agosto', '9. SETEMBRO': '9. Setembro',
                '10. OUTUBRO': '10. Outubro', '11. NOVEMBRO': '11. Novembro',
                '12. DEZEMBRO': '12. Dezembro',
            }
            meses_raw = [str(x).strip() for x in dataset['mes_pasta'].dropna().unique() if str(x).strip() not in ('N.I', 'nan', '')]
            month_counts = {}
            for m in meses_raw:
                formatted_m = _DISPLAY_MAP.get(m.upper(), m.title())
                # dataset count for this exact raw month
                count = int((dataset['mes_pasta'].astype(str).str.strip() == m).sum())
                # in case multiple raw map to same formatted
                month_counts[formatted_m] = month_counts.get(formatted_m, 0) + count

            def sort_month(m):
                match = re.search(r'(\d+)', m)
                return int(match.group(1)) if match else 99
            unique_meses = sorted(month_counts.keys(), key=sort_month)
        else:
            unique_meses = []
            month_counts = {}

        
        # Add dynamic computation for chunks and pages
        total_chunks = 0
        media_chunks_pagina = 0.0
        try:
            import json
            chunks_csv_path = os.path.join(ROOT_DIR, "chunks_por_pdf.csv")
            paginas_json_path = os.path.join(ROOT_DIR, "paginas_por_pdf.json")
            if os.path.exists(chunks_csv_path) and os.path.exists(paginas_json_path):
                df_chunks = pd.read_csv(chunks_csv_path)
                with open(paginas_json_path, 'r') as f:
                    paginas_dict = json.load(f)
                
                sum_chunks = 0
                sum_paginas = 0
                for _, r in df_chunks.iterrows():
                    codigo_csv = str(r.get('codigo_noticia', '')).strip()
                    qtd_csv = r.get('Quantidade de Chunks (Fragmentos)', 0)
                    qtd_paginas = paginas_dict.get(codigo_csv)
                    if qtd_paginas is not None and str(qtd_paginas).isdigit():
                        sum_chunks += qtd_csv
                        sum_paginas += int(qtd_paginas)
                
                total_chunks = int(df_chunks['Quantidade de Chunks (Fragmentos)'].sum()) if 'Quantidade de Chunks (Fragmentos)' in df_chunks.columns else 0
                if sum_paginas > 0:
                    media_chunks_pagina = round(sum_chunks / sum_paginas, 2)
        except Exception as e:
            logging.error(f"Erro ao calcular media de chunks: {e}")

        stats = {
            'total_noticias': total_noticias,
            'total_conflitos': total_conflitos,
            'total_pdfs': total_pdfs,
            'top_pautas': top_pautas,
            'top_movimentos': top_movimentos,
            'top_estados': top_estados,
            'top_densos': top_densos,
            'total_chunks': total_chunks,
            'media_chunks_pagina': media_chunks_pagina
        }
    else:
        stats = {
            'total_noticias': 0,
            'total_conflitos': 0,
            'total_pdfs': total_pdfs,
            'top_pautas': {},
            'top_movimentos': {},
            'top_estados': {},
            'top_densos': []
        }
        
    return render_template(
        'index.html', 
        stats=stats, 
        unique_estados=unique_estados, 
        unique_movimentos=unique_movimentos, 
        unique_pautas=unique_pautas,
        unique_meses=unique_meses,
        month_counts=month_counts,
        category_counts=category_counts,
        category_sources=category_sources,
        current_category=cat,
        cat_name={'agrario': 'Agrários', 'floresta': 'Florestais', 'urbano': 'Urbanos', 'aguas': 'de Águas'}.get(cat, cat.title())
    )

@app.route('/metodologia')
def metodologia():
    return render_template('metodologia.html')

@app.route('/desenvolvimento')
def desenvolvimento():
    return render_template('desenvolvimento.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/questoes')
def questoes():
    return render_template('questoes.html')

@app.route('/orientacoes')
def orientacoes():
    return render_template('orientacoes.html')

from sklearn.metrics.pairwise import cosine_similarity

@app.route('/api/chat', methods=['POST'])
def chat():
    """RAG Extrativo: Recebe uma pergunta e retorna os chunks mais similares usando Distância do Cosseno."""
    data = request.json
    query = data.get('query', '')
    cat = data.get('category', 'agrario')

    if not query or cat not in CATEGORIAS or MODELS[cat]['DATASET'] is None:
        return jsonify({'error': 'Parâmetros inválidos ou dataset não carregado.'}), 400

    emb_manager = MODELS[cat]['EMB_MANAGER']
    if emb_manager is None:
        return jsonify({'error': 'Modelo de embeddings não carregado para esta categoria.'}), 500

    # Lazy load dos embeddings dos chunks para economizar memória na inicialização
    if 'CHUNK_EMBEDDINGS' not in MODELS[cat] or MODELS[cat]['CHUNK_EMBEDDINGS'] is None:
        logging.info(f"[{cat}] Calculando embeddings dos chunks para o RAG (Lazy Load)...")
        chunks = MODELS[cat]['DATASET']['chunk_texto'].tolist()
        MODELS[cat]['CHUNK_EMBEDDINGS'] = emb_manager.encode_text(chunks, batch_size=32)
        logging.info(f"[{cat}] Embeddings cacheados para busca semântica.")

    # Codificar a pergunta do usuário
    query_emb = emb_manager.model.encode([query], show_progress_bar=False)

    # Calcular a Similaridade do Cosseno
    similarities = cosine_similarity(query_emb, MODELS[cat]['CHUNK_EMBEDDINGS'])[0]

    # Pegar os top 3 índices mais similares
    top_indices = np.argsort(similarities)[::-1][:3]

    results = []
    df = MODELS[cat]['DATASET']
    for idx in top_indices:
        row = df.iloc[idx]
        sim_score = similarities[idx]
        
        # Só retornar se a similaridade for razoável (evitar lixo)
        if sim_score > 0.1:
            results.append({
                'texto': row.get('chunk_texto', ''),
                'score': float(sim_score),
                'arquivo': row.get('arquivo_origem', ''),
                'acao': row.get('acao_derivada', 'Sem Categoria')
            })

    if not results:
         return jsonify({'answer': 'Desculpe, não encontrei nenhum relato específico sobre isso na base de dados atual.'})

    # Construir a resposta textual
    answer = f"Encontrei {len(results)} relatos na base de dados que respondem à sua pergunta:<br><br>"
    for i, res in enumerate(results):
        answer += f"<strong>📄 Documento {i+1}</strong> ({res['acao']} - <em>Confiança: {res['score']:.2f}</em>)<br>"
        answer += f"\"{res['texto']}\"<br><br>"

    return jsonify({'answer': answer})

@app.route('/api/ask_rag', methods=['POST'])
def ask_rag():
    """Endpoint LangChain RAG: Recebe pergunta, busca no FAISS e gera resposta com LLM via MCP Router."""
    data = request.json
    query = data.get('query', '')
    cat = data.get('category', 'agrario')

    if not query:
        return jsonify({'error': 'A pergunta não pode estar vazia.'}), 400

    from rag.qa_chain import ask_question
    
    # Executar RAG Chain
    result = ask_question(query, category=cat)
    
    return jsonify({
        'answer': result['answer'],
        'sources': result['sources']
    })

@app.route('/api/map-data')
def map_data():
    """Returns dynamic GIS markers with latitude and longitude (offline geocoding with visual jittering)."""
    cat = request.args.get('category', 'agrario')
    if cat not in CATEGORIAS or MODELS[cat]['DATASET'] is None:
        return jsonify([])
        
    markers = []
    # Filtrar registros que possuem localização válida
    df_loc = MODELS[cat]['DATASET'].dropna(subset=['estado']).copy()
    
    # Adicionar pequeno jitter aleatório para evitar sobreposição perfeita de múltiplos eventos na mesma capital
    np.random.seed(42)
    
    for idx, row in df_loc.iterrows():
        estado = str(row.get('estado', '')).strip()
        municipio = str(row.get('municipio', '')).strip()
        
        # Buscar coordenadas
        base_coords = ESTADO_COORDS.get(estado)
        if not base_coords:
            # Tentar buscar por aproximação de caracteres
            for key, val in ESTADO_COORDS.items():
                if estado.lower() in key.lower() or key.lower() in estado.lower():
                    base_coords = val
                    break
                    
        if base_coords:
            # Jitter de +-0.15 graus para espalhar os marcadores visualmente ao redor da capital do estado
            lat = base_coords[0] + np.random.uniform(-0.25, 0.25)
            lng = base_coords[1] + np.random.uniform(-0.25, 0.25)
            
            markers.append({
                'id': row.get('id_chunk', f"event_{idx}"),
                'lat': lat,
                'lng': lng,
                'estado': estado,
                'municipio': municipio if pd.notna(row.get('municipio')) else 'N.I',
                'movimento': row.get('nome_movimento', 'N.I') if pd.notna(row.get('nome_movimento')) else 'N.I',
                'acao_derivada': row.get('acao_derivada', 'N.I') if pd.notna(row.get('acao_derivada')) else 'N.I',
                'pauta': row.get('pauta_acao', 'N.I') if pd.notna(row.get('pauta_acao')) else 'N.I',
                'mes_pasta': {
                    '1. JANEIRO': '1. Janeiro', '2. FEVEREIRO': '2. Fevereiro',
                    '3. MARCO': '3. Março', '3. MARÇO': '3. Março',
                    '4. ABRIL': '4. Abril', '5. MAIO': '5. Maio',
                    '6. JUNHO': '6. Junho', '7. JULHO': '7. Julho',
                    '8. AGOSTO': '8. Agosto', '9. SETEMBRO': '9. Setembro',
                    '10. OUTUBRO': '10. Outubro', '11. NOVEMBRO': '11. Novembro',
                    '12. DEZEMBRO': '12. Dezembro',
                }.get(str(row.get('mes_pasta', 'N.I')).strip().upper(), str(row.get('mes_pasta', 'N.I')).strip())
            })

            
    return jsonify(markers)

@app.route('/api/extract-pdf-text', methods=['POST'])
def extract_pdf_text():
    """Receives a PDF file upload, extracts its text using pdfplumber, and returns it."""
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado.'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado.'}), 400
        
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'O arquivo deve ser um PDF.'}), 400
        
    try:
        # Read the file directly from memory into pdfplumber
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\\n"
                    
            text = text.strip()
            if not text:
                return jsonify({'error': 'Não foi possível extrair nenhum texto legível do PDF. Ele pode ser uma imagem escaneada.'}), 400
                
            return jsonify({'text': text})
    except Exception as e:
        logging.error(f"Erro ao processar PDF enviado via upload: {e}")
        return jsonify({'error': f'Erro ao processar o arquivo PDF: {str(e)}'}), 500

@app.route('/api/classify', methods=['POST'])
def classify_text():
    """Asynchronously extracts chunks and classifies news text."""
    data = request.get_json()
    cat = data.get('category', 'agrario') if data else 'agrario'
    if cat not in CATEGORIAS:
        cat = 'agrario'
        
    mod = MODELS[cat]
    NN_MODEL = mod['NN_MODEL']
    NN_ENCODERS = mod['NN_ENCODERS']
    EMB_MANAGER = mod['EMB_MANAGER']
    CHUNKER = mod['CHUNKER']
    
    if not NN_MODEL or not NN_ENCODERS or not EMB_MANAGER or not CHUNKER:
        return jsonify({'error': f'Os modelos da categoria {cat.upper()} não estão carregados no servidor. Por favor, treine o classificador.'}), 400
        
    if not data or 'text' not in data:
        return jsonify({'error': 'Texto para classificação não fornecido.'}), 400
        
    text = data['text']
    # Metadados opcionais fornecidos na tela
    estado = data.get('estado', 'N.I')
    pauta = data.get('pauta', 'N.I')
    movimento = data.get('movimento', 'N.I')
    
    # 1. Chunking Semântico
    chunks = CHUNKER.split_into_semantic_chunks(text)
    if not chunks:
        return jsonify({'error': 'Não foi possível segmentar o texto em partes coerentes.'}), 400
        
    results = []
    
    # 2. Gerar embeddings e classificar cada chunk
    for c_idx, chunk in enumerate(chunks):
        # Embedding do chunk
        chunk_emb = EMB_MANAGER.encode_text(chunk, batch_size=1)
        
        # Calcular similaridades
        sims = EMB_MANAGER.compute_similarities(chunk_emb)
        
        # Encodar metadados usando os encoders carregados
        meta_encoded = []
        for col, val in [('estado', estado), ('pauta_acao', pauta), ('nome_movimento', movimento)]:
            le = NN_ENCODERS[col]
            # Tratar classes não vistas no treino
            if val in le.classes_:
                meta_encoded.append(le.transform([val])[0])
            else:
                meta_encoded.append(le.transform(['OUTROS'])[0])
                
        # Construir vetor de features X
        meta_arr = np.array(meta_encoded).reshape(1, -1)
        X_chunk = np.hstack([chunk_emb, sims, meta_arr])
        
        # Converter para tensor PyTorch e passar pelo modelo
        X_tensor = torch.tensor(X_chunk, dtype=torch.float32)
        
        with torch.no_grad():
            pred_deriv, pred_mat = NN_MODEL(X_tensor)
            prob_matriz_arr = torch.softmax(pred_mat, dim=1).numpy()[0]
            prob_derivada_arr = torch.softmax(pred_deriv, dim=1).numpy()[0]
        
        # 1. Predizer Ação Matriz (Macro Categoria) primeiro
        max_prob_matriz_idx = np.argmax(prob_matriz_arr)
        pred_matriz = NN_ENCODERS['acao_matriz_derivada'].classes_[max_prob_matriz_idx]
        conf_matriz = float(prob_matriz_arr[max_prob_matriz_idx])
        
        # 2. Obter as microclasses válidas para esta macroclasse
        valid_micros = mod['MACRO_TO_MICROS_MAP'].get(pred_matriz, [])
        
        if valid_micros:
            # Encontrar os índices das microclasses válidas na lista de classes do modelo
            valid_indices = []
            valid_class_names = []
            for i, class_name in enumerate(NN_ENCODERS['acao_derivada'].classes_):
                if class_name in valid_micros:
                    valid_indices.append(i)
                    valid_class_names.append(class_name)
                    
            if valid_indices:
                # Obter as probabilidades brutas das microclasses válidas
                valid_probs = prob_derivada_arr[valid_indices]
                
                # Normalizar condicionalmente para garantir coerência: P(micro | macro)
                sum_valid_probs = np.sum(valid_probs)
                if sum_valid_probs > 0:
                    cond_probs = valid_probs / sum_valid_probs
                else:
                    cond_probs = np.ones_like(valid_probs) / len(valid_probs)
                    
                # Selecionar a microclasse com a maior probabilidade condicional
                best_idx_in_valid = np.argmax(cond_probs)
                pred_derivada = valid_class_names[best_idx_in_valid]
                
                # A confiança conjunta final P(micro ∩ macro) = P(micro | macro) * P(macro)
                conf_derivada = float(cond_probs[best_idx_in_valid] * conf_matriz)
            else:
                # Caso extremo de fallback (sem interseção na base)
                max_prob_idx = np.argmax(prob_derivada_arr)
                pred_derivada = NN_ENCODERS['acao_derivada'].classes_[max_prob_idx]
                conf_derivada = float(prob_derivada_arr[max_prob_idx])
        else:
            # Caso padrão de fallback
            max_prob_idx = np.argmax(prob_derivada_arr)
            pred_derivada = NN_ENCODERS['acao_derivada'].classes_[max_prob_idx]
            conf_derivada = float(prob_derivada_arr[max_prob_idx])
            
        results.append({
            'chunk_id': f"web_c{c_idx}",
            'texto': chunk,
            'acao_derivada': pred_derivada,
            'confianca_derivada': conf_derivada,
            'acao_matriz': pred_matriz,
            'confianca_matriz': conf_matriz
        })
        
    # Agregação final (decisão por voto ou maior confiança)
    # Selecionamos a predição com o maior nível de confiança médio entre todos os chunks
    best_derivada = max(results, key=lambda r: r['confianca_derivada'])
    
    return jsonify({
        'classificacao_geral': {
            'acao_derivada': best_derivada['acao_derivada'],
            'confianca_derivada': best_derivada['confianca_derivada'],
            'acao_matriz': best_derivada['acao_matriz'],
            'confianca_matriz': best_derivada['confianca_matriz']
        },
        'chunks': results
    })

def background_training_pipeline(cat='agrario'):
    global TRAINING_STATUS
    TRAINING_STATUS = f"Training|Iniciando ingestão da categoria {cat}..."
    try:
        # Importando aqui para evitar dependência circular
        from ingestion.ingestion_manager import ingest_dataset
        from preprocessing.text_preprocessor import preprocess_and_chunk_dataset
        from embeddings.embedding_generator import process_embeddings_and_similarities
        
        logging.info("Iniciando pipeline de retreinamento completo em background...")
        
        def update_progress(current, total):
            global TRAINING_STATUS
            TRAINING_STATUS = f"Training|Ingerindo notícias: {current}/{total}"
            
        # Executar ETL
        ingest_dataset("PLANILHA AGRARIO 2024  (3).xlsx", "DATALUTA MOV_AGRARIO_2024-20260602T191955Z-3-001.zip", progress_callback=update_progress)
        # Chunking
        preprocess_and_chunk_dataset("data/processed/dataset_processado.csv")
        # Embeddings e similaridades
        process_embeddings_and_similarities("data/processed/dataset_chunked.csv")
        
        # Treinamento 1: Classificadores Base (HistGradientBoosting)
        from training.classifier_trainer import ModelTrainer
        clf_trainer = ModelTrainer("data/processed/dataset_with_similarities.csv", "data/processed/chunk_embeddings.npy")
        clf_trainer.train_and_evaluate()
        
        # Treinamento 2: Rede Neural PyTorch MT-DNN Aprimorada
        from training.neural_network_trainer import NeuralNetworkTrainer
        nn_trainer = NeuralNetworkTrainer("data/processed/dataset_with_similarities.csv", "data/processed/chunk_embeddings.npy")
        stats = nn_trainer.train_and_evaluate(epochs=100)
        
        # Recarregar recursos na memória
        load_resources()
        
        TRAINING_STATUS = f"Success|AccDerivada:{stats['accuracy_derivada']*100:.1f}%|AccMatriz:{stats['accuracy_matriz']*100:.1f}%"
        logging.info("Pipeline de retreinamento concluído com absoluto sucesso em background!")
    except Exception as e:
        logging.error(f"Erro no pipeline de retreinamento: {e}")
        TRAINING_STATUS = f"Error: {str(e)}"

@app.route('/api/train', methods=['POST'])
def run_training():
    """Triggers the full pipeline in a separate background thread."""
    global TRAINING_STATUS
    
    data = request.get_json()
    cat = data.get('category', 'agrario') if data else 'agrario'
    if cat not in CATEGORIAS:
        cat = 'agrario'
        
    if "Training" in TRAINING_STATUS:
        return jsonify({'status': 'running', 'message': 'O pipeline de treinamento já está em execução no momento.'})
        
    thread = Thread(target=background_training_pipeline, args=(cat,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'started', 'message': 'Treinamento iniciado em background.'})

@app.route('/api/train/status')
def train_status():
    global TRAINING_STATUS
    return jsonify({'status': TRAINING_STATUS})

@app.route('/api/news-list')
def get_news_list():
    """Returns a list of unique news articles with their basic metadata."""
    cat = request.args.get('category', 'agrario')
    if cat not in CATEGORIAS or MODELS[cat]['DATASET'] is None:
        return jsonify([])
    try:
        dataset = MODELS[cat]['DATASET']
        
        # Tentar ler a quantidade total de chunks do arquivo oficial primeiro
        total_chunks_dict = {}
        csv_path = os.path.join(ROOT_DIR, "chunks_por_pdf.csv")
        if os.path.exists(csv_path):
            try:
                import pandas as pd
                df_chunks = pd.read_csv(csv_path)
                for _, r in df_chunks.iterrows():
                    codigo_csv = str(r.get('codigo_noticia', '')).strip()
                    qtd_csv = r.get('Quantidade de Chunks (Fragmentos)', 0)
                    total_chunks_dict[codigo_csv] = qtd_csv
            except Exception as e:
                logging.error(f"Erro ao ler chunks_por_pdf.csv: {e}")

        # Fallback para contagem no dataset em memória
        chunk_counts = dataset['codigo_noticia'].value_counts().to_dict()
        
        # Group by unique news code
        unique_news = dataset.drop_duplicates(subset=['codigo_noticia']).copy()
        unique_news = unique_news.fillna('N.I')
        
        news_list = []
        for idx, row in unique_news.iterrows():
            codigo = str(row.get('codigo_noticia', '')).strip()
            
            # Usar o valor do CSV oficial se existir, caso contrário usar a contagem
            qtd = total_chunks_dict.get(codigo, chunk_counts.get(codigo, 0))
            
            news_list.append({
                'codigo_noticia': codigo,
                'titulo_noticia': str(row.get('titulo_noticia', '')).strip(),
                'estado': str(row.get('estado', '')).strip(),
                'nome_movimento': str(row.get('nome_movimento', '')).strip(),
                'pauta_acao': str(row.get('pauta_acao', '')).strip(),
                'mes_pasta': {
                    '1. JANEIRO': '1. Janeiro', '2. FEVEREIRO': '2. Fevereiro',
                    '3. MARCO': '3. Março', '3. MARÇO': '3. Março',
                    '4. ABRIL': '4. Abril', '5. MAIO': '5. Maio',
                    '6. JUNHO': '6. Junho', '7. JULHO': '7. Julho',
                    '8. AGOSTO': '8. Agosto', '9. SETEMBRO': '9. Setembro',
                    '10. OUTUBRO': '10. Outubro', '11. NOVEMBRO': '11. Novembro',
                    '12. DEZEMBRO': '12. Dezembro',
                }.get(str(row.get('mes_pasta', 'N.I')).strip().upper(), str(row.get('mes_pasta', 'N.I')).strip()),

                'qtd_chunks': qtd
            })
        return jsonify(news_list)
    except Exception as e:
        logging.error(f"Erro ao listar noticias: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/news/<news_code>')
def get_news_detail(news_code):
    """Returns the full text and exact metadata of a news article."""
    cat = request.args.get('category', 'agrario')
    if cat not in CATEGORIAS:
        cat = 'agrario'
        
    try:
        processed_csv = os.path.join(ROOT_DIR, f"data/processed/{cat}/dataset_processado.csv")
        if not os.path.exists(processed_csv):
            return jsonify({'error': f'Arquivo de dados processados ausente para a categoria {cat}.'}), 404
            
        df_proc = pd.read_csv(processed_csv)
        # Find news
        row = df_proc[df_proc['Código da notícia 2024'].astype(str).str.strip() == str(news_code).strip()]
        
        if not row.empty:
            text = row.iloc[0].get('texto_noticia', '')
            title = row.iloc[0].get('Título da notícia', '')
            estado = row.iloc[0].get('Estado', 'N.I')
            pauta = row.iloc[0].get('Pauta da ação', 'N.I')
            movimento = row.iloc[0].get('Nome do movimento', 'N.I')
            if pd.isna(movimento) or not isinstance(movimento, str) or movimento.strip() == '':
                movimento = 'N.I'
            else:
                movimento = movimento.strip()
                
            if movimento == 'Não Consta na Listagem':
                custom_mov = row.iloc[0].get('Cadastrar movimento não listado', '')
                if isinstance(custom_mov, str) and custom_mov.strip() and pd.notna(custom_mov):
                    movimento = custom_mov.strip()
            
            # Tratar NaNs
            text = text if pd.notna(text) else ""
            title = title if pd.notna(title) else ""
            estado = estado if pd.notna(estado) else "N.I"
            pauta = pauta if pd.notna(pauta) else "N.I"
            movimento = movimento if pd.notna(movimento) else "N.I"
            
            return jsonify({
                'codigo_noticia': news_code,
                'titulo_noticia': title,
                'texto_noticia': text,
                'estado': estado,
                'pauta_acao': pauta,
                'nome_movimento': movimento
            })
        return jsonify({'error': f'Notícia com código {news_code} não encontrada.'}), 404
    except Exception as e:
        logging.error(f"Erro ao buscar detalhe da noticia {news_code}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/pdf/<news_code>')
def get_pdf(news_code):
    """Streams a PDF file located inside the ZIP archive directly to the browser."""
    cat = request.args.get('category', 'agrario')
    if cat not in CATEGORIAS:
        cat = 'agrario'
        
    try:
        from ingestion.ingestion_manager import get_category_files
        _, zip_path = get_category_files(cat, ROOT_DIR)
        
        if not zip_path or not os.path.exists(zip_path):
            return f"Arquivo ZIP de notícias não encontrado para a categoria {cat}.", 404
            
        with zipfile.ZipFile(zip_path) as z:
            zip_files = z.namelist()
            target_path = None
            for filepath in zip_files:
                if filepath.endswith('.pdf'):
                    filename = os.path.basename(filepath)
                    code = os.path.splitext(filename)[0]
                    if code.strip() == str(news_code).strip():
                        target_path = filepath
                        break
            
            if target_path:
                pdf_data = z.read(target_path)
                return send_file(
                    io.BytesIO(pdf_data),
                    mimetype='application/pdf',
                    as_attachment=False,
                    download_name=f"{news_code}.pdf"
                )
        return f"O PDF com o código '{news_code}' não foi localizado dentro do arquivo ZIP do MST/LCP.", 404
    except Exception as e:
        logging.error(f"Erro ao carregar PDF do ZIP: {e}")
        return f"Erro ao extrair PDF: {str(e)}", 500

@app.route('/api/knowledge-graph')
def get_knowledge_graph():
    """Extracts co-occurrence relations from dataset to form nodes and edges for the Knowledge Graph."""
    cat = request.args.get('category', 'agrario')
    if cat not in CATEGORIAS or MODELS[cat]['DATASET'] is None:
        return jsonify({'nodes': [], 'edges': []})
        
    try:
        nodes_dict = {}
        edges_dict = {}
        
        # Filtros de limpeza (remover NaNs nas colunas-chave)
        df_clean = MODELS[cat]['DATASET'].dropna(subset=['nome_movimento', 'estado', 'pauta_acao', 'acao_matriz_derivada']).copy()
        
        for idx, row in df_clean.iterrows():
            mov = str(row['nome_movimento']).strip()
            est = str(row['estado']).strip()
            pau = str(row['pauta_acao']).strip().replace(';', '')
            act = str(row['acao_matriz_derivada']).strip()
            
            # Limpar formatações comuns (ex: remover prefixos redundantes)
            if mov.startswith('Nome do movimento'):
                mov = mov.replace('Nome do movimento', '').strip()
            pau = pau.replace('Pauta da ação', '').strip()
            
            # Pular valores inválidos ou genéricos de "Não Informado"
            if not mov or mov in ('N.I', 'nan', '') or not est or est in ('N.I', 'nan', '') or not pau or pau in ('N.I', 'nan', '') or not act or act in ('N.I', 'nan', ''):
                continue
                
            # Adicionar/atualizar nós
            # Grupos: movimento, estado, pauta, acao
            for node_id, group, label in [(mov, 'movimento', mov), (est, 'estado', est), (pau, 'pauta', pau), (act, 'acao', act)]:
                if node_id not in nodes_dict:
                    nodes_dict[node_id] = {'id': node_id, 'label': label, 'group': group, 'value': 0}
                nodes_dict[node_id]['value'] += 1
                
            # Adicionar/atualizar arestas (edges)
            # Relações: mov -> est (ATUA_EM), mov -> pau (REIVINDICA), mov -> act (REALIZA)
            relations = [
                (mov, est, 'ATUA_EM'),
                (mov, pau, 'REIVINDICA'),
                (mov, act, 'REALIZA')
            ]
            
            for src, tgt, rel in relations:
                edge_id = f"{src}_{tgt}_{rel}"
                if edge_id not in edges_dict:
                    edges_dict[edge_id] = {'from': src, 'to': tgt, 'label': rel, 'value': 0}
                edges_dict[edge_id]['value'] += 1
                
        # Filtrar arestas com baixa coocorrência (coocorrência >= 2)
        filtered_edges = [edge for edge in edges_dict.values() if edge['value'] >= 2]
        
        # Manter apenas os nós que possuem pelo menos uma aresta após a filtragem
        active_nodes_ids = set()
        for edge in filtered_edges:
            active_nodes_ids.add(edge['from'])
            active_nodes_ids.add(edge['to'])
            
        filtered_nodes = [node for node in nodes_dict.values() if node['id'] in active_nodes_ids]
        
        # Escalar o tamanho do nó proporcionalmente à sua frequência para destacar entidades influentes
        for node in filtered_nodes:
            node['size'] = 12 + int(np.log2(node['value'] + 1) * 4)
            
        return jsonify({
            'nodes': filtered_nodes,
            'edges': filtered_edges
        })
    except Exception as e:
        logging.error(f"Erro ao gerar dados do grafo de conhecimento: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/log', methods=['POST'])
def receive_client_log():
    try:
        data = request.get_json()
        log_type = data.get('type', 'log')
        message = data.get('message', '')
        with open('client_logs.txt', 'a', encoding='utf-8') as f:
            f.write(f"[{log_type.upper()}] {message}\n")
        return jsonify({'status': 'ok'})
    except Exception:
        return jsonify({'status': 'error'}), 500

@app.route('/api/raw-pdfs', methods=['GET'])
def get_raw_pdfs():
    cat = request.args.get('category', 'agrario')
    if cat not in CATEGORIAS:
        cat = 'agrario'
        
    raw_dir = os.path.join(ROOT_DIR, "data", "raw", cat)
    if not os.path.exists(raw_dir):
        return jsonify([])
        
    # Tentar ler a quantidade total de chunks do arquivo oficial
    total_chunks_dict = {}
    justificativa_dict = {}
    csv_path = os.path.join(ROOT_DIR, "chunks_por_pdf.csv")
    if os.path.exists(csv_path):
        try:
            import pandas as pd
            df_chunks = pd.read_csv(csv_path)
            for _, r in df_chunks.iterrows():
                codigo_csv = str(r.get('codigo_noticia', '')).strip()
                val = r.get('Quantidade de Chunks (Fragmentos)', 0)
                just = str(r.get('Justificativa', ''))
                try:
                    qtd_csv = int(val)
                except:
                    qtd_csv = 0
                total_chunks_dict[codigo_csv] = qtd_csv
                justificativa_dict[codigo_csv] = just
        except Exception as e:
            pass

    # Tentar ler a quantidade de páginas do json
    paginas_dict = {}
    json_path = os.path.join(ROOT_DIR, "paginas_por_pdf.json")
    if os.path.exists(json_path):
        try:
            import json
            with open(json_path, 'r', encoding='utf-8') as f:
                paginas_dict = json.load(f)
        except Exception as e:
            pass

    pdf_files = []
    
    # 1. PDFs soltos
    import glob
    loose_pdfs = glob.glob(os.path.join(raw_dir, "**", "*.pdf"), recursive=True)
    for p in loose_pdfs:
        name = os.path.basename(p)
        size = round(os.path.getsize(p) / 1024, 1)
        codigo = name.replace('.pdf', '').replace('.PDF', '')
        qtd = total_chunks_dict.get(codigo, 0)
        just = justificativa_dict.get(codigo, '')
        paginas = paginas_dict.get(codigo, '?')
        pdf_files.append({"filename": name, "filepath": f"fs:{p}", "size": size, "qtd_chunks": qtd, "justificativa": just, "qtd_paginas": paginas})
        
    # 2. PDFs no ZIP
    from ingestion.ingestion_manager import get_category_files
    _, zip_path = get_category_files(cat, ROOT_DIR)
    
    # Remover duplicatas: se o arquivo já foi encontrado solto na pasta, não listá-lo do ZIP de novo
    existing_names = {f['filename'] for f in pdf_files}
    
    if zip_path and os.path.exists(zip_path):
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                for info in z.infolist():
                    if info.filename.lower().endswith('.pdf') and not info.filename.startswith('__MACOSX'):
                        name = os.path.basename(info.filename)
                        if name and name not in existing_names:
                            size = round(info.file_size / 1024, 1)
                            codigo = name.replace('.pdf', '').replace('.PDF', '')
                            qtd = total_chunks_dict.get(codigo, 0)
                            just = justificativa_dict.get(codigo, '')
                            paginas = paginas_dict.get(codigo, '?')
                            pdf_files.append({"filename": name, "filepath": f"zip:{info.filename}", "size": size, "qtd_chunks": qtd, "justificativa": just, "qtd_paginas": paginas})
                            existing_names.add(name)
        except:
            pass

    pdf_files = sorted(pdf_files, key=lambda x: x['filename'])
    return jsonify(pdf_files)

@app.route('/api/extract-pdf-from-zip', methods=['POST'])
def extract_pdf_from_zip_endpoint():
    data = request.json
    if not data or 'filepath' not in data:
        return jsonify({"error": "Filepath não fornecido."}), 400
        
    cat = data.get('category', 'agrario')
    if cat not in CATEGORIAS:
        cat = 'agrario'
        
    filepath = data['filepath']
    
    try:
        import pdfplumber
        if filepath.startswith('fs:'):
            actual_path = filepath[3:]
            if not os.path.exists(actual_path):
                return jsonify({"error": "PDF não encontrado no disco."}), 404
            text = ""
            with pdfplumber.open(actual_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t: text += t + "\n"
        else:
            actual_path = filepath[4:] if filepath.startswith('zip:') else filepath
            from ingestion.ingestion_manager import get_category_files, extract_pdf_text_from_zip
            _, zip_path = get_category_files(cat, ROOT_DIR)
            if not zip_path:
                return jsonify({"error": "Arquivo ZIP não encontrado."}), 404
            text = extract_pdf_text_from_zip(zip_path, actual_path)

        if not text or not text.strip():
            return jsonify({"error": "PDF está vazio ou contém texto ilegível."}), 400
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download-pdf', methods=['GET'])
def download_pdf_endpoint():
    filepath = request.args.get('filepath')
    cat = request.args.get('category', 'agrario')
    
    if not filepath:
        return jsonify({"error": "Filepath não fornecido."}), 400
        
    try:
        if filepath.startswith('fs:'):
            actual_path = filepath[3:]
            if not os.path.exists(actual_path):
                return jsonify({"error": "PDF não encontrado no disco."}), 404
            return send_file(actual_path, as_attachment=True, download_name=os.path.basename(actual_path))
        else:
            actual_path = filepath[4:] if filepath.startswith('zip:') else filepath
            from ingestion.ingestion_manager import get_category_files
            _, zip_path = get_category_files(cat, ROOT_DIR)
            if not zip_path or not os.path.exists(zip_path):
                return jsonify({"error": "Arquivo ZIP não encontrado."}), 404
                
            with zipfile.ZipFile(zip_path, 'r') as z:
                with z.open(actual_path) as f:
                    data = f.read()
                
            buffer = io.BytesIO(data)
            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name=os.path.basename(actual_path), mimetype='application/pdf')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    load_resources()
    app.run(debug=True, use_reloader=False, host='127.0.0.1', port=80)

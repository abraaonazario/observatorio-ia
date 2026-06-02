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

# Adicionar raiz do projeto ao path para garantir que os módulos sejam encontrados
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importações dos nossos módulos
from preprocessing.text_preprocessor import SemanticChunker
from embeddings.embedding_generator import EmbeddingManager, ACAO_DERIVADA_ENRIQUECIDA
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

# Variáveis globais para armazenar os modelos e o dataset
DATASET = None
CLF_DERIVADA = None
CLF_MATRIZ = None
ENCODERS = None
EMB_MANAGER = None
CHUNKER = None
TRAINING_STATUS = "Idle"  # Idle, Training, Success, Error

# Mapeamentos hierárquicos dinâmicos (Micro -> Macro e Macro -> [Micros])
MICRO_TO_MACRO_MAP = {}
MACRO_TO_MICROS_MAP = {}

def build_hierarchical_maps():
    """Dynamically builds hierarchical maps from the loaded dataset."""
    global MICRO_TO_MACRO_MAP, MACRO_TO_MICROS_MAP
    MICRO_TO_MACRO_MAP = {}
    MACRO_TO_MICROS_MAP = {}
    if DATASET is not None:
        try:
            # Remover NaNs nas colunas de classificação
            df_clean = DATASET.dropna(subset=['acao_derivada', 'acao_matriz_derivada'])
            for idx, row in df_clean.iterrows():
                micro = str(row['acao_derivada']).strip()
                macro = str(row['acao_matriz_derivada']).strip()
                if micro and macro and micro != 'nan' and macro != 'nan':
                    MICRO_TO_MACRO_MAP[micro] = macro
                    if macro not in MACRO_TO_MICROS_MAP:
                        MACRO_TO_MICROS_MAP[macro] = set()
                    MACRO_TO_MICROS_MAP[macro].add(micro)
            
            # Converter sets para lists
            for macro in MACRO_TO_MICROS_MAP:
                MACRO_TO_MICROS_MAP[macro] = list(MACRO_TO_MICROS_MAP[macro])
            
            logging.info(f"Mapeamento hierárquico construído com sucesso. Macros: {len(MACRO_TO_MICROS_MAP)} | Micros: {len(MICRO_TO_MACRO_MAP)}")
        except Exception as e:
            logging.error(f"Erro ao construir mapas hierárquicos: {e}")

def load_resources():
    global DATASET, CLF_DERIVADA, CLF_MATRIZ, ENCODERS, EMB_MANAGER, CHUNKER
    try:
        dataset_path = "data/processed/dataset_with_similarities.csv"
        if os.path.exists(dataset_path):
            DATASET = pd.read_csv(dataset_path)
            logging.info("Dataset carregado na memória da aplicação.")
            build_hierarchical_maps()
        else:
            logging.warning("Dataset processado não encontrado. Por favor, execute o pipeline.")
            
        models_dir = "models"
        clf_derivada_path = os.path.join(models_dir, "classifier_derivada.pkl")
        clf_matriz_path = os.path.join(models_dir, "classifier_matriz.pkl")
        encoders_path = os.path.join(models_dir, "encoders.pkl")
        
        if os.path.exists(clf_derivada_path) and os.path.exists(clf_matriz_path) and os.path.exists(encoders_path):
            with open(clf_derivada_path, 'rb') as f:
                CLF_DERIVADA = pickle.load(f)
            with open(clf_matriz_path, 'rb') as f:
                CLF_MATRIZ = pickle.load(f)
            with open(encoders_path, 'rb') as f:
                ENCODERS = pickle.load(f)
            logging.info("Modelos de machine learning carregados com sucesso.")
        else:
            logging.warning("Modelos de machine learning nao encontrados. É necessário treinar os modelos.")
            
        # Carregar embedding manager e chunker
        EMB_MANAGER = EmbeddingManager()
        CHUNKER = SemanticChunker(chunk_size=500, overlap=50)
    except Exception as e:
        logging.error(f"Erro ao carregar recursos da aplicacao: {e}")

@app.route('/')
def dashboard():
    # Prepara métricas rápidas para renderizar no dashboard
    if DATASET is not None:
        total_noticias = len(DATASET['codigo_noticia'].unique())
        total_conflitos = len(DATASET)
        
        # Obter top pautas e movimentos
        top_pautas = DATASET['pauta_acao'].value_counts().head(5).to_dict()
        top_movimentos = DATASET['nome_movimento'].value_counts().head(5).to_dict()
        top_estados = DATASET['estado'].value_counts().head(5).to_dict()
        
        stats = {
            'total_noticias': total_noticias,
            'total_conflitos': total_conflitos,
            'top_pautas': top_pautas,
            'top_movimentos': top_movimentos,
            'top_estados': top_estados
        }
    else:
        stats = {
            'total_noticias': 0,
            'total_conflitos': 0,
            'top_pautas': {},
            'top_movimentos': {},
            'top_estados': {}
        }
        
    return render_template('index.html', stats=stats)

@app.route('/api/map-data')
def map_data():
    """Returns dynamic GIS markers with latitude and longitude (offline geocoding with visual jittering)."""
    if DATASET is None:
        return jsonify([])
        
    markers = []
    # Filtrar registros que possuem localização válida
    df_loc = DATASET.dropna(subset=['estado']).copy()
    
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
                'pauta': row.get('pauta_acao', 'N.I') if pd.notna(row.get('pauta_acao')) else 'N.I'
            })
            
    return jsonify(markers)

@app.route('/api/classify', methods=['POST'])
def classify_text():
    """Asynchronously extracts chunks and classifies news text."""
    global CLF_DERIVADA, CLF_MATRIZ, ENCODERS, EMB_MANAGER, CHUNKER
    
    if not CLF_DERIVADA or not CLF_MATRIZ or not EMB_MANAGER or not CHUNKER:
        return jsonify({'error': 'Os modelos ou recursos de NLP não estão carregados no servidor. Por favor, treine o classificador.'}), 400
        
    data = request.get_json()
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
            le = ENCODERS[col]
            # Tratar classes não vistas no treino
            if val in le.classes_:
                meta_encoded.append(le.transform([val])[0])
            else:
                meta_encoded.append(le.transform(['OUTROS'])[0])
                
        # Construir vetor de features X
        meta_arr = np.array(meta_encoded).reshape(1, -1)
        X_chunk = np.hstack([chunk_emb, sims, meta_arr])
        
        # 1. Predizer Ação Matriz (Macro Categoria) primeiro
        prob_matriz_arr = CLF_MATRIZ.predict_proba(X_chunk)[0]
        max_prob_matriz_idx = np.argmax(prob_matriz_arr)
        pred_matriz = CLF_MATRIZ.classes_[max_prob_matriz_idx]
        conf_matriz = float(prob_matriz_arr[max_prob_matriz_idx])
        
        # 2. Obter as microclasses válidas para esta macroclasse
        valid_micros = MACRO_TO_MICROS_MAP.get(pred_matriz, [])
        
        prob_derivada_arr = CLF_DERIVADA.predict_proba(X_chunk)[0]
        
        if valid_micros:
            # Encontrar os índices das microclasses válidas na lista de classes do modelo
            valid_indices = []
            valid_class_names = []
            for i, class_name in enumerate(CLF_DERIVADA.classes_):
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
                pred_derivada = CLF_DERIVADA.classes_[max_prob_idx]
                conf_derivada = float(prob_derivada_arr[max_prob_idx])
        else:
            # Caso padrão de fallback
            max_prob_idx = np.argmax(prob_derivada_arr)
            pred_derivada = CLF_DERIVADA.classes_[max_prob_idx]
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

def background_training_pipeline():
    global TRAINING_STATUS, DATASET, CLF_DERIVADA, CLF_MATRIZ, ENCODERS
    TRAINING_STATUS = "Training"
    try:
        # Importando aqui para evitar dependência circular
        from ingestion.ingestion_manager import ingest_dataset
        from preprocessing.text_preprocessor import preprocess_and_chunk_dataset
        from embeddings.embedding_generator import process_embeddings_and_similarities
        
        logging.info("Iniciando pipeline de retreinamento completo em background...")
        
        # Executar ETL
        ingest_dataset("PLANILHA AGRARIO 2024  (3).xlsx", "DATALUTA MOV_AGRARIO_2024-20260525T235037Z-3-001.zip")
        # Chunking
        preprocess_and_chunk_dataset("data/processed/dataset_processado.csv")
        # Embeddings e similaridades
        process_embeddings_and_similarities("data/processed/dataset_chunked.csv")
        # Treinamento
        trainer = ModelTrainer("data/processed/dataset_with_similarities.csv", "data/processed/chunk_embeddings.npy")
        stats = trainer.train_and_evaluate()
        
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
    if TRAINING_STATUS == "Training":
        return jsonify({'status': 'running', 'message': 'O pipeline de treinamento já está em execução no momento.'})
        
    thread = Thread(target=background_training_pipeline)
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
    if DATASET is None:
        return jsonify([])
    try:
        # Group by unique news code
        unique_news = DATASET.drop_duplicates(subset=['codigo_noticia']).copy()
        unique_news = unique_news.fillna('N.I')
        
        news_list = []
        for idx, row in unique_news.iterrows():
            news_list.append({
                'codigo_noticia': str(row.get('codigo_noticia', '')).strip(),
                'titulo_noticia': str(row.get('titulo_noticia', '')).strip(),
                'estado': str(row.get('estado', '')).strip(),
                'nome_movimento': str(row.get('nome_movimento', '')).strip(),
                'pauta_acao': str(row.get('pauta_acao', '')).strip()
            })
        return jsonify(news_list)
    except Exception as e:
        logging.error(f"Erro ao listar noticias: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/news/<news_code>')
def get_news_detail(news_code):
    """Returns the full text and exact metadata of a news article."""
    try:
        processed_csv = "data/processed/dataset_processado.csv"
        if not os.path.exists(processed_csv):
            return jsonify({'error': 'Arquivo de dados processados ausente.'}), 404
            
        df_proc = pd.read_csv(processed_csv)
        # Find news
        row = df_proc[df_proc['Código da notícia 2024'].astype(str).str.strip() == str(news_code).strip()]
        
        if not row.empty:
            text = row.iloc[0].get('texto_noticia', '')
            title = row.iloc[0].get('Título da notícia', '')
            estado = row.iloc[0].get('Estado', 'N.I')
            pauta = row.iloc[0].get('Pauta da ação', 'N.I')
            movimento = row.iloc[0].get('Nome do movimento', 'N.I')
            
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
    try:
        zip_path = "DATALUTA MOV_AGRARIO_2024-20260525T235037Z-3-001.zip"
        if not os.path.exists(zip_path):
            return "Arquivo ZIP de notícias não encontrado.", 404
            
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

if __name__ == '__main__':
    load_resources()
    app.run(debug=True, use_reloader=False, host='127.0.0.1', port=5000)

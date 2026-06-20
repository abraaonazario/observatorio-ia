import os
import re
import spacy
import unicodedata
import pandas as pd
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SemanticChunker:
    def __init__(self, chunk_size=350, overlap=100):
        self.chunk_size = chunk_size
        self.overlap = overlap
        logging.info("Carregando modelo spaCy pt_core_news_lg...")
        try:
            self.nlp = spacy.load("pt_core_news_lg")
        except OSError:
            logging.warning("Modelo pt_core_news_lg nao encontrado, tentando pt_core_news_sm...")
            self.nlp = spacy.load("pt_core_news_sm")
        logging.info("Modelo spaCy carregado com sucesso.")

    def clean_text(self, text):
        """Cleans and normalizes unicode, whitespace and layout noise."""
        if not text or not isinstance(text, str):
            return ""
        # Normalização unicode
        text = unicodedata.normalize("NFKC", text)
        
        # Remover menus comuns de sites que poluem o pdf
        text = re.sub(r'(?i)(Versão digital|Buscar Menu Geral|Esportes Entretenimento|Polícia Política|ELEIÇÕES \d{4}).*?(?=\n|\.)', ' ', text)
        
        # Remover URLs residuais
        text = re.sub(r'https?://[^\s]+', ' ', text)
        
        # Remover artefatos de codificação de PDF como (cid:0), (cid:1), (cid:10), etc.
        text = re.sub(r'\(cid:\d+\)', ' ', text)
        
        # Remover ruídos comuns de PDF e hifenação de quebras de linha
        # Palavras com hífen divididas em duas linhas: "rea-\n lizaram" -> "realizaram"
        text = re.sub(r'-\s*\n\s*', '', text)
        # Palavras quebradas sem hífen: "con \n taram" -> "contaram"
        text = re.sub(r'([a-zçãõáéíóú])\s*\n\s*([a-zçãõáéíóú])', r'\1\2', text)
        
        # Substituir múltiplas quebras de linha e espaços por um único espaço
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def split_into_semantic_chunks(self, text):
        """Splits text into chunks at sentence boundaries using spaCy, trying to respect chunk_size."""
        cleaned = self.clean_text(text)
        if not cleaned:
            return []
            
        doc = self.nlp(cleaned)
        sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 3]
        
        chunks = []
        current_chunk = []
        current_len = 0
        
        for sentence in sentences:
            sent_len = len(sentence)
            # Se a frase sozinha ja for muito longa, adiciona o chunk atual se houver e a frase vira um chunk
            if sent_len >= self.chunk_size:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = []
                    current_len = 0
                chunks.append(sentence)
                continue
                
            if current_len + sent_len + 1 > self.chunk_size:
                chunks.append(" ".join(current_chunk))
                # Cria overlap: mantém a última frase do chunk anterior para preservar o contexto
                # O limite agora permite frases normais (< 250 chars) fazerem overlap tranquilamente
                if len(current_chunk) >= 1 and len(current_chunk[-1]) <= self.chunk_size // 2:
                    current_chunk = [current_chunk[-1], sentence]
                    current_len = len(current_chunk[0]) + sent_len + 1
                else:
                    current_chunk = [sentence]
                    current_len = sent_len
            else:
                current_chunk.append(sentence)
                current_len += sent_len + 1
                
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        return chunks

def preprocess_and_chunk_dataset(dataset_csv_path, output_dir="data/processed"):
    """Loads the ingested dataset, cleans texts, segments them into semantic chunks, and saves the chunked dataset."""
    os.makedirs(output_dir, exist_ok=True)
    
    logging.info(f"Lendo dataset para preprocessamento: {dataset_csv_path}")
    df = pd.read_csv(dataset_csv_path)
    
    chunker = SemanticChunker(chunk_size=350, overlap=100)
    
    chunked_records = []
    
    def find_col(row_index, keywords):
        for col in row_index:
            col_lower = unicodedata.normalize('NFKD', str(col)).encode('ASCII', 'ignore').decode('utf-8').lower()
            if any(kw in col_lower for kw in keywords):
                return col
        return None
# Incluir um proxy para filtra
# Focar  mais na acurácia para limpar os dados 
#processo tirar texto do PDF, gerar um novo PDF limpo
# #  
    logging.info("Iniciando quebra semântica das notícias em chunks...")
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        col_code = find_col(row.index, ['noticia', 'notícia', '2024'])
        if not col_code:
            col_code = find_col(row.index, ['codigo', 'código'])
        col_title = find_col(row.index, ['titulo'])
        col_state = find_col(row.index, ['estado', 'uf'])
        col_city = find_col(row.index, ['municipio', 'cidade'])
        col_matriz_derivada = find_col(row.index, ['matriz e', 'matriz_derivada'])
        col_derivada = find_col(row.index, ['derivada'])
        col_purpose = find_col(row.index, ['finalidade'])
        col_pauta = find_col(row.index, ['pauta'])
        col_movement = find_col(row.index, ['movimento'])
        col_date = find_col(row.index, ['data'])
        
        news_code = str(row.get(col_code, '')) if col_code else ''
        title = str(row.get(col_title, '')) if col_title else ''
        state = str(row.get(col_state, '')) if col_state else ''
        city = str(row.get(col_city, '')) if col_city else ''
        action_matriz_derivada = str(row.get(col_matriz_derivada, '')) if col_matriz_derivada else ''
        action_derivada = str(row.get(col_derivada, '')) if col_derivada else ''
        purpose = str(row.get(col_purpose, '')) if col_purpose else ''
        pauta = str(row.get(col_pauta, '')) if col_pauta else ''
        movement = str(row.get(col_movement, '')) if col_movement else 'N.I'
        date = str(row.get(col_date, '')) if col_date else ''
        
        text = row.get('texto_noticia', '')
        url_noticia = row.get('url_noticia', '')
        mes_pasta = row.get('mes_pasta', 'N.I')
        
        if not movement or pd.isna(movement) or movement.strip() == '':
            movement = 'N.I'
        elif isinstance(movement, str):
            movement = movement.strip()
            
        if movement == 'Não Consta na Listagem':
            custom_mov = row.get('Cadastrar movimento não listado', '')
            if isinstance(custom_mov, str) and custom_mov.strip() and not pd.isna(custom_mov):
                movement = custom_mov.strip()
        
        # Se não houver texto extraído do PDF, usamos o título da notícia e a pauta como conteúdo
        content_to_chunk = text if (isinstance(text, str) and len(text.strip()) > 50) else f"{title}. Pauta: {pauta}."
        
        chunks = chunker.split_into_semantic_chunks(content_to_chunk)
        for c_idx, chunk in enumerate(chunks):
            chunked_records.append({
                'id_chunk': f"{news_code}_c{c_idx}",
                'codigo_noticia': news_code,
                'titulo_noticia': title,
                'chunk_texto': chunk,
                'estado': state,
                'municipio': city,
                'acao_matriz_derivada': action_matriz_derivada,
                'acao_derivada': action_derivada,
                'finalidade_acao': purpose,
                'pauta_acao': pauta,
                'nome_movimento': movement,
                'data_noticia': date,
                'mes_pasta': mes_pasta,
                'url_noticia': url_noticia
            })
            
    chunked_df = pd.DataFrame(chunked_records)
    logging.info(f"Gerados {len(chunked_df)} chunks semânticos a partir de {len(df)} notícias.")
    
    output_csv = os.path.join(output_dir, "dataset_chunked.csv")
    chunked_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    logging.info(f"Dataset chunked salvo em: {output_csv}")
    
    return chunked_df

if __name__ == "__main__":
    preprocess_and_chunk_dataset("data/processed/dataset_processado.csv")

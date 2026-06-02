import os
import re
import spacy
import unicodedata
import pandas as pd
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SemanticChunker:
    def __init__(self, chunk_size=500, overlap=50):
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
        # Remover ruídos comuns de PDF e hifenação de quebras de linha
        text = re.sub(r'-\n\s*', '', text)
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
                # Cria overlap: mantém a última frase do chunk anterior se ela couber no overlap
                if len(current_chunk) > 1 and len(current_chunk[-1]) <= self.overlap:
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
    
    chunker = SemanticChunker(chunk_size=500, overlap=50)
    
    chunked_records = []
    
    logging.info("Iniciando quebra semântica das notícias em chunks...")
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        news_code = row.get('C\u00f3digo da not\u00edcia 2024', '')
        title = row.get('T\u00edtulo da not\u00edcia', '')
        text = row.get('texto_noticia', '')
        
        # Obter metadados relevantes
        state = row.get('Estado', '')
        city = row.get('Munic\u00edpio', '')
        action_matriz_derivada = row.get('A\u00e7\u00e3o Matriz e A\u00e7\u00e3o derivada', '')
        action_derivada = row.get('A\u00e7\u00e3o derivada', '')
        purpose = row.get('Finalidade da a\u00e7ot', '')
        pauta = row.get('Pauta da a\u00e7\u00e3o', '')
        movement = row.get('Nome do movimento', '')
        date = row.get('Data da not\u00edcia', '')
        
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
                'data_noticia': date
            })
            
    chunked_df = pd.DataFrame(chunked_records)
    logging.info(f"Gerados {len(chunked_df)} chunks semânticos a partir de {len(df)} notícias.")
    
    output_csv = os.path.join(output_dir, "dataset_chunked.csv")
    chunked_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    logging.info(f"Dataset chunked salvo em: {output_csv}")
    
    return chunked_df

if __name__ == "__main__":
    preprocess_and_chunk_dataset("data/processed/dataset_processado.csv")

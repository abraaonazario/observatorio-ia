import os
import zipfile
import pandas as pd
import pdfplumber
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_pdf_text_from_zip(zip_file_path, pdf_inner_path):
    """Extracts text from a PDF file located inside a ZIP archive without extracting the ZIP itself."""
    try:
        with zipfile.ZipFile(zip_file_path) as z:
            with z.open(pdf_inner_path) as f:
                with pdfplumber.open(f) as pdf:
                    text = ""
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    return text.strip()
    except Exception as e:
        logging.error(f"Erro ao extrair texto do PDF {pdf_inner_path}: {e}")
        return None

def ingest_dataset(excel_path, zip_path, output_dir="data/processed"):
    """Reads the Excel spreadsheet and matches each row to its PDF in the ZIP to extract the text."""
    os.makedirs(output_dir, exist_ok=True)
    
    logging.info(f"Lendo planilha: {excel_path}")
    df = pd.read_excel(excel_path)
    
    # Normalizando nomes de colunas (removendo acentos e caracteres estranhos para facilitar manipulação)
    df.columns = [col.strip() for col in df.columns]
    
    logging.info(f"Encontradas {len(df)} linhas na planilha.")
    
    logging.info("Mapeando arquivos do arquivo ZIP...")
    with zipfile.ZipFile(zip_path) as z:
        zip_files = z.namelist()
    
    # Criar um mapeamento de código de notícia (sem extensão e sem diretório) para o caminho completo do zip
    # Exemplo: '220824AGR_D' -> 'DATALUTA MOV_AGRARIO_2024/8. AGOSTO/220824AGR_D.pdf'
    pdf_mapping = {}
    for filepath in zip_files:
        if filepath.endswith('.pdf'):
            filename = os.path.basename(filepath)
            code = os.path.splitext(filename)[0]
            pdf_mapping[code] = filepath
            
    logging.info(f"Mapeados {len(pdf_mapping)} PDFs no arquivo ZIP.")
    
    extracted_texts = []
    matches = 0
    
    logging.info("Iniciando extração de textos dos PDFs...")
    # Usaremos apenas as colunas que importam para o nosso pipeline de ML
    # Código da notícia 2024, Título da notícia, Estado, Município, Ação Matriz e Ação derivada, Ação derivada, Pauta da ação, Nome do movimento
    # E vamos adicionar o texto extraído
    
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        news_code = str(row.get('C\u00f3digo da not\u00edcia 2024', '')).strip()
        
        pdf_text = None
        if news_code and news_code in pdf_mapping:
            pdf_inner_path = pdf_mapping[news_code]
            pdf_text = extract_pdf_text_from_zip(zip_path, pdf_inner_path)
            if pdf_text:
                matches += 1
        
        extracted_texts.append(pdf_text if pdf_text else "")
        
    df['texto_noticia'] = extracted_texts
    logging.info(f"Extração concluída. Casamento de dados bem-sucedido para {matches}/{len(df)} registros.")
    
    # Salvar o dataset resultante
    output_csv = os.path.join(output_dir, "dataset_processado.csv")
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    logging.info(f"Dataset processado salvo em: {output_csv}")
    
    # Salvar estatísticas úteis
    with open(os.path.join(output_dir, "ingest_stats.txt"), "w", encoding="utf-8") as f:
        f.write(f"Total registros: {len(df)}\n")
        f.write(f"Registros com PDF correspondente e extraído: {matches}\n")
        f.write(f"Taxa de sucesso: {(matches / len(df)) * 100:.2f}%\n")
        
    return df

if __name__ == "__main__":
    # Caminhos relativos a partir da raiz do projeto
    excel_file = "PLANILHA AGRARIO 2024  (3).xlsx"
    zip_file = "DATALUTA MOV_AGRARIO_2024-20260525T235037Z-3-001.zip"
    
    ingest_dataset(excel_file, zip_file)

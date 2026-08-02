import os
import zipfile
import pandas as pd
import pdfplumber
import logging
import re
import glob
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_category_files(category, root_dir="."):
    raw_dir = os.path.join(root_dir, "data", "raw", category)
    excel_files = glob.glob(os.path.join(raw_dir, "*.xlsx"))
    zip_files = glob.glob(os.path.join(raw_dir, "*.zip"))
    return (excel_files[0] if excel_files else None), (zip_files[0] if zip_files else None)

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
                    cleaned_text = text.replace('\x00', '').strip()
                    
                    # Heurística: Sensor de Alarme de OCR (Item 1)
                    if len(pdf.pages) > 0 and len(cleaned_text) < 50:
                        logging.warning(f"⚠️ POSSÍVEL PDF IMAGEM OU SCANEADO - REQUER OCR FUTURO: {pdf_inner_path} (Texto muito curto: {len(cleaned_text)} chars)")
                        
                    return cleaned_text
    except Exception as e:
        logging.error(f"Erro ao extrair texto do PDF {pdf_inner_path}: {e}")
        return None

# Mapeamento dos números de mês para nome por extenso (para inferir do nome do arquivo)
_MONTH_MAP = {
    '01': '1. JANEIRO', '02': '2. FEVEREIRO', '03': '3. MARÇO',
    '04': '4. ABRIL', '05': '5. MAIO', '06': '6. JUNHO',
    '07': '7. JULHO', '08': '8. AGOSTO', '09': '9. SETEMBRO',
    '10': '10. OUTUBRO', '11': '11. NOVEMBRO', '12': '12. DEZEMBRO'
}

def _infer_month_from_filename(filename):
    """Tenta inferir o mês a partir do nome do arquivo (ex: FLO150323A.pdf -> '3. MARÇO')."""
    # Padrão: 3 letras + DDMMYY + letra(s)  (ex: FLO150323A ou AGR220824D)
    m = re.search(r'[A-Z]{2,4}(\d{2})(\d{2})(\d{2})', filename.upper())
    if m:
        month_num = m.group(2)  # DDMMYY → grupo 2 é o mês
        return _MONTH_MAP.get(month_num, 'N.I')
    return 'N.I'

def ingest_from_pdfs_only(raw_dir, output_dir, progress_callback=None):
    """
    Cria um dataset a partir de PDFs soltos (sem planilha Excel).
    Cada PDF torna-se uma linha do dataset; o código da notícia é o nome do arquivo (sem extensão).
    O mês é inferido do nome do arquivo quando possível.
    """
    os.makedirs(output_dir, exist_ok=True)
    pdf_files = sorted(glob.glob(os.path.join(raw_dir, "**", "*.pdf"), recursive=True))
    
    if not pdf_files:
        logging.warning(f"Nenhum PDF encontrado em {raw_dir}")
        return None

    logging.info(f"Modo PDF-only: encontrados {len(pdf_files)} PDFs em {raw_dir}")
    
    rows = []
    for i, pdf_path in enumerate(tqdm(pdf_files, desc="Extraindo PDFs")):
        filename = os.path.basename(pdf_path)
        codigo = os.path.splitext(filename)[0]
        mes_pasta = _infer_month_from_filename(filename)
        
        text = ""
        url = ""
        titulo = codigo
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text += t + "\n"
            text = text.replace('\x00', '').strip()
            
            # Heurística: Sensor de Alarme de OCR (Item 1)
            if len(text) < 50:
                logging.warning(f"⚠️ POSSÍVEL PDF IMAGEM OU SCANEADO - REQUER OCR FUTURO: {filename} (Texto muito curto: {len(text)} chars)")
                
            # Título = primeira linha não-vazia do PDF
            for line in text.splitlines():
                if line.strip():
                    titulo = line.strip()[:120]
                    break
            # Extrair primeira URL
            url_match = re.search(r'https?://[^\s]+', text)
            if url_match:
                url = url_match.group(0).strip()
                text = text.replace(url, ' ')
        except Exception as e:
            logging.warning(f"Erro ao ler {filename}: {e}")

        rows.append({
            'codigo_noticia': codigo,
            'titulo_noticia': titulo,
            'estado': 'N.I',
            'municipio': 'N.I',
            'nome_movimento': 'N.I',
            'pauta_acao': 'N.I',
            'acao_derivada': 'N.I',
            'acao_matriz_derivada': 'N.I',
            'texto_noticia': text,
            'mes_pasta': mes_pasta,
            'url_noticia': url,
        })
        
        if progress_callback:
            progress_callback(i + 1, len(pdf_files))

    df = pd.DataFrame(rows)
    output_csv = os.path.join(output_dir, "dataset_processado.csv")
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    logging.info(f"Dataset PDF-only salvo em: {output_csv} ({len(df)} registros)")

    with open(os.path.join(output_dir, "ingest_stats.txt"), "w", encoding="utf-8") as f:
        f.write(f"Modo: PDF-only (sem planilha Excel)\n")
        f.write(f"Total de PDFs processados: {len(df)}\n")
        
    return df

def ingest_dataset(excel_path, zip_path, output_dir="data/processed", progress_callback=None):
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
    extracted_months = []
    extracted_urls = []
    matches = 0
    
    logging.info("Iniciando extração de textos dos PDFs...")
    # Usaremos apenas as colunas que importam para o nosso pipeline de ML
    # Código da notícia 2024, Título da notícia, Estado, Município, Ação Matriz e Ação derivada, Ação derivada, Pauta da ação, Nome do movimento
    # E vamos adicionar o texto extraído
    
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        news_code_col = None
        for col in row.index:
            col_lower = col.lower()
            if 'código da' in col_lower or 'codigo da' in col_lower or 'código da notícia' in col_lower or 'codigo_noticia' in col_lower:
                news_code_col = col
                break
        if not news_code_col:
            for col in row.index:
                col_lower = col.lower()
                if ('código' in col_lower or 'codigo' in col_lower) and 'único' not in col_lower and 'unico' not in col_lower:
                    news_code_col = col
                    break
        
        news_code = str(row.get(news_code_col, '')) if news_code_col else ''
        news_code = news_code.strip()
        
        pdf_text = None
        pdf_month = "N.I"
        pdf_url = ""
        if news_code and news_code in pdf_mapping:
            pdf_inner_path = pdf_mapping[news_code]
            
            # Extrair a pasta do mês (ex: '11. NOVEMBRO')
            parts = pdf_inner_path.split('/')
            if len(parts) > 1:
                pdf_month = parts[1].strip()
                
            pdf_text = extract_pdf_text_from_zip(zip_path, pdf_inner_path)
            if pdf_text:
                matches += 1
                
                # Extrair a primeira URL e remover do texto bruto
                url_match = re.search(r'https?://[^\s]+', pdf_text)
                if url_match:
                    pdf_url = url_match.group(0).strip()
                    # Apagar a URL do texto
                    pdf_text = pdf_text.replace(pdf_url, ' ')
        
        extracted_texts.append(pdf_text if pdf_text else "")
        extracted_months.append(pdf_month)
        extracted_urls.append(pdf_url)
        
        if progress_callback:
            progress_callback(idx + 1, len(df))
        
    df['texto_noticia'] = extracted_texts
    df['mes_pasta'] = extracted_months
    df['url_noticia'] = extracted_urls
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

def ingest_from_excel_only(excel_path, output_dir="data/processed", progress_callback=None):
    """Lê a planilha Excel e cria o texto sintético (já que não há PDFs)."""
    os.makedirs(output_dir, exist_ok=True)
    
    logging.info(f"Lendo planilha (Modo Excel-Only): {excel_path}")
    df = pd.read_excel(excel_path)
    df.columns = [col.strip() for col in df.columns]
    
    extracted_texts = []
    extracted_months = []
    extracted_urls = []
    
    logging.info("Sintetizando textos a partir das colunas da planilha...")
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        # Tentar achar título e pauta para formar o texto
        title_col, pauta_col, date_col = None, None, None
        for col in row.index:
            col_lower = col.lower()
            if 'título' in col_lower or 'titulo' in col_lower: title_col = col
            if 'pauta' in col_lower: pauta_col = col
            if 'data' in col_lower and 'notícia' not in col_lower and 'noticia' not in col_lower: date_col = col
            
        titulo = str(row.get(title_col, '')) if title_col else ''
        pauta = str(row.get(pauta_col, '')) if pauta_col else ''
        
        texto_sintetico = f"{titulo}. {pauta}.".strip()
        extracted_texts.append(texto_sintetico)
        
        # Extrair o mês da data
        data_val = str(row.get(date_col, '')) if date_col else ''
        mes_pasta = "N.I"
        if data_val and data_val.lower() != 'nan':
            # Tentar parsear data, ex: 2024-03-15 00:00:00 -> Mês 3
            try:
                dt = pd.to_datetime(data_val, errors='coerce')
                if not pd.isna(dt):
                    mes_nome = {1:'Janeiro', 2:'Fevereiro', 3:'Março', 4:'Abril', 5:'Maio', 6:'Junho', 7:'Julho', 8:'Agosto', 9:'Setembro', 10:'Outubro', 11:'Novembro', 12:'Dezembro'}.get(dt.month, 'N.I')
                    mes_pasta = f"{dt.month}. {mes_nome.upper()}"
            except:
                pass
        extracted_months.append(mes_pasta)
        extracted_urls.append("") # Sem URL para extrair
        
        if progress_callback:
            progress_callback(idx + 1, len(df))
            
    df['texto_noticia'] = extracted_texts
    df['mes_pasta'] = extracted_months
    df['url_noticia'] = extracted_urls
    
    output_csv = os.path.join(output_dir, "dataset_processado.csv")
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    logging.info(f"Dataset Excel-Only salvo em: {output_csv} ({len(df)} registros)")
    
    with open(os.path.join(output_dir, "ingest_stats.txt"), "w", encoding="utf-8") as f:
        f.write(f"Modo: Excel-only (texto sintético)\n")
        f.write(f"Total de registros processados: {len(df)}\n")
        
    return df

if __name__ == "__main__":
    # Caminhos relativos a partir da raiz do projeto
    excel_file = "PLANILHA AGRARIO 2024  (3).xlsx"
    zip_file = "DATALUTA MOV_AGRARIO_2024-20260602T191955Z-3-001.zip"
    
    ingest_dataset(excel_file, zip_file)


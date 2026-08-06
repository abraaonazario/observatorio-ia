import pandas as pd
import re
import os

def ingest():
    url = "https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_de_Mato_Grosso_por_popula%C3%A7%C3%A3o"
    print(f"Buscando dados de: {url}")
    
    import requests
    from bs4 import BeautifulSoup
    import io
    
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    response.encoding = 'utf-8'
    
    try:
        tables = pd.read_html(io.StringIO(response.text))
    except Exception as e:
        print(f"Erro no read_html: {e}")
        return
        
    print(f"Tabelas encontradas: {len(tables)}")
    if len(tables) > 0:
        print("Head da Tabela 0:")
        print(tables[0].head(3))
        
        # Vamos apenas assumir que a Tabela 0 é a correta
        target_table = tables[0]
        # Se as colunas estiverem na linha 0
        if str(target_table.iloc[0, 1]).startswith('Munic'):
            target_table.columns = target_table.iloc[0]
            target_table = target_table[1:]
    else:
        target_table = None
            
    if target_table is None:
        print("Erro: Tabela não encontrada.")
        return
        
    df = target_table
            
    if df is None:
        df = tables[0] # Fallback
        
    # Limpeza básica nas colunas (removendo MultiIndex se houver)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(-1)
        
    df.columns = [str(c).strip() for c in df.columns]
    
    # Salvando raw (Bronze)
    os.makedirs('data/bronze', exist_ok=True)
    df.to_csv('data/bronze/municipios_populacao_raw.csv', index=False, encoding='utf-8')
    print("Camada Bronze atualizada: data/bronze/municipios_populacao_raw.csv")
    
    df.columns = df.iloc[0]
    df = df[1:].copy()
    
    # Colunas agora são da linha 0. Ex: 'Pos.', 'Município', 'População'
    # Como os nomes podem variar ou ter problemas de encoding, vamos usar índices!
    # 0 = Pos, 1 = Município, 2 = População
    
    print("Colunas encontradas:", list(df.columns))
    print("Amostra dos dados:")
    print(df.head())
    
    # Processando (Camada Silver)
    def clean_name(name):
        return re.sub(r'\[.*?\]', '', str(name)).strip()
        
    def clean_pop(pop):
        pop_str = re.sub(r'\D', '', str(pop))
        return int(pop_str) if pop_str else 0
        
    df_clean = pd.DataFrame()
    # Pega a terceira coluna (índice 2) para Cidade e a quinta (índice 4) para População
    df_clean['municipio'] = df.iloc[:, 2].fillna('').apply(clean_name)
    df_clean['populacao'] = df.iloc[:, 4].fillna('0').apply(clean_pop)
    
    # Limpando linhas de subcabeçalhos (Ex: "Mais de 500.000 habitantes")
    df_clean = df_clean[~df_clean['municipio'].str.contains('habitante', case=False, na=False)]
    df_clean = df_clean[df_clean['municipio'] != '']
    df_clean = df_clean[df_clean['populacao'] > 0]
    
    # Remove eventuais totais que possam estar na tabela (Ex: "Total do Estado")
    df_clean = df_clean[df_clean['municipio'].str.lower() != 'total']
    df_clean = df_clean[~df_clean['municipio'].str.contains('Mato Grosso', case=False)]
    
    df_clean = df_clean.sort_values('populacao', ascending=False)
    
    os.makedirs('data/silver', exist_ok=True)
    df_clean.to_csv('data/silver/municipios_populacao_clean.csv', index=False, encoding='utf-8')
    print("Camada Silver atualizada: data/silver/municipios_populacao_clean.csv")
    
    total_mun = len(df_clean)
    total_pop = df_clean['populacao'].sum()
    
    print(f"\n=======================")
    print(f"Total de Municípios: {total_mun}")
    print(f"População Total: {total_pop}")
    print(f"=======================\n")
    
    print("Top 5 Municípios:")
    print(df_clean.head(5).to_string(index=False))

if __name__ == "__main__":
    ingest()


# coding: utf-8
import pandas as pd
df = pd.read_csv('data/processed/agrario/dataset_processado.csv')
col_code = [c for c in df.columns if '2024' in c][0]
col_title = [c for c in df.columns if 'tulo da' in c.lower() or 'titulo' in c.lower()][0]
col_fonte = [c for c in df.columns if 'fonte' in c.lower()][0]

for code in ['010924AGR_B', '240424AGR_C']:
    rows = df[df[col_code].astype(str) == code]
    if rows.empty:
        continue
    row = rows.iloc[0]
    titulo = str(row.get(col_title, ''))
    fonte = str(row.get(col_fonte, ''))
    texto = str(row.get('texto_noticia', ''))
    print('---', code, '---')
    print('TITLE:', titulo.encode('ascii', 'ignore').decode())
    print('SOURCE:', fonte.encode('ascii', 'ignore').decode())
    print('CHARS:', len(texto))
    print('TEXT START:', texto[:500].replace('\n', ' ').encode('ascii', 'ignore').decode())
    print()


import pandas as pd
from embeddings.embedding_generator import ACAO_DERIVADA_ENRIQUECIDA

df = pd.read_csv('todos_os_chunks_texto.csv')
df_keys = set(df['acao_derivada'].dropna().unique())
dict_keys = set(ACAO_DERIVADA_ENRIQUECIDA.keys())

missing = df_keys - dict_keys
unused = dict_keys - df_keys

print(f"Total df_keys: {len(df_keys)}")
print(f"Total dict_keys: {len(dict_keys)}")
print(f"Missing in dict: {missing}")
print(f"Unused in dict: {unused}")

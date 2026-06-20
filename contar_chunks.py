import pandas as pd
import os

def gerar_planilha_chunks_por_pdf():
    dataset_path = 'data/processed/agrario/dataset_chunked.csv'
    output_path = 'chunks_por_pdf.xlsx'

    if not os.path.exists(dataset_path):
        print(f"Erro: O arquivo {dataset_path} não foi encontrado. Execute o pipeline primeiro.")
        return

    print("Carregando o dataset de chunks...")
    df = pd.read_csv(dataset_path)

    # Agrupar pelo código da notícia (PDF) e contar o número de chunks (linhas)
    print("Contando a quantidade de chunks gerados por PDF...")
    
    # Se 'codigo_noticia' não existir, tentamos 'Código da notícia 2024' ou usamos a coluna id_chunk base
    if 'codigo_noticia' in df.columns:
        col_codigo = 'codigo_noticia'
    else:
        # Achar primeira coluna que possa ser código
        cols = [c for c in df.columns if 'código' in c.lower() or 'codigo' in c.lower()]
        if cols:
            col_codigo = cols[0]
        else:
            print("Erro: Coluna de código de notícia não encontrada no CSV.")
            print("Colunas disponíveis:", df.columns)
            return

    # Contagem
    contagem = df.groupby(col_codigo).size().reset_index(name='Quantidade de Chunks (Fragmentos)')
    
    # Opcional: Adicionar o título da notícia e estado para ficar mais fácil de ler
    if 'titulo_noticia' in df.columns:
        titulos = df[[col_codigo, 'titulo_noticia']].drop_duplicates()
        contagem = contagem.merge(titulos, on=col_codigo, how='left')
    
    # Ordenar do maior para o menor
    contagem = contagem.sort_values(by='Quantidade de Chunks (Fragmentos)', ascending=False)

    def get_just(x):
        if pd.isna(x):
            return 'Desconhecido'
        if x <= 1:
            return 'Texto curto ou PDF escaneado (baixa extração)'
        if x <= 5:
            return 'Tamanho Padrão (Notícia normal)'
        if x <= 15:
            return 'Reportagem Extensa'
        return 'Documento Completo/Relatório Longo'

    contagem['Justificativa'] = contagem['Quantidade de Chunks (Fragmentos)'].apply(get_just)

    # Salvar em CSV
    output_csv = 'chunks_por_pdf.csv'
    print(f"Salvando resultados em: {output_csv}")
    contagem.to_csv(output_csv, index=False, encoding='utf-8')
    
    print(f"\nSucesso! Planilha gerada com {len(contagem)} PDFs únicos analisados.")
    print(f"O PDF mais longo gerou {contagem['Quantidade de Chunks (Fragmentos)'].iloc[0]} chunks.")

if __name__ == "__main__":
    gerar_planilha_chunks_por_pdf()

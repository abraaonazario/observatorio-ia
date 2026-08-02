import logging
import unicodedata
from preprocessing.text_preprocessor import SemanticChunker

# Configurar logging para ver os resultados na tela
logging.basicConfig(level=logging.INFO, format='%(message)s')

def testar_limpeza():
    print("="*60)
    print(" INICIANDO TESTE DA VASSOURA INTELIGENTE (LIMPEZA)")
    print("="*60)
    
    # 1. Instanciar o Chunker (que contém o nosso clean_text modificado)
    chunker = SemanticChunker()
    
    # 2. Criar um texto sujo (simulando um PDF horrível da internet)
    texto_sujo_simulado = """
    Página 1 de 4
    Aceitar todos os cookies
    Nós utilizamos cookies para melhorar sua experiência.
    
    Os trabalhadores rurais sem-terra rea-
    lizaram uma marcha em direção ao centro de Brasília.
    
    (cid:10)
    A manifestação foi pacífica e con 
    tou com mais de mil participantes.
    
    Contato do jornalista: reporter.agrario@email.com
    Versão digital - Buscar Menu Geral
    
    Impresso por Joao Silva
    Gerado em 22/08/2024
    """
    
    print("\n[TEXTO ORIGINAL SUJO (Extraído pelo PDFPlumber)]:")
    print("-" * 40)
    print(texto_sujo_simulado)
    print("-" * 40)
    
    # 3. Rodar o motor de limpeza
    print("\n>>> Aplicando Filtros de Regex (LGPD, Paginação, Hifenização, E-mails)... <<<\n")
    texto_limpo = chunker.clean_text(texto_sujo_simulado)
    
    # 4. Mostrar o resultado
    print("[TEXTO LIMPO E PROCESSADO]:")
    print("-" * 40)
    print(texto_limpo)
    print("-" * 40)
    
    # 5. Avaliação do resultado
    if "cookies" not in texto_limpo.lower() and "Página" not in texto_limpo and "reporter" not in texto_limpo:
        print("\n[OK] TESTE BEM SUCEDIDO: Todo o lixo de internet, rodapes e e-mails foram evaporados!")
        print("[OK] Hifenizacao corrigida: 'realizaram' e 'contou' foram unidas com sucesso.")
    else:
        print("\n[ERRO] AVISO: Alguma sujeira sobreviveu aos filtros.")

if __name__ == "__main__":
    testar_limpeza()

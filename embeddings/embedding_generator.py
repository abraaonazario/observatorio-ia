import os
import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Dicionário de Enriquecimento Semântico das Ações Derivadas em português
#retirar a descrição 
ACAO_DERIVADA_ENRIQUECIDA = {
    'ACAMPAMENTO': 'Formação de acampamento camponês provisório ou estabelecimento de acampados em terras reivindicadas para reforma agrária.',
    'ASSEMBLEIA/PLENÁRIA': 'Reunião de membros de movimentos sociais para tomada de decisões coletivas, plenárias organizativas ou planejamento de ações agrárias.',
    'ASSISTÊNCIA TÉCNICA E EXTENSÃO RURAL': 'Atividades de formação técnica, apoio agrícola, transição agroecológica ou extensão produtiva no campo.',
    'AUDIÊNCIA': 'Encontro formal de representações camponesas com autoridades governamentais, judiciais ou ministeriais para debater conflitos de terra.',
    'AUDIÊNCIA PÚBLICA': 'Reunião pública institucional com debate entre sociedade civil, movimentos populares e poder público sobre demarcação ou conflitos.',
    'BLOQUEIO DE VIAS': 'Trancamento ou interrupção de tráfego em rodovias, estradas ou pontes como forma de protesto e visibilidade de pautas camponesas.',
    'CAMPANHA': 'Campanha institucional, solidária ou informativa promovida por movimentos para conscientização social ou arrecadação de insumos.',
    'CARTA ABERTA': 'Manifestação escrita pública dirigida à sociedade ou às autoridades denunciando violações ou reivindicando direitos agrários.',
    'CIRCUITOS CURTOS DE COMERCIALIZAÇÃO': 'Venda direta do produtor rural ao consumidor, feiras agroecológicas ou canais diretos de comercialização familiar sem intermediários.',
    'CONQUISTA DE INFRAESTRUTURA': 'Obtenção de melhorias estruturais para assentamentos e acampamentos, como energia elétrica, água encanada, estradas ou habitação rural.',
    'CONQUISTA JUDICIAL': 'Decisão favorável da justiça à causa camponesa, demarcação de terras, imissão na posse ou revogação de ordens de despejo.',
    'CRIAÇÃO DE TECNOLOGIAS SOCIAIS': 'Desenvolvimento de técnicas sustentáveis acessíveis para captação de água, biofertilizantes, habitação e manejo camponês.',
    'DEMANDA JUDICIAL': 'Ações judiciais, representações ou petições protocoladas por movimentos e comunidades em litígios de terra ou direitos do campo.',
    'DERROTA JUDICIAL': 'Decisão desfavorável do poder judiciário decretando despejo, reintegração de posse ou suspensão de processos de reforma agrária.',
    'DIREITO DE CONSULTA POPULAR': 'Exercício do direito à consulta livre, prévia e informada de comunidades tradicionais sobre empreendimentos em seus territórios.',
    'DOAÇÃO DE ALIMENTOS': 'Atos de solidariedade camponesa de distribuição de alimentos saudáveis produzidos por assentados e acampados para famílias vulneráveis urbanas.',
    'DOAÇÃO DE PRODUTOS': 'Atos solidários de entrega de mudas, sementes, roupas ou insumos produtivos para comunidades em vulnerabilidade social.',
    'DOCUMENTO DE FORMAÇÃO E INFORMAÇÃO DOS MOVIMENTOS': 'Publicação de cartilhas, circulares, jornais ou notas informativas de caráter educativo e político dos movimentos camponeses.',
    'ENCONTRO': 'Eventos de integração, debates estaduais ou nacionais entre movimentos, apoiadores e comunidades rurais.',
    'ENTREVISTA CONCEDIDA': 'Depoimento ou fala pública de lideranças agrárias para jornais, emissoras de rádio, TV ou canais digitais sobre a conjuntura agrária e conflitos.',
    'FESTIVIDADES CULTURAIS': 'Celebrações coletivas, festas da colheita, comemorações místicas, manifestações artísticas e culturais no campo.',
    'FORMAÇÃO': 'Cursos de formação política, capacitação técnica, agroecologia ou educação do campo promovidos por movimentos sociais.',
    'FÓRUM': 'Espaços amplos e periódicos de articulação entre diversas organizações, movimentos sociais, academia e ONGs sobre a questão agrária.',
    'JORNADAS DE LUTAS': 'Conjunto coordenado de ações, mobilizações de massa, protestos e audiências públicas realizadas em datas ou períodos estratégicos.',
    'MARCHA': 'Caminhada coletiva de longa distância realizada por manifestantes camponeses para visibilizar pautas da reforma agrária e justiça no campo.',
    'MERCADO INSTITUCIONAL': 'Acesso a programas públicos de compras governamentais para venda de alimentos da agricultura familiar, como PAA e PNAE.',
    'MUTIRÃO': 'Trabalho coletivo voluntário entre famílias assentadas ou acampadas para construção de moradias, plantio, colheita ou limpeza comunitária.',
    'NOTA DE DENÚNCIA': 'Comunicado público formal que denuncia violências, ataques de capangas ou policiais, criminalização ou negligência do Estado no campo.',
    'NOTA DE PESAR': 'Manifestação formal de dor e condolências pelo falecimento de lideranças camponesas, ativistas ou camponeses vítimas da violência.',
    'NOTA DE REPÚDIO': 'Manifestação institucional de crítica veemente, repulsa ou oposição relacionada a violência policial, ordens de despejo ou decisões judiciais injustas.',
    'OCUPE': 'Manifestação de acampamento em espaço ou local específico para denúncia de latifúndio ou reivindicação territorial.',
    'OCUPAÇÃO DE CARGOS PÚBLICOS OU CANDIDATURAS': 'Participação direta de quadros dos movimentos agrários em processos eleitorais ou assunção de postos estratégicos em órgãos do Estado.',
    'OCUPAÇÃO DE ESPAÇO PÚBLICO': 'Manifestação pacífica temporária com acampamentos ou vigílias em praças, estradas ou áreas públicas urbanas para pressionar negociações agrárias.',
    'OCUPAÇÃO DE PRÉDIO PRIVADO': 'Ingresso e permanência política de trabalhadores sem-terra em sedes de empresas transnacionais, bancos ou imóveis privados urbanos ou rurais.',
    'OCUPAÇÃO DE PRÉDIO PÚBLICO': 'Ingresso de manifestantes camponeses em repartições do governo (como INCRA, ministérios ou prefeituras) para exigir andamento de pautas agrárias.',
    'OCUPAÇÃO DE TERRA': 'Entrada organizada de famílias sem-terra em latifúndios improdutivos, terras públicas federais ou áreas com crimes ambientais para fins de reforma agrária.',
    'PARTICIPAÇÃO EM AUDIÊNCIA PÚBLICA': 'Presença física e fala de representantes camponeses em sessões públicas do legislativo ou órgãos governamentais debatendo conflitos agrários.',
    'PASSEATA': 'Cortejo ou deslocamento coletivo de protesto pelas ruas de centros urbanos com faixas, cartazes e palavras de ordem da reforma agrária.',
    'PREMIAÇÃO': 'Recebimento de prêmios, menções honrosas ou reconhecimento institucional nacional ou internacional à atuação camponesa, agroecológica e socioambiental.',
    'PRODUÇÃO DE ALIMENTOS SAUDÁVEIS': 'Cultivo de grãos, hortaliças e frutas livres de agrotóxicos, transição agroecológica, segurança alimentar e fortalecimento da agricultura familiar.',
    'PROJETOS TEMÁTICOS': 'Projetos de desenvolvimento agrário, convênios de fomento produtivo, assessoria técnica e projetos de sustentabilidade.',
    'REFLORESTAMENTO': 'Ações de plantio de árvores nativas, recuperação de nascentes, conservação de florestas e preservação da biodiversidade no campo.',
    'RETOMADA': 'Ocupação ou reingresso de povos indígenas, quilombolas ou comunidades tradicionais em suas terras originárias ou territórios ancestrais reivindicados.',
    'REUNIÃO': 'Encontros de planejamento interno entre militantes, reuniões organizativas de base ou círculos de discussão camponesa.',
    'TENTATIVA DE OCUPAÇÃO DE TERRA': 'Ações iniciais de aproximação ou ensaio de entrada organizada de famílias em terras desprovidas de função social, sem consolidação imediata.',
    'VIGÍLIA': 'Ato político de permanência pacífica, orações ou atos de vigília coletiva em locais públicos contra despejos ou por libertação de camponeses presos.',
    'VIOLÊNCIA JURÍDICA': 'Uso distorcido ou arbitrário do aparato legal, inquéritos abusivos, perseguição a ativistas e criminalização judicial de movimentos sociais.',
    '': 'Sem classificação de ação derivada específica ou informação insuficiente nos registros.'
}

# Dicionário de Enriquecimento Semântico das Ações Matrizes (Macroclasses) em português
ACAO_MATRIZ_ENRIQUECIDA = {
    'ARRECADAÇÃO DE RECURSOS OU EXECUÇÃO DE SERVIÇOS': 'Ações voltadas para a coleta de fundos, doações de recursos financeiros, campanhas de arrecadação ou prestação de serviços comunitários e apoio social no campo.',
    'COMERCIALIZAÇÃO': 'Atividades de venda, feiras agrícolas, circuitos curtos de comércio, mercados institucionais e canais de escoamento da produção da agricultura familiar e camponesa.',
    'COMUNICATIVA': 'Ações de comunicação, publicação de notas públicas, manifestos, cartas abertas, comunicados, entrevistas coletivas e divulgação de informações pelos movimentos sociais.',
    'DESLOCAMENTO COLETIVO': 'Marchas, caravanas, caminhadas organizadas e deslocamento em massa de trabalhadores rurais e famílias camponesas em protestos ou mobilizações.',
    'ENCONTRO DE MEDIAÇÃO': 'Reuniões, audiências com órgãos do governo, instâncias de negociação, mediação de conflitos de terra, fóruns e mesas de diálogo institucional.',
    'EVENTOS': 'Encontros organizativos, assembleias, plenárias, cursos de formação política ou técnica, seminários e congressos promovidos pelos movimentos do campo.',
    'FESTIVIDADES, RITOS E LAZER': 'Festas comunitárias, celebrações culturais, atos místicos, comemorações de conquistas, ritos tradicionais e atividades de integração cultural no campo.',
    'INTERSECCIONALIDADE INSTITUCIONAL': 'Participação de lideranças em instâncias estatais, conselhos de políticas públicas, ocupação de cargos públicos, candidaturas eleitorais e articulação com instituições civis.',
    'JUDICIALIZAÇÃO': 'Processos judiciais, petições legais, demandas na justiça, conquistas judiciais favoráveis ou disputas jurídicas envolvendo posse de terras, despejos e reintegrações.',
    'OCUPACAO': 'Ocupações de terras improdutivas, latifúndios, prédios públicos (como sedes do INCRA) ou espaços públicos urbanos e rurais como forma de pressão política.',
    'PRODUÇÃO': 'Atividades produtivas diretas, cultivo agrícola, produção de alimentos saudáveis e agroecológicos, criação de tecnologias sociais e reflorestamento no campo.'
}

class EmbeddingManager:
    def __init__(self, model_name='sentence-transformers/distiluse-base-multilingual-cased-v1', category='agrario'):
        self.model_name = model_name
        self.category = category
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logging.info(f"Carregando modelo de embeddings: {model_name} no dispositivo {device}...")
        self.model = SentenceTransformer(model_name, device=device)
        logging.info("Modelo de embeddings carregado com sucesso.")
        
        if category == 'agrario':
            derivada_dict = ACAO_DERIVADA_ENRIQUECIDA
            matriz_dict = ACAO_MATRIZ_ENRIQUECIDA
        else:
            derivada_dict = {'Ação Indefinida': 'Nenhuma classe definida'}
            matriz_dict = {'Matriz Indefinida': 'Nenhuma matriz definida'}
        
        # Gerar embeddings para as ações derivadas enriquecidas
        self.action_keys = list(derivada_dict.keys())
        self.action_descriptions = list(derivada_dict.values())
        logging.info("Gerando embeddings para as ações derivadas enriquecidas...")
        self.action_embeddings = self.model.encode(self.action_descriptions, show_progress_bar=False)
        
        # Gerar embeddings para as ações matrizes enriquecidas
        self.matriz_keys = list(matriz_dict.keys())
        self.matriz_descriptions = list(matriz_dict.values())
        logging.info("Gerando embeddings para as ações matrizes enriquecidas...")
        self.matriz_embeddings = self.model.encode(self.matriz_descriptions, show_progress_bar=False)
        logging.info("Embeddings das ações gerados com sucesso.")

    def encode_text(self, texts, batch_size=32):
        """Generates embeddings for a list of texts."""
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(texts, batch_size=batch_size, show_progress_bar=True)

    def compute_similarities(self, text_embeddings):
        """Computes cosine similarity between text embeddings and both action and matrix embeddings."""
        sim_derivada = cosine_similarity(text_embeddings, self.action_embeddings)
        sim_matriz = cosine_similarity(text_embeddings, self.matriz_embeddings)
        return np.hstack([sim_derivada, sim_matriz])

def process_embeddings_and_similarities(chunked_csv_path, output_dir="data/processed", category="agrario"):
    """Loads the chunked dataset, generates embeddings for all chunks, computes similarities to actions,
    and saves the enriched dataset containing embeddings and similarity scores.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    logging.info(f"Lendo dataset chunked: {chunked_csv_path}")
    df = pd.read_csv(chunked_csv_path)
    
    # Remover chunks vazios ou inválidos
    df = df.dropna(subset=['chunk_texto'])
    
    emb_manager = EmbeddingManager(category=category)
    
    chunks = df['chunk_texto'].tolist()
    logging.info(f"Gerando embeddings para {len(chunks)} chunks semânticos...")
    chunk_embeddings = emb_manager.encode_text(chunks)
    
    # Calcular similaridades
    logging.info("Calculando similaridade cosseno com as ações (derivada e matriz)...")
    similarities = emb_manager.compute_similarities(chunk_embeddings)
    
    # Adicionar as similaridades derivada como colunas adicionais no dataframe
    num_deriv = len(emb_manager.action_keys)
    for i, action_key in enumerate(emb_manager.action_keys):
        col_name = f"sim_score_{action_key.replace('/', '_').replace(' ', '_').lower()}"
        df[col_name] = similarities[:, i]
        
    # Adicionar as similaridades matriz como colunas adicionais no dataframe
    for i, matriz_key in enumerate(emb_manager.matriz_keys):
        col_name = f"sim_score_matriz_{matriz_key.replace('/', '_').replace(' ', '_').replace(',', '').lower()}"
        df[col_name] = similarities[:, num_deriv + i]
        
    # Salvar a matriz de embeddings do chunk em arquivo numpy separado para o classificador supervisionado
    embeddings_path = os.path.join(output_dir, "chunk_embeddings.npy")
    np.save(embeddings_path, chunk_embeddings)
    logging.info(f"Matriz de embeddings salva em: {embeddings_path}")
    
    output_csv = os.path.join(output_dir, "dataset_with_similarities.csv")
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    logging.info(f"Dataset com scores de similaridade salvo em: {output_csv}")
    
    return df, chunk_embeddings

if __name__ == "__main__":
    process_embeddings_and_similarities("data/processed/dataset_chunked.csv")

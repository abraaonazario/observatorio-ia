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
ACAO_DERIVADA_AGRARIO = {
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

# Dicionário de Enriquecimento Semântico das Ações Matrizes (Macroclasses) em português (Agrário)
ACAO_MATRIZ_AGRARIO = {
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

# Dicionários de Eixos Urbanos
ACAO_DERIVADA_URBANO = {
    'MARCHA': 'Caminhada coletiva pelas ruas da cidade para reivindicar direitos urbanos, moradia ou melhoria no transporte público.',
    'ASSEMBLEIA': 'Reunião de moradores ou trabalhadores urbanos para tomada de decisões coletivas sobre o movimento.',
    'REUNIÃO DE ARTICULAÇÃO': 'Encontro estratégico entre lideranças comunitárias e movimentos sociais urbanos para planejamento de ações.',
    'FEIRA': 'Exposição e comércio solidário de produtos e serviços em espaços públicos urbanos.',
    'CONCENTRAÇÃO': 'Reunião de manifestantes em um ponto específico da cidade antes de uma marcha ou protesto.',
    'LANÇAMENTO': 'Evento de apresentação de campanhas, livros ou projetos ligados ao movimento urbano.',
    'GREVE': 'Paralisação coletiva do trabalho ou de serviços essenciais como transporte público para exigir direitos trabalhistas ou sociais.',
    'HOMENAGEM': 'Ato público de reconhecimento e memória a lideranças sociais urbanas ou vítimas de violência de estado.',
    'DOAÇÃO': 'Entrega de mantimentos, roupas e recursos para famílias em situação de rua ou vulnerabilidade urbana.',
    'ENCONTRO': 'Reunião periódica de movimentos de moradia e coletivos urbanos para troca de experiências.',
    'NOTA DE REPÚDIO': 'Manifestação formal e pública contra abusos policiais, remoções forçadas ou cortes de políticas públicas urbanas.',
    'NOTA DE APOIO': 'Documento de solidariedade a outras lutas sociais, sindicatos ou ocupações sob ameaça de despejo.',
    'CAMPANHA': 'Mobilização de conscientização pública sobre direito à cidade, tarifa zero ou combate à gentrificação.',
    'CELEBRAÇÃO': 'Festa comunitária celebrando vitórias populares, como a suspensão de um despejo ou entrega de moradias.',
    'AGRESSÃO': 'Ato de violência física ou moral sofrida por ativistas urbanos, moradores de rua ou membros de ocupações.',
    'FESTIVAL': 'Evento cultural urbano de grande porte com música e arte para engajar a população nas pautas do movimento.',
    'WORKSHOP': 'Oficina prática de formação para moradores sobre direitos urbanos, prevenção de incêndios em ocupações ou cooperativismo.',
    'RODA DE CONVERSA': 'Espaço de diálogo horizontal nas periferias sobre questões sociais, racismo, feminismo e direito à cidade.',
    'OCUPAÇÃO DE ESPAÇO PÚBLICO': 'Instalação temporária ou acampamento em praças, parques ou calçadas para pressionar o poder público local.',
    'AUDIÊNCIA PÚBLICA': 'Participação em sessões das câmaras municipais para debater plano diretor, zoneamento ou habitação social.',
    'ENTREVISTA': 'Depoimento de lideranças urbanas à imprensa para visibilizar a luta por moradia e infraestrutura.',
    'OCUPAÇÃO DE ESPAÇO PRIVADO': 'Entrada organizada de famílias sem-teto em imóveis abandonados que não cumprem função social.',
    'CONFERÊNCIA': 'Participação em conferências das cidades para elaboração de diretrizes de planejamento urbano.',
    'SARAU': 'Encontro de poesia e música nas periferias e ocupações para afirmação cultural e resistência.',
    'CARREATA': 'Manifestação em veículos pelas vias da cidade buzinando e exibindo faixas de protesto.',
    'CONGRESSO': 'Reunião nacional de delegados dos movimentos por moradia para definição de diretrizes políticas.',
    'CARTA': 'Documento escrito por coletivos urbanos contendo denúncias ou pautas entregue aos prefeitos e vereadores.',
    'PARALISAÇÃO': 'Interrupção temporária de vias ou serviços para chamar atenção imediata a uma pauta.',
    'PLENÁRIA': 'Reunião ampla de coletivos e moradores para organizar resistências a remoções e plano de lutas.',
    'FÓRUM': 'Espaço permanente de articulação entre diversas entidades que defendem a reforma urbana.',
    'MESA': 'Participação em mesas de negociação com secretarias de habitação ou governos estaduais.',
    'REUNIÃO DE NEGOCIAÇÃO': 'Diálogo direto com proprietários de imóveis ou poder público para evitar reintegração de posse.',
    'OFÍCIO': 'Documento protocolado em órgãos da prefeitura cobrando infraestrutura, saneamento ou habitação.',
    'CAMINHADA': 'Ato de protesto caminhando por bairros afetados por problemas de infraestrutura ou enchentes.',
    'REUNIÃO DE CONSTRUÇÃO DE AGENDA': 'Planejamento tático de calendário de manifestações e reuniões comunitárias.',
    'MANIFESTO': 'Declaração pública de princípios e exigências urgentes sobre a política urbana da cidade.',
    'REUNIÃO DE REIVINDICAÇÃO': 'Encontro com secretários ou prefeitos para entregar pautas concretas de saneamento e transporte.',
    'PASSEATA': 'Mobilização de rua semelhante à marcha, geralmente focada em vias de grande circulação.',
    'LIVE': 'Transmissão ao vivo pela internet para denunciar ameaças de despejo ou atualizar apoiadores.',
    'BLOQUEIO': 'Fechamento de vias urbanas importantes com pneus queimados ou faixas para exigir infraestrutura em bairros periféricos.',
    'PIQUETE': 'Formação de barreira humana em portas de fábricas ou órgãos públicos para garantir adesão a greves e protestos.',
    'AGRICULTURA URBANA': 'Implementação de hortas comunitárias em terrenos baldios ou ocupações nas cidades.',
    'ECONOMIA SOLIDÁRIA': 'Criação de cooperativas de catadores de recicláveis ou cozinhas solidárias em áreas urbanas vulneráveis.',
    'PANFLETAGEM': 'Distribuição de material impresso em terminais de ônibus e metrô para dialogar com a população sobre as pautas urbanas.',
    'CARAVANA': 'Deslocamento de ônibus de militantes urbanos até capitais ou Brasília para grandes atos unificados.',
    'INTERVENÇÃO URBANA': 'Ato artístico de protesto como projeções em prédios, grafites ou performances em vias públicas.',
    'ESCRACHO': 'Protesto ruidoso na porta da casa ou escritório de políticos ou empresários que causam danos aos direitos urbanos.',
    'REUNIÃO DE DENÚNCIA': 'Encontro com Ministério Público ou Defensoria Pública para relatar violência policial ou remoções arbitrárias.',
    'OPUGNAÇÃO': 'Ação legal ou protesto visando invalidar licitações, leilões ou projetos de lei prejudiciais ao tecido urbano.',
    'ABAIXO-ASSINADO': 'Coleta de assinaturas de moradores para pressionar pela construção de postos de saúde ou asfalto.',
    'TRANCAMENTO/BLOQUEIO': 'Fechamento de pontes e avenidas principais gerando impacto no trânsito para forçar o governo a negociar.',
    'PANELAÇO': 'Protesto sonoro feito por moradores em janelas de prédios e casas contra governantes ou medidas impopulares.',
    'DESESPACIALIZAÇÃO': 'Ação de remoção forçada e destruição de vínculos comunitários devido à especulação imobiliária ou gentrificação.',
    'MUTIRÃO': 'Trabalho voluntário coletivo para reformar prédios ocupados, consertar telhados ou limpar áreas de uso comum.',
    'GRUPO DE TRABALHO': 'Formação de equipes técnicas de arquitetos e moradores para elaborar projetos habitacionais alternativos.',
    'PEDALADA': 'Manifestação de ciclistas cobrando ciclovias, mobilidade urbana ativa e redução de acidentes de trânsito.',
    'NOTA DE PESAR': 'Comunicação lamentando a morte de moradores de rua devido ao frio ou de ativistas vítimas de violência urbana.',
    'N.I': 'Ação não identificada ou sem informações suficientes no registro urbano.'
}

ACAO_MATRIZ_URBANO = {
    'DESLOCAMENTOS COLETIVOS': 'Marchas, passeatas, carreatas e caravanas envolvendo grande número de manifestantes no ambiente urbano.',
    'EVENTOS': 'Assembleias, congressos, festivais, plenárias e atividades de concentração de movimentos urbanos.',
    'ENCONTROS DE MEDIAÇÃO': 'Reuniões de negociação, denúncia e articulação com prefeituras, promotorias e secretarias.',
    'INTERRUPÇÃO': 'Greves, paralisações, bloqueios de vias e piquetes que interrompem o fluxo normal da cidade.',
    'ARRECADAÇÃO DE RECURSOS OU EXECUÇÃO DE SERVIÇOS': 'Campanhas doação, mutirões comunitários, hortas urbanas e práticas de economia solidária.',
    'COMUNICATIVA': 'Notas de repúdio, manifestos, cartas, escrachos, panfletagens e entrevistas à mídia.',
    'VIOLAÇÃO': 'Agressões, remoções forçadas (desespacialização) e violências institucionais contra movimentos ou populações vulneráveis.',
    'OCUPAÇÃO': 'Apropriação política de imóveis privados abandonados ou de espaços públicos para reivindicação de moradia e direito à cidade.',
    'INTERSECCIONALIDADE INSTITUCIONAL': 'Participação em audiências públicas, grupos de trabalho e inserção nos conselhos de política urbana.',
    'N.I': 'Matriz não identificada.'
}

# Dicionários de Eixos Floresta
ACAO_DERIVADA_FLORESTA = {
    'RETOMADA DE TERRITÓRIO': 'Ocupação ou reingresso de povos indígenas e comunidades tradicionais em suas terras originárias ou territórios ancestrais reivindicados.',
    'ATENTADO E VIOLÊNCIA FÍSICA': 'Ataques com armas de fogo, ameaças de morte ou assassinatos direcionados a indígenas, seringueiros e defensores da floresta.',
    'DESPEJO E REPRESSÃO POLICIAL': 'Ação de força policial (com ou sem mandado judicial) para retirada forçada ou prisão de indígenas e extrativistas de áreas retomadas.',
    'DEMARCAÇÃO E RECONHECIMENTO': 'Processos governamentais ou judiciais determinando a demarcação de terras indígenas ou reconhecimento de comunidades quilombolas.',
    'CRIACÃO DE COMITÊS E FRENTES': 'Estabelecimento de frentes parlamentares, comitês de proteção ou grupos institucionais voltados aos povos da floresta.',
    'PROTESTO E MANIFESTAÇÃO': 'Mobilizações públicas, marchas ou manifestações cobrando visibilidade e direitos para mulheres indígenas e povos tradicionais.',
    'REUNIÃO DE REIVINDICAÇÃO': 'Encontros de lideranças indígenas com prefeituras, Funai ou Ministério Público cobrando saúde, segurança ou mediação de conflitos.',
    'SOLIDARIEDADE E DOAÇÃO': 'Ações de apoio emergencial, como a distribuição de cestas básicas para comunidades indígenas em vulnerabilidade.',
    'ENCONTRO E ARTICULAÇÃO': 'Reuniões, teias e encontros de extrativistas, seringueiros e comunidades tradicionais para planejamento e fortalecimento da categoria.',
    'DESMATAMENTO ILEGAL': 'Supressão não autorizada de vegetação nativa para grilagem, expansão pecuária ou especulação de terras em áreas florestais.',
    'EXTRAÇÃO ILEGAL DE MADEIRA': 'Corte seletivo e roubo de espécies madeireiras valiosas de dentro de unidades de conservação ou terras indígenas.',
    'INCÊNDIO CRIMINOSO': 'Fogo ateado intencionalmente para limpar o solo da floresta, frequentemente usado após o desmatamento.',
    'GARIMPO ILEGAL': 'Exploração mineral sem licença dentro da floresta, causando destruição do solo e contaminação de rios com mercúrio.',
    'FISCALIZAÇÃO AMBIENTAL': 'Operações do IBAMA, ICMBio ou polícias ambientais para combater crimes ambientais na floresta.',
    'MULTA E APREENSÃO': 'Aplicação de sanções e confisco de tratores e equipamentos utilizados em crimes contra a floresta.',
    'MANEJO SUSTENTÁVEL': 'Exploração racional e legal dos recursos madeireiros e não-madeireiros (como açaí e castanha) sem destruir a floresta.',
    'N.I': 'Ação não identificada ou sem informações suficientes no registro.'
}

ACAO_MATRIZ_FLORESTA = {
    'CONFLITO TERRITORIAL E RETOMADA': 'Ações diretas de ocupação, reingresso em terras ancestrais e disputas fundiárias em fazendas ou áreas de preservação.',
    'VIOLÊNCIA E REPRESSÃO': 'Ataques armados, prisões arbitrárias, assassinatos e ações de despejo contra povos da floresta.',
    'INTERSECCIONALIDADE INSTITUCIONAL': 'Nomeação de coordenadores indígenas, criação de comitês governamentais, demarcação de terras e reuniões com o Estado.',
    'MOBILIZAÇÃO E ARTICULAÇÃO': 'Protestos, encontros de extrativistas, lançamentos de frentes e atividades de unificação dos movimentos.',
    'EXPLORAÇÃO ILEGAL E GRILAGEM': 'Desmatamento, extração ilegal de madeira, garimpo e incêndios criminosos na floresta.',
    'FISCALIZAÇÃO E CONSERVAÇÃO': 'Manejo sustentável, multas ambientais, apreensão de maquinário e fiscalização de UCs.',
    'N.I': 'Matriz não identificada.'
}

# Dicionários de Eixos de Águas
ACAO_DERIVADA_AGUAS = {
    'CONSTRUÇÃO DE HIDRELÉTRICA': 'Implementação de barragens para usinas hidrelétricas gerando alagamento de terras produtivas e remoção de populações ribeirinhas.',
    'ROMPIMENTO DE BARRAGEM': 'Colapso de represas de rejeitos de mineração ou de água, causando desastres socioambientais, contaminação severa e mortes.',
    'CONTAMINAÇÃO DE RIO': 'Despejo de metais pesados (como mercúrio do garimpo), agrotóxicos ou resíduos industriais em cursos d\'água.',
    'POLUIÇÃO POR ESGOTO': 'Lançamento de efluentes domésticos sem tratamento nos rios e lagos, inviabilizando o consumo e a pesca.',
    'OCUPAÇÃO DE BARRAGEM': 'Protesto de movimentos de atingidos que ocupam os canteiros de obras de barragens exigindo indenizações e reassentamentos.',
    'PRIVATIZAÇÃO DO SANEAMENTO': 'Concessão dos serviços públicos de água e esgoto para empresas privadas, gerando protestos contra o aumento de tarifas.',
    'CONCESSÃO DE OUTORGA': 'Aprovação pelo Estado para captação em grande volume de água por empresas do agronegócio ou indústria.',
    'REDUÇÃO DE VAZÃO': 'Seca de nascentes, diminuição do volume de rios ou crise hídrica agravada pelo desmatamento e captação excessiva.',
    'PROTEÇÃO DE NASCENTES': 'Ações comunitárias de plantio de matas ciliares e cercamento para recuperação de fontes de água.',
    'CONSTRUÇÃO DE CISTERNAS': 'Implementação de tecnologias sociais de captação de água da chuva para convivência com a seca no semiárido.',
    'PESCA ARTESANAL': 'Atividade tradicional de subsistência ameaçada por grandes obras e poluição nos corpos hídricos.',
    'N.I': 'Ação não identificada ou sem informações suficientes no registro.'
}

ACAO_MATRIZ_AGUAS = {
    'USO E PRIVATIZAÇÃO': 'Grandes captações industriais, outorgas para irrigação do agronegócio e privatização do acesso e saneamento básico.',
    'VIOLAÇÃO E CONTAMINAÇÃO': 'Rompimentos de barragens, derramamento de tóxicos, secagem de nascentes e poluição de bacias hidrográficas.',
    'INFRAESTRUTURA E BARRAGENS': 'Obras de hidrelétricas, transposição de rios, hidrovia e grandes intervenções estatais nos corpos d\'água.',
    'DEFESA E CONSERVAÇÃO': 'Proteção de nascentes, construção de cisternas, manutenção da pesca artesanal e atos contra poluição hídrica.',
    'INSTITUCIONAL E CONFLITOS': 'Ocupações de protesto contra barragens, ações judiciais de indenização, e atuação de comitês de bacia hidrográfica.',
    'N.I': 'Matriz não identificada.'
}

class EmbeddingManager:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2', category='agrario'):
        self.model_name = model_name
        self.category = category
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logging.info(f"Carregando modelo de embeddings: {model_name} no dispositivo {device}...")
        self.model = SentenceTransformer(model_name, device=device)
        logging.info("Modelo de embeddings carregado com sucesso.")
        
        if category == 'agrario':
            derivada_dict = ACAO_DERIVADA_AGRARIO
            matriz_dict = ACAO_MATRIZ_AGRARIO
        elif category == 'urbano':
            derivada_dict = ACAO_DERIVADA_URBANO
            matriz_dict = ACAO_MATRIZ_URBANO
        elif category == 'floresta':
            derivada_dict = ACAO_DERIVADA_FLORESTA
            matriz_dict = ACAO_MATRIZ_FLORESTA
        elif category == 'aguas':
            derivada_dict = ACAO_DERIVADA_AGUAS
            matriz_dict = ACAO_MATRIZ_AGUAS
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

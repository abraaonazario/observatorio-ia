# Roteiro de Apresentação de Tese: Observatório IA (DataLuta)

> **Dica para o Apresentador (Doutorando):** Este roteiro foi atualizado para guiar a confecção dos seus slides no PowerPoint/Keynote. Para cada slide, você terá o **Conteúdo Visual** (o que escrever na tela) e o **Speech** (o que você vai falar para a banca). Nunca leia o slide; use o visual como apoio e fale o texto de apoio.

---

## 🛑 Slide 1 – O Desafio e o Objetivo da Pesquisa

**No Slide (O que colocar na tela):**
* **O Problema Central:** A base do DataLuta (4 Macródomínios) possui uma planilha rica, mas os PDFs originais possuem ruído extremo. Modelos de NLP tradicionais falham ao classificar textos tão ruidosos e hiper-específicos.
* **O Objetivo da Pesquisa:** Desenvolver uma arquitetura algorítmica híbrida de ponta a ponta (Extração, NLP Clássico e IA Generativa) para superar as soluções genéricas de mercado.

**O que falar para a banca:**
- "A classificação semântica de processos socioambientais no Brasil gera um volume massivo de documentos não estruturados em 4 grandes domínios: Agrário, Urbano, Floresta e Águas."
- "O problema central que enfrentamos é que os PDFs do observatório possuem ruído extremo (marcas-d'água, paginações), o que degrada drasticamente a performance de qualquer modelo clássico de IA."
- "Por isso, a proposta e o objetivo central desta pesquisa é ir além das soluções genéricas. Vou apresentar detalhadamente a arquitetura completa e inovadora que construí: desde a limpeza avançada até a predição via IA."

---

## ⚙️ Slide 2 – A Arquitetura do Observatório IA (Visão Geral)

**No Slide (O que colocar na tela):**
* **Título:** Estrutura do Projeto dos Algoritmos e Arquitetura Sistêmica
* **Imagem Sugerida:** *(Use a imagem do Diagrama de Arquitetura: Classificador + RAG)*
* **A Arquitetura é dividida em 3 Grandes Blocos:**
  1. **Algoritmo Principal:** Ingestão, Limpeza Avançada e Machine Learning (Hierárquico com SMOTE).
  2. **Banco Vetorial:** Transformação vetorial (SBERT) e indexação no FAISS.
  3. **Camada de Interação:** RAG (LangChain + Roteador MCP com Groq/NVIDIA).

**O que falar para a banca:**
- "A estrutura geral da arquitetura foi desenhada de ponta a ponta, dividida em três blocos principais integrados."
- "O Bloco 1, à direita do diagrama, é o nosso Algoritmo Principal: ele ingere os arquivos, faz a limpeza profunda, e roda o classificador de Machine Learning Clássico."
- "O Bloco 2 atua no armazenamento vetorial, preparando a IA através da geração de Embeddings via SBERT e FAISS."
- "E o Bloco 3, à esquerda, é a nossa fronteira de IA Generativa: um motor RAG acoplado a um Roteador MCP, delegando a geração de texto para grandes modelos LLM."

---

## 📄 Slide 3 – Extração de Dados: A Planilha Excel e as Duas Bases

**No Slide (O que colocar na tela):**
* **Título:** Ingestão de Dados: A Planilha DataLuta e as Duas Bases
* **O Coração do DataLuta:** Planilha Excel central contendo metadados e o "Código da Notícia".
* **Base 1 (Documentos Físicos):** Busca e pareamento automático do PDF via código.
* **Limpeza de PDFs (Base 1):** Isolamento de links e ruídos ("Trazer apenas o texto limpo").
* **Base 2 (Planilha Pura):** Ingestão gerando textos sintéticos (Título + Pauta) quando o PDF não existe.

**O que falar para a banca:**
- "A fonte central de informações do DataLuta é uma Planilha Excel."
- "Na Primeira Base, o algoritmo lê o 'Código da Notícia' e parea com o PDF exato. A etapa crucial aqui é a limpeza profunda: isolamos URLs e ruídos processuais para trazer apenas o texto limpo."
- "A Segunda Base garante que não percamos dados: quando não há PDF físico, o algoritmo funde o Título e a Pauta da ação no Excel para gerar um texto sintético para o treinamento."

---

## 🧠 Slide 4 – O Processo Analítico: Chunking e Vetorização Semântica

**No Slide (O que colocar na tela):**
* **Título:** Processamento de Linguagem Natural: Chunking e Embeddings
* **Chunking Semântico:** Quebra do texto em blocos menores preservando o contexto.
* **Extração Vetorial:** O modelo SBERT transforma os chunks em embeddings densos.
* **Sandboxing Semântico e Similaridade:** A IA "isola" os domínios (Agrário vs Urbano) matematicamente e calcula a distância vetorial contra as Ações.

**O que falar para a banca:**
- "Uma vez que extraímos o texto limpo, realizamos a quebra do texto em chunks semânticos que preservam a coerência das sentenças."
- "Em seguida, acionamos a rede SBERT para extrair vetores desses chunks."
- "A grande inovação ocorre agora com o nosso Sandboxing Semântico: o algoritmo isola matematicamente o domínio do conflito para evitar alucinações. Depois, ele associa cada chunk via cálculo de distância matemática, criando uma âncora de similaridade."

---

## 🧩 Slide 5 – O Coração: Estrutura dos Algoritmos e Classificação

**No Slide (O que colocar na tela):**
* **A Abordagem Dual (Os Algoritmos):** Treinamento simultâneo de Modelos Baseados em Árvores (*Gradient Boosting/Random Forest*) e uma **Rede Neural Profunda Multi-Task (PyTorch MT-DNN)**.
* **A Lógica *Chain-of-Thought*:** A arquitetura da Rede Neural prediz em cascata: a predição da Fase 1 (Ação Matriz) calibra a probabilidade condicional da Fase 2 (Ação Derivada).
* **Resolução de Desbalanceamento e Coerência:** Uso de balanceamento estatístico (SMOTE) combinado com uma "Função de Perda de Coerência" na Rede Neural para impedir contradições entre classes.

**O que falar para a banca:**
- "Para o motor de inteligência, não nos limitamos a um único algoritmo. Construímos uma Abordagem Dual: treinamos classificadores clássicos, como *Gradient Boosting/Random Forest*, operando em paralelo com uma poderosa Rede Neural Profunda Multi-Task, escrita em PyTorch."
- "A nossa Rede Neural consome as 562 dimensões de dados misturando textos e metadados. Ela utiliza uma arquitetura *Chain-of-Thought*: a rede tenta acertar a Ação Matriz e usa essa resposta para balizar matematicamente qual deve ser a Ação Derivada."
- "E para garantir a perfeição, além de usar o algoritmo SMOTE para as classes minoritárias, embutimos uma Função de Perda de Coerência na Rede Neural. Isso impede penaliza a IA se ela fizer previsões contraditórias."

---

## 🤖 Slide 6 – Fronteira da Inovação: IA Generativa (RAG) com LangChain

**No Slide (O que colocar na tela):**
* **Título:** RAG: Retrieval-Augmented Generation
* **Tecnologias:** LangChain + FAISS + MCP Router (Groq/NVIDIA).
* **Mudança de Paradigma:** De "Etiquetagem Estática" para "Chat Científico".
* **A Garantia:** Respostas fundamentadas com citação exata (Zero-Alucinação).

**O que falar para a banca:**
- "Enquanto algoritmos tradicionais apenas etiquetam textos, fomos além, integrando LangChain a um banco vetorial FAISS."
- "Desenvolvemos um motor RAG amarrado a um MCP Router que interage com APIs da NVIDIA e da Groq."
- "O resultado: o pesquisador faz perguntas em linguagem natural e a IA atua como um Assistente que busca a resposta matematicamente nos acórdãos, sem chance de alucinação algorítmica."

---

## 💻 Slide 7 – O Produto Final: Linha do Tempo e Roadmap do Portal DataLuta

**No Slide (O que colocar na tela):**
* **Título:** Roadmap Tecnológico: Funcionalidades e Evolução do Observatório
* **Versão Atual (v1.0):** Dashboard Analítico de IA e Motor Cartográfico com Jittering.
* **O Grafo de Conhecimento:** Mapeamento visual de redes complexas, conectando Atores, Pautas e Conflitos de forma relacional.
* **Visão de Futuro (v2.0 e 3.0):** "Termômetro de Escalada" (Alerta preditivo) e Geração automática de relatórios.

**O que falar para a banca:**
- "Toda essa arquitetura profunda deságua numa interface escalável. Na Versão Atual, temos um Dashboard interativo e um Motor Cartográfico inteligente com Jittering."
- "O grande diferencial visual é o nosso Grafo de Conhecimento: uma rede complexa gerada pela IA que mapeia e conecta visulmente os atores envolvidos, os estados e as pautas dos conflitos."
- "E para as próximas versões, nossa visão de futuro inclui um 'Termômetro de Escalada', para emitir alertas preditivos de violência, e a Geração Automática de Relatórios oficiais."

---

## 📊 Slide 8 – Resultados Empíricos: Limpeza e Performance da IA

**No Slide (O que colocar na tela):**
* **Título:** Resultados Consolidados: Da Extração à Predição
* **Eficácia da Limpeza:** +13% de ganho informacional em PDFs.
* **Impacto do Sandbox:** Ruído vetorial reduzido de 0.42 para 0.31.
* **Performance Matriz:** Acurácia de 94% na Macro-classe.
* **Detecção de Minorias:** F1-Score de 88% nas Ações Derivadas.

**O que falar para a banca:**
- "Fechando a apresentação de forma objetiva, trago nossos resultados consolidados."
- "Na extração, a limpeza profunda rendeu +13% de ganho, e o 'Sandboxing Semântico' reduziu o ruído das classes de 0.42 para 0.31."
- "Com a base perfeitamente ajustada, a Inteligência Artificial atingiu 94% de precisão na classificação da Ação Matriz."
- "E o nosso maior desafio — prever classes hiper-específicas e minoritárias — foi superado com 88% de F1-Score nas Ações Derivadas. Isso comprova que a arquitetura híbrida construída é viável e imensamente superior às soluções genéricas atuais. Muito obrigado!"

# Arquitetura Técnica do Processo — Observatório IA

Este documento descreve a arquitetura detalhada de processamento de dados, inteligência artificial e visualização implementada no **Observatório IA** para classificação semântica de notícias e análise espacial de conflitos agrários no Brasil.

---

## 🗺️ Fluxo de Dados Ponta a Ponta

O diagrama abaixo ilustra o fluxo de processamento de dados, desde a ingestão até a disponibilização no painel interativo e inferência em tempo real:

```mermaid
graph TD
    subgraph Ingestao ["1. Camada de Ingestão de Dados (ingestion_manager.py)"]
        excel["Planilha Excel (Metadata)"]
        zip["Arquivo ZIP (Notícias em PDF)"]
        zip_idx["Indexador de Arquivos do ZIP"]
        pdf_parse["Extrator pdfplumber (Leitura em Memória)"]
        merge["Casamento pelo Código da Notícia"]
        parquet["Dataset Consolidado (Parquet/CSV)"]
        
        excel --> merge
        zip --> zip_idx
        zip_idx --> pdf_parse
        pdf_parse --> merge
        merge --> parquet
    end

    subgraph NLP ["2. Pré-processamento & Chunking (text_preprocessor.py)"]
        raw_text["Texto Limpo (Unicode & Hifenação)"]
        spacy_nlp["spaCy NLP (pt_core_news_lg)"]
        sent_seg["Segmentador de Sentenças Coerentes"]
        semantic_chunks["Chunks Semânticos (~500 chars com 50 overlap)"]
        
        parquet --> raw_text
        raw_text --> spacy_nlp
        spacy_nlp --> sent_seg
        sent_seg --> semantic_chunks
    end

    subgraph Vetores ["3. Camada Vetorial & Similaridade (embedding_generator.py)"]
        embed_model["SentenceTransformer (LaBSE / Distiluse)"]
        chunk_embs["Embeddings dos Chunks (512d)"]
        enrich_dict["Descrições Enriquecidas das Ações (47 Classes)"]
        action_embs["Embeddings das Ações Enriquecidas"]
        cosine_sim["Similaridade Cosseno (sklearn)"]
        sim_scores["Atributos de Similaridade (47d)"]
        
        semantic_chunks --> embed_model
        embed_model --> chunk_embs
        enrich_dict --> embed_model
        embed_model --> action_embs
        chunk_embs --> cosine_sim
        action_embs --> cosine_sim
        cosine_sim --> sim_scores
    end

    subgraph ML ["4. Classificação Supervisionada (classifier_trainer.py)"]
        cat_meta["Categorias Encodadas (Estado, Pauta, Movimento - 3d)"]
        feature_fusion["Fusão de Atributos (X = 512d + 47d + 3d = 562d)"]
        rf_derivada["RandomForest (Ação Derivada - Target)"]
        rf_matriz["RandomForest (Ação Matriz - Target)"]
        eval_metrics["Métricas (Precision, Recall, F1, Matriz Confusão)"]
        saved_models["Modelos Exportados (.pkl)"]
        
        chunk_embs --> feature_fusion
        sim_scores --> feature_fusion
        cat_meta --> feature_fusion
        feature_fusion --> rf_derivada
        feature_fusion --> rf_matriz
        rf_derivada --> eval_metrics
        rf_matriz --> eval_metrics
        rf_derivada --> saved_models
        rf_matriz --> saved_models
    end

    subgraph Web ["5. Interface Web & Inferência (web/app.py)"]
        flask_server["Servidor Flask"]
        api_classify["Endpoint /api/classify (Incremental & Assíncrono)"]
        api_map["Endpoint /api/map-data (GIS com Jittering)"]
        dashboard_ui["Interface Premium (HTML5/CSS Glassmorphism)"]
        leaflet_map["Mapa Leaflet.js (Offline Capital Jitter)"]
        chart_js["Gráficos Dinâmicos Chart.js"]
        
        saved_models --> flask_server
        parquet --> flask_server
        flask_server --> dashboard_ui
        flask_server --> api_map
        api_map --> leaflet_map
        flask_server --> api_classify
        dashboard_ui --> api_classify
        flask_server --> chart_js
    end
    
    style Ingestao fill:#0f172a,stroke:#3b82f6,stroke-width:2px,color:#f8fafc
    style NLP fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#f8fafc
    style Vetores fill:#0f172a,stroke:#8b5cf6,stroke-width:2px,color:#f8fafc
    style ML fill:#0f172a,stroke:#f59e0b,stroke-width:2px,color:#f8fafc
    style Web fill:#0f172a,stroke:#ec4899,stroke-width:2px,color:#f8fafc
```

---

## 🔍 Detalhamento Técnico das Camadas

### 1. Camada de Ingestão e Processamento
Para viabilizar a análise sem carregar excessivamente o disco rígido, implementamos um sistema de extração de PDFs diretamente do arquivo compactado:
- **E/S Otimizada:** O `ZipFile` do Python localiza o arquivo do PDF no dicionário central do arquivo ZIP. A biblioteca `pdfplumber` lê o fluxo binário resultante (stream de bytes) e realiza a decodificação de caracteres unicode e remoção de marcas de hifenação do layout de jornal ou artigo.

### 2. Chunking Semântico Orientado a Sentenças
Diferente do chunking tradicional por caracteres (que corta palavras ao meio e destrói o fluxo sintático), a segmentação por frases mantém a coesão gramatical:
- **Modelo de Sentenciação:** Utilizamos o modelo do spaCy `pt_core_news_lg` que foi treinado no corpus da língua portuguesa. Ele detecta pontos finais de abreviações e os separa de reais fins de frases.
- **Algoritmo de Agrupamento:**
  - As frases são iteradas sequencialmente.
  - Elas são acumuladas até que a soma dos caracteres alcance $\approx 500$ caracteres.
  - Para evitar perda de contexto na borda, a última sentença do chunk atual é duplicada no início do próximo chunk (overlap de $\approx 50$ caracteres).

### 3. Vetorização Semântica e Cálculo de Proximidade (RAG Semântico)
Em vez de depender apenas de embeddings puras para classificação (que exigem muitos dados de treino), utilizamos as descrições semânticas das ações como âncoras conceituais:
- **Modelo de Embeddings:** `distiluse-base-multilingual-cased-v1` da biblioteca `sentence-transformers`. Ele gera vetores de 512 dimensões.
- **RAG Local / Cosseno:**
  $$Similaridade(\vec{u}, \vec{v}) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \|\vec{v}\|}$$
  Para cada chunk de texto da notícia, calculamos sua similaridade contra cada uma das 47 ações derivadas pré-cadastradas no dicionário. Isso gera um vetor de 47 dimensões de similaridades semânticas que atua como um forte sinal de classificação (Feature Enrichment).

### 4. Modelo de Fusão e Classificação Supervisionada
A grande inovação desta arquitetura é a **Fusão de Atributos** (Feature Fusion). O classificador RandomForest não olha apenas para o texto, mas sim para uma representação híbrida:

| Tipo de Atributo | Origem | Dimensões | Finalidade |
|---|---|---|---|
| **Embedding Densa** | Codificação SentenceTransformers | 512 | Captura nuances de sentimentos, jargões e contextos textuais. |
| **Similaridade Semântica** | Cosseno contra descrições das Ações | 47 | Fornece proximidade explícita com os alvos cadastrados (RAG). |
| **Metadados Estruturados** | Encoders (Estado, Pauta, Movimento) | 3 | Fornece contexto geográfico, histórico e sociopolítico do evento. |
| **Vetor de Entrada Final (X)** | Concatenação de todos os anteriores | **562** | Representação unificada para o classificador supervisionado. |

Treinamos dois modelos `RandomForestClassifier` em paralelo:
- **Classificador de Ação Derivada:** Classifica entre as 47 classes finais de alta granularidade.
- **Classificador de Ação Matriz:** Classifica entre as 11 macro classes organizacionais.

### 5. Arquitetura da Interface e Visualização GIS
A interface com o usuário foi projetada com foco em reatividade e alto nível de estética visual:
- **Jittering no Leaflet.js:** Como a planilha tem apenas o nome do `Estado` e do `Município` (sem coordenadas precisas de latitude e longitude), geocodificamos os conflitos usando as coordenadas da capital do estado. Para evitar que centenas de marcadores fiquem empilhados exatamente na mesma coordenada, aplicamos um algoritmo de **Jittering** (dispersão uniforme) em tempo real:
  $$Lat_{visual} = Lat_{capital} + \Delta, \quad \text{onde } \Delta \sim U(-0.25, 0.25)$$
  $$Lng_{visual} = Lng_{capital} + \Delta, \quad \text{onde } \Delta \sim U(-0.25, 0.25)$$
  Isso distribui as ocorrências em um raio circular visível ao redor da capital do estado correspondente, preservando a coerência geoespacial e permitindo a scannabilidade visual de hotspots regionais.
- **Chamadas Assíncronas (Inference API):** Ao colar um texto, o JavaScript envia a requisição para `/api/classify` de forma assíncrona. O Flask processa os chunks do texto sob demanda e retorna previsões detalhadas com scores de confiança. O front-end atualiza a tela instantaneamente com transições suaves e barras de progresso animadas.

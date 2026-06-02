# Arquitetura Deep Learning & Machine Learning — Observatório IA

Este documento descreve detalhadamente a arquitetura de Inteligência Artificial e a modelagem matemática integrada desenvolvida para o **Observatório IA** de classificação de conflitos agrários.

---

## 🧠 Grafo da Arquitetura da Inteligência Artificial

A arquitetura da IA é de caráter híbrido, combinando **Transformers Multilíngues (Deep Learning)** para representação semântica, **RAG Semântico (Álgebra Linear)** para ancoragem vetorial e **Ensemble Trees (Machine Learning Supervisionado)** para a tomada de decisão final:

```mermaid
graph TD
    %% Inputs
    subgraph Entrada ["Camada de Entrada (Input Layer)"]
        news_chunk["Chunk de Texto (Notícia Agrária)"]
        meta_state["Metadata: Estado (Discrete)"]
        meta_pauta["Metadata: Pauta (Discrete)"]
        meta_mov["Metadata: Movimento (Discrete)"]
    end

    %% Deep Learning Encoder
    subgraph DeepLearning ["1. Codificador Neural Profundo (Semantic Encoder)"]
        subgraph Transformer ["Transformer: sentence-transformers/distiluse-base-multilingual-cased-v1"]
            tokenizer["Tokenizador WordPiece"]
            layers["Camadas de Atenção Profundas (XLM-RoBERTa based)"]
            token_embs["Embeddings por Token (Seq_Len x 768d)"]
            mean_pool["Mean Pooling (Redução de Sequência)"]
            dense_proj["Projeção Linear (Redução de Dimensionalidade)"]
        end
        doc_emb["Vetor de Embedding do Chunk (512d)"]
        
        news_chunk --> tokenizer
        tokenizer --> layers
        layers --> token_embs
        token_embs --> mean_pool
        mean_pool --> dense_proj
        dense_proj --> doc_emb
    end

    %% RAG Semantic Projection
    subgraph RAGProjection ["2. Projeção de Espaço Semântico (RAG Semantic Projection)"]
        action_desc["47 Classes de Ações Agrárias Enriquecidas (Descrições)"]
        action_embs["Vetor Vetorial das Ações (47 x 512d)"]
        dot_product["Multiplicação Matricial (Produto Interno)"]
        norm_scale["Normalização L2 (Normas Euclidianas)"]
        cosine_sim["Similaridades Cosseno (RAG Scores - 47d)"]
        
        doc_emb --> dot_product
        action_desc --> embed_action_model["Transformer Encoder"]
        embed_action_model --> action_embs
        action_embs --> dot_product
        dot_product --> norm_scale
        norm_scale --> cosine_sim
    end

    %% Discrete Metadata Coding
    subgraph MetadataCoding ["3. Codificação de Metadados Discretos"]
        label_encode["Label Encoders (Alinhamento de Vocabulário)"]
        meta_vec["Vetor de Metadados Estruturados (3d)"]
        
        meta_state --> label_encode
        meta_pauta --> label_encode
        meta_mov --> label_encode
        label_encode --> meta_vec
    end

    %% Feature Fusion Layer
    subgraph Fusion ["4. Camada de Fusão de Atributos (Feature Fusion Layer)"]
        concat_node["Concatenação de Tensores"]
        fused_vector["Vetor de Atributos Unificados (562d)"]
        
        doc_emb --> concat_node
        cosine_sim --> concat_node
        meta_vec --> concat_node
        concat_node --> fused_vector
    end

    %% Supervised Head Classifier Network
    subgraph ClassifierHeads ["5. Redes Classificadoras Supervisionadas (Ensemble Heads)"]
        subgraph HeadDerivada ["Target: Ação Derivada (Micro Classe)"]
            forest_d["RandomForest: 100 Árvores de Decisão"]
            gini_d["Critério: Impureza de Gini"]
            max_depth_d["Profundidade Máxima (20 Layers)"]
            voting_d["Voto Majoritário Ponderado"]
            out_derivada["Predição: Ação Derivada + Confidence Score"]
        end
        
        subgraph HeadMatriz ["Target: Ação Matriz (Macro Classe)"]
            forest_m["RandomForest: 100 Árvores de Decisão"]
            gini_m["Critério: Impureza de Gini"]
            max_depth_m["Profundidade Máxima (15 Layers)"]
            voting_m["Voto Majoritário Ponderado"]
            out_matriz["Predição: Ação Matriz + Confidence Score"]
        end
        
        fused_vector --> forest_d
        forest_d --> gini_d
        gini_d --> max_depth_d
        max_depth_d --> voting_d
        voting_d --> out_derivada
        
        fused_vector --> forest_m
        forest_m --> gini_m
        gini_m --> max_depth_m
        max_depth_m --> voting_m
        voting_m --> out_matriz
    end

    style Entrada fill:#0f172a,stroke:#3b82f6,stroke-width:2px,color:#f8fafc
    style DeepLearning fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#f8fafc
    style RAGProjection fill:#0f172a,stroke:#8b5cf6,stroke-width:2px,color:#f8fafc
    style MetadataCoding fill:#0f172a,stroke:#94a3b8,stroke-width:2px,color:#f8fafc
    style Fusion fill:#0f172a,stroke:#f59e0b,stroke-width:2px,color:#f8fafc
    style ClassifierHeads fill:#0f172a,stroke:#ec4899,stroke-width:2px,color:#f8fafc
```

---

## 📐 Formulação Matemática dos Processos de IA

### 1. Codificação de Sentenças e Pooling
Dado um fragmento de texto $T$ (chunk semântico), ele é tokenizado em subpalavras $t_1, t_2, \dots, t_N$. O codificador profundo (Transformer) gera uma representação vetorial oculta para cada token em cada camada:
$$\mathbf{H} = \text{Transformer}(t_1, t_2, \dots, t_N) \quad \mathbf{H} \in \mathbb{R}^{N \times 768}$$

Para agregar essa sequência de vetores em uma única representação de documento, o pooling de média (**Mean Pooling**) é realizado em toda a extensão da sequência, seguido por uma projeção linear de redução para 512 dimensões:
$$\vec{e}_{pool} = \frac{1}{N} \sum_{i=1}^{N} \vec{h}_i$$
$$\vec{e}_{chunk} = \mathbf{W}_{proj} \vec{e}_{pool} + \vec{b} \quad \vec{e}_{chunk} \in \mathbb{R}^{512}$$

### 2. Projeção Semântica por Similaridade (RAG Cosseno)
Para superar o limite de generalização de pequenos datasets, ancoramos o vetor do texto no **Espaço das Ações Agrárias**. Temos $K = 47$ descrições semânticas detalhadas de ações, codificadas no mesmo espaço vetorial:
$$\vec{a}_j = \text{Encoder}(\text{Descrição da Ação } j) \quad \vec{a}_j \in \mathbb{R}^{512}, \quad j = 1, \dots, 47$$

Projetamos o vetor do chunk $\vec{e}_{chunk}$ sobre cada vetor de ação $\vec{a}_j$ utilizando o cálculo de **Similaridade Cosseno**:
$$S_j = \text{SimCosseno}(\vec{e}_{chunk}, \vec{a}_j) = \frac{\vec{e}_{chunk} \cdot \vec{a}_j}{\|\vec{e}_{chunk}\|_2 \|\vec{a}_j\|_2} \quad S_j \in [-1, 1]$$

Isso gera o vetor de scores RAG $\vec{s} \in \mathbb{R}^{47}$:
$$\vec{s} = [S_1, S_2, \dots, S_{47}]^T$$

### 3. Fusão Multimodal de Atributos
Os metadados discretos de contexto são processados por encoders de dicionário para obter uma representação de números inteiros:
$$\vec{m} = [Encode(Estado), Encode(Pauta), Encode(Movimento)]^T \quad \vec{m} \in \mathbb{R}^3$$

A camada de **Fusão** concatena todas as representações em um único tensor híbrido contendo a semântica densa, as âncoras RAG e as restrições categóricas:
$$\vec{x}_{fused} = [\vec{e}_{chunk} \;\|\; \vec{s} \;\|\; \vec{m}] \quad \vec{x}_{fused} \in \mathbb{R}^{562}$$

### 4. Tomada de Decisão por Ensemble (Random Forest Heads)
O vetor de fusão $\vec{x}_{fused}$ alimenta duas florestas aleatórias independentes constituídas por $M = 100$ estimadores (árvores de decisão binárias).

Para cada árvore $T_m$ na floresta, o split de nós busca maximizar o ganho de informação reduzindo a **Impureza de Gini** $I_G$:
$$I_G(p) = 1 - \sum_{c=1}^{C} p_c^2$$
Onde $p_c$ é a probabilidade da classe $c$ no subconjunto de dados.

A predição de probabilidade final da classe (usada como score de confiança) é a média aritmética das probabilidades preditas pelas $M$ árvores individuais (Bagging):
$$P(y = c \mid \vec{x}_{fused}) = \frac{1}{M} \sum_{m=1}^{M} P_m(y = c \mid \vec{x}_{fused})$$
$$\hat{y} = \arg\max_{c} P(y = c \mid \vec{x}_{fused})$$
 Onde $\hat{y}$ é a classe predita final e $P(y = \hat{y} \mid \vec{x}_{fused})$ é o score de confiança exibido no dashboard.

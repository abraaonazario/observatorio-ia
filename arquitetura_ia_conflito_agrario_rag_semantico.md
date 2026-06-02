# Arquitetura de IA para Classificação Semântica de Notícias Agrárias

## Visão Geral

O sistema proposto tem como objetivo transformar notícias relacionadas ao contexto agrário em inteligência estruturada, utilizando técnicas de Processamento de Linguagem Natural (NLP), embeddings vetoriais e classificação semântica.

A arquitetura realiza:

- ingestão de notícias;
- quebra semântica em chunks;
- geração de embeddings;
- indexação vetorial;
- associação automática com ações derivadas e ações matriz;
- classificação contextual;
- análise territorial e temática.

---

# Objetivo Estratégico

Construir uma IA capaz de:

- compreender semanticamente notícias agrárias;
- identificar padrões de conflitos;
- classificar ações de movimentos sociais;
- relacionar territórios, pautas e movimentos;
- gerar inteligência analítica para monitoramento agrário.

---

# Arquitetura Geral

```text
                ┌──────────────────────┐
                │ Fontes de Notícias 
                  Agrário 
                  (om 484 
                  registros) │
                │ PDFs │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Pipeline de Ingestão │
                │ ETL + Normalização   │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Chunking Semântico   │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Geração Embeddings   │
                │ BGE-M3 / E5          │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Banco Vetorial       │
                │ Qdrant / Chroma      │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Matching Semântico   │
                │ Similaridade Vetorial│
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Classificação Final  │
                │ Ação Derivada        │
                │ Ação Matriz          │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Dashboard Analítico  │
                │ Observatório IA      │
                └──────────────────────┘
```
- **Fontes de Notícias:** planilha com 482 registros (PDFs / Sites / RSS).
---

# Estrutura dos Dados da Planilha

A planilha representa uma base semiestruturada de eventos agrários.

## Principais campos utilizados

| Campo | Finalidade |
|---|---|
| Título da notícia | Texto principal |
| Pauta da ação | Contexto semântico |
| Ação Matriz | Macro classificação |
| Ação derivada | Classe específica |
| Finalidade da ação | Complemento contextual |
| Movimento | Entidade social |
| Estado | Geolocalização |
| Município | Contexto territorial |
| Data | Temporalidade |

---

# Camada 1 — Ingestão de Dados

## Entrada

O sistema pode consumir:

- planilhas XLSX;
- PDFs;
- notícias web;
- RSS;
- APIs;
- documentos institucionais.

## Pipeline ETL

### Etapas

1. leitura do arquivo;
2. limpeza textual;
3. normalização;
4. deduplicação;
5. enriquecimento semântico.

---

# Camada 2 — Pré-processamento NLP

## Limpeza

Aplicar:

- lowercase;
- remoção de caracteres especiais;
- normalização unicode;
- remoção de ruído.

## Exemplo

```python
texto = texto.lower()
```

---

# Camada 3 — Chunking Semântico

## Objetivo

Dividir notícias longas em unidades semanticamente coerentes.

## Estratégia Recomendada

### Recursive Semantic Chunking

Parâmetros:

| Parâmetro | Valor sugerido |
|---|---|
| chunk_size | 500 |
| overlap | 50 |

## Exemplo

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_text(texto)
```

---

# Camada 4 — Geração de Embeddings

## Objetivo

Converter chunks textuais em vetores numéricos de alta dimensionalidade.

## Modelos Recomendados

### Open Source

| Modelo | Vantagem |
|---|---|
| BAAI/bge-m3 | Excelente multilíngue |
| multilingual-e5-large | Alta precisão |
| paraphrase-multilingual-mpnet-base-v2 | Boa performance PT-BR |

## Modelo Recomendado

### BGE-M3

Motivos:

- excelente para português;
- captura semântica robusta;
- funciona bem em classificação;
- ótimo para RAG.

---

# Camada 5 — Banco Vetorial

## Objetivo

Armazenar embeddings para busca semântica.

## Banco Recomendado

### Qdrant

Vantagens:

- alta performance;
- filtros por metadata;
- escalável;
- open source;
- integração com LangChain.

## Estrutura do Documento Vetorial

```json
{
  "id": "chunk_001",
  "texto": "ocupação de fazenda em Rondônia...",
  "embedding": [0.23, 0.91, ...],
  "metadata": {
    "estado": "RO",
    "municipio": "Corumbiara",
    "movimento": "LCP",
    "acao_matriz": "Mobilização",
    "acao_derivada": "Ocupação"
  }
}
```

---

# Camada 6 — Modelagem das Ações

## Problema

Não basta gerar embeddings apenas do nome da ação.

Exemplo ruim:

```text
NOTA DE REPÚDIO
```

## Solução

Enriquecimento semântico.

## Exemplo correto

```json
{
  "acao": "NOTA DE REPÚDIO",
  "descricao": "manifestação institucional de crítica, denúncia ou oposição relacionada a violência, repressão ou conflito agrário"
}
```

---

# Camada 7 — Similaridade Vetorial

## Objetivo

Associar chunks às ações mais semanticamente próximas.

## Técnica

### Similaridade Cosseno

```python
from sklearn.metrics.pairwise import cosine_similarity
```

## Exemplo

```python
similaridade = cosine_similarity(
    [embedding_chunk],
    [embedding_acao]
)
```

---

# Estratégia de Classificação

## Fase 1 — Recuperação Vetorial

A IA busca:

- top-k ações semelhantes;
- eventos correlacionados;
- padrões históricos.

## Fase 2 — Re-ranking

Classificador supervisionado:

| Modelo | Uso |
|---|---|
| XGBoost | baseline |
| LightGBM | classificação rápida |
| BERT Fine-tuning | máxima precisão |

## Entrada do modelo

- embedding do chunk;
- estado;
- pauta;
- movimento;
- similaridades vetoriais;
- contexto temporal.

## Saída

- ação derivada;
- ação matriz;
- score de confiança.

---

# Pipeline Completo

```text
NOTÍCIA
   ↓
Limpeza textual
   ↓
Chunking semântico
   ↓
Embeddings
   ↓
Indexação vetorial
   ↓
Busca semântica
   ↓
Similaridade com ações
   ↓
Classificador supervisionado
   ↓
Ação derivada final
```

---

# Metadados Estratégicos

Além do texto, o sistema deve utilizar:

| Campo | Valor Analítico |
|---|---|
| Movimento | Identificação política |
| Estado | Mapeamento territorial |
| Município | Hotspots de conflito |
| Data | Séries temporais |
| Finalidade | Motivação da ação |
| Pauta | Agrupamento temático |

---

# Inteligência Territorial

A IA poderá gerar:

- mapas de conflito agrário;
- análise temporal;
- frequência de ocupações;
- redes de movimentos sociais;
- detecção de escalada de tensão;
- agrupamentos territoriais.

---

# Arquitetura Tecnológica

| Camada | Tecnologia |
|---|---|
| NLP | spaCy |
| Embeddings | Sentence Transformers |
| Vetores | Qdrant |
| API | FastAPI |
| Pipeline | LangChain |
| Dashboard | Streamlit |
| Banco relacional | PostgreSQL |
| Treinamento | PyTorch |

---

# Estrutura Recomendada do Projeto

```text
agrarian-ai/
│
├── data/
├── ingestion/
├── preprocessing/
├── embeddings/
├── vector_db/
├── training/
├── api/
├── dashboard/
├── notebooks/
└── models/
```

---

# Estratégia de Evolução

## MVP

- embeddings;
- similaridade;
- classificação básica.

## Versão 2

- aprendizado supervisionado;
- painel analítico;
- filtros territoriais.

## Versão 3

- Knowledge Graph;
- detecção de padrões;
- previsão de conflitos.

---

# Knowledge Graph Futuro

## Entidades

- movimentos;
- territórios;
- lideranças;
- conflitos;
- ações;
- instituições.

## Relações

- ocupa;
- denuncia;
- protesta;
- reivindica;
- confronta.

---

# Resultado Esperado

O sistema funcionará como um:

## Observatório Inteligente do Conflito Agrário

Capaz de:

- classificar automaticamente notícias;
- compreender semântica agrária;
- detectar padrões;
- gerar inteligência territorial;
- apoiar monitoramento estratégico.

---

# Próxima Evolução Recomendada

## Implementar:

1. embeddings supervisionados;
2. fine-tuning contextual agrário;
3. ontologia temática;
4. RAG contextual;
5. GraphRAG;
6. painel geoespacial.

---

# Arquitetura Final Recomendada

## Modelo híbrido:

### Vetorial + Supervisionado + Knowledge Graph

Essa combinação entrega:

- compreensão semântica;
- contextualização territorial;
- explicabilidade;
- escalabilidade;
- inteligência analítica.


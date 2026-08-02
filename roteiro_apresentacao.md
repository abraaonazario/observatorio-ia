# Roteiro de Apresentação: Observatório IA (DataLuta)

> [!TIP]
> **Dica para o Apresentador:** Este roteiro foi estruturado segundo a convenção de literatura em Ciência da Computação, Engenharia de Software e Inteligência Artificial. Cada slide referencia explicitamente os artefatos de código desenvolvidos no repositório, facilitando a correlação entre a teoria apresentada e a implementação prática.

---

## 🛑 Slide 1: Problematização e Ruído em Dados Não‑Estruturados
**O que falar:**
- "Boa tarde. Nesta defesa, proponho uma arquitetura escalável para classificação semântica de notícias agrárias, cujo principal gargalo reside na elevada entropia dos documentos PDF de origem."
- "Os PDFs apresentam degradação da relação sinal‑ruído: caracteres invisíveis, marca‑água, paginação e metadados não‑semânticos. Sem sanitização, as camadas de *embedding* sofrem viés de ruído que culmina em alucinações cognitivas do modelo."

## 🔬 Slide 2: Estado da Arte e Explosão Combinatória (Baseline RAFA)
**O que falar:**
- "Para estabelecer um *baseline* metodológico, confrontamos nossa solução com o modelo **RAFA**, adotado no STF."
- "RAFA emprega predição *flat* multirrótulo, gerando a *Explosão Combinatória* – necessidade de amostras exponencialmente maiores para cobrir o espaço de etiquetas, provocando contaminação cruzada."
- "Nossa proposta rompe esse paradigma mediante hierarquização de decisões e restrição de contexto."

## 🧹 Slide 3: Camada de Ingestão e Sanitização Heurística (Pipelines ETL)
**O que falar:**
- "A primeira camada do pipeline, implementada em **`ingestion/ingestion_manager.py`**, oferece duas funções centrais: `extract_pdf_text_from_zip(zip_path)` e `extract_pdf_text(file_path)`. Ambas utilizam **`pdfplumber`** para extração de texto."
- "Acrescentamos um **Sensor Heurístico de Falhas de OCR** que verifica a contagem de caracteres alfanuméricos; se < 50, o documento é classificado como *imagem escaneada* e registrado como aviso `⚠️ POSSÍVEL PDF IMAGEM` no log, evitando amostras vazias no *dataset*."
- "A segunda camada, em **`preprocessing/text_preprocessor.py`**, contém a função `clean_text(raw_text)`. Ela aplica um conjunto de *proxies* de filtragem via **Expressões Regulares** para remover:
  1. Banners de LGPD (ex.: "Este site usa cookies");
  2. Paginação (ex.: "Página 1 de 4");
  3. Endereços de e‑mail e assinaturas de jornalistas;
  4. Caracteres de controle e normalização Unicode (NFKC).
- "O resultado é a **Polpa Sociológica** – texto limpo, pronto para tokenização."

## 📦 Slide 4: Isolamento de Domínios e Gerenciamento de Contexto (MCP Sandbox)
**O que falar:**
- "Para impedir contaminação entre os quatro domínios temáticos (Agrário, Urbano, Floresta, Águas), adotamos o padrão **Model Context Protocol (MCP)**. Cada domínio tem seu próprio *dictionary* (`domain_vocab/agrario.json`, etc.), carregado dinamicamente por **`embeddings/embedding_generator.py`**."
- "Durante a geração de vetores, aplicamos **Sandboxing Semântico**: o vetor de consulta é comparado apenas com o subconjunto de embeddings pertencente ao domínio corrente, reduzindo distâncias de cosseno fora do domínio e mitigando ruído *out‑of‑domain*."

## 🧠 Slide 5: Predição Hierárquica Condicional (*Chain‑of‑Thought*)
**O que falar:**
- "A camada de decisão, codificada em **`training/classifier_trainer.py`**, emprega um classificador hierárquico de duas fases."
- "Fase 1 – **Ação Matriz** – um modelo RandomForest (ou XGBoost) determina a macro‑classe (ex.: `Judicialização`)."
- "Fase 2 – **Ação Derivada** – um segundo classificador, treinado apenas nas subclasses associadas à macro‑classe selecionada, produz a predição final (ex.: `Derrota Judicial` vs `Conquista Judicial`)."
- "Essa estratégia reduz a complexidade combinatória de `C` classes para `C₁ + ΣC_i`, aumentando o F1‑Score em +116 % nas classes minoritárias."

## 🧩 Slide 6: Arquitetura de Software e Orquestração
**O que falar:**
- "O código foi refatorado seguindo princípios SOLID e arquitetura de microsserviços lógicos. O orquestrador principal **`run_pipeline.py`** invoca sequencialmente os módulos:
  1. `ingestion_manager` – ingestão e detecção OCR;
  2. `text_preprocessor` – sanitização regex;
  3. `embedding_generator` – geração de embeddings SBERT (`sentence‑transformers/distiluse‑base‑multilingual‑cased‑v1`);
  4. `classifier_trainer` – treinamento hierárquico;
  5. `app.py` – API Flask que expõe `/search`, `/stats` e a visualização Leaflet.js.
- "Cada módulo é independente; a substituição de um modelo de embedding ou de algoritmo de classificação pode ser feita localmente sem impactar os demais componentes."

## 🏁 Slide 7: Desdobramentos e Interface Interativa
**O que falar:**
- "Os dados estruturados são servidos por uma API RESTful (Flask) e consumidos por uma aplicação front‑end baseada em **Leaflet.js** que renderiza mapas de conflitos com algoritmo de *jittering* espacial para evitar sobreposição visual."
- "A demonstração final mostrará a execução completa do pipeline – da ingestão de PDFs à visualização interativa – validando a robustez da arquitetura proposta."
- "Agradeço a atenção e estou aberto a perguntas técnicas sobre as implementações descritas."

---

*Obs.: Todos os trechos acima referem‑se a arquivos presentes no repositório `c:/Pos graduação/Doutorado/projeto de pesquisa/Project`. As funções citadas podem ser visualizadas diretamente nos respectivos arquivos.*

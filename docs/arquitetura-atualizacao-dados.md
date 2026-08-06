# Arquitetura de Atualização e Integração de Dados

Esta documentação detalha a arquitetura recomendada para a ingestão de dados de sistemas transacionais e a atualização automática do nosso painel estático (MkDocs) construído para o **Data Lake**.

O objetivo principal desta arquitetura é garantir que o painel de indicadores (Dashboard) seja atualizado de forma contínua e escalável, **sem onerar os sistemas transacionais (OLTP)** de secretarias, ERPs ou sistemas de saúde.

---

## 1. Fluxo Macro de Dados

A arquitetura foi desenhada em três grandes etapas (Extração, Processamento e Consumo):

```mermaid
flowchart LR
    subgraph Transacional
        DB[(Banco de Dados\n(ERP, Saúde, RH))]
    end

    subgraph Data Lake
        B[Camada Bronze\n(Raw Data)] --> S[Camada Prata\n(Limpeza)]
        S --> G[Camada Ouro\n(Agregações)]
    end
    
    subgraph Front-End
        MK[MkDocs\n(Painéis Estáticos)]
        JS[JavaScript\n(Real-Time API)]
    end

    DB -- CDC ou Batch (D-1) --> B
    G -- "Python Script (Build)" --> MK
    G -- "JSON API" --> JS
```

---

## 2. Padrões de Extração (Evitando queda do Transacional)

Nunca devemos conectar o painel diretamente ao banco de dados do sistema transacional para consultas em tempo real. Os bancos OLTP não são otimizados para cargas analíticas (OLAP).

Utilizamos duas estratégias de extração para popular a nossa **Camada Bronze**:

1. **Extração Batch (D-1):** 
   - Ideal para dados financeiros, de população ou RH.
   - Um orquestrador (como Apache Airflow) roda de madrugada e puxa apenas os dados atualizados do dia anterior.
2. **CDC (Change Data Capture):** 
   - Ideal para dados críticos quase em tempo real (ex: leitos de hospital ocupados).
   - Ferramentas como **Debezium** acopladas a um **Apache Kafka** leem os *logs* de transação do banco sem sobrecarregá-lo, enviando eventos imediatamente para o Data Lake.

---

## 3. As Três Opções para Atualizar o Dashboard

Uma vez que os dados estão tratados e sumarizados na nossa **Camada Ouro** (Gold), temos três caminhos para refletir isso no painel MkDocs.

### Opção A: O "Robô" Gerador de Markdown (Recomendado)
A melhor opção para dados que atualizam diariamente ou mensalmente.
- O orquestrador de dados extrai os indicadores da Camada Ouro em formato CSV.
- Um script em **Python** é executado. Ele lê o CSV, substitui as variáveis-chave dentro dos nossos arquivos `.md` (Markdown) ou injeta os dados usando a biblioteca `Jinja2`.
- Ao final, o script roda o comando `mkdocs build` e realiza o deploy no servidor web.
- **Vantagem:** O site continua hiper-rápido (pois já nasce pronto como HTML puro) e 100% seguro contra invasões.

### Opção B: Integração Nativa via MkDocs Macros
Permite que o MkDocs leia fontes de dados nativamente durante a sua compilação.
- Instalamos o plugin `mkdocs-macros-plugin`.
- Ao invés de escrevermos tabelas fixas (Hardcoded) no Markdown, criamos loops (`{% for item in dados %}`).
- O plugin lê um CSV/JSON do Data Lake no momento do *build* e monta as tabelas.
- **Vantagem:** Separa completamente o texto/design dos dados brutos. Para atualizar, basta que o Data Lake sobrescreva o arquivo CSV na pasta do projeto.

### Opção C: Consumo via JavaScript no Navegador (Tempo Real)
A única opção viável para dados que mudam a cada hora ou segundo.
- Deixamos a estrutura do HTML (gráficos e tabelas) vazia no arquivo Markdown.
- O Data Lake precisa fornecer uma **API REST** ou um arquivo `dados.json` leve hospedado via CDN.
- Nosso script (`dashboard.js`) faz um `fetch()` assim que a tela abre, consultando o JSON e desenhando o gráfico instantaneamente.
- **Vantagem:** Atualização em tempo real sem precisar recompilar todo o site MkDocs.

---

## 4. Conclusão

Para um ecossistema focado no Governo ou num painel executivo (Observatório), recomendamos padronizar a maior parte do projeto na **Opção B (Macros)**, pois ela une o melhor de dois mundos: **escalabilidade para o time de Engenharia de Dados** e **performance imbatível para o Prefeito ou Gestor** que vai acessar o painel pelo celular. Apenas reserve a Opção C para casos onde o tempo real for o requisito número 1.

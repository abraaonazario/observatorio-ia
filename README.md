# 🌐 MT 360º

Bem-vindo ao repositório do **MT 360º**! Este é o portal de documentação e painéis interativos desenvolvido com [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

Abaixo você encontra um passo a passo completo de como instalar, visualizar e atualizar o projeto na sua máquina.

---

## 🚀 1. Pré-requisitos

Para rodar este projeto localmente, você precisa ter instalados no seu computador:

- **Python** (versão 3.8 ou superior)
- **Git** (para controle de versão)

---

## 💻 2. Como Rodar o Projeto Localmente

Siga os passos abaixo para iniciar o servidor de desenvolvimento:

1. **Abra o terminal (ou PowerShell)** na pasta raiz do projeto.
2. *(Opcional, mas recomendado)* Ative seu ambiente virtual caso esteja usando um:
   ```bash
   # No Windows
   venv\Scripts\activate
   ```
3. Instale as dependências (MkDocs e Material Theme), caso ainda não tenha feito:
   ```bash
   pip install mkdocs-material
   ```
4. Inicie o servidor local:
   ```bash
   mkdocs serve
   ```
5. Abra o seu navegador e acesse: `http://127.0.0.1:8000`. O site será atualizado automaticamente toda vez que você salvar um arquivo!

---

## 📝 3. Como Editar o Conteúdo

Toda a estrutura do site está organizada dentro da pasta `docs/`.

- **Página Inicial:** Fica em `docs/index.md`.
- **Dashboards/Painéis:** Arquivos como `saude.md`, `seguranca.md`, `educacao.md`, etc., ficam dentro de `docs/`.
- **Menus e Layout:** Se quiser adicionar novas páginas, você deve criar o arquivo `.md` e depois registrá-lo no arquivo `mkdocs.yml` (na seção `nav:`).
- **Estilos Visuais (CSS):** Ficam em `docs/stylesheets/`.

---

## ☁️ 4. Como Salvar e Enviar Atualizações (GitHub)

Sempre que você fizer alterações nos arquivos e quiser salvar na nuvem (GitHub), siga este roteiro no terminal:

1. **Verifique o que foi modificado:**
   ```bash
   git status
   ```

2. **Adicione as alterações ao pacote de envio:**
   ```bash
   git add .
   ```

3. **Crie um "pacote" com uma mensagem explicando o que você fez:**
   ```bash
   git commit -m "Explique aqui o que você alterou. Ex: Atualizei os dados da saúde"
   ```

4. **Envie para o GitHub:**
   ```bash
   git push origin main
   ```

*(Se pedir login, insira suas credenciais do GitHub).*

---

### ❓ Dúvidas Comuns
- **O site parou de rodar?** Verifique se o terminal com `mkdocs serve` não foi fechado acidentalmente.
- **Não está atualizando visualmente?** Pode ser o cache do navegador. Pressione `Ctrl + F5` (ou `Shift + F5`) na página para forçar o recarregamento.

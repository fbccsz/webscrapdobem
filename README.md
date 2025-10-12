# Painel de Informações de Perfis Específicos do Instagram

Uma aplicação web construída com Streamlit que coleta e exibe os posts mais recentes de perfis específicos do Instagram. Os dados são coletados de forma confiável através da API da Apify e apresentados em uma interface limpa e interativa.

![Screenshot da Aplicação](https://i.imgur.com/GWYly5b.png)

---

## ✨ Funcionalidades

- **Coleta de Dados Confiável:** Utiliza a plataforma Apify para extrair dados do Instagram, evitando bloqueios de IP e problemas de ambiente.
- **Interface Interativa:** Construída com Streamlit para uma experiência de usuário fluida e responsiva.
- **Cache Inteligente:** Os dados são coletados periodicamente, garantindo performance sem sobrecarregar a API.
- **Filtro Dinâmico:** Permite ao usuário selecionar quais perfis deseja visualizar na barra lateral.
- **Visualização Completa:** Exibe a imagem do post, legenda e um link direto para a publicação original.

---

## 🛠️ Tecnologias Utilizadas

- **Python:** Linguagem principal do projeto.
- **Streamlit:** Para a construção da interface web interativa.
- **Apify Client:** Para interagir com a API da Apify e coletar os dados.
- **Pandas:** Para manipulação e estruturação dos dados.
- **SQLite:** Como banco de dados local para armazenar os posts coletados pela aplicação na nuvem.

---

## 🚀 Como Executar Localmente

Siga estes passos para rodar o projeto na sua própria máquina.

### 1. Pré-requisitos

- Python 3.8+
- Git
- Uma conta gratuita na [Apify](https://apify.com/) para obter seu Token de API pessoal.

### 2. Configuração do Ambiente

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/fbccsz/webscrapdobem.git
    cd webscrapdobem
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # No Windows
    python -m venv .venv
    ./.venv/Scripts/activate

    # No macOS / Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuração dos Segredos (API Token)

Para rodar localmente, o Streamlit precisa de um lugar para ler seus segredos (rsrs), assim como ele faz na nuvem.

1.  Na pasta raiz do seu projeto, crie uma nova pasta chamada `.streamlit`.
2.  Dentro da pasta `.streamlit`, crie um arquivo chamado `secrets.toml`.
3.  Abra o arquivo `secrets.toml` e adicione sua chave da Apify no seguinte formato:

    ```toml
    # .streamlit/secrets.toml

    APIFY_TOKEN = "sua_chave_da_apify_aqui"
    ```

O arquivo `.gitignore` já está configurado para nunca enviar esta pasta para o GitHub.

### 4. Executando a Aplicação

Com tudo configurado, inicie o servidor do Streamlit com um único comando:

```bash
streamlit run app.py

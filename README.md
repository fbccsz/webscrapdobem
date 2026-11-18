<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Apify-00C853?style=for-the-badge&logo=apify&logoColor=white" alt="Apify"/>
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"/>
  <img src="https://img.shields.io/github/license/fbccsz/webscrapdobem?style=for-the-badge" alt="License"/>
</p>

<h1 align="center">🌐 WebScrap do Bem</h1>

<p align="center">
  Painel de publicações do Instagram com coleta via Apify, filtros por perfil e cache SQLite.<br/>
  <em>Instagram publication dashboard with Apify scraping, profile filters, and SQLite caching.</em>
</p>

<p align="center">
  <a href="https://www.yshdev.me/#projects"><strong>Portfólio</strong></a> · <a href="mailto:yshdev@outlook.com"><strong>Contato / Contact</strong></a>
</p>

---

## 🇧🇷 Sobre o Projeto

Ferramenta local que centraliza e exibe publicações de perfis do Instagram em um painel interativo. A coleta de dados é feita pela API da **Apify**, os registros são armazenados em **SQLite** (como cache inteligente) e a interface é construída com **Streamlit**.

### ✨ Funcionalidades

- 📊 **Painel interativo** — Exibe imagens, legendas e links das publicações
- 🔎 **Filtros por perfil** — Barra lateral para selecionar perfis de interesse
- 🗄️ **Cache SQLite** — Armazena os dados localmente e atualiza automaticamente a cada hora
- 🛡️ **Resiliência** — Preserva dados anteriores quando a API falha
- ⚡ **Configurável** — Perfis-alvo ajustáveis diretamente no código

## 🇺🇸 About the Project

A local tool that aggregates and displays Instagram profile publications on an interactive dashboard. Data collection is powered by the **Apify** API, records are stored in **SQLite** (as a smart cache), and the interface is built with **Streamlit**.

### ✨ Features

- 📊 **Interactive dashboard** — Displays images, captions, and post links
- 🔎 **Profile filters** — Sidebar to select profiles of interest
- 🗄️ **SQLite cache** — Stores data locally with automatic hourly refresh
- 🛡️ **Resilience** — Preserves previous data when the API fails
- ⚡ **Configurable** — Target profiles easily adjustable in code

---

## 🛠️ Tech Stack / Tecnologias

| Componente / Component | Tecnologia / Technology |
| :--- | :--- |
| Linguagem / Language | Python 3.11+ |
| Interface / UI | Streamlit |
| Coleta / Scraping | Apify Client |
| Dados / Data | Pandas |
| Persistência / Storage | SQLite |
| HTTP | Requests |

---

## 🚀 Getting Started / Executar Localmente

### Pré-requisitos / Prerequisites

- Python 3.11+
- Git
- Conta na [Apify](https://apify.com/) com token de API / Apify account with API token

### Instalação / Installation

```bash
# Clone o repositório / Clone the repository
git clone https://github.com/fbccsz/webscrapdobem.git
cd webscrapdobem

# Crie o ambiente virtual / Create virtual environment
python -m venv .venv

# Ative o ambiente / Activate it
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Instale as dependências / Install dependencies
pip install -r requirements.txt
```

### ⚙️ Configuração / Configuration

Crie o arquivo de segredos do Streamlit / Create the Streamlit secrets file:

```bash
mkdir -p .streamlit
```

```toml
# .streamlit/secrets.toml
APIFY_TOKEN = "seu_token_da_apify"
```

Ajuste os perfis-alvo em `app.py` / Adjust target profiles in `app.py`:

```python
PERFIS_ALVO = ["dalc.ufba", "ufba.oficial", "computacaoufba"]
```

### ▶️ Execução / Run

```bash
streamlit run app.py
```

O painel abrirá automaticamente em `http://localhost:8501`.  
The dashboard will open automatically at `http://localhost:8501`.

---

## 📦 Fluxo de Dados / Data Flow

```
Perfis Instagram ──► Apify API ──► Normalização ──► SQLite (cache)
                                                        │
                                              Streamlit ◄┘ ──► Filtros ──► Painel
```

- O cache é atualizado automaticamente quando o banco não existe, está vazio ou tem mais de **1 hora**.
- Em hospedagens com disco temporário (ex.: Streamlit Cloud), os dados podem ser perdidos após reinicializações.
- O arquivo `instagram_data.db` é criado automaticamente e **não deve ser commitado**.

---

## 📁 Estrutura / Project Structure

```
webscrapdobem/
├── .devcontainer/        # Configuração do Codespace
│   └── devcontainer.json
├── .gitignore            # Exclusão de segredos e arquivos locais
├── app.py                # Coleta, cache, banco e interface
├── requirements.txt      # Dependências Python
├── LICENSE               # MIT License
├── README.md             # Documentação
└── SECURITY.md           # Política de segurança
```

---

## 📄 Licença / License

Distribuído sob a licença **MIT**. Veja [`LICENSE`](LICENSE) para mais detalhes.  
Distributed under the **MIT** License. See [`LICENSE`](LICENSE) for details.

---

<p align="center">
  Feito por <strong><a href="https://www.yshdev.me/">ysh</a></strong> · 
  <a href="mailto:yshdev@outlook.com">yshdev@outlook.com</a>
</p>

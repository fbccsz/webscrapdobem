# WebScrap do Bem

**Status:** Ferramenta local de coleta e visualização de dados.

Painel em Python para reunir e explorar publicações de perfis do Instagram. A coleta usa a API da Apify; a interface Streamlit organiza imagens, legendas e links em uma visualização com filtros por perfil.

**[Portfólio](https://www.yshdev.me/#projects)** · **[Contato](mailto:yshdev@outlook.com)**

## O que o projeto faz

- Centraliza publicações dos perfis definidos em `PERFIS_ALVO`.
- Permite filtrar os resultados pela origem na barra lateral.
- Armazena os registros em SQLite e trata os dados com Pandas.
- Atualiza a coleta quando o banco não existe, está vazio ou tem mais de uma hora.
- Preserva os dados válidos anteriores quando a Apify falha ou não retorna publicações.

## Tecnologias

| Componente | Tecnologia |
| --- | --- |
| Aplicação | Python |
| Interface | Streamlit |
| Coleta | Apify Client |
| Tratamento | Pandas |
| Persistência local | SQLite |
| Imagens remotas | Requests |

## Executar localmente

Requisitos: Python, Git e uma conta Apify com token de API.

```sh
git clone https://github.com/fbccsz/webscrapdobem.git
cd webscrapdobem
python -m venv .venv
```

Ative o ambiente virtual:

```sh
# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```sh
python -m pip install -r requirements.txt
```

Crie `.streamlit/secrets.toml` e configure seu próprio token:

```toml
APIFY_TOKEN = "seu_token_da_apify"
```

A pasta de segredos deve permanecer fora do versionamento. Ajuste `PERFIS_ALVO` em `app.py` conforme a finalidade da coleta e inicie a aplicação:

```sh
streamlit run app.py
```

## Testes

Os testes de persistência usam somente a biblioteca padrão do Python e não
exigem token Apify, conexão com a internet ou instalação do Streamlit:

```sh
python -m unittest discover -s tests -v
```

Eles verificam a substituição do cache, a deduplicação dos posts e o rollback
que preserva os registros anteriores em caso de erro durante a gravação.

## Fluxo de dados

A aplicação verifica o cache local, consulta a Apify quando uma atualização é necessária e normaliza os posts antes de gravar no SQLite. O Streamlit lê o banco e aplica os filtros escolhidos pelo visitante.

O arquivo `instagram_data.db` é criado automaticamente e não deve ser commitado. Em hospedagens com disco temporário, incluindo Streamlit Cloud, os dados podem desaparecer após reinicializações; esse armazenamento funciona como cache, sem garantia de persistência durável.

## Estrutura

| Arquivo | Responsabilidade |
| --- | --- |
| `app.py` | Coleta, cache, banco e interface |
| `requirements.txt` | Dependências Python |
| `.gitignore` | Exclusão de segredos e arquivos locais |

## Manutenção

Mantido por **ysh** · [Portfólio](https://www.yshdev.me/) · [Contato](mailto:yshdev@outlook.com)


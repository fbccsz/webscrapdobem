import streamlit as st
import pandas as pd
import sqlite3
import os
import requests
from apify_client import ApifyClient
import time

# --- CONFIGURAÇÃO ---
PERFIS_ALVO = ["dalc.ufba", "ufba.oficial", "computacaoufba"]
NOME_BANCO_DADOS = "instagram_data.db"

def inicializar_banco():
    conn = sqlite3.connect(NOME_BANCO_DADOS)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            shortcode TEXT PRIMARY KEY, profile TEXT, caption TEXT,
            likes INTEGER, comments INTEGER, post_date TEXT, url TEXT, image_url TEXT
        )
    ''')
    conn.commit()
    return conn

def coletar_dados_apify():
    conn = inicializar_banco()
    conn.close()

    apify_token = st.secrets.get("APIFY_TOKEN", "")
    if not apify_token:
        return (False, "ERRO: Token da Apify não encontrado nos Secrets do Streamlit.")

    try:
        client = ApifyClient(apify_token)
        run_input = {"usernames": PERFIS_ALVO, "resultsLimit": 7}
        run = client.actor("apify/instagram-profile-scraper").call(run_input=run_input)
        lista_de_perfis = client.dataset(run["defaultDatasetId"]).list_items().items
    except Exception as e:
        return (False, f"Falha ao contatar a Apify: {e}")

    posts = []
    for item in lista_de_perfis:
        perfil_username = item.get("username")
        itens = item.get("latestPosts")
        if isinstance(itens, list):
            posts.extend((perfil_username, post) for post in itens)
        elif item.get("shortCode"):
            posts.append((perfil_username or item.get("ownerUsername"), item))

    if not posts:
        chaves = sorted(lista_de_perfis[0].keys()) if lista_de_perfis else []
        return (False, f"A Apify concluiu, mas não retornou posts. Chaves recebidas: {chaves}")

    conn = sqlite3.connect(NOME_BANCO_DADOS)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS posts")
    cursor.execute('''
        CREATE TABLE posts (
            shortcode TEXT PRIMARY KEY, profile TEXT, caption TEXT,
            likes INTEGER, comments INTEGER, post_date TEXT, url TEXT, image_url TEXT
        )
    ''')
    posts_salvos_total = 0
    for perfil_username, post in posts:
        cursor.execute(
            'INSERT OR IGNORE INTO posts VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (post.get("shortCode"), perfil_username or post.get("ownerUsername"), post.get("caption"),
             post.get("likesCount", 0), post.get("commentsCount", 0),
             post.get("timestamp"), post.get("url"), post.get("displayUrl"))
        )
        posts_salvos_total += cursor.rowcount

    conn.commit()
    conn.close()
    return (True, f"Coleta finalizada! {posts_salvos_total} posts salvos.")

def carregar_dados_do_banco():
    """
    Gerencia a coleta e a leitura, sem ele a bomba dos creditos da apify vão pro ralo meio que ele serve de cache.
    """
    precisa_coletar = not os.path.exists(NOME_BANCO_DADOS)
    if not precisa_coletar:
        try:
            conn = sqlite3.connect(NOME_BANCO_DADOS)
            tabela_vazia = conn.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='posts'"
            ).fetchone()[0] == 0 or conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0] == 0
            conn.close()
            precisa_coletar = tabela_vazia or time.time() - os.path.getmtime(NOME_BANCO_DADOS) > 3600
        except sqlite3.Error:
            precisa_coletar = True

    if precisa_coletar:
        try:
            with st.spinner("Buscando novos dados da Apify..."):
                sucesso, mensagem = coletar_dados_apify()
                if sucesso:
                    st.toast(mensagem, icon="🎉")
                else:
                    st.error(mensagem)
        except Exception as e:
            st.error(f"Falha ao iniciar a coleta: {e}")

    if not os.path.exists(NOME_BANCO_DADOS):
        return pd.DataFrame()
    try:
        conn = sqlite3.connect(NOME_BANCO_DADOS, check_same_thread=False)
        df = pd.read_sql_query("SELECT * FROM posts ORDER BY post_date DESC", conn)
        conn.close()
        if not df.empty:
            df['post_date'] = pd.to_datetime(df['post_date'], errors='coerce')
            df = df.dropna(subset=['post_date'])
        return df
    except Exception:
        return pd.DataFrame()

st.set_page_config(layout="wide", page_title="Painel de Informações")
st.title("Informações")

def fetch_image(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.content
    except Exception:
        return None

df = carregar_dados_do_banco()

if df.empty:
    st.error("Nenhum dado para exibir. A coleta pode ter falhado. Verifique os logs no Streamlit Cloud.")
else:
    st.sidebar.header("Filtros")
    perfis_disponiveis = sorted(df['profile'].unique())
    perfis_selecionados = st.sidebar.multiselect(
        "Filtrar por Perfil:",
        options=perfis_disponiveis,
        default=perfis_disponiveis
    )

    if not perfis_selecionados:
        st.warning("Selecione ao menos um perfil no filtro lateral.")
    else:
        df_filtrado = df[df['profile'].isin(perfis_selecionados)]

        st.markdown(f"### Exibindo `{len(df_filtrado)}` posts:")

        for index, post in df_filtrado.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    st.subheader(f"@{post['profile']}")
                    st.caption(f"Publicado em: {post['post_date'].strftime('%d/%m/%Y às %H:%M')}")
                with col2:
                    st.link_button("Ver no Instagram ↗️", post['url'])

                image_url = post.get('image_url')
                if isinstance(image_url, str) and image_url.startswith('http'):
                    image_data = fetch_image(image_url)
                    if image_data:
                        st.image(image_data, width=500)

                if post['caption']:
                    with st.expander("Ler legenda completa"):

                        st.write(post['caption'])


                # Opcional - Só tirar o comentário dos de baixo que funciona :)

                # metric_cols = st.columns(2)
                # metric_cols[0].metric("❤️ Likes", f"{post.get('likes', 0):,}")
                # metric_cols[1].metric("💬 Comentários", f"{post.get('comments', 0):,}")



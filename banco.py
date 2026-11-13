"""Persistência SQLite dos posts coletados, com atualização transacional."""

import sqlite3

NOME_BANCO_DADOS = "instagram_data.db"

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS posts (
    shortcode TEXT PRIMARY KEY, profile TEXT, caption TEXT,
    likes INTEGER, comments INTEGER, post_date TEXT,
    url TEXT, image_url TEXT
)
"""


def inicializar_banco(caminho=NOME_BANCO_DADOS):
    """Garante o esquema do cache e devolve uma conexão aberta."""
    conn = sqlite3.connect(caminho)
    try:
        conn.execute(CRIAR_TABELA)
        conn.commit()
    except Exception:
        conn.close()
        raise
    return conn


def substituir_posts(posts, caminho=NOME_BANCO_DADOS):
    """Substitui o cache somente após todas as inserções terem sucesso."""
    conn = inicializar_banco(caminho)
    try:
        conn.execute("DELETE FROM posts")
        salvos = 0
        for perfil, post in posts:
            cursor = conn.execute(
                "INSERT OR IGNORE INTO posts VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (post.get("shortCode"), perfil or post.get("ownerUsername"),
                 post.get("caption"), post.get("likesCount", 0),
                 post.get("commentsCount", 0), post.get("timestamp"),
                 post.get("url"), post.get("displayUrl")),
            )
            salvos += cursor.rowcount
        conn.commit()
        return salvos
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

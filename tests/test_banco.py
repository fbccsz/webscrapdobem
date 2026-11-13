"""Testes da persistência que não dependem de Streamlit nem de credenciais."""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from banco import substituir_posts


class TesteBanco(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)
        self.caminho = str(Path(self.pasta.name) / "cache.db")

    def ler_shortcodes(self):
        with sqlite3.connect(self.caminho) as conn:
            return [item[0] for item in conn.execute("SELECT shortcode FROM posts ORDER BY shortcode")]

    def test_substitui_cache_em_uma_transacao(self):
        primeiro = [("perfil-1", {"shortCode": "a1", "likesCount": 10})]
        segundo = [("perfil-2", {"shortCode": "b2", "likesCount": 20})]
        self.assertEqual(substituir_posts(primeiro, self.caminho), 1)
        self.assertEqual(substituir_posts(segundo, self.caminho), 1)
        self.assertEqual(self.ler_shortcodes(), ["b2"])

    def test_falha_na_gravacao_preserva_posts_anteriores(self):
        substituir_posts([("perfil-1", {"shortCode": "a1"})], self.caminho)
        with self.assertRaises(AttributeError):
            substituir_posts([
                ("perfil-2", {"shortCode": "b2"}),
                ("perfil-invalido", None),
            ], self.caminho)
        self.assertEqual(self.ler_shortcodes(), ["a1"])

    def test_post_duplicado_na_mesma_coleta_e_ignorado(self):
        registro = ("perfil", {"shortCode": "repetido"})
        self.assertEqual(substituir_posts([registro, registro], self.caminho), 1)
        self.assertEqual(self.ler_shortcodes(), ["repetido"])


if __name__ == "__main__":
    unittest.main()

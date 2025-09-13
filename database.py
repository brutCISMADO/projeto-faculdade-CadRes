import sqlite3
from typing import List, Optional

class Database:
    def __init__(self, db_path: str = "restaurantes.db"):
        self.db_path = db_path
        # check_same_thread=False para usar a conexão no Flask em modo debug/threaded
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS restaurantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            ativo INTEGER NOT NULL DEFAULT 1
        );
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

    def obter_restaurantes(self) -> List[sqlite3.Row]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, nome, categoria, ativo FROM restaurantes ORDER BY id DESC")
        return cur.fetchall()

    def cadastrar_restaurante(self, nome: str, categoria: str) -> int:
        cur = self.conn.cursor()
        cur.execute("INSERT INTO restaurantes (nome, categoria, ativo) VALUES (?, ?, 1)", (nome, categoria))
        self.conn.commit()
        return cur.lastrowid

    def obter_por_id(self, id: int) -> Optional[sqlite3.Row]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, nome, categoria, ativo FROM restaurantes WHERE id = ?", (id,))
        return cur.fetchone()

    def atualizar_restaurante(self, id: int, nome: str, categoria: str):
        cur = self.conn.cursor()
        cur.execute("UPDATE restaurantes SET nome = ?, categoria = ? WHERE id = ?", (nome, categoria, id))
        self.conn.commit()

    def alterar_estado(self, id: int, ativar: bool):
        cur = self.conn.cursor()
        cur.execute("UPDATE restaurantes SET ativo = ? WHERE id = ?", (1 if ativar else 0, id))
        self.conn.commit()

    def excluir_restaurante(self, id: int):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM restaurantes WHERE id = ?", (id,))
        self.conn.commit()

    def fechar_conexao(self):
        self.conn.close()

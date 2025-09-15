import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",          # seu usuário MySQL
            password="cismado",          # sua senha MySQL
            database="restaurantes"
        )
        self.cursor = self.conn.cursor(dictionary=True)  # retorna dicionários

    def fechar_conexao(self):
        self.cursor.close()
        self.conn.close()

    # CREATE
    def cadastrar_restaurante(self, nome, categoria):
        sql = "INSERT INTO restaurantes (nome, categoria, ativo) VALUES (%s, %s, 1)"
        self.cursor.execute(sql, (nome, categoria))
        self.conn.commit()

    # READ
    def obter_restaurantes(self):
        sql = "SELECT * FROM restaurantes"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def obter_por_id(self, id):
        sql = "SELECT * FROM restaurantes WHERE id=%s"
        self.cursor.execute(sql, (id,))
        return self.cursor.fetchone()

    # UPDATE
    def atualizar_restaurante(self, id, nome, categoria):
        sql = "UPDATE restaurantes SET nome=%s, categoria=%s WHERE id=%s"
        self.cursor.execute(sql, (nome, categoria, id))
        self.conn.commit()

    def alterar_estado(self, id, ativo=True):
        status = 1 if ativo else 0
        sql = "UPDATE restaurantes SET ativo=%s WHERE id=%s"
        self.cursor.execute(sql, (status, id))
        self.conn.commit()

    # DELETE
    def excluir_restaurante(self, id):
        sql = "DELETE FROM restaurantes WHERE id=%s"
        self.cursor.execute(sql, (id,))
        self.conn.commit()

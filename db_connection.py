import sqlite3 as sql

def connect_db():
    # Conecta ao banco de dados via SQLite
    connection = sql.connect("banco.db")
    print("Conectando ao banco de Dados\n")

    return connection

def get_db_cursor(connection):
    return connection.cursor()


def create_db():
    connection = connect_db()

    get_db_cursor(connection).execute(""" CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY, 
                nome_cliente CHAR(255) NOT NULL,
                telefone INTEGER(20) NOT NULL
                );
        """)
    connection.commit()

    print("Banco de Dados criado\n")
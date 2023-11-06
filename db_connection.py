import sqlite3 as sql

def connect_db():
    # Conecta ao banco de dados via SQLite
    connection = sql.connect("banco.db")
    print("Conectando ao banco de Dados\n")

    return connection

def get_db_cursor(connection):
    return connection.cursor()
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

    with open("banco.sql", "r") as banco:
        query=""

        for line in banco.readlines():
            query += f" {line}"
            if ";" in query:
                print(query)
                get_db_cursor(connection).execute(query)
                connection.commit()
                query = ""

              
    print("Banco de Dados criado\n")
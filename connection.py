import sqlite3 as sql

def connect_db():
    connection = sql.connect("banco.db")

    return connection
    print("Conectando ao banco de Dados\n")


def get_db_cursor(connection):
    return connection.cursor()


def create_db():
    connection = connect_db()

    with open("banco.sql", "r") as banco:
        query=""

        for line in banco.readlines():
            print(line)
            query += f" {line}"
            if ";" in query:
                print(query)
                get_db_cursor(connection).execute(query)
                connection.commit()
                query = ""

    print("Banco de Dados criado\n")

create_db()
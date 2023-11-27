import sqlite3 as sql
import re

TABLES = {}

def connect_db():
    connection = sql.connect("banco.db")

    return connection
    print("Conectando ao banco de Dados\n")


def get_db_cursor(connection):
    return connection.cursor()


def parse_sql(sql_statements):
    tables = {}
    current_table = None

    for statement in sql_statements:
        if statement.startswith('CREATE TABLE'):
            match = re.match(r'CREATE TABLE if NOT EXISTS (\w+) \(', statement)
            if match:
                current_table = match.group(1)
                tables[current_table] = []
        elif current_table and statement.strip().endswith(',') and statement.strip()[0] in "abcdefghijklmnopqrstuvwxyz":
            column_definition = statement.strip().rstrip(',').split()
            column_name = column_definition[0]
            tables[current_table].append(column_name)
        elif current_table and statement.strip().endswith(');'):
            current_table = None

    return tables


def create_db():
    connection = connect_db()

    with open("banco.sql", "r") as banco:
        query=""

        texto_banco = banco.readlines()

        for line in texto_banco:
            #print(line)
            query += f" {line}"
            if ";" in query:
                #print(query)
                get_db_cursor(connection).execute(query)
                connection.commit()
                query = ""

        print("Banco de Dados criado\n")

        #return " ".join(texto_banco).translate(str.maketrans('', '', '\n'))
        return texto_banco
text_db = create_db()

print(text_db)

TABLES = parse_sql(text_db)
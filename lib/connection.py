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

    post_processed_statements = []

    for statement in sql_statements:
        # Remove leading spaces and trailing newline characters
        statement = statement.strip()

        # Skip empty lines
        if not statement:
            continue

        post_processed_statements.append(statement)

    for statement in post_processed_statements:
        if statement.startswith('CREATE TABLE'):
            match = re.match(r'CREATE TABLE(?: if NOT EXISTS)? (\w+) \(', statement)
            if match:
                current_table = match.group(1)
                tables[current_table] = []
        elif current_table and statement[0] in "abcdefghijklmnopqrstuvwxyz":
            column_definition = statement.rstrip(',').split()
            column_name = column_definition[0]
            tables[current_table].append(column_name)
        elif current_table and statement.endswith(');'):
            current_table = None

    return tables


def create_db():
    connection = connect_db()

    with open("banco.sql", "r") as banco:
        query=""

        texto_banco = banco.readlines()

        for line in texto_banco:
            query += f" {line}"
            if ";" in query:
                get_db_cursor(connection).execute(query)
                connection.commit()
                query = ""

        print("Banco de Dados criado\n")

        return texto_banco


text_db = create_db()

TABLES = parse_sql(text_db)
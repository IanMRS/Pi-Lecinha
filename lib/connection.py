import sqlite3 as sql
import re

TABLES = {}

def connect_db():
    connection = sql.connect("banco.db")
    print("Conectando ao banco de Dados\n")
    return connection

def get_db_cursor(connection):
    return connection.cursor()

def parse_sql(sql_statements):
    tables = {}
    current_table = None

    for statement in sql_statements:
        statement = statement.strip()

        if not statement:
            continue
        elif statement.startswith('CREATE TABLE'):
            match = re.match(r'CREATE TABLE(?: if NOT EXISTS)? (\w+) \(', statement)
            if match:
                current_table = match.group(1)
                tables[current_table] = []
        elif current_table and statement[0] in "abcdefghijklmnopqrstuvwxyz":
            column_name = statement.split()[0]
            tables[current_table].append(column_name)
        elif current_table and statement.endswith(');'):
            current_table = None

    return tables

def create_db():
    connection = connect_db()

    with open("banco.sql", "r") as banco:
        texto_banco = banco.readlines()

    script = " ".join(texto_banco)

    connection.executescript(script)

    print("Banco de Dados criado\n")
    return texto_banco


text_db = create_db()

TABLES = parse_sql(text_db)
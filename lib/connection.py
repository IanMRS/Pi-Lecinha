import sqlite3 as sql
import re
import os

TABLES = {}

CONNECTION = sql.connect("banco.db")
CURSOR = CONNECTION.cursor()

def parse_sql(sql_statements):
    """
    Parse SQL statements to extract table names and column names.

    Parameters:
    - sql_statements: A list of SQL statements.

    Returns:
    A dictionary containing table names as keys and lists of column names as values.
    """
    tables = {}
    current_table = None

    for statement in sql_statements:
        statement = statement.strip()

        if not statement:
            continue
        elif statement.startswith("CREATE TABLE"):
            match = re.match(r"CREATE TABLE(?: if NOT EXISTS)? (\w+) \(", statement)
            if match:
                current_table = match.group(1)
                tables[current_table] = []
        elif current_table and statement[0] in "abcdefghijklmnopqrstuvwxyz":
            column_name = statement.split()[0]
            tables[current_table].append(column_name)
        elif current_table and statement.endswith(");"):
            current_table = None

    return tables

def read_sql():
    with open("banco.sql", "r") as banco:
        texto_banco = banco.readlines()
    return texto_banco

def create_db():
    """
    Create the SQLite database based on the SQL script.

    Returns:
    The SQL script used to create the database.
    """
    print("\nBanco de Dados: Criando")

    script = " ".join(read_sql())

    CONNECTION.executescript(script)
    CONNECTION.close()
    print("\nBanco de Dados: Criado com sucesso")

if not os.path.isfile("banco.db"):
    create_db()

text_db = read_sql()
TABLES = parse_sql(text_db)
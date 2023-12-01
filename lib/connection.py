import sqlite3 as sql
import re

TABLES = {}

def connect_db():
    """
    Connect to the SQLite database.

    Returns:
    A SQLite database connection.
    """
    connection = sql.connect("banco.db")
    return connection

def get_db_cursor(connection):
    """
    Get the database cursor.

    Parameters:
    - connection: The SQLite database connection.

    Returns:
    The database cursor.
    """
    return connection.cursor()

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

def create_db():
    """
    Create the SQLite database based on the SQL script.

    Returns:
    The SQL script used to create the database.
    """
    print("\nBanco de Dados: Criando")
    connection = connect_db()

    with open("banco.sql", "r") as banco:
        texto_banco = banco.readlines()

    script = " ".join(texto_banco)

    connection.executescript(script)
    
    print("\nBanco de Dados: Criado com sucesso")
    return texto_banco

text_db = create_db()

TABLES = parse_sql(text_db)
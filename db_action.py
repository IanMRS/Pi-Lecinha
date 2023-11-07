from tkinter import *
from tkinter import ttk

import db_connection as dbc

class CRUD:
    """
    A class for performing CRUD (Create, Read, Update, Delete) operations on a database table.

    Args:
        table_name (str): The name of the database table to interact with.
        columns (list): A list of column names in the table.
        
    Attributes:
        table_name (str): The name of the database table.
        columns (list): List of column names.
        conn: A database connection object.
        cursor: A cursor object for executing SQL commands.

    Methods:
        - db_input(query, data)
        - insert(data)
        - read(condition)
        - update(data, condition)
        - delete(condition)
        - close_connection()

    Example usage:
        my_crud = CRUD("employees", ["id", "name", "salary"])
    """


    def __init__(self, table_name : str, columns : list):
        """
        Initializes a CRUD object for a specific database table.

        Args:
            table_name (str): The name of the database table to interact with.
            columns (list): A list of column names in the table.
        """

        self.table_name = table_name
        self.columns = columns
        self.connection = dbc.connect_db()
        self.cursor = dbc.get_db_cursor(self.connection)


    def db_input(self, query, data = ""):
        """
        Execute a database query and commit the transaction.

        Args:
            query (str): A SQL query string to be executed.
            data (tuple, optional): Data to be used with the query (default: ""). The data should match the query's placeholders, if any.

        Example usage:
            db_input("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
        """
        output = self.cursor.execute(query if not data else query, data)
        self.connection.commit()
        return output


    def insert(self, data):
        """
        Insert data into the database table.

        Args:
            data (tuple): A tuple containing values to be inserted into the table, in the same order as columns.

        Raises:
            Exception: If the database connection is not established.

        Example usage:
            my_crud.insert((1, "John Doe", 50000))
        """

        placeholders = ', '.join(['?'] * len(data))
        insert_query = f"INSERT INTO {self.table_name} ({', '.join(self.columns)}) VALUES ({placeholders})"
        self.db_input(insert_query, data)


    def read(self, condition = "1"):
        """
        Retrieve all records from the database table.

        Returns:
            list: A list of tuples, each representing a row in the table.

        Raises:
            Exception: If the database connection is not established.

        Example usage:
            data = my_crud.read()
        """

        select_query = f"SELECT * FROM {self.table_name} WHERE {condition}"
        return self.db_input(select_query).fetchall()

    def update(self, data, condition = "1"):
        """
        Update records in the database table based on a condition.

        Args:
            data (str): A string representing the columns and values to update, e.g., "name = 'New Name'".
            condition (str): A string representing the condition for updating records, e.g., "id = 1".

        Raises:
            Exception: If the database connection is not established.

        Example usage:
            my_crud.update("name = 'Updated Name'", "id = 1")
        """

        update_query = f"UPDATE {self.table_name} SET {data} WHERE {condition}"
        self.db_input(update_query)


    def delete(self, condition = "1"):
        """
        Delete records from the database table based on a condition.

        Args:
            condition (str): A string representing the condition for deleting records, e.g., "id = 1".

        Raises:
            Exception: If the database connection is not established.

        Example usage:
            my_crud.delete("id = 1")
        """

        delete_query = f"DELETE FROM {self.table_name} WHERE {condition}"
        self.db_input(delete_query)


    def close_connection(self):
        """
        Close the database connection if it is open.

        Example usage:
            my_crud.close_connection()
        """

        if self.connection:
            self.connection.close()


class Funcs():
    def db_input(self, query, data = "", show = ""):
        connection = dbc.connect_db()
        cursor = dbc.get_db_cursor(connection)
        output = cursor.execute(query if not data else query, data)
        connection.commit()
        print(show)
        return output


    def variaveis(self):
        # Obtém as variáveis a partir dos campos de entrada
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.fone = self.telefone_entry.get()


    def add_cliente(self):
        # Adiciona um cliente ao banco de dados
        self.variaveis()
        self.db_input("""
                    INSERT INTO cliente (nome, fone) VALUES (?,?)
                            """, (self.nome, self.fone), "Adicionando Cliente\n")

    def deleta_cliente(self):
        # Deleta um cliente do banco de dados
        self.variaveis()
        self.db_input("""DELETE FROM cliente WHERE id= ?""", self.codigo,"Apagando cliente\n")


    def alterar_cliente(self):
        # Altera os dados de um cliente no banco de dados
        self.variaveis()
        self.db_input("""UPDATE cliente SET nome = ?, fone=? WHERE id = ?""",
                            (self.nome, self.fone, self.codigo),"Alterando Cliente")

    def busca_cliente(self):
        connection = dbc.connect_db()
        cursor = dbc.get_db_cursor(connection)
        self.lista_cliente.delete(*self.lista_cliente.get_children())
        nome = self.nome_entry.get()
        fone = self.telefone_entry.get()
        print(f"Nome: {nome}, fone: {fone}")
        
        # Monta a consulta SQL baseada nas condições preenchidas
        query = """SELECT id, nome, fone FROM cliente WHERE 1=1"""
        params = tuple()  # Tupla vazia para os parâmetros da consulta

        if nome:
            query += " AND nome LIKE ?"
            params += ('%' + nome + '%',)

        if fone:
            query += " AND fone LIKE ?"
            params += ('%' + fone + '%',)  # Adicione uma vírgula para criar uma tupla de um elemento

        query += " ORDER BY nome ASC"
        
        busca_nome = self.db_input(query, params)
        
        for i in busca_nome:
            self.lista_cliente.insert("", END, values=i)
        
        self.limpa_tela()
        
        if not nome and not fone:
            # Se nenhum campo estiver preenchido, mostrar todos os clientes
            self.update_lista()
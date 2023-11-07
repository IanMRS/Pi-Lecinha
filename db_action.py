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
        - insert(data)
        - read()
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
        self.conn = dbc.connect_db()
        self.cursor = self.conn.cursor()


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

        if self.conn is None or self.cursor is None:
            raise Exception("Connection to the database is not established. Call connect_to_database() first.")
        placeholders = ', '.join(['?'] * len(data))
        insert_query = f"INSERT INTO {self.table_name} ({', '.join(self.columns)}) VALUES ({placeholders})"
        self.cursor.execute(insert_query, data)
        self.conn.commit()


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

        if self.conn is None or self.cursor is None:
            raise Exception("Connection to the database is not established. Call connect_to_database() first.")
        select_query = f"SELECT * FROM {self.table_name} WHERE {condition}"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()


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

        if self.conn is None or self.cursor is None:
            raise Exception("Connection to the database is not established. Call connect_to_database() first.")
        update_query = f"UPDATE {self.table_name} SET {data} WHERE {condition}"
        self.cursor.execute(update_query)
        self.conn.commit()


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

        if self.conn is None or self.cursor is None:
            raise Exception("Connection to the database is not established. Call connect_to_database() first.")
        delete_query = f"DELETE FROM {self.table_name} WHERE {condition}"
        self.cursor.execute(delete_query)
        self.conn.commit()


    def close_connection(self):
        """
        Close the database connection if it is open.

        Example usage:
            my_crud.close_connection()
        """

        if self.conn:
            self.conn.close()


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


    def update_lista(self):
        # Atualiza a lista de clientes na interface
        self.lista_cliente.delete(*self.lista_cliente.get_children())
        lista = self.db_input("""SELECT id, nome, fone FROM cliente ORDER BY nome ASC;""")
        for i in lista:
            self.lista_cliente.insert("", END, values=i)


    def add_cliente(self):
        # Adiciona um cliente ao banco de dados
        self.variaveis()
        self.db_input("""
                    INSERT INTO cliente (nome, fone) VALUES (?,?)
                            """, (self.nome, self.fone), "Adicionando Cliente\n")

        self.update_lista()
        self.limpa_tela()


    def deleta_cliente(self):
        # Deleta um cliente do banco de dados
        self.variaveis()
        self.db_input("""DELETE FROM cliente WHERE id= ?""", self.codigo,"Apagando cliente\n")

        self.update_lista() # Adicione esta linha para atualizar a lista imediatamente
        self.limpa_tela()


    def alterar_cliente(self):
        # Altera os dados de um cliente no banco de dados
        self.variaveis()
        self.db_input("""UPDATE cliente SET nome = ?, fone=? WHERE id = ?""",
                            (self.nome, self.fone, self.codigo),"Alterando Cliente")
        self.update_lista()


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
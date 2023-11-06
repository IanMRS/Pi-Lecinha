from tkinter import *
from tkinter import ttk

import db_connection as dbc

class Funcs():
    connection = dbc.connect_db()
    cursor = dbc.get_db_cursor(connection)
    cursor.execute(
            """ CREATE TABLE IF NOT EXISTS clientes (
                    cod INTEGER PRIMARY KEY, 
                    nome_cliente CHAR(255) NOT NULL,
                    telefone INTEGER(20) NOT NULL
                    );
            """)

    connection.commit()
    print("Banco de Dados criado\n")


    def db_query(self, query, out = ""):
        connection = dbc.connect_db()
        cursor = dbc.get_db_cursor(connection)
        cursor.execute(query)
        connection.commit()
        print(out)
        #connection.close()


    def db_input(self, query, data, out = ""):
        connection = dbc.connect_db()
        cursor = dbc.get_db_cursor(connection)
        cursor.execute(query, data)
        connection.commit()
        print(out)
        ##connection.close()


    def limpa_tela(self):
        # Limpa os campos de entrada (Entry)
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)


    def variaveis(self):
        # Obtém as variáveis a partir dos campos de entrada
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()


    def select_lista(self):
        # Atualiza a lista de clientes na interface
        self.lista_cliente.delete(*self.lista_cliente.get_children())
        lista = self.cursor.execute("""SELECT cod, nome_cliente, telefone FROM clientes ORDER BY nome_cliente ASC;""")
        for i in lista:
            self.lista_cliente.insert("", END, values=i)


    def add_cliente(self):
        # Adiciona um cliente ao banco de dados
        self.variaveis()
        self.db_input("""
                    INSERT INTO clientes (nome_cliente, telefone) VALUES (?,?)
                            """, (self.nome, self.telefone), "Adicionando Cliente\n")

        self.select_lista()
        self.limpa_tela()


    def deleta_cliente(self):
        # Deleta um cliente do banco de dados
        self.variaveis()
        connection = dbc.connect_db()
        cursor = dbc.get_db_cursor(connection)
        self.db_input("""DELETE FROM clientes WHERE cod= ?""", (self.codigo,),"Apagando cliente\n")

        self.select_lista() # Adicione esta linha para atualizar a lista imediatamente
        self.limpa_tela()


    def alterar_cliente(self):
        # Altera os dados de um cliente no banco de dados
        self.variaveis()
        connection = dbc.connect_db()
        cursor = dbc.get_db_cursor(connection)
        self.db_input("""UPDATE clientes SET nome_cliente = ?, telefone=? WHERE cod = ?""",
                            (self.nome, self.telefone, self.codigo),"Alterando Cliente")
        self.select_lista()


    def busca_cliente(self):
        connection = dbc.connect_db()
        cursor = dbc.get_db_cursor(connection)
        self.lista_cliente.delete(*self.lista_cliente.get_children())
        nome = self.nome_entry.get()
        telefone = self.telefone_entry.get()
        print(f"Nome: {nome}, Telefone: {telefone}")
        
        # Monta a consulta SQL baseada nas condições preenchidas
        query = """SELECT cod, nome_cliente, telefone FROM clientes WHERE 1=1"""
        params = tuple()  # Tupla vazia para os parâmetros da consulta

        if nome:
            query += " AND nome_cliente LIKE ?"
            params += ('%' + nome + '%',)

        if telefone:
            query += " AND telefone LIKE ?"
            params += ('%' + telefone + '%',)  # Adicione uma vírgula para criar uma tupla de um elemento

        query += " ORDER BY nome_cliente ASC"
        
        cursor.execute(query, params)
        busca_nome_cliente = cursor.fetchall()
        
        for i in busca_nome_cliente:
            self.lista_cliente.insert("", END, values=i)
        
        self.limpa_tela()
        
        if not nome and not telefone:
            # Se nenhum campo estiver preenchido, mostrar todos os clientes
            self.select_lista()
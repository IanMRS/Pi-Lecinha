from tkinter import *
from tkinter import ttk

import db_connection as dbc

class Funcs():
    dbc.create_db()

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


    def select_lista(self):
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

        self.select_lista()
        self.limpa_tela()


    def deleta_cliente(self):
        # Deleta um cliente do banco de dados
        self.variaveis()
        self.db_input("""DELETE FROM cliente WHERE id= ?""", (self.codigo,),"Apagando cliente\n")

        self.select_lista() # Adicione esta linha para atualizar a lista imediatamente
        self.limpa_tela()


    def alterar_cliente(self):
        # Altera os dados de um cliente no banco de dados
        self.variaveis()
        self.db_input("""UPDATE cliente SET nome = ?, fone=? WHERE id = ?""",
                            (self.nome, self.fone, self.codigo),"Alterando Cliente")
        self.select_lista()


    def busca_cliente(self):
        connection = dbc.connect_db()
        cursor = dbc.get_db_cursor(connection)
        self.lista_cliente.delete(*self.lista_cliente.get_children())
        nome = self.nome_entry.get()
        fone = self.fone_entry.get()
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
            self.select_lista()
import connection as dbc
import manager_client as mc

dbc.create_db() # Cria um banco de dados local

mc.maneja_clientes.start() # Cria uma instância da classe Application, o que inicia a aplicação TKINTER
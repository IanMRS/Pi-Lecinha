import db_connection as dbc
import manager_client as mc

dbc.create_db() # Cria um banco de dados local

mc.Application().start() # Cria uma instância da classe Application, o que inicia a aplicação TKINTER
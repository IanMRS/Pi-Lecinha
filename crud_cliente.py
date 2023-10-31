#fontes:
#   https://chat.openai.com/share/4a87856a-6027-4078-bd9f-c908e482ae0d -- CRUD basico
#   https://chat.openai.com/share/b0cb3912-8d6f-4595-859e-60955d6aa3d1 -- resolvendo bug


import db_connection as dbc

connection = dbc.connect_to_db()
cursor = dbc.get_db_cursor(connection)

# Create
def create_cliente(nome, fone, obs):
    query = "INSERT INTO cliente (nome, fone, obs) VALUES (%s, %s, %s)"
    values = (nome, fone, obs)
    cursor.execute(query, values)
    connection.commit()

# Read
def read_cliente():
    query = "SELECT * FROM cliente"
    cursor.execute(query)
    cliente = cursor.fetchall()
    return cliente

# Update
def update_cliente(cliente_id, new_nome, new_fone, new_obs):
    query = "UPDATE cliente SET nome = %s, fone = %s, obs = %s WHERE id = %s"
    values = (new_nome, new_fone, new_obs, cliente_id)
    cursor.execute(query, values)
    connection.commit()

# Delete
def delete_cliente(cliente_id):
    query = "DELETE FROM cliente WHERE id = %s"
    values = (cliente_id,)#ESSA VIRGULA É NECESSÁRIA, NEM OUSE
    cursor.execute(query, values)
    connection.commit()

# Example usage:
create_cliente("joão", 11912345678,"vegano")
create_cliente("maria", 11987654321, "nda")

for cliente in read_cliente():
        print(f"ID: {cliente[0]}, Nome: {cliente[1]}, Fone: {cliente[2]}, Obs: {cliente[3]}")
        read_cliente()

update_cliente(1, "pedro", "69969696969","Xd")
delete_cliente(2)

# Close the cursor and connection when done
cursor.close()
connection.close()

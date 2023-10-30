#fontes:
#   https://chat.openai.com/share/4a87856a-6027-4078-bd9f-c908e482ae0d -- CRUD basico
#   https://chat.openai.com/share/b0cb3912-8d6f-4595-859e-60955d6aa3d1 -- resolvendo bug


import mysql.connector

# Establish a MySQL connection
connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="banco"
)

# Create a cursor object
cursor = connection.cursor()

# Create
def create_origem(nome, taxa):
    try:
        query = "INSERT INTO origem (nome, taxa) VALUES (%s, %s)"
        values = (nome, taxa)
        cursor.execute(query, values)
        connection.commit()
        print("Site created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


# Read
def read_origens():
    query = "SELECT id, nome, taxa FROM origem"
    cursor.execute(query)
    origens = cursor.fetchall()
    for origem in origens:
        print(f"ID: {origem[0]}, Nome: {origem[1]}, Taxa: {origem[2]}")

# Update
def update_origem(origem_id, new_nome, new_taxa):
    query = "UPDATE origem SET nome = %s, taxa = %s WHERE id = %s"
    values = (new_nome, new_taxa, origem_id)
    cursor.execute(query, values)
    connection.commit()

# Delete
def delete_origem(origem_id):
    query = "DELETE FROM origem WHERE id = %s"
    values = (origem_id,)
    cursor.execute(query, values)
    connection.commit()

# Example usage:
create_origem("origem 1", 100.0)
create_origem("origem 2", 150.0)
read_origens()
update_origem(1, "Updated origem 1", 120.0)
delete_origem(2)

# Close the cursor and connection when done
cursor.close()
connection.close()

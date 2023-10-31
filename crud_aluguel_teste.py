import mysql.connector

# Replace with your database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'banco',
}

# Function to establish a database connection
def connect():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create a new aluguel
def create_aluguel(clienteid, origemid, datainicio, datatermino, valor, quantia_inquilinos, contrato, obs):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO aluguel (clienteid, origemid, datainicio, datatermino, valor, quantia_inquilinos, contrato, obs) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (clienteid, origemid, datainicio, datatermino, valor, quantia_inquilinos, contrato, obs))
            conn.commit()
            print("Aluguel created successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

# Read aluguel by ID
def read_aluguel(aluguel_id):
    conn = connect()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM aluguel WHERE id = %s", (aluguel_id,))
            aluguel = cursor.fetchone()
            if aluguel:
                print("Aluguel details:")
                for key, value in aluguel.items():
                    print(f"{key}: {value}")
            else:
                print("Aluguel not found.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

# Update aluguel by ID
def update_aluguel(aluguel_id, new_valor):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE aluguel SET valor = %s WHERE id = %s", (new_valor, aluguel_id))
            conn.commit()
            print("Aluguel updated successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

# Delete aluguel by ID
def delete_aluguel(aluguel_id):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM aluguel WHERE id = %s", (aluguel_id,))
            conn.commit()
            print("Aluguel deleted successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

# Main program
if __name__ == '__main__':
    while True:
        print("Select an option:")
        print("1. Create Aluguel")
        print("2. Read Aluguel")
        print("3. Update Aluguel")
        print("4. Delete Aluguel")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_aluguel(
                int(input("Cliente ID: ")),
                int(input("Origem ID: ")),
                input("Data Inicio (YYYY-MM-DD): "),
                input("Data Termino (YYYY-MM-DD): "),
                float(input("Valor: ")),
                int(input("Quantia Inquilinos: ")),
                input("Contrato: "),
                input("Observations: ")
            )
        elif choice == "2":
            aluguel_id = int(input("Enter Aluguel ID: "))
            read_aluguel(aluguel_id)
        elif choice == "3":
            aluguel_id = int(input("Enter Aluguel ID to update: "))
            new_valor = float(input("New Valor: "))
            update_aluguel(aluguel_id, new_valor)
        elif choice == "4":
            aluguel_id = int(input("Enter Aluguel ID to delete: "))
            delete_aluguel(aluguel_id)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please select a valid option.")

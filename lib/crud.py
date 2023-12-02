from lib import connection as dbc

BANCOS = {}

class CRUD:
    """
    A class providing basic CRUD operations for a database table.

    Attributes:
    - table_name: The name of the database table.
    - columns: The list of columns in the table.
    - columns_no_id: The list of columns excluding the primary key.
    - columns_display_names: Display-friendly names for the columns.
    - connection: The database connection.
    - cursor: The database cursor.
    """

    def __init__(self, table_name: str, columns: list):
        """
        Initialize the CRUD instance.

        Parameters:
        - table_name: The name of the database table.
        - columns: The list of columns in the table.
        """
        self.table_name = table_name
        self.columns = columns
        self.columns_no_id = columns[1:]
        self.columns_display_names = [column[3:].capitalize().replace("_", " ") if "id_" in column[:3] else "Código" if "id" in column[:2] else column.capitalize().replace("_", " ") for column in self.columns]
        self.connection = dbc.connect_db()
        self.cursor = dbc.get_db_cursor(self.connection)

    def start_connection(self):
        self.connection = dbc.connect_db()
        self.cursor = dbc.get_db_cursor(self.connection)
        print(f"Banco de Dados: Conectando em ({self.table_name})")

    def stop_connection(self):
        self.connection.close()
        print(f"Banco de Dados: Desconectando-se de ({self.table_name})")

    def db_input(self, query, data=""):
        """
        Execute a database query.

        Parameters:
        - query: The SQL query to execute.
        - data: Data to be used in the query (default is an empty string).

        Returns:
        The result of the query execution.
        """
        output = self.cursor.execute(query if not data else query, data)
        self.connection.commit()
        return output

    def insert(self, data):
        """
        Insert a new record into the database.

        Parameters:
        - data: The data to be inserted.
        """
        data_no_id = data[1:]
        placeholders = ", ".join(["?"] * len(data_no_id))
        insert_query = f"INSERT INTO {self.table_name} ({', '.join(self.columns_no_id)}) VALUES ({placeholders})"
        self.db_input(insert_query, data_no_id)

    def read(self, condition="1=1"):
        """
        Read records from the database based on a condition.

        Parameters:
        - condition: The condition for filtering records (default is "1=1").

        Returns:
        A list of records that satisfy the condition.
        """
        select_query = f"SELECT * FROM {self.table_name} WHERE {condition}"
        return self.db_input(select_query).fetchall()

    def search(self, dataset):
        """
        Search records in the database based on a dataset.

        Parameters:
        - dataset: The dataset containing values for search.

        Returns:
        A list of records that match the search criteria.
        """
        conditions = ["1=1"]

        for i, data in enumerate(dataset):
            if data is not None and data != "":
                conditions.append(f" AND {self.columns[i]} LIKE '%{data}%'")

        condition = "".join(conditions)
        return self.read(condition)

    def update(self, data, condition="1=1"):
        """
        Update records in the database.

        Parameters:
        - data: The data to be updated.
        - condition: The condition for updating records (default is "1=1").
        """
        values = []
        columns_altered = []

        for i, v in enumerate(data):
            if v is not None:
                columns_altered.append(f" {self.columns[i]} = ?")
                values.append(v)

        update_query = f"UPDATE {self.table_name} SET {','.join(columns_altered)} WHERE {condition}"
        self.db_input(update_query, values)
        print("Valor atualizado com sucesso")

    def delete(self, condition):
        """
        Delete records from the database.

        Parameters:
        - condition: The condition for deleting records.
        """
        delete_query = f"DELETE FROM {self.table_name} WHERE {condition}"
        self.db_input(delete_query)
        print("Valor apagado com sucesso")

# Create CRUD instances for each table in the database
for name, table in dbc.TABLES.items():
    BANCOS[name] = CRUD(name, table)
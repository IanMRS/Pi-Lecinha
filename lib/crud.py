from lib import connection as dbc

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
        - search(dataset)
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


    def read(self, condition = "1=1"):
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


    def search(self, dataset):
        """
        Search for records in the database table based on the provided dataset.

        Args:
            dataset (list): A list of values to search for in corresponding columns.

        Returns:
            list: A list of tuples, each representing a row in the table that matches the search criteria.

        Example usage:
            # Example dataset: [value1, value2, None, value4]
            # The None value means the column will not be included in the search.
            data = my_crud.search([value1, value2, None, value4])
        """

        conditions = ["1=1"]

        for i, data in enumerate(dataset):
            if data is not None and data is not "":
                conditions.append(f" AND {self.columns[i]} LIKE '%{data}%'")

        condition = "".join(conditions)

        return self.read(condition)


    def update(self, data, condition = "1=1"):
        """
        Update records in the database table based on a condition.

        Args:
            data (str): A string representing the columns and values to update, e.g., "name = 'New Name'".
            condition (str): A string representing the condition for updating records, e.g., "id = 1".

        Raises:
            Exception: If the database connection is not established.

        Example usage:
            my_crud.update(["Patrick", "32133211232", "nda"]], "id = 1")
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

        print("Valor apagado com sucesso")


    def close_connection(self):
        """
        Close the database connection if it is open.

        Example usage:
            my_crud.close_connection()
        """

        if self.connection:
            self.connection.close()

crud_cliente = CRUD("cliente",["nome", "fone", "obs"])
crud_origem = CRUD("origem",["nome", "taxa"])
crud_aluguel = CRUD("aluguel",["clienteid", "origemid", "datainicio","datatermino","valor","quantia_inquilinos","obs"])
crud_casa = CRUD("casa",["nome", "capacidade", "quartos","camas","banheiros"])
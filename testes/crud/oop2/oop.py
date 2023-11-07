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
        self.connection = dbc.connect_db()
        self.cursor = dbc.get_db_cursor(self.connection)


    def db_input(self, query, data = ""):
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

        select_query = f"SELECT * FROM {self.table_name} WHERE {condition}"
        return self.db_input(select_query).fetchall()

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

        update_query = f"UPDATE {self.table_name} SET {data} WHERE {condition}"
        self.db_input(update_query)


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

        delete_query = f"DELETE FROM {self.table_name} WHERE {condition}"
        self.db_input(delete_query)


    def close_connection(self):
        """
        Close the database connection if it is open.

        Example usage:
            my_crud.close_connection()
        """

        if self.connection:
            self.connection.close()


# Usage example
if __name__ == "__main__":
    table_name = "cliente"
    columns = ["nome", "fone","obs"]
    
    crud = CRUD(table_name, columns)
    
    crud.insert(("John Doe", "12345432211", "fumante"))
    crud.insert(("Jane Smith", "12345432241", "sonegadora de imposto"))
    
    print(f"{crud.read()}\n")
    
    crud.update("fone=32", "id=1")
    
    print(f"{crud.read()}\n")
    
    crud.delete("id=4")
    
    print(f"{crud.read()}\n")
    
    crud.close_connection()
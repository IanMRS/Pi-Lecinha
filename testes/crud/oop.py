import sqlite3

class CRUD:
    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.columns = columns
        self.conn = None
        self.cursor = None

    def connect_to_database(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def insert(self, data):
        if self.conn is None or self.cursor is None:
            raise Exception("Connection to the database is not established. Call connect_to_database() first.")
        placeholders = ', '.join(['?'] * len(data))
        insert_query = f"INSERT INTO {self.table_name} ({', '.join(self.columns)}) VALUES ({placeholders})"
        self.cursor.execute(insert_query, data)
        self.conn.commit()

    def read(self):
        if self.conn is None or self.cursor is None:
            raise Exception("Connection to the database is not established. Call connect_to_database() first.")
        select_query = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()

    def update(self, data, condition):
        if self.conn is None or self.cursor is None:
            raise Exception("Connection to the database is not established. Call connect_to_database() first.")
        update_query = f"UPDATE {self.table_name} SET {data} WHERE {condition}"
        self.cursor.execute(update_query)
        self.conn.commit()

    def delete(self, condition):
        if self.conn is None or self.cursor is None:
            raise Exception("Connection to the database is not established. Call connect_to_database() first.")
        delete_query = f"DELETE FROM {self.table_name} WHERE {condition}"
        self.cursor.execute(delete_query)
        self.conn.commit()

    def close_connection(self):
        if self.conn:
            self.conn.close()

# Usage example
if __name__ == "__main__":
    db_name = "banco.db"
    table_name = "cliente"
    columns = ["nome", "fone","obs"]
    
    crud = CRUD(table_name, columns)
    crud.connect_to_database(db_name)
    
    crud.insert(("John Doe", "12345432211", "fumante"))
    crud.insert(("Jane Smith", "12345432241", "sonegadora de imposto"))
    
    print(crud.read())
    
    crud.update("fone=31", "id=1")
    
    print(crud.read())
    
    crud.delete("id=2")
    
    print(crud.read())
    
    crud.close_connection()
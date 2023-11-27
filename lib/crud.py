from lib import connection as dbc

class CRUD:
    def __init__(self, table_name : str, columns : list):
        self.table_name = table_name
        self.columns = columns
        self.columns_no_id = columns[1:]
        self.connection = dbc.connect_db()
        self.cursor = dbc.get_db_cursor(self.connection)


    def db_input(self, query, data = ""):
        output = self.cursor.execute(query if not data else query, data)
        self.connection.commit()
        return output


    def insert(self, data):
        data_no_id = data[1:]

        placeholders = ', '.join(['?'] * len(data_no_id))
        insert_query = f"INSERT INTO {self.table_name} ({', '.join(self.columns_no_id)}) VALUES ({placeholders})"
        self.db_input(insert_query, data)


    def read(self, condition = "1=1"):
        select_query = f"SELECT * FROM {self.table_name} WHERE {condition}"
        return self.db_input(select_query).fetchall()


    def search(self, dataset):
        conditions = ["1=1"]

        for i, data in enumerate(dataset):
            if data is not None and data is not "":
                conditions.append(f" AND {self.columns[i]} LIKE '%{data}%'")

        condition = "".join(conditions)

        return self.read(condition)


    def update(self, data, condition = "1=1"):
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
        delete_query = f"DELETE FROM {self.table_name} WHERE {condition}"
        self.db_input(delete_query)

        print("Valor apagado com sucesso")

bancos = {}

for name,table in dbc.TABLES.items():
    bancos[name] = CRUD(name, table)
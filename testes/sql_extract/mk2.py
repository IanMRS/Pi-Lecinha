import re

def parse_sql(sql_statements):
    tables = {}
    current_table = None

    for statement in sql_statements:
        if statement.startswith('CREATE TABLE'):
            match = re.match(r'CREATE TABLE if NOT EXISTS (\w+) \(', statement)
            if match:
                current_table = match.group(1)
                tables[current_table] = []
        elif current_table and statement.strip().endswith(',') and statement.strip()[0] in "abcdefghijklmnopqrstuvwxyz":
            column_definition = statement.strip().rstrip(',').split()
            column_name = column_definition[0]
            tables[current_table].append(column_name)
        elif current_table and statement.strip().endswith(');'):
            current_table = None

    return tables

# Example usage
sql_database =['CREATE TABLE if NOT EXISTS origem (\n', '    id INTEGER PRIMARY KEY,\n', '    nome VARCHAR(255) NOT NULL,\n', '    taxa FLOAT NOT NULL\n', ');\n', '\n', 'CREATE TABLE if NOT EXISTS cliente (\n', '    id INTEGER PRIMARY KEY,\n', '    nome VARCHAR(255) NOT NULL,\n', '    fone VARCHAR(13) NOT NULL,\n', '    obs VARCHAR(255)\n', ');\n', '\n', 'CREATE TABLE if NOT EXISTS aluguel (\n', '    id INTEGER PRIMARY KEY,\n', '    clienteid INT NOT NULL,\n', '    origemid INT NOT NULL,\n', '    datainicio DATE NOT NULL,\n', '    datatermino DATE NOT NULL,\n', '    valor FLOAT NOT NULL,\n', '    quantia_inquilinos INT NOT NULL,\n', '    obs VARCHAR(255) NOT NULL,\n', '\n', '    FOREIGN KEY (origemid) REFERENCES origem(id)\n', '    ON DELETE NO ACTION\n', '    ON UPDATE NO ACTION,\n', '    FOREIGN KEY (clienteid) REFERENCES cliente(id)\n', '    ON DELETE NO ACTION\n', '    ON UPDATE NO ACTION\n', ');\n', '\n', 'CREATE TABLE if NOT EXISTS casa (\n', '    id INTEGER PRIMARY KEY,\n', '    nome VARCHAR(255) NOT NULL,\n', '    capacidade INT NOT NULL,\n', '    quartos INT NOT NULL,\n', '    camas INT NOT NULL,\n', '    banheiros INT NOT NULL\n', ');\n', '\n', 'CREATE TABLE if NOT EXISTS aluguel_has_casa (\n', '    id INTEGER PRIMARY KEY,\n', '    aluguel_id INT NOT NULL,\n', '    casa_id INT NOT NULL,\n', '\n', '    FOREIGN KEY (aluguel_id) REFERENCES aluguel(id)\n', '    ON DELETE NO ACTION\n', '    ON UPDATE NO ACTION,\n', '\n', '    FOREIGN KEY (casa_id) REFERENCES casa (id)\n', '    ON DELETE NO ACTION\n', '    ON UPDATE NO ACTION\n', ');']

result = parse_sql(sql_database)
print(result)

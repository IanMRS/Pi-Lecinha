import re

def extract_tables_and_columns(sql_code):
    tables = {}

    # Use regular expressions to find CREATE TABLE statements
    create_table_regex = re.compile(r"CREATE TABLE (\w+) \((.*?)\);", re.DOTALL)

    # Find all CREATE TABLE statements in the SQL code
    table_matches = create_table_regex.findall(sql_code)

    for table_match in table_matches:
        table_name, columns_str = table_match
        columns = []

        # Use regular expressions to extract column information
        column_regex = re.compile(r"(\w+) (\w+(\(\d+\))?( \w+)?(,)?)+", re.DOTALL)
        column_matches = column_regex.findall(columns_str)

        for column_match in column_matches:
            if column_match[0][0] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                column_name = column_match[0]
                columns.append(column_name)

        tables[table_name] = columns

    return tables

# Sample SQL code
sql_code = """
CREATE TABLE origem (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    taxa FLOAT NOT NULL
);

CREATE TABLE cliente (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    fone VARCHAR(13) NOT NULL,
    obs VARCHAR(255)
);

CREATE TABLE aluguel (
    id INTEGER PRIMARY KEY,
    clienteid INT NOT NULL,
    origemid INT NOT NULL,
    datainicio DATE NOT NULL,
    datatermino DATE NOT NULL,
    valor FLOAT NOT NULL,
    quantia_inquilinos INT NOT NULL,
    obs VARCHAR(255) NOT NULL,

    FOREIGN KEY (origemid) REFERENCES origem(id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
    FOREIGN KEY (clienteid) REFERENCES cliente(id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

CREATE TABLE casa (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    capacidade INT NOT NULL,
    quartos INT NOT NULL,
    camas INT NOT NULL,
    banheiros INT NOT NULL
);

CREATE TABLE aluguel_has_casa (
    id INTEGER PRIMARY KEY,
    aluguel_id INT NOT NULL,
    casa_id INT NOT NULL,

    FOREIGN KEY (aluguel_id) REFERENCES aluguel(id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,

    FOREIGN KEY (casa_id) REFERENCES casa (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);
"""

# Extract tables and columns
result = extract_tables_and_columns(sql_code)
print(result)

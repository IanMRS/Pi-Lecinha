CREATE TABLE if NOT EXISTS origem (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    taxa FLOAT NOT NULL);

CREATE TABLE if NOT EXISTS cliente (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    fone VARCHAR(13) NOT NULL,
    obs VARCHAR(255));

CREATE TABLE if NOT EXISTS aluguel (
    id INTEGER PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_origem INT NOT NULL,
    data_inicio DATE NOT NULL,
    data_termino DATE NOT NULL,
    valor FLOAT NOT NULL,
    quantia_inquilinos INT NOT NULL,
    obs VARCHAR(255) NOT NULL,

    FOREIGN KEY (id_origem) REFERENCES origem(id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE if NOT EXISTS casa (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    capacidade INT NOT NULL,
    quartos INT NOT NULL,
    camas INT NOT NULL,
    banheiros INT NOT NULL);

CREATE TABLE if NOT EXISTS aluguel_has_casa (
    id INTEGER PRIMARY KEY,
    id_aluguel INT NOT NULL,
    id_casa INT NOT NULL,

    FOREIGN KEY (id_aluguel) REFERENCES aluguel(id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,

    FOREIGN KEY (id_casa) REFERENCES casa (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
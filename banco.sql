CREATE TABLE IF NOT EXISTS origem (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    taxa FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS cliente (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    fone VARCHAR(13) NOT NULL,
    obs VARCHAR(255) NULL
);

CREATE TABLE IF NOT EXISTS aluguel (
    id INTEGER PRIMARY KEY,
    clienteid INT NOT NULL,
    origemid INT NOT NULL,
    datainicio DATE NOT NULL,
    datatermino DATE NOT NULL,
    valor FLOAT NOT NULL,
    quantia_inquilinos INT NOT NULL,
    contrato VARCHAR(255) NOT NULL,
    obs VARCHAR(255) NOT NULL,

    FOREIGN KEY (origemid) REFERENCES origem(id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
    FOREIGN KEY (clienteid) REFERENCES cliente(id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS casa (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    capacidade INT NOT NULL,
    quartos INT NOT NULL,
    camas INT NOT NULL,
    banheiros INT NOT NULL
);

CREATE TABLE IF NOT EXISTS aluguel_has_casa (
    aluguel_id INT NOT NULL,
    casa_id INT NOT NULL,
    PRIMARY KEY (aluguel_id, casa_id),

    FOREIGN KEY (aluguel_id) REFERENCES aluguel(id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,

    FOREIGN KEY (casa_id) REFERENCES casa (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);
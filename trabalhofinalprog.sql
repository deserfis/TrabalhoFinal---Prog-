CREATE DATABASE projetofinal
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;

USE projetofinal;

CREATE TABLE filmes (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(30) NOT NULL,
    diretor VARCHAR(30) NOT NULL DEFAULT 'Hayao Miyazaki',
    ano_lancamento YEAR NOT NULL,
    duracao INT NOT NULL CHECK (duracao > 0),
    descricao TEXT NOT NULL,
    PRIMARY KEY(id)
)
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;

CREATE TABLE genero (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(30) NOT NULL,
    PRIMARY KEY(id)
)
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;

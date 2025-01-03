CREATE DATABASE projetofinal
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;

USE projetofinal;

CREATE TABLE genero (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(30) NOT NULL,
    PRIMARY KEY(id)
)
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;

CREATE TABLE filme (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(30) NOT NULL,
    ano_lancamento YEAR NOT NULL,
    descricao TEXT NOT NULL,
    nota DECIMAL(2,1) NOT NULL CHECK (nota BETWEEN 0.5 AND 5), -- Ajustado para DECIMAL
    genero_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (genero_id) REFERENCES genero (id)
)
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;

CREATE TABLE avaliacao (
    id INT NOT NULL AUTO_INCREMENT,
    usuario VARCHAR(30) NOT NULL,
    nota DECIMAL(2,1) NOT NULL CHECK (nota BETWEEN 0.5 AND 5), -- Ajustado para DECIMAL
    comentario VARCHAR(1000) NOT NULL,
    filme_id INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(filme_id) REFERENCES filme(id)
)
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;


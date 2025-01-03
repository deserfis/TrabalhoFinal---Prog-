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
    nota DECIMAL(2,1) NOT NULL CHECK (nota BETWEEN 0.5 AND 5), 
    genero_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (genero_id) REFERENCES genero (id)
)
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;

CREATE TABLE avaliacao (
    id INT NOT NULL AUTO_INCREMENT,
    usuario VARCHAR(30) NOT NULL,
    nota DECIMAL(2,1) NOT NULL CHECK (nota BETWEEN 0.5 AND 5),
    comentario VARCHAR(1000) NOT NULL,
    filme_id INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(filme_id) REFERENCES filme(id)
)
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;

INSERT INTO genero (nome) 
VALUES 
    ('Aventura'),
    ('Fantasia'),
    ('Drama'),
    ('Família'),
    ('Romance'),
    ('Histórico'),
    ('Mistério');

SELECT id, nome AS Genero
FROM genero;

INSERT INTO filme(nome, ano_lancamento, descricao, nota, genero_id)
values('Castelo Animado','2005','Uma bruxa lança uma terrível maldição sobre a jovem Sophie transformando-a em uma velha. Desesperada,
 ela embarca em uma odisseia em busca do mago Howl, um misterioso feiticeiro que pode ajudá-la a reverter o feitiço.','5.0','1'); 

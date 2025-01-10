CREATE DATABASE projetofinal
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;

USE projetofinal;

CREATE TABLE genero (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(30) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE filme (
    id INT NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(50) NOT NULL,
    descricao MEDIUMTEXT NOT NULL,
    ano YEAR NOT NULL,
    genero_id INT NOT NULL,
    nota DECIMAL(2,1) NOT NULL CHECK (nota BETWEEN 0.5 AND 5), 
    PRIMARY KEY (id),
    FOREIGN KEY (genero_id) REFERENCES genero (id));

CREATE TABLE avaliacao (
    id INT NOT NULL AUTO_INCREMENT,
    usuario VARCHAR(30) NOT NULL,
    nota_av DECIMAL(2,1) NOT NULL CHECK ((nota_av BETWEEN 0.5 AND 5) AND (MOD(nota_av * 10, 10) = 0 OR MOD(nota_av * 10, 10) = 5)),
    comentario VARCHAR(1000) NOT NULL,
    filme_id INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(filme_id) REFERENCES filme(id)
);

INSERT INTO genero (nome) 
VALUES 
    ('Aventura'),
    ('Fantasia'),
    ('Drama'),
    ('Família'),
    ('Romance'),
    ('Histórico'),
    ('Mistério');
    
-- genero ficar igual o nome e id
SELECT 
    f.id AS Filme_ID,
    f.titulo AS Filme,
    f.ano AS Ano,
    f.descricao AS Descricao,
    f.nota AS Nota,
    g.nome AS Genero
FROM 
    filme f
JOIN 
    genero g
ON 
    f.genero_id = g.id;

INSERT INTO filme (titulo, descricao, ano, nota, genero_id) 
VALUES
('Castelo Animado', 'Uma bruxa lança uma terrível maldição sobre a jovem Sophie transformando-a em uma velha. Desesperada, ela embarca em uma odisseia em busca do mago Howl, um misterioso feiticeiro que pode ajudá-la a reverter o feitiço.', 2005, 5.0, 1),
('Meu Amigo Totoro', 'Duas irmãs se mudam para o campo e descobrem criaturas mágicas, incluindo Totoro, que as ajudam a lidar com os desafios da vida.', 1988, 4.9, 4),
('O Castelo no Céu', 'Sheeta e Pazu embarcam em uma aventura para encontrar uma cidade flutuante enquanto fogem de piratas e forças militares.', 1986, 4.8, 1),
('Princesa Mononoke', 'Ashitaka tenta mediar a paz entre humanos que exploram a natureza e espíritos da floresta liderados por uma guerreira chamada Mononoke.', 1997, 5.0, 2),
('Ponyo - Uma Amizade que Veio do Mar', 'Uma peixinha mágica chamada Ponyo quer se transformar em humana após fazer amizade com um garoto.', 2008, 4.7, 4),
('O Serviço de Entregas da Kiki', 'Kiki, uma jovem bruxa em treinamento, tenta encontrar seu lugar no mundo enquanto trabalha como entregadora.', 1989, 4.6, 2),
('O Conto da Princesa Kaguya', 'Baseado em uma lenda japonesa, Kaguya é encontrada em um bambu e cresce para enfrentar escolhas difíceis sobre seu destino.', 2013, 4.8, 6);


-- VER OS IDS DE CADA GENERO
-- SELECT id, nome as 'genero'
-- FROM genero;

-- VER OS FILMES
-- SELECT * FROM FILME;

-- id do filme ficar igual o titulo
SELECT 
    a.id AS Avaliacao_ID,
    a.usuario AS Usuario,
    a.nota_av AS Nota,
    a.comentario AS Comentario,
    f.titulo AS Filme
FROM 
    avaliacao a
JOIN 
    filme f
ON 
    a.filme_id = f.id;
    
-- VER OS IDS DE CADA FILME
-- SELECT id, titulo as 'titulo do filme'
-- FROM FILME;
INSERT INTO avaliacao (usuario, nota_av, comentario, filme_id) 
VALUES
('usuario1', 2.5, 'comentarioblablabla', 1), 
('usuario2', 2.5, 'comentarioblablabla', 1),
('usuario3', 5.0, 'amei', 3);



-- ver avaliacoes
-- SELECT * FROM AVALIACAO;

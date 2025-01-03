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

SELECT 
    f.id AS Filme_ID,
    f.nome AS Filme,
    f.ano_lancamento AS Ano,
    f.descricao AS Descricao,
    f.nota AS Nota,
    g.nome AS Genero
FROM 
    filme f
JOIN 
    genero g
ON 
    f.genero_id = g.id;

INSERT INTO filme(nome, ano_lancamento, descricao, nota, genero_id)
values
('Castelo Animado','2005','Uma bruxa lança uma terrível maldição sobre a jovem Sophie transformando-a em uma velha. Desesperada,
 ela embarca em uma odisseia em busca do mago Howl, um misterioso feiticeiro que pode ajudá-la a reverter o feitiço.','5.0','1'),
('Meu Amigo Totoro', '1988', 
 'Duas irmãs se mudam para o campo e descobrem criaturas mágicas, incluindo Totoro, que as ajudam a lidar com os desafios da vida.', 
 '4.9', '4'),
('O Castelo no Céu', '1986', 
 'Sheeta e Pazu embarcam em uma aventura para encontrar uma cidade flutuante enquanto fogem de piratas e forças militares.', 
 '4.8', '1'),
('Princesa Mononoke', 1997, 
 'Ashitaka tenta mediar a paz entre humanos que exploram a natureza e espíritos da floresta liderados por uma guerreira chamada Mononoke.', 
 5.0, 2),
('Ponyo - Uma Amizade que Veio do Mar', 2008, 
 'Uma peixinha mágica chamada Ponyo quer se transformar em humana após fazer amizade com um garoto.', 
 '4.7', '4'),
('O Serviço de Entregas da Kiki', 1989, 
 'Kiki, uma jovem bruxa em treinamento, tenta encontrar seu lugar no mundo enquanto trabalha como entregadora.', 
 '4.6', '2'),
('O Conto da Princesa Kaguya', '2013', 
 'Baseado em uma lenda japonesa, Kaguya é encontrada em um bambu e cresce para enfrentar escolhas difíceis sobre seu destino.', 
'4.8', '6');

-- VER OS IDS DE CADA GENERO
-- SELECT id, nome as 'genero'
-- FROM genero;

-- VER OS FILMES
-- SELECT * FROM FILME;

import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'projetofinal'
}

try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)  

    sql = "SELECT f.id AS Filme_ID, f.titulo AS Filme, f.ano AS Ano, f.descricao AS Descricao, f.nota AS Nota, g.nome AS Genero FROM filme f JOIN genero g ON f.genero_id = g.id"
    cursor.execute(sql)

    resultados = cursor.fetchall()

    for row in resultados:
        print(f"Filme: {row['Filme']}, Ano: {row['Ano']}, Descrição: {row['Descricao']}, Nota: {row['Nota']}, Gênero: {row['Genero']}")

except mysql.connector.Error as e:
    print(f"Erro ao executar a operação: {e}")

finally:
    if cursor:
        cursor.close()
    if connection.is_connected():
        connection.close()

try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)  

    sql = "SELECT a.id AS Avaliacao_ID, a.usuario AS Usuario, a.nota_av AS Nota, a.comentario AS Comentario, f.titulo AS Filme FROM avaliacao a JOIN filme f ON a.filme_id = f.id"
    cursor.execute(sql)

    resultados = cursor.fetchall()

    for row in resultados:
        print(f"Filme: {row['Filme']}, Nota: {row['Nota']}, Avaliação ID: {row['Avaliacao_ID']}, Usuário: {row['Usuario']}, Comentário: {row['Comentario']}")

except mysql.connector.Error as e:
    print(f"Erro ao executar a operação: {e}")

finally:
    if cursor:
        cursor.close()
    if connection.is_connected():
        connection.close()
        
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)  

    sql = "SELECT id, nome FROM genero"
    cursor.execute(sql)

    resultados = cursor.fetchall()

    for row in resultados:
        print(f"Gênero: {row['nome']}, ID: {row['id']}")

except mysql.connector.Error as e:
    print(f"Erro ao executar a operação: {e}")

finally:
    if cursor:
        cursor.close()
    if connection.is_connected():
        connection.close()
    
    
class Banco:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Estabelece a conexão e o cursor quando o 'with' é usado."""
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        
        # Criando o cursor
        self.cursor = self.connection.cursor(dictionary=True)
        
        # Retorna o cursor para ser usado no contexto
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fecha o cursor e a conexão quando o 'with' sai do bloco."""
        if self.cursor:
            self.cursor.close()  # Fecha o cursor
        if self.connection:
            self.connection.close()  # Fecha a conexão


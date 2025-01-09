import mysql.connector

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

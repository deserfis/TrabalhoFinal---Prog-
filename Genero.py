from utils import *
class Genero:
    def __init__(self, nome):
        self.__nome = nome.upper()  # Nome do gênero sempre em maiúsculo

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, value):
        self.__nome = value.upper()  # Garante que o nome será sempre em maiúsculo


    # Inserir um novo gênero no banco de dados
    def inserir(self, cursor):
        if not self.pedir_senha():
            print("Senha incorreta! Acesso negado.")
            return
        
        try:
            query = "INSERT INTO generos (nome) VALUES (%s)"
            cursor.execute(query, (self.__nome,))
            print(f"Gênero '{self.__nome}' inserido com sucesso!")
        except Exception as e:
            print(f"Erro ao inserir gênero: {e}")

    # Consultar filmes por gênero
    @staticmethod
    def consultar_por_genero(cursor, genero_nome):
        try:
            genero_nome = genero_nome.upper()  # Convertendo para maiúsculo
            query = "SELECT f.titulo FROM filmes f JOIN generos g ON f.genero = g.nome WHERE g.nome = %s"
            cursor.execute(query, (genero_nome,))
            filmes = cursor.fetchall()
            if filmes:
                print(f"Filmes do gênero '{genero_nome}':")
                for filme in filmes:
                    print(f"- {filme[0]}")
            else:
                print(f"Nenhum filme encontrado para o gênero '{genero_nome}'.")
        except Exception as e:
            print(f"Erro ao consultar filmes por gênero: {e}")

    # Atualizar o nome de um gênero no banco de dados
    def atualizar(self, cursor):
        if not self.pedir_senha():
            print("Senha incorreta! Acesso negado.")
            return
        
        try:
            novo_nome = input(f"Digite o novo nome para o gênero '{self.__nome}': ").strip().upper()
            confirmacao = input(f"Você tem certeza que deseja alterar o nome do gênero para '{novo_nome}'? (s/n): ").strip().lower()
            
            if confirmacao == "s":
                query = "UPDATE generos SET nome=%s WHERE nome=%s"
                cursor.execute(query, (novo_nome, self.__nome))
                self.__nome = novo_nome
                print(f"Gênero atualizado para '{self.__nome}' com sucesso!")
            else:
                print("Alteração cancelada.")
        except Exception as e:
            print(f"Erro ao atualizar gênero: {e}")

    # Excluir um gênero do banco de dados
    def excluir(self, cursor):
        if not self.pedir_senha():
            print("Senha incorreta! Acesso negado.")
            return
        
        try:
            confirmacao = input(f"Você tem certeza que deseja excluir o gênero '{self.__nome}'? (s/n): ").strip().lower()
            if confirmacao == "s":
                query = "DELETE FROM generos WHERE nome=%s"
                cursor.execute(query, (self.__nome,))
                print(f"Gênero '{self.__nome}' excluído com sucesso!")
            else:
                print("Exclusão cancelada.")
        except Exception as e:
            print(f"Erro ao excluir gênero: {e}")

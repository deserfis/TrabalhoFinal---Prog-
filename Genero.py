from utils import *
from Banco import Banco
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
    def inserir(self):
        if not self.pedir_senha(): # Requisita senha para o acesso
            print("Senha incorreta! Acesso negado.")
            return
        
        try:
            with Banco(host="localhost", user="seu_usuario", password="sua_senha", database="nome_do_banco") as cursor:
                query = "INSERT INTO genero (nome) VALUES (%s)" #Insere o genero na tabela
                cursor.execute(query, (self.__nome,))
                # Commit para salvar as alterações no banco
                cursor.connection.commit()
                print(f"Gênero '{self.__nome}' inserido com sucesso!")
        except Exception as e:
            print(f"Erro ao inserir gênero: {e}")

    # Consultar filmes por gênero
    @staticmethod
    def consultar_por_genero(self):

        try:
            with Banco(host="localhost", user="seu_usuario", password="sua_senha", database="nome_do_banco") as cursor:
                query = "SELECT f.titulo FROM filme f JOIN genero g ON f.genero = g.nome WHERE g.nome = %s" #Seleciona o título dos filmes do respectivo gênero
                cursor.execute(query, (self.__nome,))
                filmes = cursor.fetchall()
                if filmes:
                    print(f"Filmes do gênero '{self.__nome}':") #Imprime o título dos filmes
                    for filme in filmes:
                        print(f"- {filme[0]} ")
                else:
                    print(f"Nenhum filme encontrado para o gênero '{self.__nome}'.")
        except Exception as e:
            print(f"Erro ao consultar filmes por gênero: {e}")

    # Excluir um gênero do banco de dados
    def excluir(self):
    
        if not self.pedir_senha(): # Requisita senha para o acesso
            print("Senha incorreta! Acesso negado.")
            return
        
        try:
            with Banco(host="localhost", user="seu_usuario", password="sua_senha", database="nome_do_banco") as cursor:
                confirmacao = input(f"Você tem certeza que deseja excluir o gênero '{self.__nome}'? (s/n): ").strip().lower()
                if confirmacao == "s":
                    query = "DELETE FROM genero WHERE nome=%s" #Deleta o gênero da tabela
                    cursor.execute(query, (self.__nome,))
                    # Commit para salvar as alterações no banco
                    cursor.connection.commit()
                    print(f"Gênero '{self.__nome}' excluído com sucesso!")
                else:
                    print("Exclusão cancelada.")
        except Exception as e:
            print(f"Erro ao excluir gênero: {e}")

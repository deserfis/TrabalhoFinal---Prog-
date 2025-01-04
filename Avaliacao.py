from utils import atualizar_nota
from Filme import Filme
class Avaliacao:
    def __init__(self, usuario, filme, nota_av, comentario=""):
        # Convertendo os atributos de string para maiúsculas onde necessário
        self.__usuario = usuario.upper()  # Converte o usuário para maiúsculo
        self.__filme = filme.upper()  # Converte o filme para maiúsculo
        self.__nota_av = nota_av
        self.__comentario = comentario  # Mantém o comentário como está

    @property
    def usuario(self):
        return self.__usuario

    @property
    def filme(self):
        return self.__filme

    @property
    def nota_av(self):
        return self.__nota_av

    @nota_av.setter
    def nota_av(self, value):
        if 0.5 <= value <= 5.0:  # Validando a nota
            self.__nota_av = value
        else:
            raise ValueError("Nota deve ser entre 0.5 e 5.0")

    @property
    def comentario(self):
        return self.__comentario

    @comentario.setter
    def comentario(self, value):
        self.__comentario = value  # Mantém o comentário como está

    # Método para salvar a avaliação no banco de dados
    def salvar(self, cursor):
        try:
            query = "INSERT INTO avaliacoes (usuario, filme, nota, comentario) VALUES (%s, %s, %s, %s)"
            values = (self.__usuario, self.__filme, self.__nota_av, self.__comentario)
            cursor.execute(query, values)
            
            # Atualiza a nota do filme após a inserção da avaliação
            Filme.atualizar_nota(cursor, self.__filme)
        except Exception as e:
            print(f"Erro ao salvar avaliação: {e}")

    # Consultar avaliação de um filme por usuário
    @staticmethod
    def consultar_avaliacao(cursor, usuario, filme):
        try:
            usuario = usuario.upper()  # Converte o usuário para maiúsculo
            filme = filme.upper()  # Converte o filme para maiúsculo
            query = "SELECT * FROM avaliacoes WHERE usuario=%s AND filme=%s"
            cursor.execute(query, (usuario, filme))
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao consultar avaliação: {e}")
            return None

    # Excluir avaliação
    def excluir(self, cursor):
        try:
            query = "DELETE FROM avaliacoes WHERE usuario=%s AND filme=%s"
            cursor.execute(query, (self.__usuario, self.__filme))
            
            # Atualiza a nota do filme após a exclusão da avaliação
            Filme.atualizar_nota(cursor, self.__filme)
        except Exception as e:
            print(f"Erro ao excluir avaliação: {e}")

    # Método para editar a avaliação
    def editar_avaliacao(self, cursor):
        print(f"\nVocê está editando a avaliação do filme: {self.__filme} por {self.__usuario}")
        
        while True:
            print("\nO que você deseja editar?")
            print("1. Nota")
            print("2. Comentário")
            print("3. Cancelar edição")
            opcao = input("Escolha uma opção (1-3): ").strip()
            
            if opcao == "1":
                try:
                    nova_nota = float(input("Digite a nova nota (entre 0.5 e 5.0): ").strip())
                    self.nota_av = nova_nota  # Usando a validação do setter de nota
                    confirmacao = input(f"Você tem certeza que deseja alterar a nota para '{nova_nota}'? (s/n): ").strip().lower()
                    if confirmacao == "s":
                        # Atualiza a avaliação no banco de dados
                        query = "UPDATE avaliacoes SET nota=%s WHERE usuario=%s AND filme=%s"
                        values = (self.__nota_av, self.__usuario, self.__filme)
                        cursor.execute(query, values)
                        print(f"Nota alterada para: {self.__nota_av}")
                        # Atualiza a nota do filme após a alteração
                        Filme.atualizar_nota(cursor, self.__filme)
                except ValueError:
                    print("Por favor, insira uma nota válida.")
            
            elif opcao == "2":
                nova_descricao = input("Digite o novo comentário: ").strip()
                confirmacao = input(f"Você tem certeza que deseja alterar o comentário? (s/n): ").strip().lower()
                if confirmacao == "s":
                    # Atualiza a avaliação no banco de dados
                    query = "UPDATE avaliacoes SET comentario=%s WHERE usuario=%s AND filme=%s"
                    values = (nova_descricao, self.__usuario, self.__filme)
                    cursor.execute(query, values)
                    self.__comentario = nova_descricao
                    print("Comentário alterado.")
            
            elif opcao == "3":
                print("Edição cancelada.")
                break
            else:
                print("Opção inválida! Tente novamente.")
                continue

            # Pergunta se deseja fazer outra alteração
            continuar = input("\nDeseja editar mais algum dado? (s/n): ").strip().lower()
            if continuar != "s":
                break


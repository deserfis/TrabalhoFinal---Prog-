from utils import *
from Filme import Filme
class Avaliacao:
    def __init__(self, usuario, filme, nota_av, comentario=""):
# Verificar se a nota é válida
        if not validar_nota(nota_av):
            print("A nota deve ser estrelas inteiras ou meias. Ex: 1 (estrela); 2.5 (estrelas); 4 (estrelas).")
            return  # Interrompe a criação do objeto, se a nota for inválida
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
            # Verifica se o usuário já avaliou este filme
            avaliacao_existente = self.consultar_avaliacao(cursor, self.__usuario, self.__filme)
            if avaliacao_existente:
                resposta = input(f"Você já fez uma avaliação do filme '{self.__filme}', deseja editá-la? (s/n): ").strip().lower()
                if resposta == 's':
                    # Se o usuário deseja editar, chamamos o método de edição
                    self.editar_avaliacao(cursor)
                    return  # Sai do método após edição
                else:
                    print(f"A avaliação do filme '{self.__filme}' não será alterada.")
                    return  # Sai do método sem salvar nada
            else:
                    # Busca o ID do filme com base no nome
                query = "SELECT id FROM filme WHERE nome LIKE %s"
                cursor.execute(query, (f"%{self.__filme}%",))
                filme_result = cursor.fetchone()
    
                if filme_result is None:
                    raise ValueError(f"Filme '{self.__filme}' não encontrado na tabela de filmes.")
                
                filme_id = filme_result[0]  # Obtém o ID do gênero
                # Se não houver avaliação, insere uma nova
                query = "INSERT INTO avaliacao (usuario, filme, nota, comentario) VALUES (%s, %s, %s, %s)"
                values = (self.__usuario, filme_id, self.__nota_av, self.__comentario)
                cursor.execute(query, values)

                # Atualiza a nota do filme após a inserção da avaliação
                Filme.atualizar_nota(cursor, filme_id)
                print(f"Avaliação do filme '{self.__filme}' realizada com sucesso!")
        except ValueError as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Erro ao salvar avaliação: {e}")
            
    # Excluir avaliação
    def excluir(self, cursor):
        try:
            query = "DELETE FROM avaliacao WHERE usuario=%s AND filme=%s"
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
                    if validar_nota(nova_nota):
                        self.nota_av = nova_nota  # Usando a validação do setter de nota
                        confirmacao = input(f"Você tem certeza que deseja alterar a nota para '{nova_nota}'? (s/n): ").strip().lower()
                        if confirmacao == "s":
                            # Atualiza a avaliação no banco de dados
                            query = "UPDATE avaliacao SET nota=%s WHERE usuario=%s AND filme=%s"
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
                    query = "UPDATE avaliacao SET comentario=%s WHERE usuario=%s AND filme=%s"
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


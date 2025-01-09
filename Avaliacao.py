from utils import *
from Filme import Filme
from Banco import Banco
class Avaliacao:
    def __init__(self, usuario, filme, nota_av, comentario=""):
        # Verificar se a nota inserida é válida
        if not validar_nota(nota_av):
            print("A nota deve ser estrelas inteiras ou meias. Ex: 1 (estrela); 2.5 (estrelas); 4 (estrelas).")
            return  # Interrompe a criação do objeto, se a nota for inválida
        # Convertendo os atributos de string para maiúsculas onde necessário
        self.__usuario = usuario.upper()
        self.__filme = filme.upper()
        self.__nota_av = nota_av
        self.__comentario = comentario

    @property
    def usuario(self):
        return self.__usuario

    @usuario.setter
    def usuario(self, value):
        self.__usuario = value


    @property
    def filme(self):
        return self.__filme
    
    @filme.setter
    def filme(self, value):
        self.__filme = value


    @property
    def nota_av(self):
        return self.__nota_av

    @nota_av.setter
    def nota_av(self, value):
        if 0.5 <= value <= 5.0:  # Validando a nota para ver se está nos limites
            self.__nota_av = value
        else:
            raise ValueError("Nota deve ser entre 0.5 e 5.0")

    @property
    def comentario(self):
        return self.__comentario

    @comentario.setter
    def comentario(self, value):
        self.__comentario = value

    # Método para salvar a avaliação no banco de dados
    def salvar_av(self):
        try:
            with Banco(host="localhost", user="seu_usuario", password="sua_senha", database="nome_do_banco") as cursor:
                # Verifica se o usuário já avaliou este filme
                avaliacao_existente = self.consultar_avaliacao()
                if avaliacao_existente:
                    # Dá a opção do usuário editar a avaliação de um filme que já avaliou
                    resposta = input(f"Você já fez uma avaliação do filme '{self.__filme}', deseja editá-la? (s/n): ").strip().lower()
                    if resposta == 's':
                        # Se o usuário deseja editar, chama o método de edição
                        self.editar()
                        return  # Sai do método após edição
                    else:
                        print(f"A avaliação do filme '{self.__filme}' não será alterada.")
                        return  # Sai do método sem salvar nada
                else:
                    id_filme = Avaliacao.buscar_id_filme(self.__filme) #Procura o id do respectivo filme
                    # Se não houver avaliação, insere uma nova
                    query = "INSERT INTO avaliacao (usuario, filme, nota, comentario) VALUES (%s, %s, %s, %s)"
                    values = (self.__usuario, id_filme, self.__nota_av, self.__comentario)
                    cursor.execute(query, values)
                    # Commit para salvar as alterações no banco
                    cursor.connection.commit()

                    # Atualiza a nota do filme após a inserção da avaliação
                    Filme.atualizar_nota(cursor, id_filme)
                    print(f"Avaliação do filme '{self.__filme}' realizada com sucesso!")

        except ValueError as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Erro ao salvar avaliação: {e}")

    # Método para consultar uma avaliação existente de um usuário para um filme
    def consultar_avaliacao(self):
        try:
            with Banco(host="localhost", user="seu_usuario", password="sua_senha", database="nome_do_banco") as cursor:
                # Realiza a consulta no banco de dados usando LIKE para o título do filme
                query = "SELECT a.nota, a.comentario " \
                        "FROM avaliacao a " \
                        "JOIN filme f ON a.filme = f.id " \
                        "WHERE a.usuario=%s AND f.titulo LIKE %s"
                cursor.execute(query, (self.__usuario, f"%{self.__filme}%"))
                resultado = cursor.fetchone()  # Retorna a primeira linha (se houver)

                if resultado:
                    # Caso exista, retorna os dados da avaliação (nota, comentário)
                    nota, comentario = resultado
                    return {"usuario": self.__usuario, "filme": self.__filme, "\nnota": nota, "\ncomentario": comentario}
                else:
                    # Caso não exista, exibe uma mensagem e retorna None
                    print("Não há nenhuma avaliação com os dados que você inseriu :(")
                return None
        except Exception as e:
            print(f"Erro ao consultar avaliação: {e}")
            return None

    # Método para editar a avaliação e atualizar no banco de dados no final
    def editar(self):
        print(f"\nVocê está editando a avaliação do filme: {self.__filme} por {self.__usuario}")
        
        #Variáveis booleanas para conferir depois se algo foi editado
        nota_editada = False 
        comentario_editado = False

        while True: #Mostra uma lista de opções do que o usuário pode editar
            print("\nO que você deseja editar?")
            print("1. Nota")
            print("2. Comentário")
            print("3. Cancelar edição")
            opcao = input("Escolha uma opção (1-3): ").strip()

            if opcao == "1":#Editar nota
                try:
                    nova_nota = float(input("Digite a nova nota (entre 0.5 e 5.0): ").strip())
                    if validar_nota(nova_nota) and 0.5 <= nova_nota <= 5.0:#Valida a nova nota
                        self.nota_av = nova_nota  # Usando a validação (de limite) do setter de nota
                        confirmacao = input(f"Você tem certeza que deseja alterar a nota para '{nova_nota}'? (s/n): ").strip().lower()
                        if confirmacao == "s":
                            nota_editada = True  # Marca que a nota foi editada
                            print(f"Nota alterada para: {self.__nota_av}")
                    else:
                        print("Por favor, insira uma nota válida.")
                except ValueError: #Mensagem de erro caso a função validar_nota retorne False
                    print("Por favor, insira uma nota válida.")

            elif opcao == "2":#Edita comentário
                nova_descricao = input("Digite o novo comentário: ").strip()
                confirmacao = input(f"Você tem certeza que deseja alterar o comentário? (s/n): ").strip().lower()
                if confirmacao == "s":
                    self.__comentario = nova_descricao
                    comentario_editado = True  # Marca que o comentário foi editado
                    print("Comentário alterado.")

            elif opcao == "3":#Cancela a edição
                print("Edição cancelada.")
                break
            else:
                print("Opção inválida! Tente novamente.")
                continue

            # Pergunta se deseja fazer outra alteração
            continuar = input("\nDeseja editar mais algum dado? (s/n): ").strip().lower()
            if continuar != "s":
                break

        # Após todas as edições, atualiza os dados no banco de dados
        if nota_editada or comentario_editado:
            try:
                with Banco(host="localhost", user="seu_usuario", password="sua_senha", database="nome_do_banco") as cursor:
                    id_filme = Avaliacao.buscar_id_filme(self.__filme) #Procura o id do respectivo filme
                    # Atualiza a avaliação no banco de dados
                    query = "UPDATE avaliacao SET nota=%s, comentario=%s WHERE usuario=%s AND filme=%s"
                    values = (self.__nota_av, self.__comentario, self.__usuario, id_filme)
                    cursor.execute(query, values)
                    # Commit para salvar as alterações no banco
                    cursor.connection.commit()
                    print(f"Avaliação do filme '{self.__filme}' atualizada com sucesso!")
                    
                    # Atualiza a nota do filme após a alteração da avaliação
                    Filme.atualizar_nota(cursor, id_filme)
            except Exception as e:
                print(f"Erro ao atualizar avaliação: {e}")
    
    # Excluir avaliação
    def excluir(self):
        
        id_filme = Avaliacao.buscar_id_filme(self.__filme) #Procura o id do respectivo filme
        try:
            with Banco(host="localhost", user="seu_usuario", password="sua_senha", database="nome_do_banco") as cursor:
                query = "DELETE FROM avaliacao WHERE usuario=%s AND filme=%s"
                cursor.execute(query, (self.__usuario, id_filme))
                # Commit para salvar as alterações no banco
                cursor.connection.commit()
                # Atualiza a nota do filme após a exclusão da avaliação
                Filme.atualizar_nota(cursor, id_filme)
        except Exception as e:
            print(f"Erro ao excluir avaliação: {e}")

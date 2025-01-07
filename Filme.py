from utils import *
from Genero import Genero
class Filme:
    def __init__(self, titulo, descricao, ano, genero, nota=0.5):
        # Convertendo os atributos de string para maiúsculas onde necessário
        self.__titulo = titulo.upper()
        self.__descricao = descricao  # Mantém a descrição como está
        self.__ano = ano
        self.__genero = genero.upper()
        self.__nota = nota  # Nota padrão de 0.5

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, value):
        self.__titulo = value.upper()

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, value):
        self.__descricao = value

    @property
    def ano(self):
        return self.__ano

    @ano.setter
    def ano(self, value):
        if value > 1900 and value <= 2025:  # Validação de ano
            self.__ano = value
        else:
            raise ValueError("Ano inválido!")

    @property
    def genero(self):
        return self.__genero

    @genero.setter
    def genero(self, value):
        self.__genero = value.upper()

    @property
    def nota(self):
        return self.__nota

    @nota.setter
    def nota(self, value):
        if 0.5 <= value <= 5.0:  # Validando a nota
            self.__nota = value
        else:
            raise ValueError("Nota deve ser entre 0.5 e 5.0")

    # Método para salvar o filme no banco de dados
    def salvar_filme(self, cursor):
        if not self.pedir_senha(): # Requisita senha para o acesso
            print("Acesso negado. Senha incorreta!")
            return
        try:
            # Verifica se o filme já foi salvo anteriormente
            filme_existente = self.buscar_por_nome(cursor, self.__titulo)
            if filme_existente:
                resposta = input(f"O filme '{self.__titulo}' já foi registrado no banco, deseja editá-lo? (s/n): ").strip().lower()
                if resposta == 's':
                    # Se o usuário deseja editar, chama o método de edição
                    self.atualizar(cursor)
                    return  # Sai do método após edição
                else:
                    print(f"O filme '{self.__titulo}' não será alterado.")
                    return  # Sai do método sem salvar nada
            #Se o filme não existe, prossegue
            else:
                genero_id = Filme.buscar_id_genero(self.__genero)#Trpca o nome do gênero pelo id

                # Verifica as avaliações do filme e calcula a média das notas
                query = "SELECT AVG(nota) FROM avaliacao WHERE filme=%s"
                cursor.execute(query, (self.__titulo,))
                resultado = cursor.fetchone()
                #Se existem avaliações, pega a média e arredonda para uma casa decimal
                if resultado[0] is not None:
                    self.__nota = round(resultado[0], 1)
                else: #Se não existe, coloca o valor padrão
                    self.__nota = 0.5

                # Salva o filme (com o ID do gênero)
                query = "INSERT INTO filme (titulo, descricao, ano, genero_id, nota) VALUES (%s, %s, %s, %s, %s)"
                values = (self.__titulo, self.__descricao, self.__ano, genero_id, self.__nota)
                cursor.execute(query, values)
        except Exception as e:
            print(f"Erro ao salvar filme: {e}")
            
    # Buscar filme por nome (garante que o nome seja convertido para maiúsculo na busca)
    @staticmethod
    def buscar_por_nome(cursor, nome):
        try:
            nome = nome.upper()
            query = "SELECT f.titulo, f.ano, g.nome, f.nota, f.descricao FROM filme f JOIN genero g ON f.genero_id = g.id WHERE f.titulo LIKE %s;" #Pega as informações do filme, inclusive o nome do gênero em vez do id
            cursor.execute(query, (f"%{nome}%",))
            return cursor.fetchall()  # Retorna todos os filmes encontrados
        except Exception as e:
            print(f"Erro ao buscar filme: {e}")
            return None

    # Método de atualização com senha e persistência no banco
    def atualizar(self, cursor):
        print(f"\nVocê está atualizando o filme: {self.__titulo}\n")
        
        if not self.pedir_senha(): # Requisita senha para o acesso
            print("Acesso negado. Senha incorreta!")
            return
        
        while True: #Exibe uma lista do que o usuário pode editar
            print("\nO que você deseja atualizar?")
            print("1. Título")
            print("2. Descrição")
            print("3. Ano")
            print("4. Gênero")
            print("5. Cancelar atualização")
            opcao = input("Escolha uma opção (1-5): ").strip()
            
            if opcao == "1":#Edita título
                novo_titulo = input("Digite o novo título: ").strip()
                confirmacao = input(f"Você tem certeza que deseja alterar o título para '{novo_titulo}'? (s/n): ").strip().lower()
                if confirmacao == "s":
                    self.__titulo = novo_titulo.upper()
                    print(f"Título alterado para: {self.__titulo}")
            elif opcao == "2":#Edita descrição
                nova_descricao = input("Digite a nova descrição: ").strip()
                confirmacao = input(f"Você tem certeza que deseja alterar a descrição? (s/n): ").strip().lower()
                if confirmacao == "s":
                    self.__descricao = nova_descricao
                    print("Descrição alterada.")
            elif opcao == "3":#Edita ano
                try:
                    novo_ano = int(input("Digite o novo ano: ").strip())
                    confirmacao = input(f"Você tem certeza que deseja alterar o ano para '{novo_ano}'? (s/n): ").strip().lower()
                    if confirmacao == "s":
                        self.__ano = novo_ano
                        print(f"Ano alterado para: {self.__ano}")
                except ValueError:
                    print("Por favor, insira um ano válido.")
            elif opcao == "4":#Edita gênero
                novo_genero = input("Digite o novo gênero: ").strip()
                confirmacao = input(f"Você tem certeza que deseja alterar o gênero para '{novo_genero}'? (s/n): ").strip().lower()
                if confirmacao == "s":
                    self.__genero = novo_genero.upper()
                    print(f"Gênero alterado para: {self.__genero}")
            elif opcao == "5":
                print("Atualização cancelada.")
                break
            else:
                print("Opção inválida! Tente novamente.")
                continue

            # Pergunta se deseja fazer outra alteração
            continuar = input("\nDeseja atualizar mais algum dado? (s/n): ").strip().lower()
            if continuar != "s":
                break

        # Após a atualização, atualiza os dados no banco de dados
        try:
            genero_id = Filme.buscar_id_genero(self.__genero)#Trpca o nome do gênero pelo id
            
            #Atualiza os dados no banco    
            query = "UPDATE filme SET descricao=%s, ano=%s, genero=%s, nota=%s WHERE titulo=%s"
            values = (self.__descricao, self.__ano, genero_id, self.__nota, self.__titulo)
            cursor.execute(query, values)
            print(f"Filme '{self.__titulo}' atualizado com sucesso!")
            
            # Atualiza a nota do filme após as alterações
            self.atualizar_nota(cursor)
        except Exception as e:
            print(f"Erro ao atualizar filme: {e}")

    # Excluir um filme do banco de dados
    def excluir_filme(self, cursor):
        if not self.pedir_senha(): # Requisita senha para o acesso
            print("Senha incorreta! Acesso negado.")
            return
        
        try:
            query = "DELETE FROM filme WHERE titulo=%s"
            cursor.execute(query, (self.__titulo,))
            print(f"Filme '{self.__titulo}' excluído com sucesso!")
        except Exception as e:
            print(f"Erro ao excluir filme: {e}")

# Função para atualizar a nota do filme
def atualizar_nota(cursor, filme):
    # Calcular a média das avaliações para o filme
    query = "SELECT AVG(nota) FROM avaliacao WHERE filme=%s"  # Corrigido o nome da tabela para 'avaliacao'
    cursor.execute(query, (filme,))
    resultado = cursor.fetchone()

    # Verifica se há avaliações e calcula a média
    if resultado[0] is not None:
        nova_nota = round(resultado[0], 1)  # Média arredondada
    else:
        nova_nota = 0.5  # Caso não haja avaliações, atribui a nota mínima

    # Atualiza a nota do filme com a nova média
    update_query = "UPDATE filme SET nota=%s WHERE id=%s"  # Corrigido o nome da tabela para 'filme' e o campo 'nota'
    cursor.execute(update_query, (nova_nota, filme))
    
    # Commit para garantir que a alteração seja salva
    cursor.connection.commit()  # Usando 'connection' no lugar de 'conn'


# Função para pedir a senha para operações CRUD
def pedir_senha():
    senha = input("Digite a senha para continuar: ").strip()
    return senha == "root" #Confere se a senha inserida == "root", se sim retorna True, se não retorna False

#Função para validar se a nota são estrelas inteiras ou meias
def validar_nota(nota):
    return nota.is_integer() or (nota * 2).is_integer()  # Valida 0.5, 1.0, 1.5, etc.

def buscar_id_filme(cursor, filme):
    # Busca o ID do filme com base no nome
    query = "SELECT id FROM filme WHERE titulo LIKE %s"
    cursor.execute(query, (f"%{filme}%",))
    filme_result = cursor.fetchone()
    
    if filme_result is None: #Se tentar fazer um comentário para um filme que não existe, exibe uma mensagem de erro
        raise ValueError(f"Filme '{filme}' não encontrado na tabela de filme.")
                
    filme_id = filme_result[0]  # Obtém o ID do filme
    return filme_id

def buscar_id_genero(cursor, genero):
    # Busca o ID do gênero com base no nome
    query = "SELECT id FROM genero WHERE nome = %s"
    cursor.execute(query, (genero,))
    genero_result = cursor.fetchone()
    #Se o gênero não existe, exibe uma mensagem de erro
    if genero_result is None:
        raise ValueError(f"Gênero '{genero}' não encontrado na tabela de gêneros.")
    genero_id = genero_result[0]  # Obtém o ID do gênero
    return genero_id

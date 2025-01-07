# Função para atualizar a nota do filme
def atualizar_nota(cursor, filme):
    query = "SELECT AVG(nota) FROM avaliacoes WHERE filme=%s"
    cursor.execute(query, (filme,))
    resultado = cursor.fetchone()
    
    # Verifica a média da nota e atualiza a nota do filme
    if resultado[0] is not None:
        return round(resultado[0], 1)  # Retorna a média arredondada
    return 0.5  # Caso não haja avaliações, retorna 0.5

# Função para pedir a senha para operações CRUD
def pedir_senha():
    senha = input("Digite a senha para continuar: ").strip()
    return senha == "root" #Confere se a senha inserida == "root", se sim retorna True, se não retorna False

#Função para validar se a nota são estrelas inteiras ou meias
def validar_nota(nota):
    if (nota * 10) % 10 == 0 or (nota * 10) % 10 == 5:
        return True 
    return False

def buscar_id_filme(cursor, filme):
    # Busca o ID do filme com base no nome
    query = "SELECT id FROM filme WHERE nome LIKE %s"
    cursor.execute(query, (f"%{filme}%",))
    filme_result = cursor.fetchone()
    
    if filme_result is None: #Se tentar fazer um comentário para um filme que não existe, exibe uma mensagem de erro
        raise ValueError(f"Filme '{filme}' não encontrado na tabela de filmes.")
                
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

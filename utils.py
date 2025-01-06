# Função para atualizar a nota do filme
def atualizar_nota(cursor, filme):
    query = "SELECT AVG(nota) FROM avaliacoes WHERE filme_id=%s"
    cursor.execute(query, (filme,))
    resultado = cursor.fetchone()
    
    # Verifica a média da nota e atualiza a nota do filme
    if resultado[0] is not None:
        return round(resultado[0], 1)  # Retorna a média arredondada
    return 0.5  # Caso não haja avaliações, retorna 0.5

# Função para pedir a senha para operações CRUD
def pedir_senha():
    senha = input("Digite a senha para continuar: ").strip()
    return senha == "root"

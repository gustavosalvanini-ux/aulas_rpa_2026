def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:
    # Função com tipagem de parâmetros que empacota os dados em um dicionário estruturado
    return {
        "nome": nome,
        # Chave 'nome' com o valor passado por parâmetro
        "cargo": cargo,
        # Chave 'cargo' com a função profissional
        "salario": salario
        # Chave 'salario' com o valor monetário em ponto flutuante
    }


def exibir_colaboradores(lista_colaboradores: list) -> None:
    # Função para iterar sobre a lista de colaboradores e exibir seus dados
    for colaborador in lista_colaboradores:
        # Percorre cada dicionário presente na lista
        print(f"Nome: {colaborador['nome']}, Cargo: {colaborador['cargo']}, Salário: {colaborador['salario']}")
        # Imprime os campos formatados acessando as chaves do dicionário

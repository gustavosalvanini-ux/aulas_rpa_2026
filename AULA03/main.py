from mod_rh import cadastrar_colaborador, exibir_colaboradores
# Importa as funções de manipulação de dados definidas no módulo mod_rh

lista_colaboradores = []
# Cria a lista em memória que armazenará os dicionários de cada colaborador

while True:
    # Loop infinito do menu interativo no terminal
    print("Menu de RH:")
    # Exibe o título do menu
    print("1 - Cadastrar")
    # Opção 1 para cadastrar novo colaborador
    print("2 - Listar")
    # Opção 2 para exibir os colaboradores existentes
    print("0 - Sair")
    # Opção 0 para finalizar o programa
    opcao = input("Digite a opção: ")
    # Lê a escolha digitada pelo usuário via teclado

    if opcao == "1":
        # Se a opção for cadastro
        nome = input("Digite o nome: ")
        # Solicita e armazena o nome do colaborador
        cargo = input("Digite o cargo: ")
        # Solicita e armazena o cargo ocupado
        salario = float(input("Digite o salário: "))
        # Lê o salário e converte de texto para número decimal (float)
        lista_colaboradores.append(cadastrar_colaborador(nome, cargo, salario))
        # Chama a função que cria o dicionário e o adiciona no final da lista

    elif opcao == "2":
        # Se a opção for listagem
        exibir_colaboradores(lista_colaboradores)
        # Passa a lista atual para a função responsável pela impressão formatada

    elif opcao == "0":
        # Se o usuário escolheu sair
        break
        # Quebra o laço while e encerra a execução do script

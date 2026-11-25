BOT_NAME = "RPA_FINANCEIRO_01"
# Define o nome identificador do robô para logs e relatórios

MAX_RETRIES = 3
# Número máximo de tentativas de re-execução caso ocorra alguma falha

EXECUTION_TIMEOUT = 60.0  # in seconds
# Tempo limite máximo (em segundos) antes de considerar que o bot travou

IS_PRODUCTION = True
# Flag booleana indicando se o script está rodando em ambiente de produção

tls = 47
# Define a largura (em caracteres) para as linhas decorativas de separação

print("=" * tls)
# Imprime uma linha superior de cabeçalho com 47 caracteres '='

print(f"Iniciando bot {BOT_NAME}...")
# Exibe a mensagem de inicialização informando o nome do robô

print("-" * tls)
# Imprime uma linha divisória com 47 caracteres '-'

print(f"Bot: {BOT_NAME} - Tipo: {type(BOT_NAME)}")
# Exibe o valor da variável BOT_NAME e confirma que seu tipo de dado é string (str)

print(f"Max retries: {MAX_RETRIES} - Tipo: {type(MAX_RETRIES)}")
# Exibe o número de tentativas e confirma que o tipo é inteiro (int)

print(f"Execution timeout: {EXECUTION_TIMEOUT} - Tipo: {type(EXECUTION_TIMEOUT)}")
# Exibe o tempo de timeout e confirma que o tipo é ponto flutuante (float)

print(f"Is production: {IS_PRODUCTION} - Tipo: {type(IS_PRODUCTION)}")
# Exibe o status de produção e confirma que o tipo é booleano (bool)

print("-" * tls)
# Imprime outra linha divisória com 47 caracteres '-'

print("Configuração carregada com sucesso!")
# Mensagem informando que todas as variáveis iniciais foram validadas

print("=" * tls)
# Imprime a linha de fechamento do cabeçalho

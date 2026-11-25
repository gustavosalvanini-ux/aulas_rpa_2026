import logging
# Biblioteca padrão do Python para emissão e gravação de logs de eventos

logging.basicConfig(
    # Configuração central dos logs da aplicação
    level=logging.INFO,
    # Define o nível mínimo de severidade como INFO (ignora DEBUG)
    format="%(asctime)s - %(levelname)s - %(message)s",
    # Formato do registro: data/hora, nível de severidade e a mensagem
    handlers=[
        # Lista com os destinos dos logs
        logging.FileHandler("execucao_bot.log"),
        # Grava os registros em arquivo físico no disco
        logging.StreamHandler()
        # Exibe os mesmos registros diretamente no terminal/console
    ]
)


def processar_arquivo(caminho: str):
    # Função que abre com segurança o arquivo especificado e audita cada linha lida
    try:
        # Inicia bloco de tratamento para capturar exceções durante a abertura/leitura
        with open(caminho, mode="r", encoding="utf-8") as arquivo:
            # Abre o arquivo em modo leitura ('r') usando context manager (with)
            for linha in arquivo:
                # Itera linha a linha do arquivo sem carregar tudo de uma vez na memória
                logging.info(f"Linha lida: {linha}")
                # Registra a linha no arquivo de log e no console
    except FileNotFoundError:
        # Captura erro caso o arquivo informado não exista no caminho indicado
        logging.error(f"Arquivo não encontrado: {caminho}")
        # Registra a falha no log com status de ERROR
    finally:
        # Bloco que SEMPRE é executado, ocorrendo erro ou não
        logging.info("Tentativa de processamento finalizada")
        # Registra a conclusão da operação para fins de auditoria


processar_arquivo("pneumoultramicroscopiosilicovulcanicoconiotico.csv")
# Executa a função passando o nome do arquivo que será testado

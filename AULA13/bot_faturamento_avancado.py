"""
Lab 13: Arquitetura Orientada a Filas (Queue), Processamento Assíncrono
e Resiliência.

Implementa arquitetura Produtor-Consumidor com fila (queue.Queue),
logging corporativo rotativo (RotatingFileHandler) e padrão de Retry
com tenacity para resiliência de rede.
"""

import csv
# Leitura e manipulação de arquivos delimitados CSV
import logging
# Emissão de logs com níveis de severidade
from logging.handlers import RotatingFileHandler
# Handler de rotação automática de arquivos de log por tamanho máximo
from pathlib import Path
# Manipulação de arquivos e caminhos no sistema operacional
import queue
# Fila thread-safe (FIFO) para comunicação entre produtor e consumidor
import random
# Geração de números pseudoaleatórios para simular instabilidade de rede
import time
# Controle de pausas na execução

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)
# Tenacity: biblioteca robusta para implementação do padrão de re-tentativa (Retry Pattern)


def configurar_logger():
    """Configura o logger com RotatingFileHandler de 1MB por arquivo."""
    diretorio_base = Path(__file__).resolve().parent
    # Diretório onde o script reside
    caminho_log = diretorio_base / "app_rpa.log"
    # Arquivo de log destino

    logger = logging.getLogger("RPA_Queue_Bot")
    # Cria a instância nomeada do logger
    logger.setLevel(logging.INFO)
    # Define o nível de severidade para INFO

    if not logger.handlers:
        # Se os manipuladores ainda não foram adicionados
        handler = RotatingFileHandler(
            caminho_log,
            maxBytes=1024 * 1024,  # 1MB
            backupCount=3,
            encoding="utf-8",
        )
        # Rotaciona quando atingir 1MB mantendo até 3 arquivos históricos

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s"
        )
        # Formata com data/hora, nível, nome da thread e a mensagem
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console_handler = logging.StreamHandler()
        # Envia também a saída para o terminal
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


logger = configurar_logger()
# Inicializa o logger


def converter_nota(valor_bruto):
    """Limpa e converte valor textual de nota para float. Inválidos = 0.0."""
    if not valor_bruto:
        return 0.0
    texto_limpo = str(valor_bruto).strip().replace(",", ".")
    # Limpa espaços e troca vírgula por ponto
    try:
        return float(texto_limpo)
        # Converte para float
    except ValueError:
        return 0.0
        # Valores inválidos como 'FALTOU' viram 0.0


def produtor(fila, limite=10):
    """Lê o CSV da AULA07 e adiciona os primeiros 'limite' alunos na fila."""
    caminho_csv = (
        Path(__file__).resolve().parent.parent / "AULA07" / "notas_alunos.csv"
    )
    # Localiza a base de dados na pasta AULA07

    if not caminho_csv.exists():
        logger.error("Arquivo %s não encontrado!", caminho_csv)
        return

    logger.info("Produtor: Lendo alunos do arquivo %s", caminho_csv)
    total_enfileirados = 0

    with open(caminho_csv, mode="r", encoding="utf-8") as f:
        # Abre o CSV com separador ponto e vírgula
        leitor = csv.DictReader(f, delimiter=";")
        for linha in leitor:
            if total_enfileirados >= limite:
                break
                # Limita aos 10 primeiros alunos conforme exigido

            nome = linha.get("Nome", "").strip()
            ra = linha.get("RA", "").strip()

            registro = {
                "nome": nome,
                "ra": ra,
                "nota01": linha.get("Nota01", ""),
                "tf01": linha.get("TF01", ""),
                "nota02": linha.get("Nota02", ""),
                "tf02": linha.get("TF02", ""),
            }
            # Monta o dicionário bruto do aluno

            fila.put(registro)
            # Insere o registro no final da fila (Thread-safe)
            total_enfileirados += 1
            logger.info("Produtor: Aluno enfileirado -> %s (RA: %s)", nome, ra)

    logger.info(
        "Produtor: Finalizado o enfileiramento de %d alunos.",
        total_enfileirados
    )


class ErroConexaoPortal(Exception):
    """Exceção simulada de falha transitória de rede ao lançar nota."""

    pass


@retry(
    stop=stop_after_attempt(3),
    # Limita o número de tentativas em até 3 execuções
    wait=wait_fixed(0.5),
    # Aguarda 500 milissegundos entre cada tentativa
    retry=retry_if_exception_type(ErroConexaoPortal),
    # Dispara nova tentativa apenas se a falha for de conexão
    reraise=True,
    # Se esgotar as 3 tentativas, relança a exceção
)
def lancar_nota_portal(ra, media_final, status):
    """Simula o envio da nota ao portal acadêmico com retry resilience."""
    logger.info(
        "Tentando lançar nota no portal para RA: %s (Média: %.2f)...",
        ra,
        media_final,
    )
    # Simula 30% de chance de instabilidade de rede para testar o retry
    if random.random() < 0.3:
        logger.warning(
            "Falha transitória de rede ao conectar no portal para RA: %s",
            ra
        )
        raise ErroConexaoPortal("Falha de timeout/conexão no portal acadêmico!")

    logger.info(
        "Sucesso! RA: %s registrado no portal com status: %s",
        ra,
        status
    )
    return True


def consumidor(fila):
    """Retira alunos da fila, limpa dados, calcula médias e lança no portal."""
    logger.info("Consumidor: Iniciando processamento dos itens da fila...")
    processados = 0

    while not fila.empty():
        # Continua enquanto houver elementos na fila
        try:
            aluno = fila.get(block=False)
            # Retira o próximo aluno da fila
        except queue.Empty:
            break

        nome = aluno["nome"]
        ra = aluno["ra"] or "N/A"

        nota01 = converter_nota(aluno["nota01"])
        tf01 = converter_nota(aluno["tf01"])
        nota02 = converter_nota(aluno["nota02"])
        tf02 = converter_nota(aluno["tf02"])

        # Cálculo da média bimestral ponderada (nota peso 8, TF peso 2)
        media_b1 = (nota01 * 0.8) + (tf01 * 0.2) if nota01 > 8 else (
            nota01 + tf01
        )
        media_b2 = (nota02 * 0.8) + (tf02 * 0.2) if nota02 > 8 else (
            nota02 + tf02
        )
        media_final = (media_b1 + media_b2) / 2.0
        # Média semestral final

        status = "APROVADO" if media_final >= 6.0 else "REPROVADO"
        # Regra de corte: média mínima 6.0

        logger.info(
            "Aluno: %s | RA: %s | B1: %.2f | B2: %.2f | Final: %.2f | %s",
            nome,
            ra,
            media_b1,
            media_b2,
            media_final,
            status,
        )

        try:
            lancar_nota_portal(ra, media_final, status)
            # Envia para a função protegida pelo decorator @retry
        except Exception as e:
            logger.error(
                "Falha definitiva ao lançar notas do RA %s após retentativas: %s",
                ra,
                e,
            )

        fila.task_done()
        # Notifica a fila que o processamento daquele item terminou
        processados += 1
        time.sleep(0.05)

    logger.info("Consumidor: Finalizado. Total processado: %d", processados)


def main():
    """Função orquestradora da arquitetura orientada a filas."""
    logger.info("=== Iniciando Robô de Lançamento com Filas e Resiliência ===")
    fila_alunos = queue.Queue()
    # Instancia a fila sincronizada

    # 1. Produção: Enfileira os 10 primeiros alunos
    produtor(fila_alunos, limite=10)

    # 2. Consumo: Processa a fila, calcula médias e executa lançamentos com retry
    consumidor(fila_alunos)

    logger.info("=== Processamento concluído com sucesso! ===")


if __name__ == "__main__":
    main()

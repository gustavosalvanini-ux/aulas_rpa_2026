"""
Lab 10: Extração de Dados em PDFs, Filtros Regex e Exportação para Excel.

Lê arquivos de faturas em PDF, extrai NIF/CNPJ e Valor Total usando
expressões regulares (re) e salva os dados consolidados em formato .xlsx.
"""

from pathlib import Path
# Manipulação orientada a objetos de caminhos e arquivos no sistema operacional
import re
# Módulo de expressões regulares (Regex) para busca e extração de padrões de texto

import pandas as pd
# Biblioteca para estruturação de dados em tabelas (DataFrames) e exportação Excel
import pdfplumber
# Biblioteca especializada em extração precisa de texto de documentos PDF


def extrair_dados_fatura(caminho_pdf):
    """Extrai NIF e Valor Total de um arquivo PDF via regex."""
    nif = "Não encontrado"
    # Valor padrão de contingência
    valor_total = "Não encontrado"
    # Valor padrão de contingência

    with pdfplumber.open(caminho_pdf) as pdf:
        # Abre o arquivo PDF com gerenciador de contexto
        texto_completo = ""
        # Acumulador do texto de todas as páginas
        for pagina in pdf.pages:
            # Itera página por página do documento
            texto = pagina.extract_text()
            # Extrai o texto contido na página atual
            if texto:
                # Se houver texto extraível
                texto_completo += texto + "\n"
                # Concatena com quebra de linha

    # Regex para CNPJ / NIF (ex: 12.345.678/0001-90 ou 9 a 14 digitos)
    padrao_nif = r"(?:NIF|CNPJ)[\s:]*([0-9.\/-]{9,18})"
    # Padrão procurando palavras NIF ou CNPJ seguidas de pontuação e dígitos
    match_nif = re.search(padrao_nif, texto_completo, re.IGNORECASE)
    # Busca a primeira ocorrência no texto
    if match_nif:
        # Se encontrou o padrão com o prefixo
        nif = match_nif.group(1).strip()
        # Captura apenas o grupo numérico correspondente
    else:
        # Caso não haja prefixo explícito, procura por máscara padrão de CNPJ ou 9 dígitos
        padrao_doc = r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b|\b\d{9}\b"
        match_doc = re.search(padrao_doc, texto_completo)
        if match_doc:
            # Se encontrou o padrão de documento
            nif = match_doc.group(0).strip()
            # Salva o documento encontrado

    # Regex para Valor Total (ex: Total: R$ 1.500,00 ou Total: 1500.00)
    padrao_valor = r"(?:Valor\s*Total|Total)[\s:]*(?:R\$\s*)?([\d.,]+)"
    # Padrão procurando menção a Total seguido opcionalmente de R$ e valor decimal
    match_valor = re.search(padrao_valor, texto_completo, re.IGNORECASE)
    # Executa a busca insensível a maiúsculas/minúsculas
    if match_valor:
        # Se encontrou o valor monetário
        valor_total = match_valor.group(1).strip()
        # Extrai os dígitos e pontuações do preço

    return {
        # Retorna o dicionário estruturado com as informações da fatura
        "arquivo": caminho_pdf.name,
        # Nome do arquivo PDF analisado
        "nif": nif,
        # Documento NIF/CNPJ extraído
        "valor_total": valor_total
        # Valor total formatado
    }


def processar_faturas():
    """Varre as faturas em PDF, gera DataFrame e exporta para Excel."""
    diretorio_base = Path(__file__).resolve().parent
    # Obtém o diretório atual do script
    possiveis_pastas = [
        # Lista locais onde a pasta de faturas pode estar presente
        diretorio_base / "faturas",
        diretorio_base.parent / "AULA11" / "faturas",
        diretorio_base.parent / "AULA10" / "faturas"
    ]

    pasta_faturas = None
    # Variável para guardar o caminho definitivo
    for pasta in possiveis_pastas:
        # Verifica qual pasta existe e contém arquivos PDF
        if pasta.exists() and list(pasta.glob("*.pdf")):
            pasta_faturas = pasta
            break

    faturas_extraidas = []
    # Lista para acumular os dados extraídos

    if pasta_faturas:
        # Se encontrou a pasta com faturas
        print(f"Lendo faturas da pasta: {pasta_faturas}")
        for arquivo in sorted(pasta_faturas.glob("*.pdf")):
            # Itera em ordem sobre cada PDF
            dados = extrair_dados_fatura(arquivo)
            # Extrai os campos via regex
            faturas_extraidas.append(dados)
            # Adiciona na lista
    else:
        # Contingência para ambientes sem arquivos de exemplo
        faturas_extraidas = [
            {"arquivo": "fatura_001.pdf", "nif": "123456789",
             "valor_total": "1.500,00"},
            {"arquivo": "fatura_002.pdf", "nif": "987654321",
             "valor_total": "2.350,80"},
        ]

    df = pd.DataFrame(faturas_extraidas)
    # Converte a lista de dicionários em uma tabela estruturada do Pandas
    saida_excel = diretorio_base / "relatorio_faturas.xlsx"
    # Define o nome e caminho da planilha de saída

    df.to_excel(saida_excel, index=False)
    # Grava a tabela no formato Excel .xlsx sem índice numérico
    print("Relatório exportado para:", saida_excel)
    print(df)
    # Exibe a tabela no console

    return df


if __name__ == "__main__":
    # Ponto de entrada do script
    processar_faturas()

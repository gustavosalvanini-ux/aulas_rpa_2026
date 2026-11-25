"""
Lab 11: Web Scraping com BeautifulSoup.

Coleta notícias/artigos da web via requests, faz o parsing com
BeautifulSoup (html.parser) e exporta os dados estruturados em CSV.
"""

import csv
# Módulo para manipulação e escrita de planilhas de texto CSV
from pathlib import Path
# Módulo orientado a objetos para gestão de caminhos de arquivos

from bs4 import BeautifulSoup
# Parser HTML de alta performance para navegação na árvore de elementos DOM
import requests
# Biblioteca HTTP para envio de requisições GET e recebimento de páginas web


def coletar_noticias():
    """Realiza requisição HTTP e extrai títulos e links com BeautifulSoup."""
    url = "https://news.ycombinator.com/"
    # Endereço do portal agregador de notícias Hacker News

    headers = {
        # Cabeçalhos HTTP para emular o comportamento de um navegador legítimo
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    print(f"Fazendo requisição para: {url}")
    resposta = requests.get(url, headers=headers, timeout=10)
    # Executa a requisição GET com tempo limite de 10 segundos

    # Validação do status_code 200
    if resposta.status_code != 200:
        # Se o servidor responder qualquer código diferente de 200 OK
        print(f"Erro na requisição: status code {resposta.status_code}")
        return []
        # Encerra retornando lista vazia

    soup = BeautifulSoup(resposta.text, "html.parser")
    # Converte a resposta HTML em texto para uma árvore navegável de tags
    elementos = soup.find_all("span", class_="titleline")
    # Busca todas as tags <span> com a classe CSS 'titleline' onde ficam as notícias

    noticias = []
    # Lista para armazenar as notícias extraídas
    for item in elementos:
        # Percorre cada elemento de notícia encontrado
        tag_link = item.find("a")
        # Localiza o elemento de âncora <a> interno
        if tag_link:
            # Se a tag existir
            titulo = tag_link.text.strip()
            # Extrai o texto do título da matéria
            link = tag_link.get("href", "").strip()
            # Extrai a URL para onde a notícia aponta
            noticias.append({"titulo": titulo, "link": link})
            # Adiciona o dicionário com título e link na lista

    print(f"Total de notícias coletadas: {len(noticias)}")
    print("\n--- Primeiras 5 Notícias ---")
    for noticia in noticias[:5]:
        # Exibe apenas os primeiros 5 registros formatados no console
        print(f"Título: {noticia['titulo']}\nLink: {noticia['link']}\n")

    # Salvamento em arquivo CSV
    diretorio_base = Path(__file__).resolve().parent
    # Diretório onde o script está salvo
    caminho_csv = diretorio_base / "noticias.csv"
    # Caminho final do arquivo CSV

    with open(caminho_csv, mode="w", newline="", encoding="utf-8") as f:
        # Abre o arquivo em modo escrita com codificação UTF-8
        writer = csv.DictWriter(f, fieldnames=["titulo", "link"])
        # Instancia gravador mapeando as chaves dos dicionários como colunas
        writer.writeheader()
        # Escreve a linha de cabeçalho (titulo, link)
        writer.writerows(noticias)
        # Escreve todos os registros de uma só vez

    print(f"Arquivo CSV salvo em: {caminho_csv}")
    return noticias
    # Retorna as notícias em memória


if __name__ == "__main__":
    # Ponto de entrada do script
    coletar_noticias()

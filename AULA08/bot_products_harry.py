"""
Lab 08: Web Scraping e Interação com Elementos via Selenium.

Extração de produtos da loja Harry Potter (título e preço).
"""

from selenium import webdriver
# Módulo do Selenium para instanciar e controlar o navegador web
from selenium.webdriver.common.by import By
# Estratégia de localização de elementos HTML (ID, CSS_SELECTOR, XPATH, etc.)
from selenium.webdriver.support import expected_conditions as EC
# Condições esperadas para sincronização (elemento visível, presente, clicável)
from selenium.webdriver.support.ui import WebDriverWait
# Mecanismo de espera explícita para páginas com conteúdo dinâmico


def coletar_produtos():
    """Acessa a loja oficial do Harry Potter e extrai produtos."""
    url = "https://harrypottershop.com/collections/gifts/Under-$10"
    # URL da seção de presentes até 10 dólares da loja oficial

    options = webdriver.ChromeOptions()
    # Cria objeto de configuração do navegador Chrome
    options.add_argument("--headless=new")
    # Executa o navegador em segundo plano (sem abrir janela gráfica na tela)
    options.add_argument("--no-sandbox")
    # Argumento necessário para rodar de forma segura em ambientes Linux/Docker
    options.add_argument("--disable-dev-shm-usage")
    # Evita problemas de memória compartilhada em sistemas Linux

    driver = webdriver.Chrome(options=options)
    # Inicializa a instância do navegador Chrome controlado pelo Selenium
    produtos = []
    # Lista para armazenar os produtos extraídos

    try:
        # Inicia bloco protegido garantindo o fechamento posterior do browser
        driver.get(url)
        # Navega até o endereço web indicado

        wait = WebDriverWait(driver, 10)
        # Define tempo limite de até 10 segundos para esperas explícitas
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".card, .product"))
        )
        # Bloqueia a execução até que os cards de produto sejam renderizados no DOM

        cards = driver.find_elements(By.CSS_SELECTOR, ".card, .product-card")
        # Localiza todos os containers que representam produtos na listagem

        for card in cards:
            # Itera sobre cada card individual de produto
            try:
                # Tenta localizar o título do produto dentro do card
                elem_titulo = card.find_element(
                    By.CSS_SELECTOR, ".card__heading, .title, h3"
                )
                titulo = elem_titulo.text.strip()
                # Extrai o texto limpo do título
            except Exception:
                # Se não encontrar o elemento de título
                titulo = "Sem título"
                # Define valor padrão

            try:
                # Tenta localizar o elemento de preço dentro do card
                elem_preco = card.find_element(
                    By.CSS_SELECTOR, ".price-item, .price"
                )
                preco = elem_preco.text.strip()
                # Extrai o texto do preço
            except Exception:
                # Se não encontrar o elemento de preço
                preco = "Sem preço"
                # Define valor padrão

            if titulo != "Sem título":
                # Filtra apenas cards válidos que possuem título
                produtos.append({"titulo": titulo, "preco": preco})
                # Adiciona o dicionário com os dados coletados

        print(f"Total de produtos coletados: {len(produtos)}")
        # Exibe a contagem de produtos raspados da página
        for item in produtos:
            # Percorre a lista exibindo cada item
            print(f"Título: {item['titulo']} | Preço: {item['preco']}")
            # Imprime o título e o preço

    finally:
        # Bloco que roda obrigatoriamente ao final
        driver.quit()
        # Fecha todas as janelas do navegador e encerra o processo do chromedriver

    return produtos
    # Retorna a lista completa com os produtos


if __name__ == "__main__":
    # Ponto de entrada do script
    coletar_produtos()
    # Executa a rotina de raspagem web

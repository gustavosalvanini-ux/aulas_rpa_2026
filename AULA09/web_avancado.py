"""
Lab 09: Manipulação de Dropdowns, Pop-ups e Web Elements Complexos.

Automação web com Selenium tratando Selects, Alerts, Iframes e Janelas.
"""

import logging
# Biblioteca para emissão de logs com timestamps e níveis de criticidade
from selenium import webdriver
# Instanciador do navegador web
from selenium.webdriver.common.by import By
# Mapeador de estratégias de localização de seletores
from selenium.webdriver.support import expected_conditions as EC
# Condições prontas para esperas explícitas
from selenium.webdriver.support.ui import Select, WebDriverWait
# Select: abstrai elementos <select>; WebDriverWait: espera baseada em eventos

logging.basicConfig(
    # Configura o padrão de logs do módulo
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)
# Instancia o logger para este script


def parte_1_selects(driver):
    """Interação com elemento <select> via classe Select."""
    url = "https://the-internet.herokuapp.com/dropdown"
    # URL da página de teste com caixa suspensa
    logger.info("Acessando %s", url)
    driver.get(url)
    # Abre a página no navegador

    wait = WebDriverWait(driver, 10)
    # Cria espera explícita com timeout de 10 segundos
    elemento_select = wait.until(
        EC.presence_of_element_located((By.ID, "dropdown"))
    )
    # Aguarda o elemento <select id='dropdown'> existir no DOM
    select = Select(elemento_select)
    # Encapsula o elemento HTML na classe Select do Selenium

    opcoes = [opcao.text for opcao in select.options]
    # Monta lista com os textos de todas as opções contidas no dropdown
    logger.info("Opções encontradas: %s", opcoes)

    select.select_by_index(2)
    # Seleciona a terceira opção da lista (índice 2, correspondente a 'Option 2')
    opcao_selecionada = select.first_selected_option.text
    # Lê qual opção está atualmente marcada como selecionada
    logger.info("Opção selecionada: %s", opcao_selecionada)
    assert opcao_selecionada == "Option 2", "Opção 2 não foi selecionada!"
    # Valida com assert se a opção correta foi ativada


def parte_2_alerts(driver):
    """Manipulação de JavaScript Alerts (alert, confirm, prompt)."""
    url = "https://the-internet.herokuapp.com/javascript_alerts"
    # URL da página de testes com caixas nativas do navegador
    logger.info("Acessando %s", url)
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # 1. JS Alert simples
    btn_alert = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Click for JS Alert')]")
        )
    )
    # Localiza o botão por XPath relativo
    btn_alert.click()
    # Clica para disparar a caixa de alerta nativa
    alert = wait.until(EC.alert_is_present())
    # Espera a caixa de diálogo nativa surgir no navegador
    logger.info("Texto do JS Alert: %s", alert.text)
    alert.accept()
    # Confirma/fecha o alerta clicando em 'OK'

    # 2. JS Confirm (confirmação com Cancelar)
    btn_confirm = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Click for JS Confirm')]")
        )
    )
    btn_confirm.click()
    # Dispara a caixa de confirmação
    confirm = wait.until(EC.alert_is_present())
    # Aguarda a caixa surgir
    logger.info("Cancelando JS Confirm...")
    confirm.dismiss()
    # Clica no botão 'Cancelar' (dismiss)
    resultado = driver.find_element(By.ID, "result").text
    # Lê o texto de feedback impresso na página
    assert "You clicked: Cancel" in resultado, "Cancel não registrado!"
    # Valida se a rejeição foi computada

    # 3. JS Prompt (caixa de entrada de texto)
    btn_prompt = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Click for JS Prompt')]")
        )
    )
    btn_prompt.click()
    # Dispara o prompt interativo
    prompt = wait.until(EC.alert_is_present())
    # Aguarda o prompt estar disponível
    ra = "6326138"
    # Define o RA do aluno
    prompt.send_keys(ra)
    # Digita o RA dentro da caixa nativa do alerta
    prompt.accept()
    # Confirma o envio do texto
    resultado_prompt = driver.find_element(By.ID, "result").text
    # Lê a resposta na página
    assert ra in resultado_prompt, "RA não encontrado no resultado do prompt!"
    # Valida se o texto digitado foi aceito e exibido


def parte_3_iframe(driver):
    """Navegação e escrita em iframe rico."""
    url = "https://the-internet.herokuapp.com/iframe"
    # URL da página com editor dentro de iframe isolado
    logger.info("Acessando %s", url)
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # Localiza o iframe por CSS Selector
    iframe = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.tox-edit-area__iframe, iframe#mce_0_ifr"))
    )
    driver.switch_to.frame(iframe)
    # Muda o foco de execução do Selenium para DENTRO do documento do iframe

    corpo = wait.until(EC.presence_of_element_located((By.ID, "tinymce")))
    # Localiza a área editável interna
    corpo.clear()
    # Apaga o texto de demonstração existente
    corpo.send_keys("Robo RPA ativo - RA 6326138")
    # Digita o novo texto dentro do editor

    driver.switch_to.default_content()
    # Retorna o contexto do Selenium de volta para a página HTML principal
    h3_texto = driver.find_element(By.TAG_NAME, "h3").text
    # Lê o cabeçalho <h3> presente apenas na página raiz
    assert "An iFrame containing the TinyMCE WYSIWYG Editor" in h3_texto, (
        "Não retornou ao documento principal!"
    )
    # Confirma que saímos do iframe com sucesso


def parte_4_janelas(driver):
    """Controle de múltiplas abas/janelas."""
    url = "https://the-internet.herokuapp.com/windows"
    # URL com link que abre uma nova guia no navegador
    logger.info("Acessando %s", url)
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    aba_original = driver.current_window_handle
    # Salva o identificador único (handle) da aba inicial
    link = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))
    )
    link.click()
    # Clica no link configurado com target='_blank'

    wait.until(EC.number_of_windows_to_be(2))
    # Espera até que existam exatamente duas abas abertas no navegador
    todas_abas = driver.window_handles
    # Obtém a lista com os dois handles
    nova_aba = [h for h in todas_abas if h != aba_original][0]
    # Identifica o handle da nova aba (diferente da original)

    driver.switch_to.window(nova_aba)
    # Transfere o foco do Selenium para a nova aba aberta
    assert driver.find_element(By.TAG_NAME, "h3").text == "New Window"
    # Valida o texto exibido na nova página

    driver.close()
    # Fecha apenas a aba secundária atual
    driver.switch_to.window(aba_original)
    # Retorna o controle para a aba inicial

    assert len(driver.window_handles) == 1
    # Confirma que restou apenas uma aba ativa
    assert "The Internet" in driver.title
    # Valida que estamos de volta na página inicial


def main():
    """Função principal executando os 4 módulos."""
    options = webdriver.ChromeOptions()
    # Cria opções do Chrome
    options.add_argument("--headless=new")
    # Execução em modo invisível (headless)
    options.add_argument("--no-sandbox")
    # Execução em sandbox Linux
    options.add_argument("--disable-dev-shm-usage")
    # Prevenção contra estouro de memória compartilhada

    driver = webdriver.Chrome(options=options)
    # Instancia o navegador
    try:
        # Executa as 4 etapas sequencialmente
        parte_1_selects(driver)
        # Etapa 1: Dropdown
        parte_2_alerts(driver)
        # Etapa 2: Caixas de alerta
        parte_3_iframe(driver)
        # Etapa 3: Iframe
        parte_4_janelas(driver)
        # Etapa 4: Abas
        logger.info("Todas as partes foram executadas com sucesso!")
    finally:
        # Garante o encerramento do navegador
        driver.quit()
        # Fecha todas as instâncias e conexões do driver


if __name__ == "__main__":
    # Ponto de entrada do script
    main()

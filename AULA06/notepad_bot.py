"""
Lab 06 - Controle de Periféricos e Segurança Fail-Safe.

Robô que abre o editor de texto via atalho de teclado,
digita um relatório e salva o arquivo automaticamente.
"""

import platform
# Biblioteca para identificar o sistema operacional hospedeiro (Windows, Linux, macOS)
import time
# Biblioteca para gerenciar pausas e contagem de tempo

import pyautogui
# Biblioteca principal para controle programático de mouse e teclado

# ─── Configurações de Segurança ──────────────────────────────────────────────
pyautogui.FAILSAFE = True
# Trava de emergência: mover o mouse para o canto superior esquerdo (0,0) aborta o bot na hora

pyautogui.PAUSE = 0.5
# Define uma pausa obrigatória de 500ms após cada comando do pyautogui para evitar atropelamentos

# ─── Detecta o sistema operacional ───────────────────────────────────────────
SO = platform.system()
# Retorna 'Windows', 'Linux' ou 'Darwin' (macOS)

print(f"[INFO] Sistema detectado: {SO}")
# Mostra ao operador qual sistema foi identificado

print("[INFO] Iniciando robô em 3 segundos... (mova o mouse para o canto superior esquerdo para cancelar)")
# Aviso de contagem regressiva dando tempo para o usuário trocar de janela se quiser

time.sleep(3)
# Pausa de 3 segundos antes do início das ações

# ─── Passo 1: Abrir o editor de texto via tecla Super/Win ────────────────────
if SO == "Windows":
    # Fluxo específico para ambiente Windows
    print("[PASSO 1] Abrindo menu Iniciar...")
    # Log informativo do passo
    pyautogui.press("win")
    # Pressiona a tecla Windows para abrir o menu Iniciar
    time.sleep(1)
    # Aguarda o menu abrir visualmente

    print("[PASSO 2] Digitando 'notepad'...")
    # Log do segundo passo
    pyautogui.typewrite("notepad", interval=0.1)
    # Digita 'notepad' com intervalo de 100ms entre teclas para simular digitação humana
    pyautogui.press("enter")
    # Confirma para iniciar o Bloco de Notas

else:
    # Fluxo para ambiente Linux
    print("[PASSO 1] Pressionando tecla Super para abrir o launcher...")
    # Log informativo do passo
    pyautogui.press("super")
    # Pressiona a tecla Super (Windows key) para abrir o lançador de aplicativos
    time.sleep(1)
    # Aguarda 1 segundo para a barra de pesquisa do Linux focar

    print("[PASSO 2] Digitando 'gedit'...")
    # Log do segundo passo
    pyautogui.typewrite("gedit", interval=0.1)
    # Digita o nome do editor de texto padrão do GNOME
    pyautogui.press("enter")
    # Pressiona Enter para abrir o editor

# ─── Passo 3: Aguardar o aplicativo carregar ─────────────────────────────────
print("[PASSO 3] Aguardando o editor carregar (2s)...")
# Informa início da espera da janela carregar
time.sleep(2)
# Pausa de 2 segundos garantindo que a janela do editor já tem o foco

# ─── Passo 4: Digitar o texto do relatório ───────────────────────────────────
texto = "Relatorio de Execucao Automatica - RPA PyAutoGUI Ativo!"
# Mensagem que será digitada no corpo do documento aberto
print(f"[PASSO 4] Digitando: {texto!r}")
# Exibe no console o texto que está sendo enviado
pyautogui.typewrite(texto, interval=0.05)
# Digita caractere por caractere de forma visível

# ─── Passo 5: Salvar o arquivo com Ctrl+S ────────────────────────────────────
print("[PASSO 5] Salvando o arquivo (Ctrl+S)...")
# Informa que acionará o atalho de salvamento
pyautogui.hotkey("ctrl", "s")
# Pressiona simultaneamente Ctrl + S para abrir o diálogo de salvar arquivo
time.sleep(1)
# Aguarda 1 segundo para a janela de salvar carregar na tela

# ─── Passo 6: Digitar o nome do arquivo e confirmar ──────────────────────────
nome_arquivo = "status_bot.txt"
# Nome do arquivo a ser salvo
print(f"[PASSO 6] Digitando o nome do arquivo: {nome_arquivo!r}")
# Exibe o nome do arquivo
pyautogui.typewrite(nome_arquivo, interval=0.1)
# Digita o nome no campo de texto
pyautogui.press("enter")
# Pressiona Enter para confirmar a gravação do arquivo no disco

print("[OK] Robô concluído com sucesso!")
# Mensagem final confirmando que o fluxo de UI automatizado terminou

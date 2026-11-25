"""
Lab 12: Integração de Sistemas via APIs REST e Notificações por E-mail.

Consome a API da AwesomeAPI para buscar a cotação do Dólar (USD-BRL)
e envia alertas via protocolo SMTP e pela Gmail API com OAuth 2.0.
"""

import base64
# Módulo para codificação binária em base64 exigida pela Gmail API
from email.mime.text import MIMEText
# Construtor de mensagens de e-mail formatadas com cabeçalhos MIME
import os
# Acesso a variáveis de ambiente do sistema operacional
from pathlib import Path
# Manipulação de caminhos e arquivos locais
import smtplib
# Protocolo cliente SMTP para envio nativo de e-mails via socket de rede

from google.auth.transport.requests import Request
# Mecanismo de renovação automática de credenciais do Google
from google.oauth2.credentials import Credentials
# Representação do token de acesso OAuth 2.0 do usuário
from google_auth_oauthlib.flow import InstalledAppFlow
# Fluxo de autorização do Google para aplicativos desktop
from googleapiclient.discovery import build
# Construtor dinâmico do cliente de serviços da Google Cloud API
import requests
# Cliente HTTP para consumo de APIs REST

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
# Escopo de permissão OAuth mínimo necessário apenas para enviar e-mails


def buscar_cotacao_dolar():
    """Consulta a API pública da AwesomeAPI e retorna o valor de compra."""
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    # Endpoint público da AwesomeAPI com cotação em tempo real
    resposta = requests.get(url, timeout=10)
    # Executa a requisição GET na API
    resposta.raise_for_status()
    # Lança exceção caso a API responda com erro HTTP (4xx ou 5xx)
    dados = resposta.json()
    # Converte o payload JSON recebido em dicionário Python
    bid = dados["USDBRL"]["bid"]
    # Extrai o valor de compra ('bid') da moeda Dólar para Real
    return bid


def enviar_email_smtp(cotacao):
    """Monta e envia e-mail via SMTP utilizando smtplib e email.mime."""
    remetente = os.getenv("EMAIL_REMETENTE")
    # Lê o e-mail de envio das variáveis de ambiente
    senha_app = os.getenv("EMAIL_SENHA_APP")
    # Lê a senha de aplicativo de 16 caracteres gerada no Google
    destinatario = os.getenv("EMAIL_DESTINATARIO")
    # Lê o e-mail do destinatário da notificação

    assunto = "Alerta de Cotação - Dólar Atualizado"
    # Assunto do e-mail
    corpo = (
        f"Olá,\n\nA cotação atual do Dólar (USD-BRL) é R$ {cotacao}.\n\n"
        "Notificação automática via RPA Bot."
    )
    # Texto do corpo da mensagem

    msg = MIMEText(corpo, "plain", "utf-8")
    # Constrói o objeto de mensagem MIME em texto puro e UTF-8
    msg["Subject"] = assunto
    # Define o cabeçalho de assunto
    msg["From"] = remetente or "bot@exemplo.com"
    # Define o cabeçalho de remetente
    msg["To"] = destinatario or "usuario@exemplo.com"
    # Define o cabeçalho de destinatário

    if not (remetente and senha_app and destinatario):
        # Se as variáveis de ambiente não foram configuradas
        print("[SMTP - MOCK] Variáveis de ambiente não configuradas.")
        print(f"[SMTP - MOCK] Para: {msg['To']} | Assunto: {msg['Subject']}")
        print(f"[SMTP - MOCK] Corpo:\n{corpo}")
        return True
        # Executa como mock sem quebrar o teste ou o CI

    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
        # Conecta no servidor SMTP do Gmail na porta 587
        servidor.starttls()
        # Eleva a conexão para criptografia TLS segura
        servidor.login(remetente, senha_app)
        # Autentica com o usuário e a senha de aplicativo
        servidor.send_message(msg)
        # Dispara o e-mail

    print("[SMTP] E-mail enviado com sucesso!")
    return True


def enviar_email_gmail_api(cotacao):
    """Envia o e-mail pela Gmail API do Google com autenticação OAuth 2.0."""
    diretorio_base = Path(__file__).resolve().parent
    # Diretório local do script
    caminho_credenciais = diretorio_base / "credentials.json"
    # Arquivo de configuração OAuth baixado do Google Cloud
    caminho_token = diretorio_base / "token.json"
    # Arquivo onde o token de autorização do usuário é salvo

    assunto = "Alerta de Cotação - Gmail API"
    corpo = f"Cotação do Dólar capturada via API: R$ {cotacao}"

    msg = MIMEText(corpo, "plain", "utf-8")
    msg["Subject"] = assunto
    msg["To"] = os.getenv("EMAIL_DESTINATARIO", "usuario@exemplo.com")

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    # Converte os bytes MIME em string base64 segura para URLs exigida pela API

    if not caminho_credenciais.exists() and not caminho_token.exists():
        # Se as credenciais OAuth não estiverem presentes
        print("[Gmail API - MOCK] credentials.json não encontrado.")
        print(f"[Gmail API - MOCK] Para: {msg['To']} | Cotação: R$ {cotacao}")
        return True
        # Executa como mock didático

    creds = None
    if caminho_token.exists():
        # Se o token já existe no disco
        creds = Credentials.from_authorized_user_file(
            str(caminho_token), SCOPES
        )
        # Carrega as credenciais salvas

    if not creds or not creds.valid:
        # Se as credenciais forem inválidas ou inexistentes
        if creds and creds.expired and creds.refresh_token:
            # Se apenas expirou e tem refresh token
            creds.refresh(Request())
            # Renova o token automaticamente
        else:
            # Abre o fluxo de consentimento no navegador do usuário
            fluxo = InstalledAppFlow.from_client_secrets_file(
                str(caminho_credenciais), SCOPES
            )
            creds = fluxo.run_local_server(port=0)

        with open(caminho_token, "w", encoding="utf-8") as token_file:
            # Salva o novo token gerado para reutilização futura
            token_file.write(creds.to_json())

    servico = build("gmail", "v1", credentials=creds)
    # Constrói o cliente da Gmail API v1 autenticado
    mensagem = servico.users().messages().send(
        userId="me", body={"raw": raw}
    ).execute()
    # Envia a mensagem codificada em base64 pelo endpoint users.messages.send

    print(f"[Gmail API] Mensagem enviada! ID: {mensagem.get('id')}")
    return True


def main():
    """Função orquestradora."""
    print("Buscando cotação do Dólar na AwesomeAPI...")
    cotacao = buscar_cotacao_dolar()
    print(f"Cotação encontrada: R$ {cotacao}")

    print("\n1. Testando envio via SMTP:")
    try:
        # Testa envio via SMTP
        enviar_email_smtp(cotacao)
    except Exception as erro_smtp:
        print(f"[ERRO SMTP] Falha ao enviar via SMTP: {erro_smtp}")

    print("\n2. Testando envio via Gmail API:")
    try:
        # Testa envio via Gmail API
        enviar_email_gmail_api(cotacao)
    except Exception as erro_gmail:
        print(f"[ERRO Gmail API] Falha ao enviar via Gmail API: {erro_gmail}")


if __name__ == "__main__":
    main()

transacoes = [150.0, 3200.5, 12500.0, 450.0, -50.0, 800.0, 0]
# Lista contendo os valores monetários de transações a serem auditadas pelo bot

for transacao in transacoes:
    # Laço de repetição que itera por cada valor de transação individualmente

    if transacao > 10000.00:
        # Regra de negócio: transações acima de R$ 10.000 são consideradas suspeitas
        print(f"[ALERTA] Transação suspeita de R$ {transacao}: Encaminhada para auditoria.")
        # Emite alerta no console e não interrompe o bot
        continue
        # Pula para a próxima transação sem processar as regras seguintes

    elif transacao <= 0:
        # Regra de segurança: valores negativos ou zero indicam inconsistência grave
        print(f"[ERRO CRÍTICO] Transação inválida encontrada (R$ {transacao}). Interrompendo bot...")
        # Emite notificação de parada imediata
        break
        # Interrompe bruscamente o laço for (fail-fast) para evitar fraudes

    else:
        # Fluxo normal: transação dentro dos parâmetros permitidos
        print(f"[SUCESSO] Transação de R$ {transacao} processada.")
        # Registra a confirmação de sucesso da transação

"""
Lab 07 - Lançamento de Notas com RPA.

Lê o CSV de notas, calcula a média e simula o lançamento.
RA: 6326138
"""

import csv
# Módulo padrão para leitura e escrita de arquivos no formato CSV delimitado
import time
# Módulo para controle de tempo e execução

import pyautogui
# Automação de teclado e mouse

# Configurações de segurança do pyautogui
pyautogui.FAILSAFE = True
# Habilita parada de emergência caso o mouse seja arrastado para o canto (0,0)

pyautogui.PAUSE = 0.5
# Aplica pausa de segurança de 0.5s entre ações

CSV_PATH = "AULA07/notas_alunos.csv"
# Caminho relativo para a base de dados de alunos e notas

NOTA_COLS = ["Nota01", "Nota02"]
# Lista com os nomes das colunas de notas que compõem o cálculo da média


def parse_nota(valor):
    """Converte string de nota para float, retorna 0 se inválido."""
    if valor is None:
        # Se o campo estiver vazio ou nulo
        return 0.0
        # Retorna nota zero
    v = valor.strip().replace(",", ".")
    # Remove espaços em branco nas pontas e substitui vírgula decimal brasileira por ponto
    try:
        # Tenta a conversão numérica
        resultado = float(v)
        # Converte para float
        return resultado
        # Retorna o valor numérico
    except ValueError:
        # Se for um texto não numérico (ex: 'FALTOU', 'N/A')
        return 0.0
        # Trata a inconsistência retornando 0.0


def ler_alunos(caminho_csv):
    """Lê o CSV e retorna lista de dicts com matricula e nota."""
    lista = []
    # Inicializa a lista que guardará os registros dos alunos
    with open(caminho_csv, encoding="utf-8", newline="") as f:
        # Abre o arquivo CSV com suporte a caracteres acentuados
        reader = csv.DictReader(f, delimiter=";")
        # Cria leitor que mapeia cada linha para um dicionário baseado no cabeçalho
        for row in reader:
            # Percorre cada aluno do arquivo
            ra = row.get("RA", "").strip()
            # Obtém e higieniza a matrícula do aluno
            notas = [parse_nota(row.get(col, "")) for col in NOTA_COLS]
            # Extrai e converte as notas de cada coluna da lista NOTA_COLS
            nota_final = sum(notas) / len(notas) if notas else 0.0
            # Calcula a média aritmética das notas válidas
            lista.append({
                # Adiciona o dicionário padronizado do aluno
                "matricula": ra,
                # Chave 'matricula' com o RA
                "nota": round(nota_final, 2),
                # Chave 'nota' com a média arredondada em duas casas decimais
            })
    return lista
    # Retorna a lista completa com todos os alunos


alunos = ler_alunos(CSV_PATH)
# Executa a leitura da base de dados e guarda o resultado na variável global 'alunos'


def lancar_notas(lista_alunos):
    """Simula o lançamento de notas (apenas log, sem ação real)."""
    print("=" * 50)
    # Linha separadora de cabeçalho
    print("SIMULAÇÃO DE LANÇAMENTO DE NOTAS")
    # Título do processo
    print("=" * 50)
    # Linha separadora
    for aluno in lista_alunos:
        # Itera sobre cada aluno da lista
        matricula = aluno["matricula"]
        # Extrai o RA
        nota = aluno["nota"]
        # Extrai a nota calculada
        status = "APROVADO" if nota >= 5 else "REPROVADO"
        # Regra de negócio: nota igual ou superior a 5 aprova o aluno
        print(
            f"Matrícula: {matricula:<12} "
            f"Nota: {nota:>5.2f}  "
            f"Status: {status}"
        )
        # Exibe linha formatada com alinhamentos de colunas
        time.sleep(0)
        # Ponto de extensão para simulação de delay de digitação
    print("=" * 50)
    # Linha separadora de rodapé
    print(f"Total de alunos processados: {len(lista_alunos)}")
    # Exibe a quantidade total de registros tratados
    print("Lançamento simulado com sucesso.")
    # Mensagem de conclusão da rotina


if __name__ == "__main__":
    # Garante que só executa se o arquivo for chamado diretamente no terminal
    lancar_notas(alunos)
    # Dispara a simulação de lançamento

import os, sys
from datetime import datetime
import random
import string

def criar_alfanumerico():
    """
    Cria um alfanumérico de 10 valores.
    """
    # conjunto de caracteres alfanuméricos
    caracteres = string.ascii_letters + string.digits  # A-Z, a-z, 0-9

    # gera uma string de 10 caracteres aleatórios
    s = ''.join(random.choices(caracteres, k=10))

    return s

def log_spev(mensagem: str, nome_arquivo="spev.log"):
    """
    Adiciona uma mensagem em um arquivo de log dentro da pasta do SPEV.
    Cria o arquivo caso ele não exista.

    :param mensagem: texto a ser adicionado no log
    :param nome_arquivo: nome do arquivo de log (opcional)
    """
    try:
        # Pega o diretório do executável atual
        # pasta_spev = os.path.dirname(os.path.abspath(__file__))
        # Caso esteja rodando como exe (pyinstaller), use:
        pasta_spev = os.path.dirname(sys.executable)

        caminho_log = os.path.join(pasta_spev, nome_arquivo)

        # Adiciona timestamp na mensagem
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        texto_log = f"[{timestamp}] {mensagem}\n"

        # Abre o arquivo no modo append, criando se não existir
        with open(caminho_log, "a", encoding="utf-8") as f:
            f.write(texto_log)

    except Exception as e:
        # Se falhar, apenas imprime no console (não interrompe o programa)
        print(f"[ERRO] Não foi possível gravar no log: {e}")

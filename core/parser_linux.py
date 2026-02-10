# core/parser_linux.py

import os

LOG_PATHS = [
    "/var/log/auth.log",   # Ubuntu / Debian
    "/var/log/secure"      # CentOS / RHEL
]

def localizar_log():
    """
    Verifica quais logs existem e devolve o primeiro encontrado.
    Se nenhum existir, devolve (None, lista_de_logs_em_falta)
    """
    existentes = []
    em_falta = []

    for caminho in LOG_PATHS:
        if os.path.exists(caminho):
            existentes.append(caminho)
        else:
            em_falta.append(caminho)

    if existentes:
        # Devolve o primeiro log válido encontrado
        return existentes[0], em_falta
    else:
        # Nenhum log encontrado
        return None, em_falta


def ler_log(caminho):
    """
    Lê o ficheiro de log linha a linha e devolve uma lista de strings.
    """
    try:
        with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
            return f.readlines()
    except PermissionError:
        return "PERMISSAO_NEGADA"
    except Exception as e:
        return f"ERRO: {str(e)}"


def obter_linhas():
    """
    Função principal do parser Linux.
    Tenta localizar o log e lê-lo.
    Devolve:
      - lista de linhas (sucesso)
      - None (falha)
      - string especial "PERMISSAO_NEGADA" se faltar sudo
    """
    caminho, faltam = localizar_log()

    if caminho is None:
        # Nenhum log encontrado → devolve None e a lista de logs em falta
        return None, faltam

    linhas = ler_log(caminho)

    if linhas == "PERMISSAO_NEGADA":
        return "PERMISSAO_NEGADA", caminho

    if isinstance(linhas, str) and linhas.startswith("ERRO:"):
        return None, [f"Erro ao ler {caminho}: {linhas}"]

    return linhas, caminho

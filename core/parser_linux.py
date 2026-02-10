# core/parser_linux.py

import os, re
from datetime import datetime

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

# -----------------------------
# Converter timestamp para ISO
# -----------------------------
def converter_timestamp_iso(timestamp_str):
    """
    Converte timestamps do auth.log (ex: 'Feb 10 14:22:01')
    para formato ISO (ex: '2026-02-10 14:22:01')
    """
    ano_atual = datetime.now().year
    try:
        dt = datetime.strptime(f"{ano_atual} {timestamp_str}", "%Y %b %d %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp_str  # fallback


# -----------------------------
# Extrair eventos relevantes
# -----------------------------
def extrair_eventos(linhas):
    eventos = []

    # Padrões importantes
    padrao_falha = re.compile(r"Failed password for (\w+|invalid user) (\w+)? from ([\d\.]+)")
    padrao_invalid = re.compile(r"Invalid user (\w+) from ([\d\.]+)")
    padrao_sucesso = re.compile(r"Accepted password for (\w+) from ([\d\.]+)")
    padrao_sudo = re.compile(r"sudo: .*incorrect password")

    for linha in linhas:
        # Extrair timestamp (primeiros 15 chars)
        timestamp_raw = linha[:15]
        timestamp_iso = converter_timestamp_iso(timestamp_raw)

        # Falha de login
        if "Failed password" in linha:
            m = re.search(r"Failed password for (invalid user )?(\w+) from ([\d\.]+)", linha)
            if m:
                eventos.append({
                    "tipo": "falha_login",
                    "timestamp": timestamp_iso,
                    "utilizador": m.group(2),
                    "ip": m.group(3),
                    "mensagem": linha.strip()
                })
                continue

        # Utilizador inválido
        if "Invalid user" in linha:
            m = padrao_invalid.search(linha)
            if m:
                eventos.append({
                    "tipo": "utilizador_invalido",
                    "timestamp": timestamp_iso,
                    "utilizador": m.group(1),
                    "ip": m.group(2),
                    "mensagem": linha.strip()
                })
                continue

        # Login bem-sucedido
        if "Accepted password" in linha:
            m = padrao_sucesso.search(linha)
            if m:
                eventos.append({
                    "tipo": "login_sucesso",
                    "timestamp": timestamp_iso,
                    "utilizador": m.group(1),
                    "ip": m.group(2),
                    "mensagem": linha.strip()
                })
                continue

        # Sudo falhado
        if "sudo" in linha and "incorrect password" in linha:
            eventos.append({
                "tipo": "sudo_falhado",
                "timestamp": timestamp_iso,
                "utilizador": None,
                "ip": None,
                "mensagem": linha.strip()
            })
            continue

    return eventos


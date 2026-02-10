# core/analyzer.py

def detetar_bruteforce(eventos):
    falhas_por_ip = {}

    for ev in eventos:
        if ev["tipo"] == "falha_login":
            ip = ev["ip"]
            falhas_por_ip[ip] = falhas_por_ip.get(ip, 0) + 1

    alertas = []
    for ip, qtd in falhas_por_ip.items():
        if qtd >= 5:
            alertas.append(f"Bruteforce: {ip} ({qtd} falhas)")

    return alertas


def detetar_utilizadores_invalidos(eventos):
    invalidos = {}

    for ev in eventos:
        if ev["tipo"] == "utilizador_invalido":
            user = ev["utilizador"]
            invalidos[user] = invalidos.get(user, 0) + 1

    alertas = []
    for user, qtd in invalidos.items():
        if qtd >= 3:
            alertas.append(f"User inválido: {user} ({qtd} tentativas)")

    return alertas


def detetar_sudo_falhado(eventos):
    qtd = sum(1 for ev in eventos if ev["tipo"] == "sudo_falhado")

    if qtd > 0:
        return [f"Sudo falhado: {qtd} tentativa(s)"]
    return []


def detetar_login_suspeito(eventos):
    falhas_por_ip = {}
    alertas = []

    for ev in eventos:
        if ev["tipo"] == "falha_login":
            ip = ev["ip"]
            falhas_por_ip[ip] = falhas_por_ip.get(ip, 0) + 1

        if ev["tipo"] == "login_sucesso":
            ip = ev["ip"]
            if ip in falhas_por_ip and falhas_por_ip[ip] >= 3:
                alertas.append(f"Login suspeito: {ip} (falhou {falhas_por_ip[ip]} vezes antes de entrar)")

    return alertas


def gerar_alertas(eventos):
    alertas = []
    alertas += detetar_bruteforce(eventos)
    alertas += detetar_utilizadores_invalidos(eventos)
    alertas += detetar_sudo_falhado(eventos)
    alertas += detetar_login_suspeito(eventos)
    return alertas

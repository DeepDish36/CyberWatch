#  core/utils.py

# Detetar o OS para usar as opções corretas de logs
import platform, os

def get_os():
    """
    Get the current operating system.

    Returns:
        str: The name of the operating system ('Windows', 'Linux', 'Darwin').
    """
    return platform.system()

def clean():
    """
    Limpa a consola de acordo com o sistema operativo.
    """
    os_name = get_os()
    if os_name == "Windows":
        os.system("cls")
    else:
        os.system("clear")
        
def pause():
    """
    Pausa a execução até o utilizador pressionar Enter.
    """
    input("\nPressione Enter para continuar...")
#  core/utils.py

# Detetar o OS para usar as opções corretas de logs
import platform

def get_os():
    """
    Get the current operating system.

    Returns:
        str: The name of the operating system ('Windows', 'Linux', 'Darwin').
    """
    return platform.system()
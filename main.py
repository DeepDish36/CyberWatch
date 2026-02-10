# main.py

from core.utils import get_os
from core import parser_linux

def mostrar_menu():
    print("=== CyberWatch CLI ===\n")
    print("[1] Análise Rápida")
    print("[2] Análise Completa")
    print("[3] Ver Alertas Guardados")
    print("[4] Configurações")
    print("[5] Sair\n")

def opcao_analise_rapida():
    sistema = get_os()

    if sistema != "Linux":
        print("\n[ERRO] A Análise Rápida ainda só está disponível para Linux.\n")
        return

    while True:
        resultado, info = parser_linux.obter_linhas()

        # Caso 1: Falta de permissões (sudo)
        if resultado == "PERMISSAO_NEGADA":
            print("\n[ERRO CRÍTICO] Permissões insuficientes para ler o log:")
            print(f" - {info}")
            print("\nExecute a CyberWatch com sudo.\n")
            return

        # Caso 2: Nenhum log encontrado
        if resultado is None:
            print("\n[ERRO CRÍTICO] Não foi possível localizar os seguintes logs:")
            for caminho in info:
                print(f" - {caminho}")
            print("\nEstes ficheiros são essenciais para a Análise Rápida.")
            
            escolha = input("Pretende tentar novamente? (s/n): ").strip().lower()
            if escolha == "s":
                continue
            else:
                print("\nA regressar ao menu...\n")
                return

        # Caso 3: Sucesso → logs carregados
        linhas = resultado
        caminho = info

        print("\n[OK] Log encontrado e carregado com sucesso:")
        print(f" - {caminho}")
        print(f"Total de linhas lidas: {len(linhas)}\n")

        print("A análise detalhada dos eventos será implementada no próximo passo.\n")
        return

def opcao_analise_completa():
    print("\n[Análise Completa] ainda não implementada.\n")

def opcao_ver_alertas():
    print("\n[Ver Alertas] ainda não implementado.\n")

def opcao_configuracoes():
    print("\n[Configurações] ainda não implementado.\n")

def main():
    sistema = get_os()
    print(f"Sistema detetado: {sistema}\n")

    while True:
        mostrar_menu()
        opcao = input("Escolhe uma opção: ").strip()

        if opcao == "1":
            opcao_analise_rapida()
        elif opcao == "2":
            opcao_analise_completa()
        elif opcao == "3":
            opcao_ver_alertas()
        elif opcao == "4":
            opcao_configuracoes()
        elif opcao == "5":
            print("\nA sair....\n")
            break
        else:
            print("\nOpção inválida.\n")

if __name__ == "__main__":
    main()

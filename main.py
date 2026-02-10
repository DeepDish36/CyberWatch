# main.py

from core.utils import get_os
from core import parser_linux, analyzer

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

        if resultado == "PERMISSAO_NEGADA":
            print("\n[ERRO CRÍTICO] Permissões insuficientes para ler o log:")
            print(f" - {info}")
            print("\nExecute a CyberWatch com sudo.\n")
            return

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

        linhas = resultado
        caminho = info

        print("\n[OK] Log encontrado e carregado com sucesso:")
        print(f" - {caminho}")
        print(f"Total de linhas lidas: {len(linhas)}\n")

        eventos = parser_linux.extrair_eventos(linhas)

        print("=== Resumo da Análise Rápida ===")
        if not eventos:
            print("Nenhum evento relevante encontrado.")
        else:
            contagem = {}
            for ev in eventos:
                tipo = ev["tipo"]
                contagem[tipo] = contagem.get(tipo, 0) + 1

            for tipo, qtd in contagem.items():
                print(f"- {tipo}: {qtd} evento(s)")

        # Gerar alertas
        alertas = analyzer.gerar_alertas(eventos)

        print("\n=== Alertas ===")
        if not alertas:
            print("Nenhum alerta gerado.")
        else:
            for alerta in alertas:
                print(alerta)

        print("\nAnálise Rápida concluída.\n")
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

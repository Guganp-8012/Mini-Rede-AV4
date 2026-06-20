# Interface textual do sistema, estilizada com caracteres de desenho de caixa (box-drawing).
# Responsável pelos menus, entrada de dados e chamadas às funções da RedeSocial.
# É o ponto de entrada do programa: python main.py

import sys
from rede import RedeSocial
from init_db import criar_banco

# Força a saída em UTF-8, garantindo que os caracteres especiais
# (═, ║, ╔, etc.) sejam exibidos corretamente em qualquer terminal,
# incluindo o cmd.exe do Windows, que por padrão usa outra codificação.
sys.stdout.reconfigure(encoding='utf-8')

LARGURA = 60


def linha_da_caixa(texto, borda):
    # Monta uma linha de conteúdo dentro da caixa, cortando o texto
    # se ele for maior que a largura disponível, para não desalinhar
    # a borda direita
    espaco_disponivel = LARGURA - 4

    if len(texto) > espaco_disponivel:
        texto = texto[:espaco_disponivel - 3] + "..."

    print(f"{borda} " + texto.ljust(espaco_disponivel) + f" {borda}")


def caixa_dupla(titulo_texto, linhas):
    # Desenha uma caixa com bordas duplas (═ ║ ╔ ╗ ╚ ╝ ╠ ╣)
    # Usada no menu principal, para dar destaque
    print("╔" + "═" * (LARGURA - 2) + "╗")
    print("║" + titulo_texto.center(LARGURA - 2) + "║")
    print("╠" + "═" * (LARGURA - 2) + "╣")

    for linha_texto in linhas:
        linha_da_caixa(linha_texto, "║")

    print("╚" + "═" * (LARGURA - 2) + "╝")


def caixa_simples(titulo_texto):
    # Desenha um cabeçalho com bordas simples (─ │ ┌ ┐ └ ┘)
    # Usado nas telas de listagem (perfis, amigos)
    print("┌" + "─" * (LARGURA - 2) + "┐")
    print("│" + titulo_texto.center(LARGURA - 2) + "│")
    print("├" + "─" * (LARGURA - 2) + "┤")


def fechar_caixa_simples():
    print("└" + "─" * (LARGURA - 2) + "┘")


def pausar():
    input("\nPressione Enter para continuar...")


def menu():
    opcoes = [
        "[1] Adicionar usuário",
        "[2] Remover usuário",
        "[3] Criar amizade",
        "[4] Remover amizade",
        "[5] Listar amizades",
        "[6] Listar perfis",
        "[7] Sair",
    ]
    caixa_dupla("REDE SOCIAL", opcoes)


def adicionar_usuario(rede):
    username = input("Username: ").strip()
    nome = input("Nome: ").strip()

    # Valida se a idade é um número inteiro
    try:
        idade = int(input("Idade: "))
    except ValueError:
        print("Idade inválida.")
        return

    # Campos obrigatórios não podem estar vazios
    if not username or not nome:
        print("Username e nome são obrigatórios.")
        return

    if rede.adicionar_usuario(username, nome, idade):
        print("Usuário cadastrado com sucesso!")
    else:
        # Falha ocorre quando o username já existe no banco
        print("Username já existe.")


def remover_usuario(rede):
    username = input("Username do usuário: ").strip()

    if rede.remover_usuario(username):
        print("Usuário removido.")
    else:
        print("Usuário não encontrado.")


def criar_amizade(rede):
    username1 = input("Username 1: ").strip()
    username2 = input("Username 2: ").strip()

    if rede.criar_amizade(username1, username2):
        print("Amizade criada.")
    else:
        # Pode falhar por: usuário inexistente, autoamizade ou amizade duplicada
        print("Não foi possível criar amizade.")


def remover_amizade(rede):
    username1 = input("Username 1: ").strip()
    username2 = input("Username 2: ").strip()

    if rede.remover_amizade(username1, username2):
        print("Amizade removida.")
    else:
        print("Amizade não encontrada.")


def listar_amigos(rede):
    username = input("Username: ").strip()

    amigos = rede.listar_amigos(username)

    caixa_simples("AMIGOS")

    if not amigos:
        linha_da_caixa("Nenhum amigo encontrado.", "│")
    else:
        # Exibe username e nome de cada amigo
        for amigo in amigos:
            texto = f"{amigo.username} | {amigo.nome}"
            linha_da_caixa(texto, "│")

    fechar_caixa_simples()


def listar_perfis(rede):
    usuarios = rede.listar_usuarios()

    caixa_simples("PERFIS")

    if not usuarios:
        linha_da_caixa("Nenhum usuário cadastrado.", "│")
    else:
        # Para cada usuário, busca a quantidade de amigos pelo ID
        for usuario in usuarios:
            quantidade = rede.contar_amigos(usuario.id)

            texto = (
                f"ID:{usuario.id} {usuario.username} "
                f"{usuario.nome} {usuario.idade}a "
                f"Amigos:{quantidade}"
            )
            linha_da_caixa(texto, "│")

    fechar_caixa_simples()


def main():
    # Garante que o banco e as tabelas existam antes de qualquer operação
    # Usa CREATE TABLE IF NOT EXISTS, então é seguro chamar sempre
    criar_banco()

    rede = RedeSocial()

    while True:
        menu()

        opcao = input("Escolha uma opção: ").strip()
        print()

        # match/case: estrutura moderna do Python 3.10+ para tratar múltiplas opções
        match opcao:

            case "1":
                adicionar_usuario(rede)

            case "2":
                remover_usuario(rede)

            case "3":
                criar_amizade(rede)

            case "4":
                remover_amizade(rede)

            case "5":
                listar_amigos(rede)

            case "6":
                listar_perfis(rede)

            case "7":
                print("Encerrando...")
                break

            case _:
                print("Opção inválida.")

        # Pausa entre operações para o usuário ler o resultado
        pausar()


if __name__ == "__main__":
    main()

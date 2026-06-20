# Arquivo auxiliar de testes automatizados.
# Valida as principais funcionalidades do sistema de forma rápida.
# Útil para verificar que tudo funciona antes da apresentação.

from rede import RedeSocial
from init_db import criar_banco


# Contadores globais de testes aprovados e reprovados
ok = 0
falhas = 0


def checar(descricao, condicao):
    # Avalia uma condição e registra o resultado do teste
    global ok, falhas

    if condicao:
        ok += 1
        print(f"✓ {descricao}")
    else:
        falhas += 1
        print(f"✗ {descricao}")


def titulo(texto):
    print("\n" + "=" * 50)
    print(texto)
    print("=" * 50)


def main():
    global ok, falhas

    # Garante que o banco existe antes de rodar os testes
    criar_banco()

    rede = RedeSocial()

    titulo("TESTES DO SISTEMA")

    # Usernames usados apenas durante os testes
    usuario_teste = "teste_usuario"
    amigo_teste = "teste_amigo"

    # Teste 1: cadastrar um novo usuário
    resultado = rede.adicionar_usuario(usuario_teste, "Usuário Teste", 20)
    checar("Cadastro de usuário", resultado)

    # Teste 2: tentar cadastrar o mesmo username de novo (deve falhar)
    resultado = rede.adicionar_usuario(usuario_teste, "Outro Usuário", 30)
    checar("Bloqueio de username duplicado", not resultado)

    # Cria um segundo usuário para testar as amizades
    rede.adicionar_usuario(amigo_teste, "Amigo Teste", 21)

    # Teste 3: criar amizade entre os dois usuários de teste
    resultado = rede.criar_amizade(usuario_teste, amigo_teste)
    checar("Criar amizade", resultado)

    # Teste 4: tentar criar amizade consigo mesmo (deve falhar)
    resultado = rede.criar_amizade(usuario_teste, usuario_teste)
    checar("Bloqueio de autoamizade", not resultado)

    # Teste 5: verificar se a listagem de amigos retorna resultados
    amigos = rede.listar_amigos(usuario_teste)
    checar("Listar amigos", len(amigos) > 0)

    # Teste 6: remover a amizade criada
    resultado = rede.remover_amizade(usuario_teste, amigo_teste)
    checar("Remover amizade", resultado)

    # Teste 7: remover o usuário principal de teste
    resultado = rede.remover_usuario(usuario_teste)
    checar("Remover usuário", resultado)

    # Limpa também o segundo usuário criado durante os testes
    rede.remover_usuario(amigo_teste)

    # Exibe o resultado final
    print("\n" + "=" * 50)
    print(f"Resultado: {ok} passaram | {falhas} falharam")
    print("=" * 50)


if __name__ == "__main__":
    main()

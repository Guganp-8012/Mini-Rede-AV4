import database as db

def popular_banco_teste():
    print("Inicializando o banco de dados...")
    db.inicializar_banco()
    
    print("\nCadastrando usuários de teste...")
    # Formato: (Nome, Idade, Login, Senha)
    usuarios = [
        ("Professor Joselito", 40, "joselito", "1234"),
        ("Ana Silva", 19, "ana", "senha123"),
        ("Carlos Eduardo", 21, "carlos", "carlos1"),
        ("Beatriz Souza", 18, "bia", "biabia"),
        ("Bruno Lima", 22, "bruno", "bruno99"),
        ("Amanda Costa", 20, "amanda", "vitoria1")
    ]
    
    # Dicionário para guardar os IDs gerados dinamicamente para cada login
    ids = {}
    
    for nome, idade, login, senha in usuarios:
        ok, msg = db.cadastrar_conta(nome, idade, login, senha)
        if ok:
            print(f"✓ Usuário {nome} cadastrado com sucesso!")
        else:
            print(f"✗ Falha ao cadastrar {nome}: {msg}")
            
    # Como as contas foram criadas sequencialmente no banco limpo:
    # joselito = ID 1, ana = ID 2, carlos = ID 3, bia = ID 4, bruno = ID 5, amanda = ID 6
    print("\nCriando vínculos de amizade de teste...")
    amizades = [
        (1, 2), # Joselito e Ana
        (1, 3), # Joselito e Carlos
        (2, 3), # Ana e Carlos
        (2, 4), # Ana e Bia
        (4, 5), # Bia e Bruno
        (5, 6), # Bruno e Amanda
        (3, 6)  # Carlos e Amanda
    ]
    
    for id1, id2 in amizades:
        ok, msg = db.criar_amizade(id1, id2)
        if ok:
            print(f"✓ Amizade criada entre ID {id1} e ID {id2}")
        else:
            print(f"✗ Falha na amizade ({id1}, {id2}): {msg}")

    print("\n[PRONTO] Banco de dados preenchido com sucesso para os testes!")

if __name__ == "__main__":
    popular_banco_teste()
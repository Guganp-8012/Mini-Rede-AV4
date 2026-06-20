# Arquivo auxiliar para popular o banco com dados de exemplo.
# Usado para demonstração na apresentação.
# Pode ser executado múltiplas vezes: limpa os dados anteriores antes de inserir.

from rede import RedeSocial
from init_db import criar_banco
import database
import sqlite3


def limpar_banco():
    # Remove todos os registros das tabelas e reseta o contador de IDs
    # Necessário para evitar conflitos ao rodar o script mais de uma vez
    conn = database.conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM amizades")
    cursor.execute("DELETE FROM usuarios")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='usuarios'")
    conn.commit()
    conn.close()


def main():
    # Garante que o banco existe antes de tentar popular
    criar_banco()
    limpar_banco()

    rede = RedeSocial()

    # Lista de usuários de exemplo: (username, nome, idade)
    usuarios = [
        ("joao123", "João Silva", 20),
        ("maria456", "Maria Souza", 19),
        ("ana789", "Ana Lima", 21),
        ("carlos10", "Carlos Oliveira", 22),
        ("pedro22", "Pedro Santos", 18)
    ]

    for username, nome, idade in usuarios:
        rede.adicionar_usuario(username, nome, idade)

    # Lista de amizades de exemplo: (username1, username2)
    amizades = [
        ("joao123", "maria456"),
        ("joao123", "ana789"),
        ("maria456", "carlos10"),
        ("pedro22", "joao123")
    ]

    for user1, user2 in amizades:
        rede.criar_amizade(user1, user2)

    print("Banco populado com sucesso!")


if __name__ == "__main__":
    main()

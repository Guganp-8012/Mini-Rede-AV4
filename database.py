# Camada de acesso ao banco de dados.
# Contém todas as operações de leitura e escrita no SQLite.
# É o arquivo mais importante do projeto: centraliza toda a lógica de persistência.

import sqlite3
from usuario import Usuario

# Nome do arquivo do banco — deve ser o mesmo definido em init_db.py
DB_NAME = "rede_social.db"


def conectar():
    # Abre e retorna uma conexão com o banco de dados
    return sqlite3.connect(DB_NAME)


def adicionar_usuario(username, nome, idade):
    conn = conectar()
    cursor = conn.cursor()

    try:
        # Tenta inserir o novo usuário no banco
        # O SQLite rejeita automaticamente se o username já existir (UNIQUE)
        cursor.execute(
            """
            INSERT INTO usuarios
            (username, nome, idade)
            VALUES (?, ?, ?)
            """,
            (username, nome, idade)
        )

        conn.commit()
        return True  # Inserção bem-sucedida

    except sqlite3.IntegrityError:
        # Erro disparado quando o username já existe no banco
        return False

    finally:
        # Garante que a conexão seja fechada mesmo em caso de erro
        conn.close()


def remover_usuario(username):
    conn = conectar()
    cursor = conn.cursor()

    # Busca o ID do usuário pelo username
    cursor.execute(
        """
        SELECT id
        FROM usuarios
        WHERE username = ?
        """,
        (username,)
    )

    usuario = cursor.fetchone()

    # Se não encontrou, encerra sem fazer nada
    if not usuario:
        conn.close()
        return False

    user_id = usuario[0]

    # Remove todas as amizades do usuário antes de removê-lo
    # Necessário para não deixar registros órfãos na tabela de amizades
    cursor.execute(
        """
        DELETE FROM amizades
        WHERE usuario1 = ?
           OR usuario2 = ?
        """,
        (user_id, user_id)
    )

    # Agora remove o próprio usuário
    cursor.execute(
        """
        DELETE FROM usuarios
        WHERE id = ?
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()

    return True


def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    # Busca todos os usuários ordenados por username
    cursor.execute(
        """
        SELECT id, username, nome, idade
        FROM usuarios
        ORDER BY username
        """
    )

    # Converte cada linha do resultado em um objeto Usuario
    usuarios = [
        Usuario(*dados)
        for dados in cursor.fetchall()
    ]

    conn.close()

    return usuarios


def obter_id(username):
    # Função auxiliar: retorna o ID de um usuário pelo username
    # Usada internamente por criar_amizade e remover_amizade
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM usuarios
        WHERE username = ?
        """,
        (username,)
    )

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado[0]

    return None  # Usuário não encontrado


def criar_amizade(username1, username2):
    # Impede que um usuário se adicione como amigo de si mesmo
    if username1 == username2:
        return False

    # Obtém os IDs dos dois usuários
    id1 = obter_id(username1)
    id2 = obter_id(username2)

    # Se qualquer um dos usernames não existir, cancela
    if id1 is None or id2 is None:
        return False

    conn = conectar()
    cursor = conn.cursor()

    # Verifica se a amizade já existe, checando as duas ordens possíveis
    # (id1, id2) ou (id2, id1) — amizade é bidirecional
    cursor.execute(
        """
        SELECT *
        FROM amizades
        WHERE
        (usuario1 = ? AND usuario2 = ?)
        OR
        (usuario1 = ? AND usuario2 = ?)
        """,
        (id1, id2, id2, id1)
    )

    # Se já existe amizade, não cria duplicata
    if cursor.fetchone():
        conn.close()
        return False

    # Insere a nova amizade no banco
    cursor.execute(
        """
        INSERT INTO amizades
        (usuario1, usuario2)
        VALUES (?, ?)
        """,
        (id1, id2)
    )

    conn.commit()
    conn.close()

    return True


def remover_amizade(username1, username2):
    # Obtém os IDs dos dois usuários
    id1 = obter_id(username1)
    id2 = obter_id(username2)

    # Se qualquer um não existir, não há o que remover
    if id1 is None or id2 is None:
        return False

    conn = conectar()
    cursor = conn.cursor()

    # Remove a amizade checando as duas ordens possíveis
    cursor.execute(
        """
        DELETE FROM amizades
        WHERE
        (usuario1 = ? AND usuario2 = ?)
        OR
        (usuario1 = ? AND usuario2 = ?)
        """,
        (id1, id2, id2, id1)
    )

    conn.commit()

    # rowcount indica quantas linhas foram afetadas
    # Se for 0, a amizade não existia
    removidas = cursor.rowcount

    conn.close()

    return removidas > 0


def listar_amigos(username):
    user_id = obter_id(username)

    # Se o usuário não existe, retorna lista vazia
    if user_id is None:
        return []

    conn = conectar()
    cursor = conn.cursor()

    # Busca todos os usuários que têm amizade com user_id
    # O JOIN cruza a tabela usuarios com amizades considerando as duas ordens
    cursor.execute(
        """
        SELECT u.id,
               u.username,
               u.nome,
               u.idade
        FROM usuarios u
        JOIN amizades a
        ON (
            (a.usuario1 = ? AND a.usuario2 = u.id)
            OR
            (a.usuario2 = ? AND a.usuario1 = u.id)
        )
        """,
        (user_id, user_id)
    )

    # Converte cada resultado em um objeto Usuario
    amigos = [
        Usuario(*dados)
        for dados in cursor.fetchall()
    ]

    conn.close()

    return amigos


def contar_amigos(user_id):
    conn = conectar()
    cursor = conn.cursor()

    # Conta quantas amizades existem envolvendo esse user_id
    # em qualquer uma das colunas (usuario1 ou usuario2)
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM amizades
        WHERE usuario1 = ?
           OR usuario2 = ?
        """,
        (user_id, user_id)
    )

    quantidade = cursor.fetchone()[0]

    conn.close()

    return quantidade

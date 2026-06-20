import sqlite3
import hashlib

DB_FILE = "rede_social.db"


def codificar_senha(senha: str) -> str:
    """Função automática de duas linhas para criptografia SHA-256."""
    return hashlib.sha256(senha.encode()).hexdigest()


def get_connection():
    """Abre conexão direta aplicando as restrições de chaves estrangeiras."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def inicializar_banco():
    """Cria a estrutura das tabelas relacionais do sistema."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            nome  TEXT    NOT NULL,
            idade INTEGER NOT NULL CHECK(idade > 0),
            login TEXT    NOT NULL UNIQUE,
            senha TEXT    NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS amizades (
            id_a INTEGER NOT NULL,
            id_b INTEGER NOT NULL,
            PRIMARY KEY (id_a, id_b),
            FOREIGN KEY (id_a) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (id_b) REFERENCES usuarios(id) ON DELETE CASCADE,
            CHECK (id_a < id_b)
        )
    """)
    conn.commit()
    conn.close()


def cadastrar_conta(nome: str, idade: int, login: str, senha: str) -> tuple:
    if nome.strip() == "" or login.strip() == "" or senha == "":
        return (False, "Preencha todos os campos.")
    if idade <= 0:
        return (False, "Idade deve ser maior que zero.")
    if len(senha) < 4:
        return (False, "A senha deve ter pelo menos 4 caracteres.")
        
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO usuarios (nome, idade, login, senha) VALUES (?, ?, ?, ?)",
            (nome.strip(), idade, login.strip(), codificar_senha(senha))
        )
        conn.commit()
        conn.close()
        return (True, "Conta criada com sucesso!")
    except sqlite3.IntegrityError:
        return (False, "Este login já existe. Escolha outro.")


def fazer_login(login: str, senha: str) -> tuple:
    conn = get_connection()
    row = conn.execute(
        "SELECT id, nome, idade, login, senha FROM usuarios WHERE login = ?", (login.strip(),)
    ).fetchone()
    conn.close()
    
    if row is None or row[4] != codificar_senha(senha):
        return (False, "Login ou senha incorretos.")
    # Converte o retorno para formato de dicionário para manter compatibilidade
    user_dict = {"id": row[0], "nome": row[1], "idade": row[2], "login": row[3]}
    return (True, user_dict)


def remover_usuario(user_id: int) -> tuple:
    conn = get_connection()
    linhas = conn.execute("DELETE FROM usuarios WHERE id = ?", (user_id,)).rowcount
    conn.commit()
    conn.close()
    if int(linhas) == 0:
        return (False, "Usuário não encontrado.")
    return (True, "Sua conta foi removida com sucesso.")


def listar_usuarios_exceto(user_id: int) -> list:
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, nome, idade, login FROM usuarios WHERE id != ? ORDER BY nome", (user_id,)
    ).fetchall()
    conn.close()
    
    # Mapeia as tuplas do SQLite de volta para dicionários dinâmicos
    return [{"id": r[0], "nome": r[1], "idade": r[2], "login": r[3]} for r in rows]


def contar_amigos(user_id: int) -> int:
    conn = get_connection()
    total = conn.execute(
        "SELECT COUNT(*) FROM amizades WHERE id_a = ? OR id_b = ?", (user_id, user_id)
    ).fetchone()[0]
    conn.close()
    return total


def _par(id1: int, id2: int) -> tuple:
    return (min(id1, id2), max(id1, id2))


def sao_amigos(id1: int, id2: int) -> bool:
    id_a, id_b = _par(id1, id2)
    conn = get_connection()
    r = conn.execute("SELECT 1 FROM amizades WHERE id_a = ? AND id_b = ?", (id_a, id_b)).fetchone()
    conn.close()
    return r is not None


def criar_amizade(id1: int, id2: int) -> tuple:
    if id1 == id2:
        return (False, "Você não pode adicionar a si mesmo.")
    if sao_amigos(id1, id2):
        return (False, "Vocês já são amigos.")
        
    id_a, id_b = _par(id1, id2)
    conn = get_connection()
    conn.execute("INSERT INTO amizades (id_a, id_b) VALUES (?, ?)", (id_a, id_b))
    conn.commit()
    conn.close()
    return (True, "Amizade adicionada!")


def remover_amizade(id1: int, id2: int) -> tuple:
    id_a, id_b = _par(id1, id2)
    conn = get_connection()
    linhas = conn.execute("DELETE FROM amizades WHERE id_a = ? AND id_b = ?", (id_a, id_b)).rowcount
    conn.commit()
    conn.close()
    if int(linhas) == 0:
        return (False, "Amizade não encontrada.")
    return (True, "Amizade desfeita.")


def listar_amigos(user_id: int) -> list:
    conn = get_connection()
    rows = conn.execute("""
        SELECT u.id, u.nome, u.idade, u.login FROM usuarios u
        JOIN amizades a ON (a.id_a = u.id OR a.id_b = u.id)
        WHERE (a.id_a = ? OR a.id_b = ?) AND u.id != ? ORDER BY u.nome
    """, (user_id, user_id, user_id)).fetchall()
    conn.close()
    return [{"id": r[0], "nome": r[1], "idade": r[2], "login": r[3]} for r in rows]
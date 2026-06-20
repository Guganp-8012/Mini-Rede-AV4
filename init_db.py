# Responsável por criar o banco de dados e as tabelas necessárias.
# Deve ser executado uma única vez antes de usar o sistema,
# mas pode ser chamado a qualquer momento pois usa IF NOT EXISTS.

import sqlite3

# Nome do arquivo do banco de dados SQLite
DB_NAME = "rede_social.db"


def criar_banco():
    # Abre (ou cria) o arquivo do banco de dados
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Cria a tabela de usuários, caso ainda não exista
    # O id é gerado automaticamente pelo SQLite (AUTOINCREMENT)
    # O username é único: o banco rejeita duplicatas automaticamente
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL
        )
    """)

    # Cria a tabela de amizades, caso ainda não exista
    # Cada linha representa um vínculo entre dois usuários (pelos seus IDs)
    # As FOREIGN KEYs garantem que os IDs referenciam usuários existentes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS amizades (
            usuario1 INTEGER NOT NULL,
            usuario2 INTEGER NOT NULL,

            FOREIGN KEY (usuario1)
                REFERENCES usuarios(id),

            FOREIGN KEY (usuario2)
                REFERENCES usuarios(id)
        )
    """)

    # Salva as alterações e fecha a conexão
    conn.commit()
    conn.close()

    print("Banco criado com sucesso!")


# Permite executar diretamente: python init_db.py
if __name__ == "__main__":
    criar_banco()

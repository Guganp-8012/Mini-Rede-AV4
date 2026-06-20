# Responsável por representar um usuário como objeto Python.
# Utilizado pelo database.py para retornar dados estruturados ao invés de tuplas brutas.

class Usuario:
    # Construtor: recebe os dados vindos do banco e os armazena como atributos
    def __init__(self, user_id, username, nome, idade):
        self.id = user_id        # ID gerado automaticamente pelo SQLite
        self.username = username  # Identificador único do usuário (ex: joao123)
        self.nome = nome          # Nome completo (ex: João Silva)
        self.idade = idade        # Idade em anos

    # Representação textual do objeto, usada ao imprimir um usuário diretamente
    def __str__(self):
        return (
            f"ID: {self.id} | "
            f"Username: {self.username} | "
            f"Nome: {self.nome} | "
            f"Idade: {self.idade}"
        )

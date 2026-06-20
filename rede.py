# Camada intermediária entre a interface (main.py) e o banco de dados (database.py).
# Mantida principalmente para atender ao requisito de modularização:
# main.py nunca acessa database.py diretamente, sempre passa por RedeSocial.

import database


class RedeSocial:

    def adicionar_usuario(self, username, nome, idade):
        # Repassa o cadastro para o banco e retorna True/False
        return database.adicionar_usuario(username, nome, idade)

    def remover_usuario(self, username):
        # Remove o usuário e todas as suas amizades do banco
        return database.remover_usuario(username)

    def listar_usuarios(self):
        # Retorna uma lista de objetos Usuario com todos os cadastrados
        return database.listar_usuarios()

    def criar_amizade(self, username1, username2):
        # Cria vínculo entre dois usuários; retorna False se inválido ou duplicado
        return database.criar_amizade(username1, username2)

    def remover_amizade(self, username1, username2):
        # Remove o vínculo entre dois usuários; retorna False se não existia
        return database.remover_amizade(username1, username2)

    def listar_amigos(self, username):
        # Retorna lista de objetos Usuario que são amigos do username informado
        return database.listar_amigos(username)

    def contar_amigos(self, user_id):
        # Retorna a quantidade de amigos de um usuário pelo seu ID
        return database.contar_amigos(user_id)

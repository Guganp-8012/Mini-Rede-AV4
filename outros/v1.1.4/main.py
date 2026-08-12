import database as db
import auth_gui as auth

if __name__ == "__main__":
    db.inicializar_banco()
    auth.abrir_tela_inicial()
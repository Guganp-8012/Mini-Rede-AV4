import tkinter as tk
from tkinter import messagebox
import database as db
import sistema_gui as sys_gui  # Importa o próximo módulo de telas

usuario_logado = None


def abrir_tela_inicial():
    janela = tk.Tk()
    janela.title("Rede Social")
    janela.geometry("300x220")

    tk.Label(janela, text="MINI REDE SOCIAL", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Button(janela, text="Entrar (Login)", width=22, command=lambda: [janela.destroy(), abrir_tela_login()]).pack(pady=5)
    tk.Button(janela, text="Criar Conta (Cadastro)", width=22, command=lambda: [janela.destroy(), abrir_tela_cadastro()]).pack(pady=5)
    tk.Button(janela, text="Sair do Programa", width=22, command=janela.quit).pack(pady=5)

    janela.mainloop()


def abrir_tela_login():
    janela = tk.Tk()
    janela.title("Login")
    janela.geometry("280x200")

    tk.Label(janela, text="Login:").pack(pady=2)
    campo_login = tk.Entry(janela)
    campo_login.pack()

    tk.Label(janela, text="Senha:").pack(pady=2)
    campo_senha = tk.Entry(janela, show="*")
    campo_senha.pack()

    def realizar_login():
        global usuario_logado
        ok, resultado = db.fazer_login(campo_login.get(), campo_senha.get())
        if ok:
            usuario_logado = resultado  # Dicionário do usuário logado
            janela.destroy()
            # Passa o usuário logado por parâmetro para o outro módulo de interface!
            sys_gui.abrir_menu_principal(usuario_logado)
        else:
            messagebox.showerror("Erro de Autenticação", resultado)

    tk.Button(janela, text="Entrar", width=15, command=realizar_login).pack(pady=10)
    tk.Button(janela, text="Voltar", width=15, command=lambda: [janela.destroy(), abrir_tela_inicial()]).pack()
    janela.mainloop()


def abrir_tela_cadastro():
    janela = tk.Tk()
    janela.title("Cadastro")
    janela.geometry("280x280")

    tk.Label(janela, text="Nome Completo:").pack()
    campo_nome = tk.Entry(janela)
    campo_nome.pack()

    tk.Label(janela, text="Idade:").pack()
    campo_idade = tk.Entry(janela)
    campo_idade.pack()

    tk.Label(janela, text="Login desejado:").pack()
    campo_login = tk.Entry(janela)
    campo_login.pack()

    tk.Label(janela, text="Senha:").pack()
    campo_senha = tk.Entry(janela, show="*")
    campo_senha.pack()

    def salvar_cadastro():
        try:
            idade = int(campo_idade.get())
        except ValueError:
            messagebox.showerror("Erro", "A idade deve ser um número inteiro.")
            return

        ok, msg = db.cadastrar_conta(campo_nome.get(), idade, campo_login.get(), campo_senha.get())
        if ok:
            messagebox.showinfo("Sucesso", msg)
            janela.destroy()
            abrir_tela_inicial()
        else:
            messagebox.showerror("Erro", msg)

    tk.Button(janela, text="Salvar Cadastro", width=15, command=salvar_cadastro).pack(pady=10)
    tk.Button(janela, text="Cancelar", width=15, command=lambda: [janela.destroy(), abrir_tela_inicial()]).pack()
    janela.mainloop()
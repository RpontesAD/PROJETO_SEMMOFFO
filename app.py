import customtkinter as ctk
from ui.tela_principal import TelaPrincipal
from ui.tela_cadastro import TelaCadastro


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        
        self.title("SEMMOFFO - Monitor de Rotinas")
        self.geometry("700x700")

        self.container = ctk.CTkFrame(self)
        self.container.pack(
            fill="both",
            expand=True
        )

        self.mostrar_tela_principal()


    def trocar_tela(self, tela):

        for widget in self.container.winfo_children():
            widget.destroy()

        nova_tela = tela(
            self.container,
            self
        )

        nova_tela.pack(
            fill="both",
            expand=True
        )


    def mostrar_tela_principal(self):
        self.trocar_tela(TelaPrincipal)
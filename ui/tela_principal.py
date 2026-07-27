import customtkinter as ctk
from database import listar_rotinas
from ui.componentes import CardRotina
from ui.tela_cadastro import TelaCadastro
from monitor import verificar_rotina


class TelaPrincipal(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app

        self.criar_widgets()


    def carregar_rotinas(self):

        for widget in self.lista_rotinas.winfo_children():
            widget.destroy()

        rotinas = listar_rotinas()

        for rotina in rotinas:

            resultado = verificar_rotina(rotina[0])

            card = CardRotina(
                self.lista_rotinas,
                resultado
            )

            card.pack(
                fill="x",
                padx=10,
                pady=10
            )


    def abrir_cadastro(self):
        self.app.trocar_tela(TelaCadastro)


    def criar_widgets(self):

        topo = ctk.CTkFrame(self)
        topo.pack(fill="x", padx=15, pady=15)


        titulo = ctk.CTkLabel(
            topo,
            text="SEMMOFFO - Monitor de Rotinas",
            font=("Arial", 24, "bold")
        )

        titulo.pack(
            side="left",
            padx=15,
            pady=15
        )


        botao_adicionar = ctk.CTkButton(
            topo,
            text="+ Nova Rotina",
            fg_color="#856C00",
            hover_color="#B19000",
            command=self.abrir_cadastro
        )

        botao_adicionar.pack(
            side="right",
            padx=5
        )


        self.lista_rotinas = ctk.CTkScrollableFrame(self)

        self.lista_rotinas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0,15)
        )


        self.carregar_rotinas()
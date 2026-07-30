import customtkinter as ctk
from database import listar_rotinas_ativas
from database import inativar_rotina as db_inativar_rotina
from ui.estilos import *
from ui.componentes import JanelaConfirmacao
from ui.componentes import CardRotina
from monitor import verificar_rotina


class TelaPrincipal(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app

        self.criar_widgets()


    def carregar_rotinas(self):

        for widget in self.lista_rotinas.winfo_children():
            widget.destroy()

        rotinas = listar_rotinas_ativas()

        if not rotinas:
        
            ctk.CTkLabel(
                self.lista_rotinas,
                text="Nenhuma rotina cadastrada...",
                font=FONTE_NORMAL,
                text_color="gray60"
            ).pack(
                expand=True,
                pady=40
            )

            return

        for rotina in rotinas:

            resultado = verificar_rotina(rotina["id"])

            card = CardRotina(
                self.lista_rotinas,
                resultado,
                on_inativar=self.confirmar_inativacao,
                on_editar=self.editar_rotina,
                on_detalhes=self.ver_detalhes
            )

            card.pack(
                fill="x",
                padx=10,
                pady=10
            )


    def abrir_cadastro(self):
        self.app.trocar_tela("cadastro")
        
    def editar_rotina(self, id_rotina):

        self.app.trocar_tela(
            "cadastro",
            id_rotina=id_rotina
        )
        
    def abrir_inativas(self):
        self.app.trocar_tela("inativas")

    def ver_detalhes(self, id_rotina):

        self.app.trocar_tela(
            "detalhes",
            id_rotina=id_rotina
        )


    def criar_widgets(self):

        topo = ctk.CTkFrame(self)
        topo.pack(fill="x", padx=15, pady=15)


        titulo = ctk.CTkLabel(
            topo,
            text="SEMMOFFO - ROTINAS",
            font= FONTE_TITULO
        )

        titulo.pack(
            side="left",
            padx=15,
            pady=15
        )


        botao_adicionar = ctk.CTkButton(
            topo,
            text="+ Nova Rotina",
            text_color= TX_AMARELO,
            font=FONTE_NORMAL_BOLD,
            fg_color=AMARELO,
            hover_color=AMARELO_HOVER,
            command=self.abrir_cadastro
        )

        botao_adicionar.pack(
            side="right",
            padx=10
        )
        
        ctk.CTkButton(  
            topo,
            text="Rotinas Inativas",
            text_color= TX_CINZA,
            font= FONTE_NORMAL_BOLD,
            fg_color=CINZA,
            hover_color=CINZA_HOVER,
            command=self.abrir_inativas
        ).pack(side="right", padx=5)


        self.lista_rotinas = ctk.CTkScrollableFrame(self)

        self.lista_rotinas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0,15)
        )


        self.carregar_rotinas()
    
    def confirmar_inativacao(self, id_rotina, nome):

        JanelaConfirmacao(
            parent=self,
            titulo="Inativar rotina",
            mensagem=(
                f'Deseja realmente inativar a rotina\n\n'
                f'"{nome}"?\n\n'
                "Ela será movida para a lista de rotinas inativas."
            ),
            texto_confirmar="Inativar",
            callback_confirmar=lambda: self.inativar_rotina(id_rotina)
        )
        
    def inativar_rotina(self, id_rotina):

        db_inativar_rotina(id_rotina)

        self.app.notificar(
            "Rotina inativada com sucesso.",
            "sucesso",
            bg_color="#2b2b2b"
        )

        self.carregar_rotinas()
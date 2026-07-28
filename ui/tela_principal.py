import customtkinter as ctk
from database import listar_rotinas_ativas
from database import inativar_rotina as db_inativar_rotina
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

        for rotina in rotinas:

            resultado = verificar_rotina(rotina["id"])

            card = CardRotina(
                self.lista_rotinas,
                resultado,
                on_inativar=self.confirmar_inativacao,
                on_editar=self.editar_rotina
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
        
        ctk.CTkButton(
            topo,
            text="Rotinas Inativas",
            fg_color="#555555",
            hover_color="#444444",
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

        janela = ctk.CTkToplevel(self)
        janela.title("Inativar rotina")
        janela.geometry("400x180")
        janela.grab_set()
        janela.resizable(False, False)

        ctk.CTkLabel(
            janela,
            text=f"Inativar a rotina\n\n'{nome}'?",
            font=("Arial", 18, "bold"),
            justify="center"
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            janela,
            text="Ela será movida para a lista de rotinas inativas.",
            justify="center"
        ).pack()

        frame = ctk.CTkFrame(janela, fg_color="transparent")
        frame.pack(pady=20)

        ctk.CTkButton(
            frame,
            text="Cancelar",
            fg_color="gray",
            command=janela.destroy
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            frame,
            text="Inativar",
            fg_color="#D32F2F",
            hover_color="#B71C1C",
            command=lambda: self.inativar_rotina(
                id_rotina,
                janela
            )
        ).pack(side="left", padx=10)
        
    def inativar_rotina(self, id_rotina, janela):

        db_inativar_rotina(id_rotina)

        janela.destroy()

        self.carregar_rotinas()
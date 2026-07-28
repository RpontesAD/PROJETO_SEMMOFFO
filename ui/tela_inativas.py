import customtkinter as ctk
from database import listar_rotinas_inativas, restaurar_rotina, excluir_rotina
from monitor import verificar_rotina
from ui.componentes import CardRotinaInativa


class TelaInativas(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app

        self.criar_widgets()


    def carregar_rotinas(self):

        for widget in self.lista_rotinas.winfo_children():
            widget.destroy()

        rotinas = listar_rotinas_inativas()

        for rotina in rotinas:

            resultado = verificar_rotina(rotina[0])

            card = CardRotinaInativa(
                self.lista_rotinas,
                resultado,
                on_restaurar=self.confirmar_restauracao,
                on_excluir=self.confirmar_exclusao
            )

            card.pack(
                fill="x",
                padx=10,
                pady=10
            )


    def voltar(self):
        self.app.trocar_tela("principal")


    def criar_widgets(self):

        topo = ctk.CTkFrame(self)
        topo.pack(fill="x", padx=15, pady=15)

        ctk.CTkButton(
            topo,
            text="← Voltar",
            command=self.voltar
        ).pack(side="left")

        ctk.CTkLabel(
            topo,
            text="Rotinas Inativas",
            font=("Arial",24,"bold")
        ).pack(side="left", padx=20)

        self.lista_rotinas = ctk.CTkScrollableFrame(self)

        self.lista_rotinas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0,15)
        )

        self.carregar_rotinas()
        
    def confirmar_restauracao(self, id_rotina, nome):

        janela = ctk.CTkToplevel(self)
        janela.title("Restaurar rotina")
        janela.geometry("420x180")
        janela.grab_set()
        janela.resizable(False, False)

        ctk.CTkLabel(
            janela,
            text=f"Restaurar a rotina\n\n'{nome}'?",
            font=("Arial",18,"bold"),
            justify="center"
        ).pack(pady=(20,10))

        ctk.CTkLabel(
            janela,
            text="Ela voltará para a lista de rotinas ativas."
        ).pack()

        botoes = ctk.CTkFrame(janela, fg_color="transparent")
        botoes.pack(pady=20)

        ctk.CTkButton(
            botoes,
            text="Cancelar",
            command=janela.destroy
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            botoes,
            text="Restaurar",
            fg_color="#2E8B57",
            hover_color="#256F46",
            command=lambda: self.restaurar(id_rotina, janela)
        ).pack(side="left", padx=8)
        
    def restaurar(self, id_rotina, janela):

        restaurar_rotina(id_rotina)

        janela.destroy()

        self.carregar_rotinas()
        
    def confirmar_exclusao(self, id_rotina, nome):

        janela = ctk.CTkToplevel(self)
        janela.title("Excluir permanentemente")
        janela.geometry("470x220")
        janela.grab_set()
        janela.resizable(False, False)

        ctk.CTkLabel(
            janela,
            text="Excluir permanentemente?",
            font=("Arial",18,"bold"),
            text_color="#D32F2F"
        ).pack(pady=(20,10))

        ctk.CTkLabel(
            janela,
            text=(
                f"A rotina '{nome}' será removida do banco de dados.\n\n"
                "Todos os monitoramentos também serão excluídos.\n\n"
                "Esta ação não pode ser desfeita."
            ),
            justify="center"
        ).pack()

        botoes = ctk.CTkFrame(janela, fg_color="transparent")
        botoes.pack(pady=20)

        ctk.CTkButton(
            botoes,
            text="Cancelar",
            command=janela.destroy
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            botoes,
            text="Excluir",
            fg_color="#D32F2F",
            hover_color="#B71C1C",
            command=lambda: self.excluir(id_rotina, janela)
        ).pack(side="left", padx=8)
        
    def excluir(self, id_rotina, janela):

        excluir_rotina(id_rotina)

        janela.destroy()

        self.carregar_rotinas()
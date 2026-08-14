import customtkinter as ctk
from database import listar_rotinas_inativas, restaurar_rotina, excluir_rotina
from monitor import verificar_rotina
from ui.componentes import CardRotinaInativa
from ui.estilos import *

# Classe da tela de rotinas inativas
class TelaInativas(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app

        self.criar_widgets()

    # Carrega as rotinas inativas
    def carregar_rotinas(self):

        for widget in self.lista_rotinas.winfo_children():
            widget.destroy()

        rotinas = listar_rotinas_inativas()

        for rotina in rotinas:

            resultado = verificar_rotina(rotina["id"])

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

    # Método de voltar a tela principal
    def voltar(self):
        self.app.trocar_tela("principal")


    def criar_widgets(self):

        topo = ctk.CTkFrame(self)
        topo.pack(fill="x", padx=15, pady=15)
        
        # Botão de voltar
        ctk.CTkButton(
            topo,
            text="←",
            font=FONTE_PEQUENA_BOLD,
            width=50,
            command=self.voltar
        ).pack(side="left", padx=15, pady=15)

        # Título
        ctk.CTkLabel(
            topo,
            text="ROTINAS INATIVAS",
            font=FONTE_TITULO
        ).pack(side="left",)

        self.lista_rotinas = ctk.CTkScrollableFrame(self)

        self.lista_rotinas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0,15)
        )

        self.carregar_rotinas()
     
    # Popup de confirmação de restauração da rotina   
    def confirmar_restauracao(self, id_rotina, nome):

        janela = ctk.CTkToplevel(self)
        janela.title("Restaurar rotina")
        janela.geometry("420x180")
        janela.grab_set()
        janela.resizable(False, False)

        ctk.CTkLabel(
            janela,
            text=f'Restaurar a rotina\n\n"{nome}"?',
            font=FONTE_SUBTITULO,
            justify="center"
        ).pack(pady=(20,10))

        ctk.CTkLabel(
            janela,
            text="Ela voltará para a lista de rotinas ativas.",
            font=FONTE_PEQUENA_BOLD
        ).pack()

        botoes = ctk.CTkFrame(janela, fg_color="#242424")
        botoes.pack(pady=16)

        ctk.CTkButton(
            botoes,
            text="Cancelar",
            font=FONTE_PEQUENA_BOLD,
            width=100,
            command=janela.destroy
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            botoes,
            text="Restaurar",
            font=FONTE_PEQUENA_BOLD,
            fg_color=VERDE,
            hover_color=VERDE_HOVER,
            width=100,
            command=lambda: self.restaurar(id_rotina, janela)
        ).pack(side="left", padx=8)
        
    # Método de restaurar a rotina
    def restaurar(self, id_rotina, janela):

        restaurar_rotina(id_rotina)

        janela.destroy()

        self.carregar_rotinas()
        
    # Popup de confirmar a exclusão
    def confirmar_exclusao(self, id_rotina, nome):

        janela = ctk.CTkToplevel(self)
        janela.title("Excluir permanentemente")
        janela.geometry("470x220")
        janela.grab_set()
        janela.resizable(False, False)

        ctk.CTkLabel(
            janela,
            text="Excluir permanentemente?",
            font=FONTE_SUBTITULO,
            text_color=VERMELHO
        ).pack(pady=(20,10))

        ctk.CTkLabel(
            janela,
            text=(
                f'A rotina "{nome}" será removida do banco de dados.\n\n'
                "Todos os monitoramentos também serão excluídos.\n\n"
            ),
            font=FONTE_PEQUENA_BOLD,
            justify="center"
        ).pack()

        ctk.CTkLabel(
            janela,
            text=("Esta ação não pode ser desfeita."),
            text_color="#ffc400",
            font=FONTE_PEQUENA_BOLD,
            justify="center"
        ).pack()

        # Botões de cancelar e excluir 
        botoes = ctk.CTkFrame(janela, fg_color="#242424")
        botoes.pack(pady=20)

        ctk.CTkButton(
            botoes,
            text="Cancelar",
            font=FONTE_PEQUENA_BOLD,
            command=janela.destroy,
            width=100
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            botoes,
            text="Excluir",
            font=FONTE_PEQUENA_BOLD,
            fg_color=VERMELHO,
            hover_color=VERMELHO_HOVER,
            width=100,
            command=lambda: self.excluir(id_rotina, janela)
        ).pack(side="left", padx=8)
        
    # Método de excluir permanentemente a rotina
    def excluir(self, id_rotina, janela):

        excluir_rotina(id_rotina)

        janela.destroy()

        self.carregar_rotinas()
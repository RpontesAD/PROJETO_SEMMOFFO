import customtkinter as ctk
from tkinter import messagebox
import os
import re
from database import criar_monitoramento, buscar_monitoramento, atualizar_monitoramento
from ui.estilos import *
from tkinter import filedialog


class TelaCadastroMonitoramento(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        app,
        id_rotina,
        id_monitoramento=None
    ):
        super().__init__(parent)

        self.app = app
        self.id_rotina = id_rotina
        self.id_monitoramento = id_monitoramento
        

        self.criar_widgets()
        
        if self.id_monitoramento:
            self.carregar_monitoramento()
        
    def criar_widgets(self):

        # ---------- Topo ----------

        topo = ctk.CTkFrame(self)
        topo.pack(fill="x", padx=15, pady=15)

        ctk.CTkButton(
            topo,
            text="← Voltar",
            font=FONTE_PEQUENA_BOLD,
            text_color=TX_AZUL,
            command=self.voltar
        ).pack(side="left")

        titulo = (
            "EDITAR MONITORAMENTO"
            if self.id_monitoramento
            else "NOVO MONITORAMENTO"
        )
        
        # Adicionado .pack() com alinhamento e espaçamento
        ctk.CTkLabel(
            topo,
            text=titulo,
            font=FONTE_TITULO
        ).pack(side="left", padx=15)

        # ---------- Formulário ----------

        formulario = ctk.CTkFrame(self)
        formulario.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # Tipo

        ctk.CTkLabel(
            formulario,
            text="Tipo",
            font=FONTE_NORMAL_BOLD
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.tipo = ctk.StringVar(value="ARQUIVO_ALVO")

        ctk.CTkSegmentedButton(
            formulario,
            values=[
                "ARQUIVO_ALVO",
                "ULTIMO_ARQUIVO"
            ],
            variable=self.tipo,
            command=self.alterar_tipo
        ).pack(
            fill="x",
            padx=15
        )

        # Nome

        ctk.CTkLabel(
            formulario,
            text="Nome",
            font=FONTE_NORMAL_BOLD
        ).pack(anchor="w", padx=15, pady=(20, 5))

        self.entry_nome = ctk.CTkEntry(formulario)

        self.entry_nome.pack(
            fill="x",
            padx=15
        )

        # Caminho

        self.label_caminho = ctk.CTkLabel(
            formulario,
            text="Arquivo",
            font=FONTE_NORMAL_BOLD
        )

        self.label_caminho.pack(
            anchor="w",
            padx=15,
            pady=(20, 5)
        )

        frame_caminho = ctk.CTkFrame(
            formulario,
            fg_color="transparent"
        )

        frame_caminho.pack(
            fill="x",
            padx=15
        )

        self.entry_caminho = ctk.CTkEntry(frame_caminho)

        self.entry_caminho.pack(
            side="left",
            fill="x",
            expand=True
        )

        ctk.CTkButton(
            frame_caminho,
            text="Selecionar",
            text_color=TX_CINZA,
            font=FONTE_PEQUENA_BOLD,
            fg_color=CINZA,
            hover_color=CINZA_HOVER,
            command=self.procurar
        ).pack(
            side="left",
            padx=(10, 0)
        )

        # Obrigatório

        self.obrigatorio = ctk.BooleanVar(value=True)

        ctk.CTkCheckBox(
            formulario,
            text="Monitoramento obrigatório",
            variable=self.obrigatorio
        ).pack(
            anchor="w",
            padx=15,
            pady=25
        )

        # ---------- Rodapé ----------

        rodape = ctk.CTkFrame(self, fg_color="#333333")
        rodape.pack(fill="x", padx=15, pady=(0, 15))
        
        botoes = ctk.CTkFrame(rodape, fg_color="#333333")
        botoes.pack(pady=10)

        ctk.CTkButton(
            botoes,
            text="Cancelar",
            font=FONTE_NORMAL_BOLD,
            fg_color=VERMELHO, 
            hover_color=VERMELHO_HOVER,
            text_color=TX_VERMELHO,
            command=self.voltar
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            botoes,
            text="Salvar",
            font=FONTE_NORMAL_BOLD,
            fg_color=VERDE,
            hover_color=VERDE_HOVER,
            text_color=TX_VERDE,
            command=self.salvar
        ).pack(side="left", padx=10)
        
    def alterar_tipo(self, valor):

        if valor == "ARQUIVO_ALVO":
            self.label_caminho.configure(text="Arquivo")
        else:
            self.label_caminho.configure(text="Pasta")
            
    def voltar(self):

        self.app.trocar_tela(
            "detalhes",
            id_rotina=self.id_rotina
        )
            
    def procurar(self):

        if self.tipo.get() == "ARQUIVO_ALVO":

            caminho = filedialog.askopenfilename()

            if caminho:
                self.entry_caminho.delete(0, "end")
                self.entry_caminho.insert(0, caminho)

        else:

            caminho = filedialog.askdirectory()

            if caminho:
                self.entry_caminho.delete(0, "end")
                self.entry_caminho.insert(0, caminho)
                
    def carregar_monitoramento(self):

        monitoramento = buscar_monitoramento(
            self.id_monitoramento
        )

        if not monitoramento:
            return

        self.entry_nome.insert(
            0,
            monitoramento["nome"]
        )

        self.tipo.set(
            monitoramento["tipo"]
        )

        self.entry_caminho.insert(
            0,
            (
                os.path.join(
                    monitoramento["pasta"],
                    monitoramento["arquivo"]
                )
                if monitoramento["arquivo"]
                else monitoramento["pasta"]
            )
        )

        self.obrigatorio.set(
            bool(monitoramento["obrigatorio"])
        )

        self.alterar_tipo(
            monitoramento["tipo"]
        )
                
    def salvar(self):

        nome = self.entry_nome.get().strip()
        tipo = self.tipo.get()
        caminho = self.entry_caminho.get().strip()

        if not nome:
            return

        if not caminho:
            return

        if tipo == "ARQUIVO_ALVO":

            pasta = os.path.dirname(caminho)
            arquivo = os.path.basename(caminho)

        else:

            pasta = caminho
            arquivo = None
            
        obrigatorio = 1 if self.obrigatorio.get() else 0

        if self.id_monitoramento:

            atualizar_monitoramento(
                self.id_monitoramento,
                nome,
                tipo,
                pasta,
                arquivo,
                obrigatorio
            )

        else:

            criar_monitoramento(
                self.id_rotina,
                nome,
                tipo,
                pasta,
                arquivo,
                obrigatorio
            )

        self.voltar()
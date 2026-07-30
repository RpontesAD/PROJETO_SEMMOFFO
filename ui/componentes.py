import customtkinter as ctk
from ui.estilos import *
import tkinter as tk

class CardRotina(ctk.CTkFrame):

    def __init__(self, master, resultado, on_inativar=None, on_editar=None, on_detalhes=None):
        super().__init__(master)
        
        self.on_inativar = on_inativar
        self.on_editar = on_editar
        self.on_detalhes = on_detalhes

        id_rotina = resultado["id"]
        self.id_rotina = id_rotina
        nome = resultado["nome"]
        self.nome = nome
        executavel = resultado["executavel"]
        periodicidade = resultado["periodicidade"]
        hora = resultado["hora"]
        prazo = resultado["prazo"]
        quantidade = resultado["monitoramentos"]
        arquivos = resultado["arquivos"]
        
        if arquivos:
            arquivo = arquivos[0]

            status = arquivo["status"]
            nome_arquivo = arquivo["arquivo"]
            data_modificacao = arquivo["data_modificacao"]
        else:
            status = "⚠ Sem monitoramentos"
            nome_arquivo = "-"
            data_modificacao = "-"

        titulo = ctk.CTkLabel(
            self,
            text=nome,
            text_color="#38BDF8",
            font=FONTE_SUBTITULO,
        )

        titulo.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Telinha das rotinas
        info = ctk.CTkFrame(self, fg_color="transparent")
        info.pack(anchor="w", padx=15, pady=(0, 10))
        
        cor_status = "#22C55E"  # Verde

        if "Atrasado" in status:
            cor_status = "#EF4444"  # Vermelho
        elif "Sem monitoramentos" in status:
            cor_status = "#F59E0B"  # Amarelo
            
        linha_status = ctk.CTkFrame(info, fg_color="transparent")
        linha_status.pack(anchor="w")

        ctk.CTkLabel(
            linha_status,
            text="Status: ",
            font=FONTE_NORMAL
        ).pack(side="left")

        ctk.CTkLabel(
            linha_status,
            text=status,
            text_color=cor_status,
            font=FONTE_NORMAL_BOLD
        ).pack(side="left")    
        
        ctk.CTkLabel(
            info,
            text=f"Monitoramentos: {quantidade}",
            font=FONTE_NORMAL
        ).pack(anchor="w", pady=(5, 0))

        ctk.CTkLabel(
            info,
            text=f"Periodicidade: {periodicidade}",
            font=FONTE_NORMAL
        ).pack(anchor="w")

        botoes = ctk.CTkFrame(self, fg_color="#2b2b2b")
        botoes.pack(anchor="e", padx=15, pady=10)
        
        linha = tk.Canvas(
            self,
            height=2,
            bg="#2b2b2b",
            highlightthickness=0,
            bd=0
        )

        linha.create_line(
            0, 1, 1000, 1,
            fill="#555555",
            dash=(6, 4)
        )

        linha.pack(
            fill="x",
            padx=15,
            pady=(10, 0)
        )

        ctk.CTkButton(
            botoes, 
            text="Ver Detalhes",
            text_color=TX_VERDE,
            font=FONTE_NORMAL_BOLD,
            fg_color=VERDE,      # Verde
            hover_color=VERDE_HOVER,   # Verde mais escuro
            command=self.ver_detalhes
            ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            botoes,
            text="Editar Rotina",
            text_color=TX_AZUL,
            font=FONTE_NORMAL_BOLD,
            command=self.editar
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            botoes, 
            text="Inativar",
            text_color=TX_VERMELHO,
            font=FONTE_NORMAL_BOLD,
            fg_color=VERMELHO,
            hover_color=VERMELHO_HOVER,
            command=self.inativar
            ).pack(side="left", padx=5)
    
    def inativar(self):
        
        if self.on_inativar:
            self.on_inativar(
                self.id_rotina,
                self.nome
            )
            
    def editar(self):

        if self.on_editar:
            self.on_editar(self.id_rotina)

    def ver_detalhes(self):

        if self.on_detalhes:
            self.on_detalhes(self.id_rotina)
            
class CardRotinaInativa(ctk.CTkFrame):

    def __init__(
        self,
        master,
        resultado,
        on_restaurar=None,
        on_excluir=None
    ):
        super().__init__(master)

        self.id_rotina = resultado["id"]
        self.nome = resultado["nome"]

        self.on_restaurar = on_restaurar
        self.on_excluir = on_excluir

        quantidade = resultado["monitoramentos"]
        arquivos = resultado["arquivos"]

        if arquivos:
            arquivo = arquivos[0]

            status = arquivo["status"]
            nome_arquivo = arquivo["arquivo"]
            data_modificacao = arquivo["data_modificacao"]

        else:
            status = "⚪ Sem monitoramentos"
            nome_arquivo = "-"
            data_modificacao = "-"

        titulo = ctk.CTkLabel(
            self,
            text=self.nome,
            font=("Arial", 18, "bold")
        )

        titulo.pack(anchor="w", padx=15, pady=(10, 5))

        info = ctk.CTkLabel(
            self,
            text=f"""
Status: {status}

Monitoramentos: {quantidade}

Arquivo: {nome_arquivo}
Última modificação: {data_modificacao}
"""
        )

        info.pack(anchor="w", padx=15)

        botoes = ctk.CTkFrame(self, fg_color="#2b2b2b")
        botoes.pack(anchor="e", padx=15, pady=10)

        ctk.CTkButton(
            botoes,
            text="Restaurar",
            text_color=TX_VERDE,
            font=FONTE_NORMAL_BOLD,
            fg_color=VERDE,
            hover_color=VERDE_HOVER,
            command=self.restaurar
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            botoes,
            text="Excluir",
            text_color=TX_VERMELHO,
            font=FONTE_NORMAL_BOLD,
            fg_color=VERMELHO,
            hover_color=VERMELHO_HOVER,
            command=self.excluir
        ).pack(side="left", padx=5)

    def restaurar(self):

        if self.on_restaurar:
            self.on_restaurar(
                self.id_rotina,
                self.nome
            )


    def excluir(self):

        if self.on_excluir:
            self.on_excluir(
                self.id_rotina,
                self.nome
            )

class Notificacao(ctk.CTkFrame):

    CORES = {
        "sucesso": ("#16A34A", "✓"),
        "erro": ("#DC2626", "✕"),
        "aviso": ("#D97706", "⚠"),
        "info": ("#2563EB", "ℹ")
    }

    def __init__(
        self,
        parent,
        mensagem,
        tipo="info",
        duracao=3000,
        width=350,
        height=55,
        bg_color=None
    ):
        if bg_color is None:
            bg_color = parent.cget("fg_color")
        
        super().__init__(
            parent,
            width=width,
            height=height,
            corner_radius=10,
            fg_color="#292a2b",
            bg_color=bg_color
        )

        cor, icone = self.CORES.get(tipo, self.CORES["info"])

        self.configure(border_width=2, border_color=cor)

        ctk.CTkLabel(
            self,
            text=f"{icone}  {mensagem}",
            text_color="white",
            font=FONTE_PEQUENA_BOLD
        ).pack(
            padx=15,
            pady=10
        )

        self.after(duracao, self.destroy)

class JanelaConfirmacao(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        titulo,
        mensagem,
        callback_confirmar,
        texto_confirmar="Confirmar",
        cor_confirmar="#DC2626",
        hover_confirmar="#B91C1C"
    ):
        super().__init__(parent)

        self.callback_confirmar = callback_confirmar

        self.title(titulo)
        self.geometry("420x180")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text=titulo,
            font=FONTE_SUBTITULO
        ).grid(
            row=0,
            column=0,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            self,
            text=mensagem,
            justify="center",
            wraplength=350
        ).grid(
            row=1,
            column=0,
            padx=20
        )

        frame_botoes = ctk.CTkFrame(
            self,
            fg_color="#242424"
        )

        frame_botoes.grid(
            row=2,
            column=0,
            pady=20
        )

        ctk.CTkButton(
            frame_botoes,
            text="Cancelar",
            width=100,
            command=self.destroy
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            frame_botoes,
            text=texto_confirmar,
            width=100,
            fg_color=cor_confirmar,
            hover_color=hover_confirmar,
            command=self.confirmar
        ).pack(
            side="left",
            padx=5
        )

    def confirmar(self):
        self.callback_confirmar()
        self.destroy()
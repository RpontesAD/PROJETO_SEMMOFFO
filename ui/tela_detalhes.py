import customtkinter as ctk
from database import buscar_rotina, listar_monitoramentos, excluir_monitoramento
from ui.estilos import *
from ui.componentes import JanelaConfirmacao
import tkinter as tk
from monitor import verificar_rotina
import subprocess
import threading
import os
from tkinter import messagebox


class TelaDetalhes(ctk.CTkFrame):

    def __init__(self, parent, app, id_rotina):
        super().__init__(parent)

        self.app = app
        self.id_rotina = id_rotina

        self.rotina = buscar_rotina(id_rotina)

        self.criar_widgets()
        self.carregar_monitoramentos()


    def criar_widgets(self):

        # ---------- Topo ----------

        topo = ctk.CTkFrame(self)
        topo.pack(fill="x", padx=15, pady=15)

        ctk.CTkButton(
            topo,
            text="←",
            font=FONTE_PEQUENA_BOLD,
            text_color=TX_AZUL,
            command=self.voltar,
            width=50
        ).pack(side="left", padx=15, pady=15)

        ctk.CTkLabel(
            topo,
            text=self.rotina["nome"],
            font=FONTE_TITULO
        ).pack(side="left")
        
        ctk.CTkButton(
            topo,
            text="+ Novo Monitoramento",
            text_color=TX_AMARELO,
            font=FONTE_NORMAL_BOLD,
            fg_color=AMARELO,
            hover_color=AMARELO_HOVER,
            command=self.novo_monitoramento
        ).pack(
            side="right",
            padx=15
        )

        # ---------- Informações ----------

        periodos = {
            "DIARIO": "Diário",
            "SEMANAL": "Semanal",
            "MENSAL": "Mensal"
        }

        dias_semana = {
            0: "Segunda-feira",
            1: "Terça-feira",
            2: "Quarta-feira",
            3: "Quinta-feira",
            4: "Sexta-feira",
            5: "Sábado",
            6: "Domingo"
        }

        # Informações frame
        info = ctk.CTkFrame(self)
        info.pack(fill="x", padx=15)
        

        informacoes = []

        informacoes.append(
            f"Periodicidade: {periodos[self.rotina['periodo']]}"
        )

        informacoes.append(
            f"Horário: {self.rotina['hora']}"
        )

        if self.rotina["periodo"] == "SEMANAL":

            informacoes.append(
                f"Dia da semana: {dias_semana[self.rotina['dia_semana']]}"
            )

        elif self.rotina["periodo"] == "MENSAL":

            if self.rotina["regra_dia"] == "PRIMEIRO_DIA_UTIL":

                informacoes.append(
                    "Regra: Primeiro dia útil"
                )

            elif self.rotina["regra_dia"] == "ULTIMO_DIA_UTIL":

                informacoes.append(
                    "Regra: Último dia útil"
                )

            elif self.rotina["regra_dia"] == "DIA_ESPECIFICO":

                informacoes.append(
                    f"Regra: Dia {self.rotina['dia_mes']} do mês"
                )

        ctk.CTkLabel(
            info,
            text="\n".join(informacoes),
            justify="left",
            anchor="w",
            font=FONTE_NORMAL_BOLD
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )
        
        if self.rotina["executavel"]:

            nome = os.path.basename(self.rotina["executavel"])

            ctk.CTkLabel(
                info,
                text=f"Executável: {nome}",
                text_color=COR_ATUALIZADO,
                font=FONTE_NORMAL_BOLD
            ).pack(anchor="w", padx=15)

            ctk.CTkLabel(
                info,
                text=self.rotina["executavel"],
                text_color="#a1a1a1",
                font=FONTE_PEQUENININHA
            ).pack(anchor="w", padx=15)

            ctk.CTkButton(
                info,
                text="Mostrar na pasta",
                font=FONTE_PEQUENA_BOLD,
                fg_color=CINZA,
                hover_color=CINZA_HOVER,
                text_color=TX_CINZA,
                command=self.mostrar_executavel_na_pasta
            ).pack(anchor="e", padx=15, pady=(0, 15))
            
        else:
            ctk.CTkLabel(
                info,
                text="Esta rotina é manual",
                text_color="#a1a1a1",
                font=FONTE_NORMAL_BOLD
            ).pack(anchor="w", padx=15)

            ctk.CTkLabel(
                info,
                text="Nenhum executável foi associado...",
                text_color="#808080",
                font=FONTE_PEQUENA
            ).pack(anchor="w", padx=15, pady=(0, 15))

        # ---------- Lista de monitoramentos ----------

        self.lista_monitoramentos = ctk.CTkScrollableFrame(
            self,
            height=350
        )

        self.lista_monitoramentos.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # ---------- Botões ----------

        rodape = ctk.CTkFrame(self, fg_color="#333333")
        rodape.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkButton(
            rodape,
            text="Executar Rotina",
            text_color=TX_VERDE,
            font=FONTE_NORMAL_BOLD,
            fg_color=VERDE,   
            hover_color=VERDE_HOVER,
            command=self.executar_rotina
        ).pack(side="bottom", padx=5)


    def voltar(self):

        self.app.trocar_tela("principal")
        
    def novo_monitoramento(self):
        self.app.trocar_tela(
            "cadastro_monitoramento",
            id_rotina=self.id_rotina
        )
        
    def carregar_monitoramentos(self):

        for widget in self.lista_monitoramentos.winfo_children():
            widget.destroy()

        resultado = verificar_rotina(self.id_rotina)

        monitoramentos = resultado["arquivos"]

        if not monitoramentos:

            ctk.CTkLabel(
                self.lista_monitoramentos,
                text='Clique em "+ Novo Monitoramento" para criar seu 1º monitoramento...',
                font=FONTE_VAZIO,
                text_color= "#5A5A5A"
            ).pack(
                expand=True,
                pady=40
            )

            return

        for monitoramento in monitoramentos:
            self.criar_card_monitoramento(monitoramento)
            
    # Card monitoramento e todos os elementos que o compõe
    def criar_card_monitoramento(self, monitoramento):

        card = ctk.CTkFrame(
            self.lista_monitoramentos,
            corner_radius=10
        )

        card.pack(
            fill="x",
            padx=5,
            pady=5
        )

        # Nome do monitoramento
        ctk.CTkLabel(
            card,
            text=monitoramento["nome"],
            font=FONTE_SUBTITULO
        ).pack(anchor="w", padx=15, pady=(10, 0))
        
        tipo = str(monitoramento["tipo"])
        
        if tipo == "ULTIMO_ARQUIVO":
            tipo = "Ultimo arquivo da pasta"
        else: 
            tipo = "Arquivo alvo"
        
        ctk.CTkLabel(
            card,
            text=f"Monitorando por: {tipo}",
            font=FONTE_PEQUENA,
        ).pack(anchor="w", padx=15)
        
        fonte_sublinhada = ctk.CTkFont(
            family="Roboto",
            size=14,
            weight="bold",
            underline=True
        )

        # Nome do arquivo
        status = monitoramento["status"]

        if status == "Atualizado":
            cor = "#2580e8"
            fonte = fonte_sublinhada
        else:
            cor = "#7A7A7A"      # cinza
            fonte = FONTE_NORMAL_BOLD

        label_arquivo = ctk.CTkLabel(
            card,
            text=monitoramento["arquivo"],
            text_color=cor,
            font=fonte,
            cursor="hand2"
        )

        label_arquivo.pack(anchor="w", padx=15)

        label_arquivo.bind(
            "<Button-1>",
            lambda e: self.clicar_no_arquivo(monitoramento)
        )

        # Status
        status = monitoramento["status"]

        if status == "Atualizado":
            cor = COR_ATUALIZADO
            fundo = COR_ATUALIZADO_FUNDO
            texto = "● Atualizado"
        else:
            cor = COR_ATRASADO
            fundo = COR_ATRASADO_FUNDO
            texto = "● Atrasado"

        ctk.CTkLabel(
            card,
            text=texto,
            text_color=cor,
            fg_color=fundo,
            font=FONTE_NORMAL_BOLD,
            corner_radius=20
        ).pack(
            anchor="w",
            padx=15,
            pady=(8, 0)
        )
        
        # Data de modificação
        ctk.CTkLabel(
            card,
            text=f"Última modificação: {monitoramento['data_modificacao'] if monitoramento['data_modificacao'] else 'Não encontrado'}",
            font=FONTE_PEQUENA
        ).pack(
            anchor="w",
            padx=15
        )

        # Caminho
        ctk.CTkLabel(
            card,
            text=monitoramento["caminho"],
            text_color="#a1a1a1",
            font=FONTE_PEQUENININHA,
        ).pack(anchor="w", padx=15, pady=(0, 10))
        

        botoes = ctk.CTkFrame(
            card,
            fg_color="#2b2b2b"
        )

        botoes.pack(
            anchor="e",
            padx=15,
            pady=(0, 10)
        )
        
        ctk.CTkButton(
            botoes,
            text="Editar",
            text_color=TX_AZUL,
            font=FONTE_PEQUENA_BOLD,
            width=80,
            command=lambda: self.editar_monitoramento(monitoramento)
        ).pack(
            side="left",
            padx=10
        )
        
        ctk.CTkButton(
            botoes,
            text="Mostrar na pasta",
            text_color=TX_CINZA,
            fg_color=CINZA,
            hover_color=CINZA_HOVER,
            font=FONTE_PEQUENA_BOLD,
            command=lambda: self.mostrar_na_pasta(monitoramento)
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            botoes,
            text="Excluir",
            text_color=TX_VERMELHO,
            fg_color=VERMELHO,
            hover_color=VERMELHO_HOVER,
            font=FONTE_PEQUENA_BOLD,
            width=80,
            command=lambda: self.excluir_monitoramento(monitoramento)
        ).pack(side="left", padx=10)
        
        # Linha
        linha = tk.Canvas(
            card,
            height=2,
            bg="#2b2b2b",
            highlightthickness=0,
            bd=0
        )

        linha.pack(fill="x", padx=15, pady=(10, 10))

        def desenhar(event):
            linha.delete("all")
            linha.create_line(
                0, 1,
                event.width, 1,
                fill="#424242",
                # dash=(6, 4)
            )

        linha.bind("<Configure>", desenhar)
        
    def editar_monitoramento(self, monitoramento):

        self.app.trocar_tela(
            "cadastro_monitoramento",
            id_rotina=self.id_rotina,
            id_monitoramento=monitoramento["id"]
        )
        
    def mostrar_na_pasta(self, monitoramento):

        caminho = monitoramento["caminho"]

        if not caminho:
            self.app.notificar(
                "Nenhum caminho foi encontrado.",
                "erro"
            )
            return

        if not os.path.exists(caminho):
            self.app.notificar(
                "Arquivo não encontrado.",
                "erro"
            )
            return

        subprocess.run(["explorer", "/select,", caminho])
        
    def mostrar_executavel_na_pasta(self):

        caminho = self.rotina["executavel"]

        if not caminho:
            self.app.notificar(
                "Nenhum executável foi cadastrado.",
                "erro"
            )
            return

        if not os.path.exists(caminho):
            self.app.notificar(
                "Executável não encontrado.",
                "erro"
            )
            return

        pasta = os.path.dirname(caminho)

        os.startfile(pasta)
        
    def clicar_no_arquivo(self, monitoramento):

        if monitoramento["status"] == "Atrasado":
            self.app.notificar(
                "O arquivo não pode ser aberto porque a rotina está atrasada.",
                "aviso",
                bg_color="#2b2b2b"
                
            )
            return

        caminho = monitoramento["caminho"]

        if not caminho:
            self.app.notificar(
                "Nenhum caminho foi encontrado.",
                "erro",
                bg_color="#2b2b2b"
            )
            return

        if not os.path.exists(caminho):
            self.app.notificar(
                "Arquivo não encontrado.",
                "erro",
                bg_color="#2b2b2b"
            )
            return

        os.startfile(caminho)

    def excluir_monitoramento(self, monitoramento):

        JanelaConfirmacao(
            parent=self,
            titulo="Excluir monitoramento",
            mensagem=f'Deseja realmente excluir o monitoramento\n\n"{monitoramento["nome"]}"?',
            callback_confirmar=lambda: self.confirmar_exclusao_monitoramento(monitoramento)
        )

    def confirmar_exclusao_monitoramento(self, monitoramento):

        excluir_monitoramento(monitoramento["id"])

        self.app.notificar(
            "Monitoramento excluído com sucesso.",
            "sucesso",
            bg_color="#2b2b2b"
        )

        self.carregar_monitoramentos()

    def _executar_rotina(self):
        executavel = self.rotina.get("executavel")

        if not executavel:
            self.after(
                0,
                lambda: self.app.notificar(
                    "Nenhum executável foi cadastrado.",
                    "erro",
                    bg_color="#2b2b2b"
                )
            )
            return

        if not os.path.exists(executavel):
            self.after(
                0,
                lambda: self.app.notificar(
                    "Executável não encontrado.",
                    "erro",
                    bg_color="#2b2b2b"
                )
            )
            return

        try:
            subprocess.run(executavel, shell=True)

            self.after(
                0,
                lambda: self.app.notificar(
                    "Rotina executada com sucesso.",
                    "sucesso",
                    bg_color="#2b2b2b"
                )
            )

            self.after(0, self.carregar_monitoramentos)

        except Exception as e:
            erro = str(e)

            self.after(
                0,
                lambda: self.app.notificar(
                    erro,
                    "erro",
                    tempo=5000
                )
            )
                
    def executar_rotina(self):
        threading.Thread(target=self._executar_rotina, daemon=True).start()

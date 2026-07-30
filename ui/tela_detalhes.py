import customtkinter as ctk
from database import buscar_rotina, listar_monitoramentos, excluir_monitoramento
from ui.estilos import *
from ui.componentes import JanelaConfirmacao
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
            text="← Voltar",
            font=FONTE_PEQUENA_BOLD,
            text_color=TX_AZUL,
            command=self.voltar,
            width=100
        ).pack(side="left")

        ctk.CTkLabel(
            topo,
            text=self.rotina["nome"],
            font=FONTE_TITULO
        ).pack(side="left", padx=20)
        
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
            padx=10
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

        if self.rotina["executavel"]:

            informacoes.append(
                f"Executável: {self.rotina['executavel']}"
            )

        else:

            informacoes.append(
                "Executável: Manual"
            )

        ctk.CTkLabel(
            info,
            text="\n".join(informacoes),
            justify="left",
            anchor="w",
            font=FONTE_NORMAL
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )

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
            text="Atualizar",
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
                text="Nenhum monitoramento cadastrado...",
                font=FONTE_NORMAL,
                text_color="gray60"
            ).pack(
                expand=True,
                pady=40
            )

            return

        for monitoramento in monitoramentos:
            self.criar_card_monitoramento(monitoramento)
            
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
            font=FONTE_NORMAL_BOLD
        ).pack(anchor="w", padx=15, pady=(10, 0))

        # Nome do arquivo
        ctk.CTkLabel(
            card,
            text=monitoramento["arquivo"],
            font=FONTE_NORMAL
        ).pack(anchor="w", padx=15)

        # Status
        status = monitoramento["status"]

        if status == "Atualizado":
            cor = VERDE
            texto = "● Atualizado"
        else:
            cor = VERMELHO
            texto = "● Atrasado"

        ctk.CTkLabel(
            card,
            text=texto,
            text_color=cor,
            font=FONTE_NORMAL_BOLD
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
            font=FONTE_PEQUENA
        ).pack(anchor="w", padx=15, pady=(0, 10))

        botoes = ctk.CTkFrame(
            card,
            fg_color="transparent"
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
            padx=(0, 5)
        )

        ctk.CTkButton(
            botoes,
            text="Excluir",
            text_color=TX_VERMELHO,
            fg_color=VERMELHO,
            hover_color=VERMELHO_HOVER,
            font=FONTE_PEQUENA_BOLD,
            width=80,
            command=lambda: self.excluir_monitoramento(monitoramento)
        ).pack(side="left")
        
    def editar_monitoramento(self, monitoramento):

        self.app.trocar_tela(
            "cadastro_monitoramento",
            id_rotina=self.id_rotina,
            id_monitoramento=monitoramento["id"]
        )

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

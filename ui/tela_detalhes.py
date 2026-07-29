import customtkinter as ctk
from database import buscar_rotina
from ui.estilos import *


class TelaDetalhes(ctk.CTkFrame):

    def __init__(self, parent, app, id_rotina):
        super().__init__(parent)

        self.app = app
        self.id_rotina = id_rotina

        self.rotina = buscar_rotina(id_rotina)
        

        self.criar_widgets()


    def criar_widgets(self):

        # ---------- Topo ----------

        topo = ctk.CTkFrame(self)
        topo.pack(fill="x", padx=15, pady=15)

        ctk.CTkButton(
            topo,
            text="← Voltar",
            text_color=TX_AZUL,
            command=self.voltar,
            width=100
        ).pack(side="left")

        ctk.CTkLabel(
            topo,
            text=self.rotina["nome"],
            font=FONTE_TITULO
        ).pack(side="left", padx=20)

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
            font=("Arial", 15)
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

        rodape = ctk.CTkFrame(self)
        rodape.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkButton(
            rodape,
            text="+ Novo Monitoramento",
            text_color=TX_AMARELO,
            font=FONTE_NORMAL_BOLD,
            fg_color=AMARELO,
            hover_color=AMARELO_HOVER,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            rodape,
            text="Editar Monitoramentos",
            text_color=TX_AZUL,
            font=FONTE_NORMAL_BOLD
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            rodape,
            text="Atualizar",
            text_color=TX_VERDE,
            font=FONTE_NORMAL_BOLD,
            fg_color=VERDE,   
            hover_color=VERDE_HOVER,
        ).pack(side="right", padx=5)


    def voltar(self):

        self.app.trocar_tela("principal")
import customtkinter as ctk
from database import buscar_rotina, listar_monitoramentos
from ui.estilos import *
from monitor import verificar_rotina


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
            command=self.novo_monitoramento
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
        ctk.CTkLabel(
            card,
            text=monitoramento["status"],
            font=FONTE_NORMAL
        ).pack(anchor="w", padx=15, pady=(8, 0))

        # Caminho
        ctk.CTkLabel(
            card,
            text=monitoramento["caminho"],
            font=FONTE_PEQUENA
        ).pack(anchor="w", padx=15, pady=(0, 10))
            
    
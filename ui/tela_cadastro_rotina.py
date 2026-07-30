import customtkinter as ctk
from tkinter import messagebox
import os
import re
from database import criar_rotina, buscar_rotina, atualizar_rotina
from ui.estilos import *
from tkinter import filedialog


class TelaCadastro(ctk.CTkFrame):

    def __init__(self, parent, app, id_rotina=None):
        super().__init__(parent)

        self.app = app
        self.id_rotina = id_rotina

        self.criar_widgets()

        if self.id_rotina:
            self.carregar_rotina()
        
    def selecionar_executavel(self):

        caminho = filedialog.askopenfilename(
            title="Selecione o executável",
            filetypes=[
                ("Executáveis", "*.exe"),
                ("Todos os arquivos", "*.*")
            ]
        )


        if caminho:

            self.executavel_entry.delete(0, "end")

            self.executavel_entry.insert(
                0,
                caminho
            )

    def criar_widgets(self):

        self.grid_columnconfigure(0, weight=1)


        texto_titulo = "EDITAR ROTINA" if self.id_rotina else "NOVA ROTINA"

        titulo = ctk.CTkLabel(
            self,
            text=texto_titulo,
            font=FONTE_TITULO
        )

        titulo.grid(
            row=0,
            column=0,
            pady=20
        )


        # Nome

        ctk.CTkLabel(
            self,
            text="Nome da rotina"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=50
        )


        self.nome_entry = ctk.CTkEntry(
            self,
            width=300
        )

        self.nome_entry.grid(
            row=2,
            column=0,
            pady=10
        )


        # Periodicidade

        ctk.CTkLabel(
            self,
            text="Periodicidade"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=50
        )


        self.periodicidade_combo = ctk.CTkComboBox(
            self,
            values=[
                "Diario",
                "Semanal",
                "Mensal"
            ],
            width=300,
            command=self.alterar_periodo
        )

        self.periodicidade_combo.grid(
            row=4,
            column=0,
            pady=10
        )


        # Área dinâmica

        self.frame_condicional = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.frame_condicional.grid(
            row=5,
            column=0,
            pady=10
        )


        self.criar_campos_condicionais()


        # Horário

        ctk.CTkLabel(
            self,
            text="Horário"
        ).grid(
            row=6,
            column=0,
            sticky="w",
            padx=50
        )


        self.hora_entry = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="08:00",
            placeholder_text_color=PLACEHOLDER
        )

        self.hora_entry.grid(
            row=7,
            column=0,
            pady=10
        )


        # Executável

        ctk.CTkLabel(
            self,
            text="Executável (opcional)"
        ).grid(
            row=8,
            column=0,
            sticky="w",
            padx=50
        )


        frame_executavel = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        frame_executavel.grid(
            row=9,
            column=0,
            pady=10
        )


        self.executavel_entry = ctk.CTkEntry(
            frame_executavel,
            width=220
        )

        self.executavel_entry.pack(
            side="left",
            padx=(0, 10)
        )


        botao_selecionar = ctk.CTkButton(
            frame_executavel,
            text="Selecionar",
            font=FONTE_PEQUENA_BOLD,
            fg_color=CINZA,
            hover_color=CINZA_HOVER,
            width=80,
            command=self.selecionar_executavel
        )

        botao_selecionar.pack(
            side="left"
        )


        # Salvar

        frame_botoes = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        frame_botoes.grid(
            row=10,
            column=0,
            pady=30
        )

        ctk.CTkButton(
            frame_botoes,
            text="← Voltar",
            text_color=TX_AZUL,
            font=FONTE_NORMAL_BOLD,
            command=self.voltar
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            frame_botoes,
            text="Salvar",
            fg_color=VERDE,
            hover_color=VERDE_HOVER,
            text_color=TX_VERDE,
            font=FONTE_NORMAL_BOLD,
            command=self.salvar_rotina
        ).pack(
            side="left",
            padx=10
        )
        
        self.alterar_periodo("Diario")

    def criar_campos_condicionais(self):

        ctk.CTkLabel(
            self.frame_condicional,
            text="Dia da semana"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )


        self.dia_semana_combo = ctk.CTkComboBox(
            self.frame_condicional,
            values=[
                "Segunda",
                "Terça",
                "Quarta",
                "Quinta",
                "Sexta",
                "Sábado",
                "Domingo"
            ],
            width=300
        )

        self.dia_semana_combo.grid(
            row=1,
            column=0,
            pady=5
        )



        ctk.CTkLabel(
            self.frame_condicional,
            text="Regra mensal"
        ).grid(
            row=2,
            column=0,
            sticky="w"
        )


        self.regra_combo = ctk.CTkComboBox(
            self.frame_condicional,
            values=[
                "Primeiro dia útil",
                "Último dia útil",
                "Dia específico"
            ],
            width=300,
            command=self.alterar_regra
        )

        self.regra_combo.grid(
            row=3,
            column=0,
            pady=5
        )



        ctk.CTkLabel(
            self.frame_condicional,
            text="Dia do mês"
        ).grid(
            row=4,
            column=0,
            sticky="w"
        )


        self.dia_mes_entry = ctk.CTkEntry(
            self.frame_condicional,
            width=300,
            placeholder_text="Ex: 25",
            placeholder_text_color=PLACEHOLDER
        )

        self.dia_mes_entry.grid(
            row=5,
            column=0,
            pady=5
        )
        
    def bloquear_campo(self, campo):

        campo.configure(
            state="disabled"
        )

    def liberar_campo(self, campo):

        campo.configure(
            state="normal"
        )

    def alterar_periodo(self, periodo):

        self.bloquear_campo(self.dia_semana_combo)
        self.bloquear_campo(self.regra_combo)
        self.bloquear_campo(self.dia_mes_entry)


        if periodo == "Semanal":

            self.liberar_campo(
                self.dia_semana_combo
            )


        elif periodo == "Mensal":

            self.liberar_campo(
                self.regra_combo
            )

            self.alterar_regra(
                self.regra_combo.get()
            )

    def alterar_regra(self, regra):

        self.bloquear_campo(
            self.dia_mes_entry
        )


        if regra == "Dia específico":

            self.liberar_campo(
                self.dia_mes_entry
            )

    def voltar(self):
        self.app.trocar_tela("principal")

    def destacar_erro(self, campo):
        campo.configure(border_color="#E53935")

    def limpar_erros(self):

        cor_padrao = ("#979DA2", "#565B5E")  # borda padrão do CTk

        campos = [
            self.nome_entry,
            self.hora_entry,
            self.executavel_entry,
            self.dia_semana_combo,
            self.regra_combo,
            self.dia_mes_entry
        ]

        for campo in campos:
            campo.configure(border_color=cor_padrao)

    def validar_campos(self):

        self.limpar_erros()

        nome = self.nome_entry.get().strip()
        hora = self.hora_entry.get().strip()
        executavel = self.executavel_entry.get().strip()
        periodo = self.periodicidade_combo.get()

        # Nome
        if not nome:
            self.destacar_erro(self.nome_entry)
            self.nome_entry.focus()
            return False

        # Horário
        if not hora:
            self.destacar_erro(self.hora_entry)
            self.hora_entry.focus()
            return False

        if not re.fullmatch(r"([01]\d|2[0-3]):([0-5]\d)", hora):
            self.destacar_erro(self.hora_entry)
            self.hora_entry.focus()
            return False

        # Executável
        if executavel:

            if not os.path.exists(executavel):
                self.destacar_erro(self.executavel_entry)
                self.executavel_entry.focus()
                return False

        # Semanal
        if periodo == "Semanal":

            if not self.dia_semana_combo.get():
                self.destacar_erro(self.dia_semana_combo)
                self.dia_semana_combo.focus()
                return False
            

        # Mensal
        elif periodo == "Mensal":

            regra = self.regra_combo.get()

            if not regra:
                self.destacar_erro(self.regra_combo)
                self.regra_combo.focus()
                return False

            if regra == "Dia específico":

                dia = self.dia_mes_entry.get().strip()

                if not dia:
                    self.destacar_erro(self.dia_mes_entry)
                    self.dia_mes_entry.focus()
                    return False

                try:

                    dia = int(dia)

                except ValueError:

                    self.destacar_erro(self.dia_mes_entry)
                    self.dia_mes_entry.focus()
                    return False

                if dia < 1 or dia > 31:
                    self.destacar_erro(self.dia_mes_entry)
                    self.dia_mes_entry.focus()
                    return False

        return True

    def salvar_rotina(self):

        if not self.validar_campos():
            return

        nome = self.nome_entry.get()

        executavel = self.executavel_entry.get()

        periodo_map = {
            "Diario": "DIARIO",
            "Semanal": "SEMANAL",
            "Mensal": "MENSAL"
        }

        periodo = periodo_map[
            self.periodicidade_combo.get()
        ]

        hora = self.hora_entry.get()


        regra_dia = None
        dia_semana = None
        dia_mes = None


        if periodo == "SEMANAL":

            dias_semana = {
                "Segunda": 0,
                "Terça": 1,
                "Quarta": 2,
                "Quinta": 3,
                "Sexta": 4,
                "Sábado": 5,
                "Domingo": 6
            }

            dia_semana = dias_semana[
                self.dia_semana_combo.get()
            ]


        elif periodo == "MENSAL":

            regra = self.regra_combo.get()

            if regra == "Primeiro dia útil":

                regra_dia = "PRIMEIRO_DIA_UTIL"

            elif regra == "Último dia útil":

                regra_dia = "ULTIMO_DIA_UTIL"

            elif regra == "Dia específico":

                regra_dia = "DIA_ESPECIFICO"
                dia_mes = int(self.dia_mes_entry.get())



        if self.id_rotina:

            atualizar_rotina(
                self.id_rotina,
                nome,
                executavel,
                periodo.upper(),
                hora,
                regra_dia,
                dia_semana,
                dia_mes
            )

        else:

            criar_rotina(
                nome.upper(),
                executavel,
                periodo.upper(),
                hora,
                regra_dia,
                dia_semana,
                dia_mes
            )
            
        if self.id_rotina:

            self.app.notificar(
                "Rotina atualizada com sucesso!",
                "sucesso",
                bg_color="#333333"
            )

        else:

            self.app.notificar(
                "Rotina criada com sucesso!",
                "sucesso",
                bg_color="#333333"
            )
        
    def carregar_rotina(self):

        rotina = buscar_rotina(self.id_rotina)

        self.nome_entry.insert(0, rotina["nome"])
        
        if rotina["executavel"]:
            self.executavel_entry.insert(0, rotina["executavel"])

        self.periodicidade_combo.set(
            rotina["periodo"].capitalize()
        )

        self.hora_entry.insert(
            0,
            rotina["hora"]
        )


        if rotina["dia_semana"] is not None:

            dias_semana = {
                0: "Segunda",
                1: "Terça",
                2: "Quarta",
                3: "Quinta",
                4: "Sexta",
                5: "Sábado",
                6: "Domingo"
            }

            self.dia_semana_combo.set(
                dias_semana[rotina["dia_semana"]]
            )
        

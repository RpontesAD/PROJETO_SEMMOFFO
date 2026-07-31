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

    # ------------------------------------------------------------------
    # Ações
    # ------------------------------------------------------------------

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
            self.executavel_entry.insert(0, caminho)

    # ------------------------------------------------------------------
    # Construção da UI
    # ------------------------------------------------------------------

    def criar_widgets(self):
        self.grid_columnconfigure(0, weight=1)

        texto_titulo = "EDITAR ROTINA" if self.id_rotina else "NOVA ROTINA"

        titulo = ctk.CTkLabel(self, text=texto_titulo, font=FONTE_TITULO)
        titulo.grid(row=0, column=0, pady=(30, 20))

        # Container principal: tudo em grid, 2 colunas de mesmo peso
        conteudo = ctk.CTkFrame(self, fg_color="#2b2b2b")
        conteudo.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")
        conteudo.grid_columnconfigure(0, weight=1, uniform="col")
        conteudo.grid_columnconfigure(1, weight=1, uniform="col")

        PAD_LABEL = (0, 10)
        PAD_CAMPO = (0, 15)
        
        self.ALTURA_CAMPO = 40

        # --- Linha 0: Nome (ocupa as duas colunas) --------------------
        ctk.CTkLabel(
            conteudo, text="Nome da rotina", font=FONTE_NORMAL_BOLD
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=30, pady=(20, 10))

        self.nome_entry = ctk.CTkEntry(conteudo, height=self.ALTURA_CAMPO)
        self.nome_entry.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=30, pady=PAD_CAMPO
        )

        # --- Linha 2: Periodicidade | Horário --------------------------
        ctk.CTkLabel(
            conteudo, text="Periodicidade", font=FONTE_NORMAL_BOLD
        ).grid(row=2, column=0, sticky="w", padx=30, pady=PAD_LABEL)

        ctk.CTkLabel(
            conteudo, text="Horário", font=FONTE_NORMAL_BOLD
        ).grid(row=2, column=1, sticky="w", padx=30, pady=PAD_LABEL)

        self.periodicidade_combo = ctk.CTkComboBox(
            conteudo,
            height=self.ALTURA_CAMPO,
            values=["Diario", "Semanal", "Mensal"],
            command=self.alterar_periodo
        )
        self.periodicidade_combo.grid(
            row=3, column=0, sticky="ew", padx=(30, 0), pady=PAD_CAMPO
        )

        self.hora_entry = ctk.CTkEntry(
            conteudo,
            height=self.ALTURA_CAMPO,
            placeholder_text="08:00",
            placeholder_text_color=PLACEHOLDER
        )
        self.hora_entry.grid(
            row=3, column=1, sticky="ew", padx=30, pady=PAD_CAMPO
        )

        # --- Linha 4: Executável (ocupa as duas colunas) ---------------
        ctk.CTkLabel(
            conteudo, text="Executável (opcional)", font=FONTE_NORMAL_BOLD
        ).grid(row=4, column=0, columnspan=2, sticky="w", padx=30, pady=PAD_LABEL)

        frame_executavel = ctk.CTkFrame(conteudo, fg_color="transparent")
        frame_executavel.grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=PAD_CAMPO
        )
        frame_executavel.grid_columnconfigure(0, weight=1)

        self.executavel_entry = ctk.CTkEntry(frame_executavel, height=self.ALTURA_CAMPO)
        self.executavel_entry.grid(row=0, column=0, sticky="ew", padx=(30, 0))

        ctk.CTkButton(
            frame_executavel,
            text="Selecionar",
            font=FONTE_PEQUENA_BOLD,
            fg_color=CINZA,
            hover_color=CINZA_HOVER,
            width=90,
            command=self.selecionar_executavel
        ).grid(row=0, column=1, padx=30)

        # --- Linha 6: área condicional (dia da semana / regra mensal) --
        self.frame_condicional = ctk.CTkFrame(conteudo, fg_color="transparent")
        self.frame_condicional.grid(
            row=6, column=0, columnspan=2, sticky="ew", pady=(5, 0)
        )
        self.frame_condicional.grid_columnconfigure(0, weight=1)

        self.criar_campos_condicionais()

        # --- Linha 7: botões --------------------------------------------
        frame_botoes = ctk.CTkFrame(conteudo, fg_color="transparent")
        frame_botoes.grid(row=7, column=0, columnspan=2, pady=25)

        ctk.CTkButton(
            frame_botoes,
            text="←",
            text_color=TX_AZUL,
            font=FONTE_NORMAL_BOLD,
            width=40,
            command=self.voltar
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            frame_botoes,
            text="Salvar",
            fg_color=VERDE,
            hover_color=VERDE_HOVER,
            text_color=TX_VERDE,
            font=FONTE_NORMAL_BOLD,
            command=self.salvar_rotina
        ).grid(row=0, column=1, padx=10)

        self.alterar_periodo("Diario")

    def criar_campos_condicionais(self):
        PAD_LABEL = (10, 5)
        PAD_CAMPO = (0, 10)

        ctk.CTkLabel(
            self.frame_condicional, text="Dia da semana", font=FONTE_NORMAL_BOLD
        ).grid(row=0, column=0, sticky="w", padx=30, pady=PAD_LABEL)

        self.dia_semana_combo = ctk.CTkComboBox(
            self.frame_condicional,
            height=self.ALTURA_CAMPO,
            values=["Segunda", "Terça", "Quarta", "Quinta",
                    "Sexta", "Sábado", "Domingo"]
        )
        self.dia_semana_combo.grid(row=1, column=0, sticky="ew", padx=30, pady=PAD_CAMPO)

        ctk.CTkLabel(
            self.frame_condicional, text="Regra mensal", font=FONTE_NORMAL_BOLD
        ).grid(row=2, column=0, sticky="w", padx=30, pady=PAD_LABEL)

        self.regra_combo = ctk.CTkComboBox(
            self.frame_condicional,
            height=self.ALTURA_CAMPO,
            values=["Primeiro dia útil", "Último dia útil", "Dia específico"],
            command=self.alterar_regra
        )
        self.regra_combo.grid(row=3, column=0, sticky="ew", padx=30, pady=PAD_CAMPO)

        ctk.CTkLabel(
            self.frame_condicional, text="Dia do mês", font=FONTE_NORMAL_BOLD
        ).grid(row=4, column=0, sticky="w", padx=30, pady=PAD_LABEL)

        self.dia_mes_entry = ctk.CTkEntry(
            self.frame_condicional,
            height=self.ALTURA_CAMPO,
            placeholder_text="Ex: 25",
            placeholder_text_color=PLACEHOLDER
        )
        self.dia_mes_entry.grid(row=5, column=0, sticky="ew", padx=30, pady=PAD_CAMPO)

    # ------------------------------------------------------------------
    # Regras de habilitação de campos
    # ------------------------------------------------------------------

    def bloquear_campo(self, campo):
        campo.configure(state="disabled")

    def liberar_campo(self, campo):
        campo.configure(state="normal")

    def alterar_periodo(self, periodo):
        self.bloquear_campo(self.dia_semana_combo)
        self.bloquear_campo(self.regra_combo)
        self.bloquear_campo(self.dia_mes_entry)

        if periodo == "Semanal":
            self.liberar_campo(self.dia_semana_combo)

        elif periodo == "Mensal":
            self.liberar_campo(self.regra_combo)
            self.alterar_regra(self.regra_combo.get())

    def alterar_regra(self, regra):
        self.bloquear_campo(self.dia_mes_entry)

        if regra == "Dia específico":
            self.liberar_campo(self.dia_mes_entry)

    def voltar(self):
        self.app.trocar_tela("principal")

    # ------------------------------------------------------------------
    # Validação
    # ------------------------------------------------------------------

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

        if not nome:
            self.destacar_erro(self.nome_entry)
            self.nome_entry.focus()
            return False

        if not hora:
            self.destacar_erro(self.hora_entry)
            self.hora_entry.focus()
            return False

        if not re.fullmatch(r"([01]\d|2[0-3]):([0-5]\d)", hora):
            self.destacar_erro(self.hora_entry)
            self.hora_entry.focus()
            return False

        if executavel:
            if not os.path.exists(executavel):
                self.destacar_erro(self.executavel_entry)
                self.executavel_entry.focus()
                return False

        if periodo == "Semanal":
            if not self.dia_semana_combo.get():
                self.destacar_erro(self.dia_semana_combo)
                self.dia_semana_combo.focus()
                return False

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

    # ------------------------------------------------------------------
    # Persistência
    # ------------------------------------------------------------------

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
        periodo = periodo_map[self.periodicidade_combo.get()]
        hora = self.hora_entry.get()

        regra_dia = None
        dia_semana = None
        dia_mes = None

        if periodo == "SEMANAL":
            dias_semana = {
                "Segunda": 0, "Terça": 1, "Quarta": 2, "Quinta": 3,
                "Sexta": 4, "Sábado": 5, "Domingo": 6
            }
            dia_semana = dias_semana[self.dia_semana_combo.get()]

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
                self.id_rotina, nome.upper(), executavel, periodo.upper(),
                hora, regra_dia, dia_semana, dia_mes
            )
            self.app.notificar(
                "Rotina atualizada com sucesso!", "sucesso", bg_color="#333333"
            )
        else:
            criar_rotina(
                nome.upper(), executavel, periodo.upper(),
                hora, regra_dia, dia_semana, dia_mes
            )
            self.app.notificar(
                "Rotina criada com sucesso!", "sucesso", bg_color="#333333"
            )

    def carregar_rotina(self):
        rotina = buscar_rotina(self.id_rotina)

        self.nome_entry.insert(0, rotina["nome"])

        if rotina["executavel"]:
            self.executavel_entry.insert(0, rotina["executavel"])

        self.periodicidade_combo.set(rotina["periodo"].capitalize())
        self.hora_entry.insert(0, rotina["hora"])

        if rotina["dia_semana"] is not None:
            dias_semana = {
                0: "Segunda", 1: "Terça", 2: "Quarta", 3: "Quinta",
                4: "Sexta", 5: "Sábado", 6: "Domingo"
            }
            self.dia_semana_combo.set(dias_semana[rotina["dia_semana"]])
import customtkinter as ctk

class CardRotina(ctk.CTkFrame):

    def __init__(self, master, resultado, on_inativar=None, on_editar=None):
        super().__init__(master)
        
        self.on_inativar = on_inativar
        self.on_editar = on_editar

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
            status = "⚪ Sem monitoramentos"
            nome_arquivo = "-"
            data_modificacao = "-"

        titulo = ctk.CTkLabel(
            self,
            text=nome,
            font=("Arial", 18, "bold")
        )

        titulo.pack(anchor="w", padx=15, pady=(10, 5))

        info = ctk.CTkLabel(
            self,
            text=f"""
Status: {status}

Monitoramentos: {quantidade}
Periodicidade: {periodicidade}

Arquivo: {nome_arquivo}
Última modificação: {data_modificacao}
"""
        )

        info.pack(anchor="w", padx=15)

        botoes = ctk.CTkFrame(self)
        botoes.pack(anchor="e", padx=15, pady=10)

        ctk.CTkButton(
            botoes, text="Visualizar",
            fg_color="#2E8B57",      # Verde
            hover_color="#256F46",   # Verde mais escuro
            text_color="white"
            ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            botoes, text="Mostrar Pasta",
            fg_color="#555555",
            hover_color="#444444"
            ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            botoes,
            text="Editar",
            command=self.editar
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            botoes, text="Inativar",
            fg_color="#D32F2F",
            hover_color="#B71C1C",
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

        botoes = ctk.CTkFrame(self)
        botoes.pack(anchor="e", padx=15, pady=10)

        ctk.CTkButton(
            botoes,
            text="Restaurar",
            fg_color="#2E8B57",
            hover_color="#256F46",
            command=self.restaurar
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            botoes,
            text="Excluir",
            fg_color="#D32F2F",
            hover_color="#B71C1C",
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
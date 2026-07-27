import customtkinter as ctk

class CardRotina(ctk.CTkFrame):

    def __init__(self, master, resultado):
        super().__init__(master)

        id_rotina = resultado["id"]
        nome = resultado["nome"]
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

        ctk.CTkButton(botoes, text="Editar").pack(side="left", padx=5)
        ctk.CTkButton(botoes, text="Excluir").pack(side="left", padx=5)
        ctk.CTkButton(botoes, text="Mostrar Pasta").pack(side="left", padx=5)
        ctk.CTkButton(botoes, text="Atualizar").pack(side="left", padx=5)
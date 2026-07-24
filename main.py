import customtkinter as ctk
from database import criar_tabelas, listar_rotinas, contar_monitoramentos

ctk.set_appearance_mode("System")   # System, Dark ou Light
ctk.set_default_color_theme("blue") # blue, dark-blue ou green


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SEMMOFFO APP")
        self.geometry("1200x700")

        self.criar_widgets()
        
    def carregar_rotinas(self):

        # limpa os cards antigos
        for widget in self.lista_rotinas.winfo_children():
            widget.destroy()

        rotinas = listar_rotinas()

        for rotina in rotinas:
            self.criar_card_rotina(rotina)
        
    def criar_card_rotina(self, rotina):
        
        id_rotina = rotina[0]
        nome = rotina[1]
        executavel = rotina[2]
        periodicidade = rotina[3]
        intervalo = rotina[4]
    
        card = ctk.CTkFrame(
            self.lista_rotinas
        )

        card.pack(
            fill="x",
            padx=10,
            pady=10
        )


        titulo = ctk.CTkLabel(
            card,
            text=nome,
            font=("Arial", 18, "bold")
        )

        titulo.pack(
            anchor="w",
            padx=15,
            pady=(10,5)
        )
        
        quantidade = contar_monitoramentos(id_rotina)

        info = ctk.CTkLabel(
            card,
            text=f"""
        Status: 🟡 Aguardando verificação

        Monitoramentos: {quantidade}
        Periodicidade: {periodicidade}
        """
        )

        info.pack(
            anchor="w",
            padx=15
        )


        botoes = ctk.CTkFrame(card)

        botoes.pack(
            anchor="e",
            padx=15,
            pady=10
        )


        ctk.CTkButton(
            botoes,
            text="Editar"
        ).pack(
            side="left",
            padx=5
        )


        ctk.CTkButton(
            botoes,
            text="Excluir"
        ).pack(
            side="left",
            padx=5
        )


        ctk.CTkButton(
            botoes,
            text="Mostrar Pasta"
        ).pack(
            side="left",
            padx=5
        )


        ctk.CTkButton(
            botoes,
            text="Atualizar"
        ).pack(
            side="left",
            padx=5
        )


    def criar_widgets(self):

        topo = ctk.CTkFrame(self)
        topo.pack(fill="x", padx=15, pady=15)

        titulo = ctk.CTkLabel(
            topo,
            text="SEMMOFFO - Monitor de Rotinas",
            font=("Arial", 24, "bold")
        )

        titulo.pack(side="left", padx=15, pady=15)


        botao_adicionar = ctk.CTkButton(
            topo,
            text="Adicionar"
        )

        botao_adicionar.pack(side="right", padx=5)


        self.lista_rotinas = ctk.CTkScrollableFrame(self)
        

        self.lista_rotinas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0,15)
        )
        
        self.carregar_rotinas()

if __name__ == "__main__":
    app = App()
    app.mainloop()
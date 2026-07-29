import customtkinter as ctk
from ui.tela_principal import TelaPrincipal
from ui.tela_cadastro_rotina import TelaCadastro
from ui.tela_cadastro_monitoramento import TelaCadastroMonitoramento
from ui.tela_inativas import TelaInativas
from ui.tela_detalhes import TelaDetalhes



class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        
        self.telas = {
            "principal": TelaPrincipal,
            "cadastro": TelaCadastro,
            "inativas": TelaInativas,
            "detalhes": TelaDetalhes,
            "cadastro_monitoramento": TelaCadastroMonitoramento
        }
        
        self.title("SEMMOFFO - Monitor de Rotinas")
        self.geometry("950x850")

        self.container = ctk.CTkFrame(self)
        self.container.pack(
            fill="both",
            expand=True
        )

        self.mostrar_tela_principal()


    def trocar_tela(self, nome_tela, **kwargs):

        for widget in self.container.winfo_children():
            widget.destroy()

        tela = self.telas[nome_tela]

        nova_tela = tela(
            self.container,
            self,
            **kwargs
        )

        nova_tela.pack(
            fill="both",
            expand=True
        )

    def mostrar_tela_principal(self):
        self.trocar_tela("principal")
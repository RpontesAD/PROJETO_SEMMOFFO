import customtkinter as ctk
from ui.tela_principal import TelaPrincipal
from ui.tela_cadastro_rotina import TelaCadastro
from ui.tela_cadastro_monitoramento import TelaCadastroMonitoramento
from ui.tela_inativas import TelaInativas
from ui.tela_detalhes import TelaDetalhes
from ui.componentes import Notificacao



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

        self.notificacoes = []
        
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

    def notificar(self, mensagem, tipo="info", bg_color=None):

        notificacao = Notificacao(
            self,
            mensagem,
            tipo,
            bg_color=bg_color
        )

        largura = 350
        altura = 75
        margem = 35

        indice = len(self.notificacoes)

        y = self.winfo_height() - margem - altura - indice * (altura + 10)

        notificacao.place(
            relx=1,
            x=-margem,
            y=y,
            anchor="ne",
        )

        self.notificacoes.append(notificacao)

        self.after(
            3000,
            lambda: self.remover_notificacao(notificacao)
    )

    def remover_notificacao(self, notificacao):

        if notificacao in self.notificacoes:
            self.notificacoes.remove(notificacao)

        notificacao.destroy()

        largura = 350
        altura = 55
        margem = 20

        for i, notif in enumerate(self.notificacoes):

            y = self.winfo_height() - margem - altura - i * (altura + 10)

            notif.place_configure(
                y=y
            )
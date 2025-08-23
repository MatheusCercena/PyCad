from pathlib import Path
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout

from widgets.elementos_main import linha_separadora, menu_etapas
from widgets.vaos import VaosWidget
from widgets.sentidos_abertura import SentidosAberturaWidget
from widgets.resumo import ResumoWidget

ETAPAS_NOMES = [
    'Vãos',
    'Sentidos de Abertura',
    'Resumo'
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dados_sacada = []

        self.setWindowTitle('SPEV - SISTEMA PARA PROJETOS DE ENVIDRAÇAMENTO VERSATEEL')
        self.setGeometry(100, 100, 900, 700)
        self.showMaximized()  # Abrir em tela cheia

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_ = QVBoxLayout(self.central_widget)

        self.menu_etapas = menu_etapas(ETAPAS_NOMES, self.ir_para_etapa)
        self.separador = linha_separadora()
        self.stack = QStackedWidget()

        self.layout_.addLayout(self.menu_etapas)
        self.layout_.addWidget(self.separador)
        self.layout_.addWidget(self.stack)

        self.etapa_atual = 0
        self.iniciar_etapas()
        self.atualizar_estados()

    def iniciar_etapas(self):
        self.vaos_widget = VaosWidget()
        self.sentidos_widget = SentidosAberturaWidget()
        self.resumo_widget = ResumoWidget()

        self.etapas = [
            self.vaos_widget,
            self.sentidos_widget,
            self.resumo_widget
        ]

        for widget in self.etapas:
            self.stack.addWidget(widget)

        self.stack.setCurrentIndex(0)

    def atualizar_estados(self):
        self.stack.setCurrentIndex(self.etapa_atual)
        self.menu_etapas.atualizar_estado_menu_etapas(self.etapa_atual)

    def ir_para_etapa(self, etapa_idx):
        """Navega diretamente para uma etapa específica"""
        if etapa_idx == self.etapa_atual:
            return
        self.etapa_atual = etapa_idx
        self.atualizar_dados_etapa_atual()
        self.atualizar_estados()

    def atualizar_dados_etapa_atual(self):
        """Atualiza os dados da etapa atual baseado nas dependências"""
        dados = self.vaos_widget.get_dados_vaos()

        # if self.etapa_atual == 1:

        # elif self.etapa_atual == 2:

    def passar_dados_para_proxima_etapa(self):
        """Passa os dados para a próxima etapa conforme necessário"""
        if self.etapa_atual == 0:
            quant_vidros = self.vaos_widget.get_quantidade_vidros()
            lcs = self.vaos_widget.get_linhas_centro()
            # self.ang_secoes_widget.lcs = lcs
            # self.ang_secoes_widget.angulos = []
            # self.ang_secoes_widget.update_list()

        elif self.etapa_atual == 1:
            self.sentidos_widget.sentidos = []
            # Coletar todos os dados e exibir no resumo
            dados = {
                # 'linhas_de_centro': self.vaos_widget.get_linhas_centro(),
                # 'alturas': self.vaos_widget.get_alturas(),
                # 'niveis': self.vaos_widget.get_niveis(),
                # 'quantidade_vidros': self.vaos_widget.get_quantidade_vidros(),
                # 'sentidos_abertura': self.sentidos_widget.get_sentidos(),
                # 'angulos_secoes': self.vaos_widget.get_angulos(),
                # 'angulos_paredes': self.vaos_widget.get_angulos(),
                # 'elevador': self.vaos_widget.get_elevador()
            }
            self.resumo_widget.set_dados(dados)

    def avancar_etapa(self):
        """Avança para a próxima etapa"""
        if self.etapa_atual < len(self.etapas) - 1:
            self.etapa_atual += 1
            self.atualizar_dados_etapa_atual()
            self.atualizar_estados()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Path("UI/styles.qss").read_text(encoding="utf-8"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
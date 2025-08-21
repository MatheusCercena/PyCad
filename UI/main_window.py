from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QFrame, QMessageBox
import sys
from PyQt6.QtCore import Qt
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
        self.setWindowTitle('SPEV - SISTEMA PARA PROJETOS DE ENVIDRAÇAMENTO VERSATEEL')
        self.setGeometry(100, 100, 900, 700)
        self.showMaximized()  # Abrir em tela cheia

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Menu superior de etapas
        self.menu_etapas = QHBoxLayout()
        self.etapa_labels = []
        for i, nome in enumerate(ETAPAS_NOMES):
            label = QLabel(nome)
            label.setObjectName(f'etapa_{i}')
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.mousePressEvent = lambda event, idx=i: self.ir_para_etapa(idx)
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            self.etapa_labels.append(label)
            self.menu_etapas.addWidget(label)
            if i < len(ETAPAS_NOMES) - 1:
                seta = QLabel('→')
                seta.setAlignment(Qt.AlignmentFlag.AlignCenter)
                seta.setStyleSheet('color: #888; font-size: 18px;')
                self.menu_etapas.addWidget(seta)
        self.layout.addLayout(self.menu_etapas)

        # Linha separadora
        linha = QFrame()
        linha.setFrameShape(QFrame.Shape.HLine)
        linha.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(linha)

        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # Botão Anterior
        self.btn_prev = QPushButton('Anterior')
        self.btn_prev.setFixedHeight(35)
        self.btn_prev.clicked.connect(self.go_prev)

        # Botão Próximo
        self.btn_next = QPushButton('Próximo')
        self.btn_next.setFixedHeight(35)
        self.btn_next.clicked.connect(self.go_next)

        # Adicionando botões ao layout
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.btn_next)
        self.layout.addLayout(nav_layout)

        self.current_step = 0
        self.init_steps()
        self.atualizar_estado_nav_buttons()
        self.atualizar_estado_menu_etapas()

    def init_steps(self):
        self.vaos_widget = VaosWidget()
        self.sentidos_widget = SentidosAberturaWidget()
        self.resumo_widget = ResumoWidget()

        self.steps = [
            self.vaos_widget, # 0
            self.sentidos_widget, # 1
            self.resumo_widget # 2
        ]
        for widget in self.steps:
            self.stack.addWidget(widget)
        self.stack.setCurrentIndex(0)

    def ir_para_etapa(self, etapa_idx):
        """Navega diretamente para uma etapa específica"""
        if etapa_idx == self.current_step:
            return  # Já está na etapa

        # Sempre permite navegar para qualquer etapa
        self.current_step = etapa_idx
        self.stack.setCurrentIndex(self.current_step)

        self.atualizar_etapa_atual()
        self.atualizar_estado_nav_buttons()
        self.atualizar_estado_menu_etapas()

    def atualizar_etapa_atual(self):
        """Atualiza os dados da etapa atual baseado nas dependências"""
        if self.current_step == 1:  # Sentidos de Abertura
            # quant_vidros = self.vaos_widget.get_quantidade_vidros()
            # if quant_vidros:
            #     # Preservar sentidos existentes se já existem
            #     sentidos_existentes = self.sentidos_widget.get_sentidos()
            #     if not sentidos_existentes:  # Só resetar se não há dados
            #         self.sentidos_widget.quant_vidros = quant_vidros
            #         self.sentidos_widget.sentidos = []
            #         self.sentidos_widget.update_list()
            pass
        elif self.current_step == 2:  # Resumo
            # Atualizar resumo com dados atuais
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

    def atualizar_estado_nav_buttons(self):
        self.btn_prev.setEnabled(self.current_step > 0)
        self.btn_next.setEnabled(self.current_step < len(self.steps) - 1)

    def atualizar_estado_menu_etapas(self):
        for i, label in enumerate(self.etapa_labels):
            if i == self.current_step:
                label.setStyleSheet('background: #d0eaff; border-radius: 6px; font-weight: bold; color: #005080; font-size: 16px; padding: 4px 8px;')
            else:
                # Todas as outras etapas são clicáveis
                label.setStyleSheet('color: #888; font-size: 14px; padding: 4px 8px; cursor: pointer;')

    def go_prev(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.stack.setCurrentIndex(self.current_step)
            self.atualizar_etapa_atual()
            self.update_nav_buttons()
            self.update_menu_etapas()

    def go_next(self):
        # Verificar se há dados necessários na página atual
        if self.current_step == 0:  # Vãos
            # Verificar se há pelo menos um vão com dados
            lcs = self.vaos_widget.get_linhas_centro()
            if not lcs:
                QMessageBox.warning(self, 'Aviso', 'Adicione pelo menos uma linha de centro em um vão.')
                return
            self.passar_dados_para_proxima_etapa()
            self.avancar_etapa()
        elif self.current_step == 1:  # Sentidos de Abertura
            # Sentidos não tem validação específica, avança direto
            self.passar_dados_para_proxima_etapa()
            self.avancar_etapa()
        elif self.current_step == 5:  # Resumo
            pass  # Última etapa

    def passar_dados_para_proxima_etapa(self):
        """Passa os dados para a próxima etapa conforme necessário"""
        if self.current_step == 0:
            quant_vidros = self.vaos_widget.get_quantidade_vidros()
            lcs = self.vaos_widget.get_linhas_centro()
            # self.ang_secoes_widget.lcs = lcs
            # self.ang_secoes_widget.angulos = []
            # self.ang_secoes_widget.update_list()

        elif self.current_step == 1:
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
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.stack.setCurrentIndex(self.current_step)
            self.atualizar_etapa_atual()
            self.update_nav_buttons()
            self.update_menu_etapas()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Estilo global reduzido para interface mais compacta
    app.setStyleSheet('''
        QWidget { font-size: 16px; }
        QLineEdit, QComboBox, QListWidget, QTextEdit { font-size: 16px;}
        QPushButton { font-size: 16px; min-width: 90px; padding: 6px; }
        QLabel { font-size: 18px; font-weight: bold; }
        QFrame { margin: 2px; padding: 2px; }
        QHBoxLayout, QVBoxLayout { margin: 4px; spacing: 4px; }
    ''')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QFrame, QMessageBox
import sys
from PyQt6.QtCore import Qt
from widgets.vaos import VaosWidget
from widgets.sentidos_abertura import SentidosAberturaWidget
from widgets.ang_secoes import AngSecoesWidget
from widgets.ang_paredes import AngParedesWidget
from widgets.elevador import ElevadorWidget
from widgets.resumo import ResumoWidget

ETAPAS_NOMES = [
    'Vãos',
    'Sentidos de Abertura',
    'Ângulos Seções',
    'Ângulos Paredes',
    'Elevador',
    'Resumo'
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyCad - Interface Gráfica')
        self.setGeometry(100, 100, 900, 700)
        self.showMaximized()  # Abrir em tela cheia

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Menu superior de etapas
        self.menu_etapas = QHBoxLayout()
        self.etapa_labels = []
        for i, nome in enumerate(ETAPAS_NOMES):
            lbl = QLabel(nome)
            lbl.setObjectName(f'etapa_{i}')
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.mousePressEvent = lambda event, idx=i: self.ir_para_etapa(idx)
            lbl.setCursor(Qt.CursorShape.PointingHandCursor)
            self.etapa_labels.append(lbl)
            self.menu_etapas.addWidget(lbl)
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

        # Navegação inferior
        nav_layout = QHBoxLayout()
        self.btn_prev = QPushButton('Anterior')
        self.btn_next = QPushButton('Próximo')
        self.btn_prev.setFixedHeight(35)
        self.btn_next.setFixedHeight(35)
        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.btn_next)
        self.layout.addLayout(nav_layout)

        # Etapas reais
        self.current_step = 0
        self.init_steps()
        self.setup_sync_connections()
        self.update_nav_buttons()
        self.update_menu_etapas()

        self.btn_prev.clicked.connect(self.go_prev)
        self.btn_next.clicked.connect(self.go_next)

    def init_steps(self):
        self.vaos_widget = VaosWidget()
        self.sentidos_widget = SentidosAberturaWidget()
        self.ang_secoes_widget = AngSecoesWidget()
        self.ang_paredes_widget = AngParedesWidget()
        self.elevador_widget = ElevadorWidget()
        self.resumo_widget = ResumoWidget()

        self.steps = [
            self.vaos_widget,         # 0
            self.sentidos_widget,      # 1
            self.ang_secoes_widget,    # 2
            self.ang_paredes_widget,   # 3
            self.elevador_widget,      # 4
            self.resumo_widget         # 5
        ]
        for w in self.steps:
            self.stack.addWidget(w)
        self.stack.setCurrentIndex(0)

    def setup_sync_connections(self):
        """Configura as conexões para sincronização automática entre widgets"""
        # Conectar mudanças nos vãos para sincronizar outros widgets
        # (Implementar quando necessário)

    def ir_para_etapa(self, etapa_idx):
        """Navega diretamente para uma etapa específica"""
        if etapa_idx == self.current_step:
            return  # Já está na etapa
        
        # Sempre permite navegar para qualquer etapa
        self.current_step = etapa_idx
        self.stack.setCurrentIndex(self.current_step)
        
        # Atualizar dados da etapa atual
        self.atualizar_etapa_atual()
        
        self.update_nav_buttons()
        self.update_menu_etapas()

    def atualizar_etapa_atual(self):
        """Atualiza os dados da etapa atual baseado nas dependências"""
        if self.current_step == 1:  # Sentidos de Abertura
            quant_vidros = self.vaos_widget.get_quantidade_vidros()
            if quant_vidros:
                # Preservar sentidos existentes se já existem
                sentidos_existentes = self.sentidos_widget.get_sentidos()
                if not sentidos_existentes:  # Só resetar se não há dados
                    self.sentidos_widget.quant_vidros = quant_vidros
                    self.sentidos_widget.sentidos = []
                    self.sentidos_widget.update_list()
        elif self.current_step == 2:  # Ângulos das Seções
            lcs = self.vaos_widget.get_linhas_centro()
            if lcs:
                # Preservar ângulos existentes se já existem
                angulos_existentes = self.ang_secoes_widget.get_angulos()
                if not angulos_existentes:  # Só resetar se não há dados
                    self.ang_secoes_widget.lcs = lcs
                    self.ang_secoes_widget.angulos = []
                    self.ang_secoes_widget.update_list()
        elif self.current_step == 5:  # Resumo
            # Atualizar resumo com dados atuais
            dados = {
                'linhas_de_centro': self.vaos_widget.get_linhas_centro(),
                'alturas': self.vaos_widget.get_alturas(),
                'niveis': self.vaos_widget.get_niveis(),
                'quantidade_vidros': self.vaos_widget.get_quantidade_vidros(),
                'sentidos_abertura': self.sentidos_widget.get_sentidos(),
                'angulos_secoes': self.ang_secoes_widget.get_angulos(),
                'angulos_paredes': self.ang_paredes_widget.get_angulos(),
                'elevador': self.elevador_widget.get_elevador()
            }
            self.resumo_widget.set_dados(dados)

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
        elif self.current_step == 2:  # Ângulos das Seções
            # Ângulos não tem validação específica, avança direto
            self.passar_dados_para_proxima_etapa()
            self.avancar_etapa()
        elif self.current_step == 3:  # Ângulos das Paredes
            # Ângulos das paredes não tem validação específica, avança direto
            self.passar_dados_para_proxima_etapa()
            self.avancar_etapa()
        elif self.current_step == 4:  # Elevador
            # Elevador não tem validação específica, avança direto
            self.passar_dados_para_proxima_etapa()
            self.avancar_etapa()
        elif self.current_step == 5:  # Resumo
            pass  # Última etapa

    def passar_dados_para_proxima_etapa(self):
        """Passa os dados para a próxima etapa conforme necessário"""
        if self.current_step == 0:
            # Vãos já contém todos os dados necessários
            pass
        elif self.current_step == 1:
            quant_vidros = self.vaos_widget.get_quantidade_vidros()
            self.sentidos_widget.quant_vidros = quant_vidros
            self.sentidos_widget.sentidos = []
            self.sentidos_widget.update_list()
        elif self.current_step == 2:
            lcs = self.vaos_widget.get_linhas_centro()
            self.ang_secoes_widget.lcs = lcs
            self.ang_secoes_widget.angulos = []
            self.ang_secoes_widget.update_list()
        elif self.current_step == 3:
            pass  # Ângulos das paredes não afetam widgets seguintes
        elif self.current_step == 4:
            # Coletar todos os dados e exibir no resumo
            dados = {
                'linhas_de_centro': self.vaos_widget.get_linhas_centro(),
                'alturas': self.vaos_widget.get_alturas(),
                'niveis': self.vaos_widget.get_niveis(),
                'quantidade_vidros': self.vaos_widget.get_quantidade_vidros(),
                'sentidos_abertura': self.sentidos_widget.get_sentidos(),
                'angulos_secoes': self.ang_secoes_widget.get_angulos(),
                'angulos_paredes': self.ang_paredes_widget.get_angulos(),
                'elevador': self.elevador_widget.get_elevador()
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

    def update_nav_buttons(self):
        self.btn_prev.setEnabled(self.current_step > 0)
        self.btn_next.setEnabled(self.current_step < len(self.steps) - 1)

    def update_menu_etapas(self):
        for i, lbl in enumerate(self.etapa_labels):
            if i == self.current_step:
                lbl.setStyleSheet('background: #d0eaff; border-radius: 6px; font-weight: bold; color: #005080; font-size: 16px; padding: 4px 8px;')
            else:
                # Todas as outras etapas são clicáveis
                lbl.setStyleSheet('color: #888; font-size: 14px; padding: 4px 8px; cursor: pointer;')

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
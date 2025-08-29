from PyQt6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QRegularExpression

from UI.vao_frame_widgets import HeaderLayout, LinhaCentroLayout, QuantidadeVidrosLayout, AngulosLayout, VaoFrame, Layout_Frame, BotaoAdicionarAlturas
from UI.elementos_main import linha_separadora

regex = QRegularExpression(r"^(?:\d{1,2}(?:\.\d)?|1[0-7]\d(?:\.\d)?|179(?:\.[0-9])?)$")
validator = QRegularExpressionValidator(regex)

ALTURA_FIXA = 40
LARGURA_FIXA = 100

class VaoWidget(QWidget):
    def __init__(self, numeracao_vao, parent_widget):
        super().__init__()
        self.numeracao_vao = numeracao_vao
        self.parent_widget = parent_widget
        self.titulo = ''
        self.alturas = []
        self.niveis = []
        self.quant_vidros = []
        self.angs = []
        self.juncoes = []
        self.linha_layouts = []

        self.interface_vao()

    def interface_vao(self):
        self.header_layout = HeaderLayout(self.numeracao_vao, self.remover_vao)
        self.titulo = self.header_layout.titulo_vao
        self.linhas_centro_layout = LinhaCentroLayout()
        self.quant_vidos_layout = QuantidadeVidrosLayout()
        self.angulos_layout = AngulosLayout(self)
        self.juncoes_layout = JuncoesLayout(self)
        self.prumos_layout = PrumosLayout(self)

        if self.numeracao_vao > 1:
            angulo_direito_anterior = self.parent_widget.vaos[self.numeracao_vao-2].angulos_layout.input_ang_dir.text()
            angulo_direito_anterior = float(angulo_direito_anterior) if angulo_direito_anterior else 0.0
            self.angulos_layout.input_ang_es.setReadOnly(False)
            self.angulos_layout.input_ang_es.setText(str(angulo_direito_anterior))
            self.angulos_layout.input_ang_es.setReadOnly(True)

        self.botao_add_altura = BotaoAdicionarAlturas(self.adicionar_altura)
        self.alturas_container = QVBoxLayout()

        self.frame = Layout_Frame()

        self.vao_layout = VaoFrame()
        self.vao_layout.addLayout(self.header_layout)
        self.vao_layout.addLayout(self.linhas_centro_layout)
        self.vao_layout.addLayout(self.quant_vidos_layout)
        self.vao_layout.addLayout(self.angulos_layout)
        self.vao_layout.addWidget(self.botao_add_altura)
        self.vao_layout.addLayout(self.alturas_container)

        self.frame.setLayout(self.vao_layout)

        self.separador = linha_separadora()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.frame, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.separador)

    def remover_vao(self):
        self.parent_widget.remover_vao(self.numeracao_vao-1)

    def adicionar_altura(self):
        altura_idx = len(self.alturas)

        lbl_altura = QLabel(f'Altura {altura_idx + 1}:')
        lbl_altura.setFixedWidth(LARGURA_FIXA)
        lbl_altura.setFixedHeight(ALTURA_FIXA)
        lbl_altura.setAlignment(Qt.AlignmentFlag.AlignCenter)

        input_altura = QLineEdit()
        input_altura.setPlaceholderText('Digite a altura')
        input_altura.setFixedWidth(LARGURA_FIXA*2)
        input_altura.setFixedHeight(ALTURA_FIXA)
        input_altura.setValidator(QIntValidator(0, 4000))

        lbl_nivel = QLabel('Nível:')
        lbl_nivel.setFixedWidth(LARGURA_FIXA)
        lbl_nivel.setFixedHeight(ALTURA_FIXA)
        lbl_nivel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        input_nivel = QLineEdit()
        input_nivel.setPlaceholderText('Digite o nível')
        input_nivel.setFixedWidth(LARGURA_FIXA*2)
        input_nivel.setFixedHeight(ALTURA_FIXA)
        input_nivel.setValidator(QIntValidator(0, 4000))

        btn_remove = QPushButton('×')
        btn_remove.setFixedHeight(ALTURA_FIXA)
        btn_remove.setFixedWidth(ALTURA_FIXA)
        btn_remove.setStyleSheet('''
            QPushButton {background-color: #ff4444; color: white; border: 1px solid red; border-radius: 15px; font-weight: bold;font-size: 14px;}
            QPushButton:hover {background-color: #ff6666;}''')
        btn_remove.clicked.connect(lambda: self.remover_altura(altura_idx))

        linha_layout = QHBoxLayout()
        linha_layout.setSpacing(5)
        linha_layout.setContentsMargins(2, 2, 2, 2)
        linha_layout.addWidget(lbl_altura)
        linha_layout.addWidget(input_altura)
        linha_layout.addWidget(lbl_nivel)
        linha_layout.addWidget(input_nivel)
        linha_layout.addWidget(btn_remove)

        self.alturas_container.addLayout(linha_layout)

        self.alturas.append(input_altura)
        self.niveis.append(input_nivel)
        self.linha_layouts.append((linha_layout, lbl_altura))

        self.vao_layout.removeWidget(self.botao_add_altura)
        self.vao_layout.addWidget(self.botao_add_altura)

        self.ajustar_altura_frame()

    def remover_altura(self, idx):
        if idx < len(self.linha_layouts):
            linha_layout  = self.linha_layouts[idx][0]
            while linha_layout.count() > 0:
                item = linha_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)

            self.alturas_container.removeItem(linha_layout)

            self.alturas.pop(idx)
            self.niveis.pop(idx)
            self.linha_layouts.pop(idx)

            for i, (layout, lbl) in enumerate(self.linha_layouts):
                lbl.setText(f'Altura {i + 1}:')

            self.ajustar_altura_frame()

    def ajustar_altura_frame(self):
        """Ajusta a altura mínima do frame baseado no conteúdo"""
        altura_base = 225
        altura_por_linha = 50
        altura_total = altura_base + (len(self.alturas) * altura_por_linha)
        if altura_total < 300:
            altura_total = 300
        self.frame.setMinimumHeight(altura_total)

    def sincronizar_angulos(self):
        ang_dir = self.angulos_layout.input_ang_dir.text()
        if self.numeracao_vao < len(self.parent_widget.vaos):
            proximo_vao = self.parent_widget.vaos[self.numeracao_vao]

            proximo_vao.angulos_layout.input_ang_es.blockSignals(True)
            proximo_vao.angulos_layout.input_ang_es.setText(ang_dir)
            proximo_vao.angulos_layout.input_ang_es.blockSignals(False)

    def checar_campos_preenchidos(self) -> bool:
        """
        Verifica se todos os QLineEdit do vão foram preenchidos.
        Se algum estiver vazio, abre um QDialog informando quais campos faltam.

        Returns:
            bool: True se todos preenchidos, False se algum estiver vazio.
        """
        campos_vazios = []

        if not self.linhas_centro_layout.input_lc.text():
            campos_vazios.append(f"Linha de Centro vão {self.numeracao_vao}")

        if not self.quant_vidos_layout.input_quant_vidros.text():
            campos_vazios.append(f"Quantidade de Vidros vão {self.numeracao_vao}")

        if len(self.alturas) == 0:
            campos_vazios.append(f"Alturas vão {self.numeracao_vao}")

        if len(self.niveis) == 0:
            campos_vazios.append(f"Níveis vão {self.numeracao_vao}")

        for idx, altura in enumerate(self.alturas):
            if not altura.text():
                campos_vazios.append(f"Altura {idx+1} vão {self.numeracao_vao}")

        for idx, nivel in enumerate(self.niveis):
            if not nivel.text():
                campos_vazios.append(f"Nível {idx+1} vão {self.numeracao_vao}")

        if not self.angulos_layout.input_ang_es.text():
            campos_vazios.append(f"Ângulo Esquerdo vão {self.numeracao_vao}")

        if not self.angulos_layout.input_ang_dir.text():
            campos_vazios.append(f"Ângulo Direito vão {self.numeracao_vao}")

        if campos_vazios:
            dialog = QDialog(self)
            dialog.setWindowTitle("Campos não preenchidos")
            layout = QVBoxLayout()

            msg = "Os seguintes campos não foram preenchidos:\n\n" + "\n".join(campos_vazios)
            layout.addWidget(QLabel(msg))

            btn_ok = QPushButton("OK")
            btn_ok.clicked.connect(dialog.accept)
            layout.addWidget(btn_ok)

            dialog.setLayout(layout)
            dialog.exec()

            return False
        return True

    def get_dados_vao(self):
        lc = int(self.linhas_centro_layout.input_lc.text())
        qv = int(self.quant_vidos_layout.input_quant_vidros.text())
        ang_esq = float(self.angulos_layout.input_ang_es.text())
        ang_dir = float(self.angulos_layout.input_ang_dir.text())
        angulos = [ang_esq, ang_dir]
        alturas = []
        niveis = []

        for altura, nivel in zip(self.alturas, self.niveis):
            if altura.text() and nivel.text():
                altura = int(altura.text())
                nivel = int(nivel.text())
                alturas.append(altura)
                niveis.append(nivel)

        return {
            'linha_centro': lc,
            'quantidade_vidros': qv,
            'alturas': alturas,
            'niveis': niveis,
            'angulos': angulos,
        }

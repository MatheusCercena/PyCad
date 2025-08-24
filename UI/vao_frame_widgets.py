from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator

regex = QRegularExpression(r"^(?:\d{1,2}(?:\.\d)?|-359[0-7]\d(?:\.\d)?|359(?:\.[0-9])?)$")
validator = QRegularExpressionValidator(regex)

ALTURA_FIXA = 40
LARGURA_FIXA = 100

class HeaderLayout(QHBoxLayout):
    def __init__(self, numeracao_vao, funcao_remover):
        super().__init__()
        self.titulo_vao = QLabel(f'VÃO {numeracao_vao}')
        self.titulo_vao.setObjectName("TituloVao")
        self.titulo_vao.setFixedHeight(ALTURA_FIXA)

        botao_remover_vao = QPushButton('×')
        botao_remover_vao.setFixedHeight(ALTURA_FIXA)
        botao_remover_vao.setFixedWidth(ALTURA_FIXA)
        botao_remover_vao.setObjectName("btnRemoveVao")
        botao_remover_vao.clicked.connect(funcao_remover)

        self.addWidget(self.titulo_vao)
        self.addWidget(botao_remover_vao)

class LinhaCentroLayout(QHBoxLayout):
	def __init__(self):
		super().__init__()
		lbl_lc = QLabel('Linha de Centro:')
		lbl_lc.setFixedWidth(LARGURA_FIXA*3)
		lbl_lc.setFixedHeight(40)
		lbl_lc.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self.input_lc = QLineEdit()
		self.input_lc.setPlaceholderText('Digite a linha de centro')
		self.input_lc.setFixedWidth(LARGURA_FIXA*3)
		self.input_lc.setFixedHeight(40)
		self.input_lc.setValidator(QIntValidator(0, 99999))

		self.addWidget(lbl_lc)
		self.addWidget(self.input_lc)

class QuantidadeVidrosLayout(QHBoxLayout):
	def __init__(self):
		super().__init__()
		lbl_quant_vidros = QLabel('Quantidade de Vidros:')
		lbl_quant_vidros.setFixedWidth(LARGURA_FIXA*3)
		lbl_quant_vidros.setFixedHeight(40)
		lbl_quant_vidros.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self.input_quant_vidros = QLineEdit()
		self.input_quant_vidros.setPlaceholderText('Digite a quantidade de vidros')
		self.input_quant_vidros.setFixedWidth(LARGURA_FIXA*3)
		self.input_quant_vidros.setFixedHeight(40)
		self.input_quant_vidros.setValidator(QIntValidator(0, 99))

		self.addWidget(lbl_quant_vidros)
		self.addWidget(self.input_quant_vidros)

class AngulosLayout(QHBoxLayout):
	def __init__(self, vao_widget):
		super().__init__()
		lbl_ang_esq = QLabel('Ângulo esquerdo:')
		lbl_ang_esq.setFixedWidth(LARGURA_FIXA*2)
		lbl_ang_esq.setFixedHeight(40)
		lbl_ang_esq.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self.input_ang_es = QLineEdit()
		self.input_ang_es.setPlaceholderText('Ângulo')
		self.input_ang_es.setFixedWidth(LARGURA_FIXA*2)
		self.input_ang_es.setFixedHeight(40)
		self.input_ang_es.setValidator(validator)

		lbl_ang_dir = QLabel('Ângulo direito:')
		lbl_ang_dir.setFixedWidth(LARGURA_FIXA*2)
		lbl_ang_dir.setFixedHeight(40)
		lbl_ang_dir.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self.input_ang_dir = QLineEdit()
		self.input_ang_dir.setPlaceholderText('Ângulo')
		self.input_ang_dir.setFixedWidth(LARGURA_FIXA*2)
		self.input_ang_dir.setFixedHeight(40)
		self.input_ang_dir.setValidator(validator)
		self.input_ang_dir.textChanged.connect(vao_widget.sincronizar_angulos)

		self.addWidget(lbl_ang_esq)
		self.addWidget(self.input_ang_es)
		self.addWidget(lbl_ang_dir)
		self.addWidget(self.input_ang_dir)

class Layout_Frame(QFrame):
	def __init__(self):
		super().__init__()
		self.setFrameStyle(QFrame.Shape.Box)
		self.setStyleSheet('border: 1px solid #ddd; border-radius: 4px; padding: 5px; margin: 2px;')
		self.setMinimumHeight(300)
		self.setFixedWidth(850)
		self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

class VaoFrame(QVBoxLayout):
	def __init__(self):
		super().__init__()
		self.setSpacing(4)
		self.setContentsMargins(5, 5, 5, 5)

class BotaoAdicionarAlturas(QPushButton):
	def __init__(self, funcao_adicionar_altura):
		super().__init__('Adicionar altura')
		self.clicked.connect(funcao_adicionar_altura)

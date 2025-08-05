from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QHBoxLayout, QComboBox
from PyQt6.QtCore import Qt

class QuantVidrosWidget(QWidget):
    def __init__(self, lcs=None):
        super().__init__()
        self.lcs = lcs or []
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel('QUANTIDADE DE VIDROS'))

        self.combo_lado = QComboBox()
        self.combo_lado.addItems([f'Vão {i+1}' for i in range(len(self.lcs))] or ['Vão 1'])
        self.layout().addWidget(self.combo_lado)

        self.input = QLineEdit()
        self.input.setPlaceholderText('Digite a quantidade de vidros')
        self.layout().addWidget(self.input)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton('Adicionar')
        self.btn_remove = QPushButton('Remover Selecionado')
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_remove)
        self.layout().addLayout(btn_layout)

        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.layout().addWidget(self.list_widget)

        self.btn_add.clicked.connect(self.add_quant)
        self.btn_remove.clicked.connect(self.remove_quant)
        self.combo_lado.currentIndexChanged.connect(self.update_list)

        self.quant_vidros = [[] for _ in range(len(self.lcs) or 1)]
        self.update_list()

    def add_quant(self):
        text = self.input.text()
        try:
            valor = int(text)
        except ValueError:
            QMessageBox.warning(self, 'Erro', 'O valor deve ser um número inteiro.')
            return
        idx = self.combo_lado.currentIndex()
        self.quant_vidros[idx].append(valor)
        self.input.clear()
        self.update_list()

    def remove_quant(self):
        idx = self.combo_lado.currentIndex()
        for item in self.list_widget.selectedItems():
            self.quant_vidros[idx].remove(int(item.text()))
        self.update_list()

    def update_list(self):
        idx = self.combo_lado.currentIndex()
        self.list_widget.clear()
        for quant in self.quant_vidros[idx]:
            self.list_widget.addItem(str(quant))

    def get_quant_vidros(self):
        return self.quant_vidros
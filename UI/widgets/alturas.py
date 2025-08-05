from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QHBoxLayout, QComboBox
from PyQt6.QtCore import Qt

class AlturasWidget(QWidget):
    def __init__(self, lcs=None):
        super().__init__()
        self.lcs = lcs or []
        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(4)
        self.layout().setContentsMargins(5, 5, 5, 5)
        
        self.layout().addWidget(QLabel('ALTURAS'))

        # Layout horizontal para combo e input
        input_layout = QHBoxLayout()
        input_layout.setSpacing(5)
        
        self.combo_lado = QComboBox()
        self.combo_lado.addItems([f'Vão {i+1}' for i in range(len(self.lcs))] or ['Vão 1'])
        self.combo_lado.setMinimumWidth(120)
        input_layout.addWidget(self.combo_lado)

        self.input = QLineEdit()
        self.input.setPlaceholderText('Digite a altura (mm)')
        self.input.setMinimumWidth(200)
        self.input.setFixedHeight(60)
        input_layout.addWidget(self.input)
        
        self.layout().addLayout(input_layout)

        # Layout horizontal para botões
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(5)
        
        self.btn_add = QPushButton('Adicionar')
        self.btn_remove = QPushButton('Remover Selecionado')
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_remove)
        self.layout().addLayout(btn_layout)

        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.list_widget.setMaximumHeight(200)
        self.list_widget.setFixedHeight(100)

        self.layout().addWidget(self.list_widget)

        self.btn_add.clicked.connect(self.add_altura)
        self.btn_remove.clicked.connect(self.remove_altura)
        self.combo_lado.currentIndexChanged.connect(self.update_list)

        self.alturas = [[] for _ in range(len(self.lcs) or 1)]
        self.update_list()

    def add_altura(self):
        text = self.input.text()
        try:
            valor = int(text)
        except ValueError:
            QMessageBox.warning(self, 'Erro', 'O valor deve ser um número inteiro.')
            return
        idx = self.combo_lado.currentIndex()
        self.alturas[idx].append(valor)
        self.input.clear()
        self.update_list()

    def remove_altura(self):
        idx = self.combo_lado.currentIndex()
        for item in self.list_widget.selectedItems():
            self.alturas[idx].remove(int(item.text()))
        self.update_list()

    def update_list(self):
        idx = self.combo_lado.currentIndex()
        self.list_widget.clear()
        for altura in self.alturas[idx]:
            self.list_widget.addItem(str(altura))

    def get_alturas(self):
        return self.alturas
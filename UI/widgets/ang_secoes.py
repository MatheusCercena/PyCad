from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QHBoxLayout
from PyQt6.QtCore import Qt

class AngSecoesWidget(QWidget):
    def __init__(self, lcs=None):
        super().__init__()
        self.lcs = lcs or []
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel('ÂNGULOS DAS SEÇÕES'))

        self.input = QLineEdit()
        self.input.setPlaceholderText('Digite o ângulo (graus)')
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

        self.btn_add.clicked.connect(self.add_angulo)
        self.btn_remove.clicked.connect(self.remove_angulo)

        self.angulos = []
        self.update_list()

    def add_angulo(self):
        text = self.input.text()
        try:
            valor = float(text.replace(',', '.'))
            if not 40 <= valor <= 320:
                QMessageBox.warning(self, 'Erro', 'O ângulo deve estar entre 40 e 320 graus.')
                return
        except ValueError:
            QMessageBox.warning(self, 'Erro', 'O valor deve ser um número.')
            return
        self.angulos.append(valor)
        self.input.clear()
        self.update_list()

    def remove_angulo(self):
        for item in self.list_widget.selectedItems():
            self.angulos.remove(float(item.text()))
        self.update_list()

    def update_list(self):
        self.list_widget.clear()
        for ang in self.angulos:
            self.list_widget.addItem(str(ang))

    def get_angulos(self):
        return self.angulos
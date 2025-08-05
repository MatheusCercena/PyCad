from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class ElevadorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel('ALTURA ELEVADOR'))

        self.input = QLineEdit()
        self.input.setPlaceholderText('Digite a medida segura do elevador (4 dígitos)')
        self.layout().addWidget(self.input)

        self.btn_set = QPushButton('Definir')
        self.layout().addWidget(self.btn_set)

        self.btn_set.clicked.connect(self.set_elevador)
        self.elevador = None

    def set_elevador(self):
        text = self.input.text()
        if not (text.isdigit() and len(text) == 4):
            QMessageBox.warning(self, 'Erro', 'O valor deve conter apenas números inteiros e ter 4 dígitos.')
            return
        self.elevador = int(text)

    def get_elevador(self):
        return self.elevador
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QHBoxLayout
from PyQt6.QtCore import Qt

class LinhasDeCentroWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel('LINHAS DE CENTRO'))

        self.input = QLineEdit()
        self.input.setPlaceholderText('Digite a linha de centro (mm)')
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

        self.btn_add.clicked.connect(self.add_linha)
        self.btn_remove.clicked.connect(self.remove_linha)

    def add_linha(self):
        text = self.input.text()
        try:
            valor = int(text)
            if not 30 <= valor <= 30000:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, 'Erro', 'O valor deve ser um número inteiro entre 30 e 30000.')
            return
        self.list_widget.addItem(str(valor))
        self.input.clear()

    def remove_linha(self):
        for item in self.list_widget.selectedItems():
            self.list_widget.takeItem(self.list_widget.row(item))

    def get_linhas(self):
        return [int(self.list_widget.item(i).text()) for i in range(self.list_widget.count())]
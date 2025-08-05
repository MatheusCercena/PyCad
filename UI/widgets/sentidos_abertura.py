from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QHBoxLayout, QComboBox
from PyQt6.QtCore import Qt

class SentidosAberturaWidget(QWidget):
    def __init__(self, quant_vidros=None):
        super().__init__()
        self.quant_vidros = quant_vidros or []
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel('SENTIDOS DE ABERTURA'))

        self.input_ini = QLineEdit()
        self.input_ini.setPlaceholderText('Vidro início')
        self.input_fim = QLineEdit()
        self.input_fim.setPlaceholderText('Vidro fim')
        self.input_giratorio = QLineEdit()
        self.input_giratorio.setPlaceholderText('Vidro giratório')
        self.input_adjacente = QLineEdit()
        self.input_adjacente.setPlaceholderText('Vidro adjacente')
        self.combo_sentido = QComboBox()
        self.combo_sentido.addItems(['direita', 'esquerda'])

        self.layout().addWidget(self.input_ini)
        self.layout().addWidget(self.input_fim)
        self.layout().addWidget(self.input_giratorio)
        self.layout().addWidget(self.input_adjacente)
        self.layout().addWidget(self.combo_sentido)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton('Adicionar')
        self.btn_remove = QPushButton('Remover Selecionado')
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_remove)
        self.layout().addLayout(btn_layout)

        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.layout().addWidget(self.list_widget)

        self.btn_add.clicked.connect(self.add_sentido)
        self.btn_remove.clicked.connect(self.remove_sentido)

        self.sentidos = []
        self.update_list()

    def add_sentido(self):
        try:
            v_ini = int(self.input_ini.text())
            v_fim = int(self.input_fim.text())
            giratorio = int(self.input_giratorio.text())
            adjacente = int(self.input_adjacente.text())
            sentido = self.combo_sentido.currentText()
        except ValueError:
            QMessageBox.warning(self, 'Erro', 'Todos os campos devem ser preenchidos corretamente.')
            return
        self.sentidos.append([v_ini, v_fim, giratorio, adjacente, sentido])
        self.input_ini.clear()
        self.input_fim.clear()
        self.input_giratorio.clear()
        self.input_adjacente.clear()
        self.update_list()

    def remove_sentido(self):
        for item in self.list_widget.selectedItems():
            idx = self.list_widget.row(item)
            self.sentidos.pop(idx)
        self.update_list()

    def update_list(self):
        self.list_widget.clear()
        for s in self.sentidos:
            self.list_widget.addItem(str(s))

    def get_sentidos(self):
        return self.sentidos
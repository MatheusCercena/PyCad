from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout

class AngParedesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel('ÂNGULOS DAS PAREDES'))

        self.input_esq = QLineEdit()
        self.input_esq.setPlaceholderText('Ângulo da extremidade esquerda')
        self.input_dir = QLineEdit()
        self.input_dir.setPlaceholderText('Ângulo da extremidade direita')
        self.layout().addWidget(self.input_esq)
        self.layout().addWidget(self.input_dir)

        btn_layout = QHBoxLayout()
        self.btn_set = QPushButton('Definir')
        btn_layout.addWidget(self.btn_set)
        self.layout().addLayout(btn_layout)

        self.btn_set.clicked.connect(self.set_angulos)
        self.angulos = [None, None]

    def set_angulos(self):
        try:
            ang_esq = float(self.input_esq.text().replace(',', '.'))
            ang_dir = float(self.input_dir.text().replace(',', '.'))
            if not (20 < ang_esq < 160) or not (20 < ang_dir < 160):
                QMessageBox.warning(self, 'Erro', 'Os ângulos devem estar entre 20 e 160 graus.')
                return
            self.angulos = [ang_esq, ang_dir]
        except ValueError:
            QMessageBox.warning(self, 'Erro', 'Os valores devem ser números.')
            return

    def get_angulos(self):
        return self.angulos
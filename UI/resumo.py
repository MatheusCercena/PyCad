from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog, QMessageBox
import json

from src.logs import criar_alfanumerico
from src.main import projetar

class ResumoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel('RESUMO FINAL'))

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.layout().addWidget(self.text_edit)

        self.btn_export = QPushButton('Projetar')
        self.layout().addWidget(self.btn_export)
        self.btn_export.clicked.connect(self.exportar_json)

        self.dados = {}

    def atualizar_dados(self, dados):
        self.dados = dados
        texto = json.dumps(dados, indent=4, ensure_ascii=False)
        self.text_edit.setText(texto)

    def exportar_json(self):
        codigo_projeto = criar_alfanumerico()
        if not self.dados:
            QMessageBox.warning(self, 'Erro', 'Nenhum dado para exportar.')
            return
        file_path = f'exportacoes\\projeto_{codigo_projeto}.json'
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.dados, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, 'Sucesso', f'Dados exportados para {file_path}')

        # projetar(file_path, codigo_projeto)
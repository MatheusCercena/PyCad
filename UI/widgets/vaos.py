from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from widgets.elementos_main import scroll_area
from widgets.vao import VaoWidget

class VaosWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.vaos = []
        self.interface_vaos()

    def interface_vaos(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(5, 5, 5, 5)

        titulo = QLabel('VÃOS')
        titulo.setStyleSheet('font-weight: bold; font-size: 18px; margin: 5px 0;')

        self.scroll_area = scroll_area()

        self.botao_adicionar_vao = QPushButton('Adicionar Vão')
        self.botao_adicionar_vao.clicked.connect(self.adicionar_vao)

        layout.addWidget(titulo)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.botao_adicionar_vao)

        self.adicionar_vao()

    def adicionar_vao(self):
        numeracao_vao = len(self.vaos) + 1
        vao_widget = VaoWidget(numeracao_vao, self)
        self.vaos.append(vao_widget)
        self.scroll_area.adicionar_item(vao_widget)

    def remover_vao(self, numeracao_vao):
        for i, vao in enumerate(self.vaos):
            if i == numeracao_vao:
                self.scroll_area.remover_item(vao)
                self.vaos.pop(i)
                self.renomear_vaos()
                break

    def renomear_vaos(self):
        for i, vao_restante in enumerate(self.vaos):
            vao_restante.numeracao_vao = i + 1
            vao_restante.titulo.setText(f'VÃO {i + 1}')

    def get_dados_vaos(self):

        linhas_centro = get_linhas_centro()
        alturas = get_alturas()
        niveis = get_niveis()
        quant_vidros = get_quantidade_vidros()
        angulos = get_angulos()

        def get_linhas_centro(self):
            """Retorna lista de linhas de centro no formato esperado"""
            lcs = []
            for vao in self.vaos:
                dados_vao = vao.get_dados_vao()
                lcs.append(dados_vao['linha_centro'])
            return lcs

        def get_alturas(self):
            alturas = []
            for vao in self.vaos:
                dados_vao = vao.get_dados_vao()
                alturas.append(dados_vao['alturas'])
            return alturas

        def get_niveis(self):
            niveis = []
            for vao in self.vaos:
                dados_vao = vao.get_dados_vao()
                niveis.append(dados_vao['niveis'])
            return niveis

        def get_quantidade_vidros(self):
            quant_vidros = []
            for vao in self.vaos:
                dados_vao = vao.get_dados_vao()
                quant_vidros.append(dados_vao['quantidade_vidros'])
            return quant_vidros

        def get_angulos(self):
            angs_in = []
            angs_paredes = []

            for i, vao in enumerate(self.vaos):
                dados_vao = vao.get_dados_vao()
                if i == 0:
                    angs_paredes.append(dados_vao['angulos'][0])
                    angs_in.append(dados_vao['angulos'][1])
                if i == len(self.vaos) - 1:
                    angs_paredes.append(dados_vao['angulos'][1])
                if i > 0 and i < len(self.vaos) - 1:
                    angs_in.append(dados_vao['angulos'][1])

            return angs_paredes, angs_in

        return {
            'linhas_de_centro': linhas_centro,
            'alturas': alturas,
            'niveis': niveis,
            'quantidade_vidros': quant_vidros,
            'angulos_secoes': angulos
        }
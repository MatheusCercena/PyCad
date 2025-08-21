from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QScrollArea, QFrame, QGridLayout)
from PyQt6.QtCore import Qt

ALTURA_FIXA = 40
LARGURA_FIXA = 100

class VaoWidget(QWidget):
    def __init__(self, vao_num, parent_widget):
        super().__init__()
        self.vao_num = vao_num
        self.parent_widget = parent_widget
        self.alturas = []
        self.niveis = []
        self.quant_vidros = []
        self.angs_in = []
        self.angs_paredes = []
        self.juncoes = []
        self.elevador = int()
        self.linha_layouts = []

        self.setup_ui()

    def setup_ui(self):
        """Configura a interface do vão"""
        # Titulo do vão
        titulo = QLabel(f'VÃO {self.vao_num}')
        titulo.setStyleSheet('font-weight: bold; font-size: 30px; color: #005080; margin: 5px 0; border: none;')
        titulo.setFixedHeight(ALTURA_FIXA)

        # Botão X para remover vão
        self.btn_remove_vao = QPushButton('×')
        self.btn_remove_vao.setFixedHeight(ALTURA_FIXA)
        self.btn_remove_vao.setFixedWidth(ALTURA_FIXA)
        self.btn_remove_vao.setStyleSheet('''
            QPushButton {background-color: #ff4444; color: white; border: none;border-radius: 12px; font-weight: bold; font-size: 30px;}
            QPushButton:hover {background-color: #ff6666;}''')
        self.btn_remove_vao.clicked.connect(self.remover_vao)

        header_layout = QHBoxLayout()
        header_layout.addWidget(titulo)
        header_layout.addWidget(self.btn_remove_vao)

        # Linha de centro
        lbl_lc = QLabel('Linha de Centro:')
        lbl_lc.setFixedWidth(LARGURA_FIXA*3)
        lbl_lc.setFixedHeight(ALTURA_FIXA)
        lbl_lc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_lc = QLineEdit()
        self.input_lc.setPlaceholderText('Digite a linha de centro')
        self.input_lc.setFixedWidth(LARGURA_FIXA*3)
        self.input_lc.setFixedHeight(ALTURA_FIXA)

        lc_layout = QHBoxLayout()
        lc_layout.addWidget(lbl_lc)
        lc_layout.addWidget(self.input_lc)

        # Quantidade de vidros
        lbl_quant_vidros = QLabel('Quantidade de Vidros:')
        lbl_quant_vidros.setFixedWidth(LARGURA_FIXA*3)
        lbl_quant_vidros.setFixedHeight(ALTURA_FIXA)
        lbl_quant_vidros.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_quant_vidros = QLineEdit()
        self.input_quant_vidros.setPlaceholderText('Digite a quantidade de vidros')
        self.input_quant_vidros.setFixedWidth(LARGURA_FIXA*3)
        self.input_quant_vidros.setFixedHeight(ALTURA_FIXA)

        quant_vidos_layout = QHBoxLayout()
        quant_vidos_layout.addWidget(lbl_quant_vidros)
        quant_vidos_layout.addWidget(self.input_quant_vidros)

        # Angulos

        # Label ang esquerdo
        lbl_ang_esq = QLabel(f'Âng. esq.:')
        lbl_ang_esq.setFixedWidth(LARGURA_FIXA*2)
        lbl_ang_esq.setFixedHeight(ALTURA_FIXA)
        lbl_ang_esq.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Input ang esquerdo
        input_ang_es = QLineEdit()
        input_ang_es.setPlaceholderText('Ângulo')
        input_ang_es.setFixedWidth(LARGURA_FIXA*2)
        input_ang_es.setFixedHeight(ALTURA_FIXA)

        # Label ang direito
        lbl_ang_dir = QLabel(f'Âng. esq.:')
        lbl_ang_dir.setFixedWidth(LARGURA_FIXA*2)
        lbl_ang_dir.setFixedHeight(ALTURA_FIXA)
        lbl_ang_dir.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Input ang direito
        input_ang_dir = QLineEdit()
        input_ang_dir.setPlaceholderText('Ângulo')
        input_ang_dir.setFixedWidth(LARGURA_FIXA*2)
        input_ang_dir.setFixedHeight(ALTURA_FIXA)

        angulos_layout = QHBoxLayout()
        angulos_layout.addWidget(lbl_ang_esq)
        angulos_layout.addWidget(input_ang_es)
        angulos_layout.addWidget(lbl_ang_dir)
        angulos_layout.addWidget(input_ang_dir)

        # Frame dos vaos com largura adaptável
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Shape.Box)
        self.frame.setStyleSheet('border: 1px solid #ddd; border-radius: 4px; padding: 5px; margin: 2px;')
        self.frame.setMinimumHeight(250)
        self.frame.setFixedWidth(850)

        # Container para alturas dinâmicas
        self.btn_add_altura = QPushButton('Adicionar Altura')
        self.btn_add_altura.clicked.connect(self.adicionar_altura)
        self.alturas_container = QVBoxLayout()
        self.alturas_container.setSpacing(2)

        self.vao_layout = QVBoxLayout(self.frame)
        self.vao_layout.setContentsMargins(5, 5, 5, 5)
        self.vao_layout.addLayout(header_layout)
        self.vao_layout.addLayout(lc_layout)
        self.vao_layout.addLayout(quant_vidos_layout)
        self.vao_layout.addLayout(angulos_layout)
        self.vao_layout.addWidget(self.btn_add_altura)
        self.vao_layout.addLayout(self.alturas_container)

        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.frame)

    def remover_vao(self):
        """Remove este vão"""
        self.parent_widget.remover_vao(self.vao_num)

    def adicionar_altura(self):
        """Adiciona uma nova linha de altura e nível"""
        altura_idx = len(self.alturas)

        # Label da altura
        lbl_altura = QLabel(f'Altura {altura_idx + 1}:')
        lbl_altura.setFixedWidth(LARGURA_FIXA)
        lbl_altura.setFixedHeight(ALTURA_FIXA)
        lbl_altura.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Input da altura
        input_altura = QLineEdit()
        input_altura.setPlaceholderText('Digite a altura')
        input_altura.setFixedWidth(LARGURA_FIXA*2)
        input_altura.setFixedHeight(ALTURA_FIXA)

        # Label do nível
        lbl_nivel = QLabel('Nível:')
        lbl_nivel.setFixedWidth(LARGURA_FIXA)
        lbl_nivel.setFixedHeight(ALTURA_FIXA)
        lbl_nivel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Input do nível
        input_nivel = QLineEdit()
        input_nivel.setPlaceholderText('Digite o nível')
        input_nivel.setFixedWidth(LARGURA_FIXA*2)
        input_nivel.setFixedHeight(ALTURA_FIXA)

        # Botão remover (quadrado, vermelho, mesma altura)
        btn_remove = QPushButton('×')
        btn_remove.setFixedHeight(ALTURA_FIXA)
        btn_remove.setFixedWidth(ALTURA_FIXA)
        btn_remove.setStyleSheet('''
            QPushButton {background-color: #ff4444; color: white; border: 1px solid red; border-radius: 15px; font-weight: bold;font-size: 14px;}
            QPushButton:hover {background-color: #ff6666;}''')
        btn_remove.clicked.connect(lambda: self.remover_altura(altura_idx))

        # Layout horizontal para a linha
        linha_layout = QHBoxLayout()
        linha_layout.setSpacing(5)
        linha_layout.setContentsMargins(2, 2, 2, 2)
        linha_layout.addWidget(lbl_altura)
        linha_layout.addWidget(input_altura)
        linha_layout.addWidget(lbl_nivel)
        linha_layout.addWidget(input_nivel)
        linha_layout.addWidget(btn_remove)

        self.alturas_container.addLayout(linha_layout)

        # Armazenar referências
        self.alturas.append(input_altura)
        self.niveis.append(input_nivel)
        self.linha_layouts.append(linha_layout)

        # Mover botão para baixo
        self.vao_layout.removeWidget(self.btn_add_altura)
        self.vao_layout.addWidget(self.btn_add_altura)

        # Ajustar altura mínima do frame baseado no conteúdo
        self.ajustar_altura_frame()

    def ajustar_altura_frame(self):
        """Ajusta a altura mínima do frame baseado no conteúdo"""
        altura_base = 225
        altura_por_linha = 50  # Altura de cada linha de altura (40px + 10px de espaçamento)
        altura_total = altura_base + (len(self.alturas) * altura_por_linha)
        self.frame.setMinimumHeight(altura_total)

    def remover_altura(self, idx):
        """Remove uma linha de self.alturas"""
        if idx < len(self.alturas):
            linha_layout = self.linha_layouts[idx]
            while linha_layout.count() > 0:
                item = linha_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)

            self.alturas_container.removeItem(linha_layout)

            # Remover das listas
            self.alturas.pop(idx)
            self.niveis.pop(idx)
            self.linha_layouts.pop(idx)

            # Reorganizar labels
            for i, altura in enumerate(self.alturas):
                # Encontrar o label correspondente
                layout = altura.parent().layout()
                for j in range(layout.count()):
                    widget = layout.itemAt(j).widget()
                    if isinstance(widget, QLabel) and widget.text().startswith('Altura'):
                        widget.setText(f'Altura {i + 1}:')
                        break

            # Ajustar altura mínima do frame baseado no conteúdo
            self.ajustar_altura_frame()

    def get_dados(self):
        """Retorna os dados do vão no formato esperado"""
        try:
            lc = int(self.input_lc.text()) if self.input_lc.text() else 0
            qv = int(self.input_quant_vidros.text()) if self.input_quant_vidros.text() else 0
            alturas = []
            niveis = []

            for altura, nivel in zip(self.alturas, self.niveis):
                if altura.text() and nivel.text():
                    altura = int(altura.text())
                    nivel = int(nivel.text())
                    alturas.append(altura)
                    niveis.append(nivel)

            return {
                'linha_centro': lc,
                'quantidade_vidros': qv,
                'alturas': alturas,
                'niveis': niveis
            }
        except ValueError:
            return None

class VaosWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.vaos = []
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface principal"""
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(5, 5, 5, 5)

        # Título
        titulo = QLabel('VÃOS')
        titulo.setStyleSheet('font-weight: bold; font-size: 18px; margin: 5px 0;')
        layout.addWidget(titulo)

        # Área de scroll
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        # Botão adicionar vão
        self.btn_add_vao = QPushButton('Adicionar Vão')
        self.btn_add_vao.clicked.connect(self.adicionar_vao)
        layout.addWidget(self.btn_add_vao)

        # Adicionar primeiro vão
        self.adicionar_vao()

    def adicionar_vao(self):
        """Adiciona um novo vão"""
        vao_num = len(self.vaos) + 1
        vao_widget = VaoWidget(vao_num, self)
        self.vaos.append(vao_widget)
        self.scroll_layout.addWidget(vao_widget)

    def remover_vao(self, vao_num):
        """Remove um vão específico"""
        # Encontrar o vão pelo número
        for i, vao in enumerate(self.vaos):
            if vao.vao_num == vao_num:
                # Remover o widget
                vao.setParent(None)
                self.vaos.pop(i)

                # Renumerar os vãos restantes
                for j, vao_restante in enumerate(self.vaos):
                    vao_restante.vao_num = j + 1
                    # Atualizar o título
                    for child in vao_restante.children():
                        if isinstance(child, QHBoxLayout):
                            for k in range(child.count()):
                                item = child.itemAt(k)
                                if item.widget() and isinstance(item.widget(), QLabel) and item.widget().text().startswith('Vão'):
                                    item.widget().setText(f'Vão {j + 1}')
                                    break
                break

    def get_linhas_centro(self):
        """Retorna lista de linhas de centro no formato esperado"""
        lcs = []
        for vao in self.vaos:
            # dados = vao.get_dados()
            # if dados and dados['linha_centro'] > 0:
            #     lcs.append(dados['linha_centro'])
            pass
        return lcs

    def get_alturas(self):
        """Retorna lista de alturas no formato esperado"""
        alturas = []
        for vao in self.vaos:
            dados = vao.get_dados()
            if dados and dados['alturas']:
                alturas.append(dados['alturas'])
        return alturas

    def get_niveis(self):
        """Retorna lista de níveis no formato esperado"""
        niveis = []
        for vao in self.vaos:
            dados = vao.get_dados()
            if dados and dados['niveis']:
                niveis.append(dados['niveis'])
        return niveis

    def get_quantidade_vidros(self):
        """Retorna lista de quantidade de vidros no formato esperado"""
        quant_vidros = []
        for vao in self.vaos:
            dados = vao.get_dados()
            if dados and dados['quantidade_vidros'] > 0:
                quant_vidros.append(dados['quantidade_vidros'])
        return quant_vidros
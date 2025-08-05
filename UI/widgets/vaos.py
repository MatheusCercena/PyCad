from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QHBoxLayout, QScrollArea, QFrame, QGridLayout)
from PyQt6.QtCore import Qt

class VaoWidget(QWidget):
    def __init__(self, vao_num, parent_widget):
        super().__init__()
        self.vao_num = vao_num
        self.parent_widget = parent_widget
        self.alturas = []
        self.niveis = []
        self.altura_inputs = []
        self.nivel_inputs = []
        self.linha_layouts = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do vão"""
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Header com título e botão X
        header_layout = QHBoxLayout()
        header_layout.setSpacing(5)
        
        titulo = QLabel(f'VÃO {self.vao_num}')
        titulo.setStyleSheet('font-weight: bold; font-size: 20px; color: #005080; margin: 5px 0;')
        header_layout.addWidget(titulo)
        
        # Botão X para remover vão
        self.btn_remove_vao = QPushButton('×')
        self.btn_remove_vao.setFixedHeight(25)
        self.btn_remove_vao.setFixedWidth(25)
        self.btn_remove_vao.setStyleSheet('''
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
        ''')
        self.btn_remove_vao.clicked.connect(self.remover_vao)
        header_layout.addWidget(self.btn_remove_vao)
        
        layout.addLayout(header_layout)
        
        # Frame principal com largura adaptável
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Shape.Box)
        self.frame.setStyleSheet('border: 1px solid #ddd; border-radius: 4px; padding: 5px; margin: 2px;')
        self.frame.setMinimumHeight(250)  # Altura mínima reduzida
        self.frame.setFixedWidth(800)  # Largura máxima para não ocupar toda a tela
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setSpacing(2)
        self.frame_layout.setContentsMargins(5, 5, 5, 5)
        
        # Linha de centro 
        lc_layout = QHBoxLayout()
        lc_layout.setSpacing(5)
        
        lbl_lc = QLabel('Linha de Centro:')
        lbl_lc.setFixedWidth(250)
        lbl_lc.setFixedHeight(30)
        lc_layout.addWidget(lbl_lc)
        
        self.input_lc = QLineEdit()
        self.input_lc.setPlaceholderText('Digite a linha de centro')
        self.input_lc.setFixedWidth(250)
        self.input_lc.setFixedHeight(30) 
        lc_layout.addWidget(self.input_lc)
        
        # Adicionar espaço flexível para ocupar o restante da largura
        self.frame_layout.addLayout(lc_layout)
        
        # Quantidade de vidros
        qv_layout = QHBoxLayout()
        qv_layout.setSpacing(5)
        
        lbl_qv = QLabel('Quantidade de Vidros:')
        lbl_qv.setFixedWidth(250)  
        lbl_qv.setFixedHeight(30)
        qv_layout.addWidget(lbl_qv)
        
        self.input_qv = QLineEdit()
        self.input_qv.setPlaceholderText('Digite a quantidade de vidros')
        self.input_qv.setFixedWidth(250)
        self.input_qv.setFixedHeight(30)  # Altura consistente
        qv_layout.addWidget(self.input_qv)
        
        # Adicionar espaço flexível para ocupar o restante da largura
        self.frame_layout.addLayout(qv_layout)
        
        # Container para alturas dinâmicas (sem frame)
        self.alturas_container = QVBoxLayout()
        self.alturas_container.setSpacing(2)
        self.frame_layout.addLayout(self.alturas_container)
        
        # Botão adicionar altura
        self.btn_add_altura = QPushButton('Adicionar Altura')
        self.btn_add_altura.clicked.connect(self.adicionar_altura)
        self.frame_layout.addWidget(self.btn_add_altura)
        
        layout.addWidget(self.frame)
        
    def remover_vao(self):
        """Remove este vão"""
        self.parent_widget.remover_vao(self.vao_num)
        
    def adicionar_altura(self):
        """Adiciona uma nova linha de altura e nível"""
        altura_idx = len(self.altura_inputs)
        
        # Criar um layout horizontal para a linha (sem widget container)
        linha_layout = QHBoxLayout()
        linha_layout.setSpacing(5)
        linha_layout.setContentsMargins(0, 0, 0, 0)
        
        # Altura fixa para todos os elementos
        altura_fixa = 40
        largura_fixa = 100
        
        # Label da altura 
        lbl_altura = QLabel(f'Altura {altura_idx + 1}:')
        lbl_altura.setFixedWidth(largura_fixa)
        lbl_altura.setFixedHeight(altura_fixa)
        lbl_altura.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_altura.setStyleSheet('background-color: #333; color: white; border: 1px solid #ddd; padding: 2px;')
        linha_layout.addWidget(lbl_altura)
        
        # Input da altura 
        input_altura = QLineEdit()
        input_altura.setPlaceholderText('Digite a altura')
        input_altura.setFixedWidth(largura_fixa*2)
        input_altura.setFixedHeight(altura_fixa)
        linha_layout.addWidget(input_altura)
        
        # Label do nível (1/4 da largura)
        lbl_nivel = QLabel('Nível:')
        lbl_nivel.setFixedWidth(largura_fixa)
        lbl_nivel.setFixedHeight(altura_fixa)
        lbl_nivel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        linha_layout.addWidget(lbl_nivel)
        
        # Input do nível (1/4 da largura)
        input_nivel = QLineEdit()
        input_nivel.setPlaceholderText('Digite o nível')
        input_nivel.setFixedWidth(largura_fixa*2)
        input_nivel.setFixedHeight(altura_fixa)
        linha_layout.addWidget(input_nivel)
        
        # Botão remover (quadrado, vermelho, mesma altura)
        btn_remove = QPushButton('×')
        btn_remove.setFixedWidth(altura_fixa)
        btn_remove.setFixedHeight(altura_fixa)
        btn_remove.setStyleSheet('''
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: 1px solid red;
                border-radius: 15px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
        ''')
        btn_remove.clicked.connect(lambda: self.remover_altura(altura_idx))
        linha_layout.addWidget(btn_remove)
            
        # Adicionar o layout da linha ao container
        self.alturas_container.addLayout(linha_layout)
        
        # Armazenar referências
        self.altura_inputs.append(input_altura)
        self.nivel_inputs.append(input_nivel)
        self.linha_layouts.append(linha_layout)
        
        # Mover botão para baixo
        self.frame_layout.removeWidget(self.btn_add_altura)
        self.frame_layout.addWidget(self.btn_add_altura)
        
        # Ajustar altura mínima do frame baseado no conteúdo
        self.ajustar_altura_frame()
        
    def ajustar_altura_frame(self):
        """Ajusta a altura mínima do frame baseado no conteúdo"""
        altura_base = 120  # Altura base (linha de centro + quantidade de vidros + botão)
        altura_por_linha = 40  # Altura de cada linha de altura (30px + 10px de espaçamento)
        altura_total = altura_base + (len(self.altura_inputs) * altura_por_linha)
        self.frame.setMinimumHeight(altura_total)
        
    def remover_altura(self, idx):
        """Remove uma linha de altura"""
        if idx < len(self.altura_inputs):
            # Remover o layout da linha
            linha_layout = self.linha_layouts[idx]
            
            # Remover todos os widgets do layout
            while linha_layout.count() > 0:
                item = linha_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)
            
            # Remover o layout do container
            self.alturas_container.removeItem(linha_layout)
            
            # Remover das listas
            self.altura_inputs.pop(idx)
            self.nivel_inputs.pop(idx)
            self.linha_layouts.pop(idx)
            
            # Reorganizar labels
            for i, input_altura in enumerate(self.altura_inputs):
                # Encontrar o label correspondente
                layout = input_altura.parent().layout()
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
            # Linha de centro
            lc = int(self.input_lc.text()) if self.input_lc.text() else 0
            
            # Quantidade de vidros
            qv = int(self.input_qv.text()) if self.input_qv.text() else 0
            
            # Alturas e níveis
            alturas = []
            niveis = []
            
            for input_altura, input_nivel in zip(self.altura_inputs, self.nivel_inputs):
                if input_altura.text() and input_nivel.text():
                    altura = int(input_altura.text())
                    nivel = int(input_nivel.text())
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
            dados = vao.get_dados()
            if dados and dados['linha_centro'] > 0:
                lcs.append(dados['linha_centro'])
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
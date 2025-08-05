from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QComboBox, QScrollArea, QFrame
from PyQt6.QtCore import Qt

class NiveisWidget(QWidget):
    def __init__(self, alturas=None):
        super().__init__()
        self.alturas = alturas or [[]]
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel('NÍVEIS'))

        # Combo para tipo de nível
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems([
            'Nível ok (ou não informado)',
            'Nível Variável (adicionar manualmente)',
            'Desnível inferior (sem medidas)'
        ])
        self.layout().addWidget(self.combo_tipo)
        self.combo_tipo.currentIndexChanged.connect(self.update_tipo)

        # Área de scroll para os vãos
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.layout().addWidget(self.scroll_area)

        # Botões
        btn_layout = QHBoxLayout()
        self.btn_apply = QPushButton('Aplicar Níveis')
        self.btn_clear = QPushButton('Limpar Todos')
        btn_layout.addWidget(self.btn_apply)
        btn_layout.addWidget(self.btn_clear)
        self.layout().addLayout(btn_layout)

        self.btn_apply.clicked.connect(self.aplicar_niveis)
        self.btn_clear.clicked.connect(self.limpar_todos)

        self.niveis = [[] for _ in range(len(self.alturas))]
        self.nivel_inputs = []  # Para armazenar os inputs de nível
        self.update_tipo()

    def update_tipo(self):
        tipo = self.current_step = self.combo_tipo.currentIndex()
        
        # Limpar área de scroll
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)
        
        self.nivel_inputs = []
        
        if tipo == 0:
            # Nível ok: tudo zero
            self.niveis = [[0 for _ in lado] for lado in self.alturas]
            self.criar_interface_visual()
            self.desabilitar_inputs()
        elif tipo == 1:
            # Nível variável: manual
            self.niveis = [[] for _ in range(len(self.alturas))]
            self.criar_interface_visual()
            self.habilitar_inputs()
        else:
            # Desnível inferior: menor altura - altura
            todas_alturas = [altura for lado in self.alturas for altura in lado]
            menor_altura = min(todas_alturas) if todas_alturas else 0
            self.niveis = [[menor_altura - altura for altura in lado] for lado in self.alturas]
            self.criar_interface_visual()
            self.desabilitar_inputs()

    def criar_interface_visual(self):
        """Cria a interface visual organizada por vãos e alturas"""
        for vao_idx, vao_alturas in enumerate(self.alturas):
            if not vao_alturas:
                continue
                
            # Título do vão
            titulo_vao = QLabel(f'Vão {vao_idx + 1}')
            titulo_vao.setStyleSheet('font-weight: bold; font-size: 16px; color: #005080; margin: 5px 0;')
            self.scroll_layout.addWidget(titulo_vao)
            
            # Frame para o vão
            frame_vao = QFrame()
            frame_vao.setFrameStyle(QFrame.Shape.Box)
            frame_vao.setStyleSheet('border: 1px solid #ddd; border-radius: 4px; padding: 5px; margin: 2px;')
            layout_vao = QVBoxLayout(frame_vao)
            layout_vao.setSpacing(2)
            layout_vao.setContentsMargins(5, 5, 5, 5)
            
            # Cabeçalho
            header_layout = QHBoxLayout()
            header_layout.setSpacing(5)
            
            lbl_altura_header = QLabel('Altura (mm)')
            lbl_altura_header.setMinimumWidth(100)
            lbl_altura_header.setMaximumWidth(100)
            lbl_altura_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header_layout.addWidget(lbl_altura_header)
            
            lbl_nivel_header = QLabel('Nível (mm)')
            lbl_nivel_header.setMinimumWidth(150)
            lbl_nivel_header.setMaximumWidth(150)
            lbl_nivel_header.setFixedHeight(100)
            lbl_nivel_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header_layout.addWidget(lbl_nivel_header)
            
            layout_vao.addLayout(header_layout)
            
            # Linhas de altura e nível
            vao_inputs = []
            for altura_idx, altura in enumerate(vao_alturas):
                linha_layout = QHBoxLayout()
                linha_layout.setSpacing(5)
                
                # Label da altura
                lbl_altura = QLabel(f'{altura}')
                lbl_altura.setMinimumWidth(100)
                lbl_altura.setMaximumWidth(100)
                lbl_altura.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lbl_altura.setStyleSheet('background-color: #f8f8f8; border: 1px solid #ddd; padding: 2px;')
                linha_layout.addWidget(lbl_altura)
                
                # Input do nível
                input_nivel = QLineEdit()
                input_nivel.setPlaceholderText('Digite o nível')
                input_nivel.setMinimumWidth(150)
                input_nivel.setMaximumWidth(150)
                
                # Definir valor inicial baseado no tipo
                if self.combo_tipo.currentIndex() == 0:  # Nível ok
                    input_nivel.setText('0')
                elif self.combo_tipo.currentIndex() == 2:  # Desnível inferior
                    todas_alturas = [alt for lado in self.alturas for alt in lado]
                    menor_altura = min(todas_alturas) if todas_alturas else 0
                    nivel_calculado = menor_altura - altura
                    input_nivel.setText(str(nivel_calculado))
                
                linha_layout.addWidget(input_nivel)
                vao_inputs.append(input_nivel)
                
                layout_vao.addLayout(linha_layout)
            
            self.nivel_inputs.append(vao_inputs)
            self.scroll_layout.addWidget(frame_vao)

    def desabilitar_inputs(self):
        """Desabilita todos os inputs de nível"""
        for vao_inputs in self.nivel_inputs:
            for input_nivel in vao_inputs:
                input_nivel.setEnabled(False)
                input_nivel.setStyleSheet('background-color: #f0f0f0; color: #666;')

    def habilitar_inputs(self):
        """Habilita todos os inputs de nível"""
        for vao_inputs in self.nivel_inputs:
            for input_nivel in vao_inputs:
                input_nivel.setEnabled(True)
                input_nivel.setStyleSheet('')

    def aplicar_niveis(self):
        """Aplica os níveis inseridos pelo usuário"""
        if self.combo_tipo.currentIndex() != 1:  # Só aplica se for nível variável
            return
            
        self.niveis = []
        for vao_idx, vao_inputs in enumerate(self.nivel_inputs):
            vao_niveis = []
            for input_nivel in vao_inputs:
                try:
                    nivel = int(input_nivel.text())
                    vao_niveis.append(nivel)
                except ValueError:
                    QMessageBox.warning(self, 'Erro', 'Todos os níveis devem ser números inteiros.')
                    return
            self.niveis.append(vao_niveis)

    def limpar_todos(self):
        """Limpa todos os inputs de nível"""
        for vao_inputs in self.nivel_inputs:
            for input_nivel in vao_inputs:
                input_nivel.clear()

    def get_niveis(self):
        """Retorna os níveis organizados por vão"""
        if self.combo_tipo.currentIndex() == 1:  # Nível variável
            self.aplicar_niveis()  # Aplica os níveis antes de retornar
        return self.niveis
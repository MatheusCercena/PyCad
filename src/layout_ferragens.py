from pyautocad import Autocad, APoint

acad = Autocad()
layout_space = acad.doc.PaperSpace 

def adicionar_ferragem(texto: str, posicao: tuple[float, float]):
    layout_space.AddText(texto, posicao, 1.75)

# PEGAR TODAS AS POSICOES DO PAPERSPACE
# FAZER AS FORMULAS DAS FERRAGENS
# VER O QUE PRECISA PEGAR DO ECG PELO SELENIUM E DA AUTOMACAO DE TRTS

def formula_tampa_de_leito():
    posicao = (0, 0)
    quantidade = 0
    pass

def formula_molduras():
    pass

def formula_molas():
    pass

def formula_aparador():
    pass

def formula_tubo_aparador():
    pass

def formula_estacionamento():
    pass

def formula_giratorio():
    pass

def formula_kit_painel_producao():
    pass

def formula_kit_painel_instalacao():
    pass

def formula_escovinha_7x8():
    pass

def formula_escovinha_5x7():
    pass

def formula_fecho_leito():
    pass

def ppa():
    pass

def data_aprovacao():
    pass

def projetista():
    pass

def data_projeto():
    pass

def ordem_servico():
    pass
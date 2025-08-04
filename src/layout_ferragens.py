from pyautocad import Autocad, APoint

acad = Autocad()
layout_space = acad.doc.PaperSpace 

def adicionar_ferragem(texto: str, posicao: tuple[float, float]):
    layout_space.AddText(texto, posicao, 1.75)

# PEGAR TODAS AS POSICOES DO PAPERSPACE
# FAZER AS FORMULAS DAS FERRAGENS
# VER O QUE PRECISA PEGAR DO ECG PELO SELENIUM E DA AUTOMACAO DE TRTS

def formula_tampa_de_leito(juncoes):
    juncoes_lista = [juncao for lado in juncoes for juncao in lado]
    quantidade = 0
    for juncao in juncoes_lista:
        if juncao == 1 or juncao == 2:
            quantidade += 1
    juncoes_45 = quantidade/2
    quant_tampinhas_45 = juncoes_45*2
    return quant_tampinhas_45

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
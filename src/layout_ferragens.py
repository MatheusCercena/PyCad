from pyautocad import Autocad, APoint
from math import ceil

acad = Autocad()
layout_space = acad.doc.PaperSpace 

def adicionar_texto(texto, posicao: tuple[float, float, float]):
    layout_space.AddText(texto, posicao, 2.2)

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

def formula_molas(sentidos_abert):
    molas = 0
    for sentido in sentidos_abert:
        quant_vidros_abertura = contar_entre_numeros(sentido[0], sentido[1])
        quant_molas = ceil((quant_vidros_abertura - 1)/3)
        molas += quant_molas
    return molas

def contar_entre_numeros(a: int, b: int) -> int:
    return max(0, abs(b - a) - 1)

def formula_tubo_aparador(sentidos_abert):
    tubos = []
    for sentido in sentidos_abert:
        quant_vidros = contar_entre_numeros(sentido[0], sentido[1])
        tamanho_aparador = 30*(quant_vidros + 2)
        tubos.append(tamanho_aparador)
    return tubos

def formula_kit_aparador(giratorios):
    return len(giratorios)
    
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
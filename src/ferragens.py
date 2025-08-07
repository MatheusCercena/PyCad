from math import ceil
from src.calcs_vetor import contar_entre_numeros

# PEGAR TODAS AS POSICOES DO PAPERSPACE
# FAZER AS FORMULAS DAS FERRAGENS - feito
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

def formula_tubo_aparador(sentidos_abert):
    tubos = []
    for sentido in sentidos_abert:
        quant_vidros = contar_entre_numeros(sentido[0], sentido[1])
        tamanho_aparador = 30*(quant_vidros + 2)
        tubos.append(tamanho_aparador)
    return tubos

def formula_kit_aparador(giratorios):
    return len(giratorios)
    
def formula_estacionamento(sentidos_abert):
    estacionamentos = 0
    for sentido in sentidos_abert:
        quant_vidros = contar_entre_numeros(sentido[0], sentido[1])
        quant_corrigida = quant_vidros + (quant_vidros % 2)
        quant_estac = (quant_corrigida-2)*2
        estacionamentos.append(quant_estac)
    return estacionamentos

def formula_giratorio(giratorios):
    return len(giratorios)*2

def formula_kit_painel_producao(quant_vidros, giratorios):
    return sum(quant_vidros)-len(giratorios)

def formula_kit_painel_instalacao(giratorios):
    return len(giratorios)
    
def formula_polietileno(medidas_perfis_U):
    comprimento_sacada = [sum(lado) for lado in medidas_perfis_U]
    return comprimento_sacada

def formula_escovinha_7x8(medidas_perfis_U):
    comprimento_sacada = [sum(lado) for lado in medidas_perfis_U]
    return comprimento_sacada

def formula_escovinha_5x7(comprimento_pe3, quantidade):
    return (comprimento_pe3 - 164) * 3

def formula_fecho_leito(giratorios):
    return len(giratorios)


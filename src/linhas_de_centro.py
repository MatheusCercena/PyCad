"""
Funções para definir as coordenadas das linhas de centro com base nos inputs de input_data e desenha-las na instância aberta de Autocad.
"""

from pyautocad import Autocad, APoint
from math import radians
from src.autocad_conn import get_acad

cad, acad_ModelSpace = get_acad()

acad = Autocad(create_if_not_exists=True)

def definir_linhas_de_centro(lcs: list, angs_in: list):
    '''
    Define as posições iniciais e finais nos eixos x e y para cada uma das linhas de centro entregues no parametro lcs.\n
    lcs: linhas de centro a serem definidas\n
    angs_in: angulos internos entre cada linha de centro. Note que angs_in[0] equivale ao angulo entre lcs[0] e lcs[1]\n
    retorno: as posições definidas para cada linha de centro, no formato [[xi1, yi1, xf1, yf1], [xi2, yi2, xf2, yf2], [xin, yin, xfn, yfn]].
    '''
    lista_de_LCs = lcs.copy()
    linha = acad.model.AddLine(APoint(0, 0), APoint(lcs[0], 0))
    inicio = linha.StartPoint
    final = linha.EndPoint
    angs = 0
    coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
    coord_de_linhas_de_centro = []
    coord_de_linhas_de_centro.append(coord_linhas)
    linha.Delete()

    for l in range(1, len(lista_de_LCs)):
        linha = acad.model.AddLine(APoint(final[0], final[1]), APoint(final[0] + lista_de_LCs[l], final[1]))
        linha.Rotate(APoint(final[0], final[1]), radians(angs_in[l-1] + angs))
        angs += angs_in[l-1]
        inicio = linha.StartPoint
        final = linha.EndPoint
        
        coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
        coord_de_linhas_de_centro.append(coord_linhas)
        linha.Delete()

    return coord_de_linhas_de_centro

def ordem_lcs(lcs, sec_princ):
    lista = []
    lista.append(sec_princ)
    if sec_princ < len(lcs)-1:
        for c in range(sec_princ + 1, len(lcs)):
            lista.append(c) 
    if sec_princ >= 1:
        lista.append(sec_princ-1) 
        if sec_princ >= 1:
            for c in reversed(range(sec_princ-1)):
                lista.append(c) 
    return lista

def redesenhar_linhas_de_centro(lcs:list, angs_in: list, sec_princ: int):
    '''
    Desenha as linhas de centro na instancia de AutoCad e retorna uma lista com as posições iniciais e finais nos eixos x e y para cada uma das linhas de centro entregues no parametro lcs.\n
    lcs: linhas de centro a serem definidas\n
    angs_in: angulos internos entre cada linha de centro. Note que angs_in[0] equivale ao angulo entre lcs[0] e lcs[1]\n
    return: retorna as posições corrigidas para cada linha de centro de lcs, no formato [[xi1, yi1, xf1, yf1], [xi2, yi2, xf2, yf2], [xin, yin, xfn, yfn]] e a lista de handles das linhas de centro.
    '''
    lista_de_LCs = lcs.copy() 
    #desenha a seção principal a partir de (0, 0)
    linha = acad.model.AddLine(APoint(0, 0), APoint(lista_de_LCs[sec_princ], 0))
    linha.Layer = 'Linha de Centro'
    inicio = linha.StartPoint
    final = linha.EndPoint
    angs = 0
    coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
    lista_de_LCs[sec_princ] = coord_linhas
 
    #desenha as seções depois da seção principal, SE existirem | se a seção principal for 0 e só tiver uma seção, ignora
    if sec_princ < len(lcs)-1:
        for l in range(sec_princ + 1, len(lista_de_LCs)):
            linha = acad.model.AddLine(APoint(final[0], final[1]), APoint(final[0] + lista_de_LCs[l], final[1]))
            linha.Rotate(APoint(final[0], final[1]), radians(angs_in[l-1] + angs))
            linha.Layer = 'Linha de Centro'
            angs += angs_in[l-1]
            inicio = linha.StartPoint
            final = linha.EndPoint
            
            coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
            lista_de_LCs[l] = coord_linhas
    
    #desenha a primeira seção antes da seção principal, SE existirem
    if sec_princ >= 1:
        linha = acad.model.AddLine(APoint(0 - lista_de_LCs[sec_princ-1], 0), APoint(0, 0))
        linha.Rotate(APoint(0, 0), radians(angs_in[sec_princ-1] * -1))
        linha.Layer = 'Linha de Centro'
        inicio = linha.StartPoint
        final = linha.EndPoint
        angs = angs_in[sec_princ-1]
        coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
        lista_de_LCs[sec_princ-1] = coord_linhas

    #desenha as seções antes da seção principal, SE existirem
        if sec_princ >= 2:
            for l in reversed(range(sec_princ-1)):
                linha = acad.model.AddLine(APoint(inicio[0] - lista_de_LCs[l], inicio[1]), APoint(inicio[0], inicio[1]))
                linha.Rotate(APoint(inicio[0], inicio[1]), radians((angs_in[l] + angs)*-1))
                linha.Layer = 'Linha de Centro'
                angs += angs_in[l]
                inicio = linha.StartPoint
                final = linha.EndPoint
    
                coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
                lista_de_LCs[l] = coord_linhas

    novas_lcs = []
    for linha in acad_ModelSpace:
        if linha.EntityName == 'AcDbLine' and linha.Layer == 'Linha de Centro':
            novas_lcs.append(linha)

    ordem_desenho = ordem_lcs(novas_lcs, sec_princ)
    lista = novas_lcs.copy()

    for index, value in enumerate(ordem_desenho):
        lista[value] = novas_lcs[index]
    return lista_de_LCs, lista


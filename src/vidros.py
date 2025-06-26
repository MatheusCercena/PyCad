"""
Desenha os vidros, através de offsets chamados via COM e fillets por lisp.
"""

from pyautocad import Autocad, APoint
from src.autocad_conn import get_acad
from copy import deepcopy
from math import tan, radians, floor, sqrt

acad, acad_ModelSpace = get_acad()

def offset_vidros(handles_lcs, vidros_sacada, posicao_dos_vidros):
    # offset_ext = 4
    # offset_int = 4

    # handles = {'externos': [], 'internos': []}
    # for linha in handles_lcs:
    #     linha_ext = linha.Offset(offset_ext)#.Offset retorna uma tupla
    #     linha_ext[0].Layer = 'Vidro Externo'
    #     handles['externos'].append(linha_ext[0].Handle)

    #     linha_int = linha.Offset(-offset_int)
    #     linha_int[0].Layer = 'Vidro Interno'
    #     handles['internos'].append(linha_int[0].Handle)
    # return handles

    for i, secao in enumerate(handles_lcs):
        p1 = tuple(map(float, secao.StartPoint))
        p2 = tuple(map(float, secao.EndPoint))

        # p1 = secao.StartPoint  # ponto inicial (x, y, z)
        # p2 = secao.EndPoint    # ponto final

        vetor_linha = (p2[0] - p1[0], p2[1] - p1[1])

        def normalizar(vetor):
            print(f'Vetor {vetor}')
            mag = sqrt(vetor[0]**2 + vetor[1]**2)
            print(f'mag {mag}')
            return (vetor[0]/mag, vetor[1]/mag)

        vetor_unitario = normalizar(vetor_linha)

        def ponto_na_secao(Inicio_secao, vetor_unitario, distancia):
                return (
                    Inicio_secao[0] + vetor_unitario[0] * distancia,
                    Inicio_secao[1] + vetor_unitario[1] * distancia
                )
            
        for index in range(0, len(vidros_sacada[i])):
            comeco_vidro = posicao_dos_vidros[index][0]
            fim_vidro = posicao_dos_vidros[index][1]
            print(f'p1 {p1}')
            print(f'Vetor uni {vetor_unitario}')
            print(f'Comeco vidro {comeco_vidro}')
            inicio = ponto_na_secao(p1, vetor_unitario, comeco_vidro)
            fim = ponto_na_secao(p1, vetor_unitario, fim_vidro)
            acad.model.AddLine(APoint(inicio[0], inicio[1]), APoint(fim[0], fim[1]))

def fillet_vidros(handles):
    linhas_externas = deepcopy(handles['externos'])
    linhas_internas = deepcopy(handles['internos'])

    for index in range(0, len(linhas_externas)-1):
        acad.SendCommand(f'(c:custom_fillet "{linhas_externas[index]}" "{linhas_externas[index+1]}")\n')
        acad.SendCommand(f'(c:custom_fillet "{linhas_internas[index]}" "{linhas_internas[index+1]}")\n')

def calcular_gaps_vidro_vidro(ang):
    '''
    calcula o gap entre o vidro e a linha de centro quando é juncão do tipo vidro-vidro.
    '''
    cat_adj = 4
    gap_vidro = round((tan(radians(abs(ang/2))) * cat_adj), 2)
    return gap_vidro

def definir_folgas_vidros(juncoes: list, gaps_lcs: list, angs_in: list):
    '''
    Retorna uma lista com as folgas de cada secao da sacada, de forma que cada elemento é outra lista com 4 elementos, sendo eles:
    0 - Folga parede esquerdo
    1 - Folga parede direito
    2 - Folga ajuste de angulo esquerdo
    3 - Folga ajuste de angulo direito
    '''
    folga_parede = float(-12) 
    folga_passante = float(2)
    folga_colante = float(-7)
    folga_vidro_vidro = float(-1) 
    juncoes_secoes = deepcopy(juncoes)
    folgas_secoes = []

    for index, secao in enumerate(juncoes_secoes):
        folgas_secao = []
        for lado in range(0, 2):
            if secao[lado] == 0:
                folgas_secao.append(folga_parede)
            elif secao[lado] == 1:
                folgas_secao.append(folga_passante)
            elif secao[lado] == 2:
                folgas_secao.append(folga_colante)
            else:
                folgas_secao.append(folga_vidro_vidro)
        for lado in range(0, 2):
            if index == 0 and lado == 0:
                folgas_secao.append(gaps_lcs[0]) 
            elif index == 0 and lado == 1:
                folgas_secao.append(gaps_lcs[1]) 
            elif index == 1 or index == 2:
                folgas_secao.append(0)
            elif index == 3 and lado == 0:
                folgas_secao.append(calcular_gaps_vidro_vidro(angs_in[index-1]))
            elif index == 3 and lado == 1:
                folgas_secao.append(calcular_gaps_vidro_vidro(angs_in[index]))
        folgas_secoes.append(folgas_secao)

    return folgas_secoes

def pontos_dos_vidros(vidros, folgas):
    folga_vep = float(3)
    todos_pontos = []
    for i, linha_de_centro in enumerate(vidros):
        pos_acumulada = 0
        pontos_linha_de_centro = []
        for index, vidro in enumerate(linha_de_centro):
            pontos = []
            if index == 0:
                pos_inicial = folgas[i][0]*-1 + folgas[i][2]*-1
            if index > 0:
                pos_inicial = pos_acumulada
            pos_final = pos_inicial + vidro
            pos_acumulada = pos_final + folga_vep                
            pontos.append(pos_inicial)
            pontos.append(pos_final)
            pontos_linha_de_centro.append(pontos)
        todos_pontos.append(pontos_linha_de_centro)
    return todos_pontos

def medida_dos_vidros(lcs:list, quant_vidros: list, folgas: list):
    folga_vep = float(3)
    vidros_totais = []

    for i, linha_de_centro in enumerate(lcs):
        folga_esq = folgas[i][0]
        folga_dir = folgas[i][1]
        folga_ajuste_angulo_esq = folgas[i][2]
        folga_ajuste_angulo_dir = folgas[i][3]
        vidros_secao = []

        medida_com_vidro = linha_de_centro + folga_esq + folga_dir - folga_ajuste_angulo_esq - folga_ajuste_angulo_dir 
        medida_com_vidro -= folga_vep*(quant_vidros[i]-1)
        vidros_individuais = floor(medida_com_vidro/quant_vidros[i])
        if quant_vidros[i] > 1:
            medida_ultimo_vidro = int(round((medida_com_vidro - (vidros_individuais*(quant_vidros[i]-1))), 0))
            for vidro in range(quant_vidros[i]-1):
                vidros_secao.append(vidros_individuais)
            vidros_secao.append(medida_ultimo_vidro)
        else:
            vidros_secao.append(vidros_individuais)
        vidros_totais.append(vidros_secao)

    return vidros_totais

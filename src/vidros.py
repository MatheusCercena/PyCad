"""
Desenha os vidros, através de offsets chamados via COM e fillets por lisp.
"""

from src.autocad_conn import get_acad
from copy import deepcopy
from math import tan, radians, floor

acad, acad_ModelSpace = get_acad()

def offset_vidros(handles_lcs):
    offset_ext = 4
    offset_int = 4

    handles = {'externos': [], 'internos': []}
    for linha in handles_lcs:
        linha_ext = linha.Offset(offset_ext)#.Offset retorna uma tupla
        linha_ext[0].Layer = 'Vidro Externo'
        handles['externos'].append(linha_ext[0].Handle)

        linha_int = linha.Offset(-offset_int)
        linha_int[0].Layer = 'Vidro Interno'
        handles['internos'].append(linha_int[0].Handle)
    return handles

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

def medida_dos_vidros(gaps_lcs: list, lcs:list, quant_vidros: list, angs_in: list, juncoes: list):
    folga_parede = float(-12) 
    folga_vep = float(3)
    folga_passante = float(2)
    folga_colante = float(-7)
    folga_vidro_vidro = float(-1) 
    tipos_juncoes = deepcopy(juncoes)
    folgas_juncoes = []
    vidros_totais = []

    for par in tipos_juncoes:
        folgas_esq_dir = []
        for index in range(0, 2):
            if par[index] == 0:
                folgas_esq_dir.append(folga_parede)
            elif par[index] == 1:
                folgas_esq_dir.append(folga_passante)
            elif par[index] == 2:
                folgas_esq_dir.append(folga_colante)
            else:
                folgas_esq_dir.append(folga_vidro_vidro)
        folgas_juncoes.append(folgas_esq_dir)

    for i, par in enumerate(tipos_juncoes):
        folga_esq = folgas_juncoes[i][0]
        folga_dir = folgas_juncoes[i][1]
        folgas_ajuste_de_angulo = []
        for index in range(0, 2):
            if par[index] == 0 and index == 0:
                folgas_ajuste_de_angulo.append(gaps_lcs[0]) 
            elif par[index] == 0 and index == 1:
                folgas_ajuste_de_angulo.append(gaps_lcs[1]) 
            elif par[index] == 1 or par[index] == 2:
                folgas_ajuste_de_angulo.append(0)
            elif par[index] == 3:
                folgas_ajuste_de_angulo.append(calcular_gaps_vidro_vidro(angs_in[i]))
        folga_ajuste_angulo_esq = folgas_ajuste_de_angulo[0]
        folga_ajuste_angulo_dir = folgas_ajuste_de_angulo[1]
        print(f"Lcs: {lcs[i]}, folga_esq: {folga_esq}, folga_dir: {folga_dir}, folga_ajuste_angulo_esq: {folga_ajuste_angulo_esq}, folga_ajuste_angulo_dir: {folga_ajuste_angulo_dir}")

        medida_com_vidro = lcs[i] + folga_esq + folga_dir - folga_ajuste_angulo_esq - folga_ajuste_angulo_dir 
        print(medida_com_vidro)
        medida_com_vidro -= folga_vep*(quant_vidros[i]-1)
        print(medida_com_vidro)
        vidros_individuais = floor(medida_com_vidro/quant_vidros[i])
        print(vidros_individuais)
        if quant_vidros[i] > 1:
            medida_ultimo_vidro = int(round((medida_com_vidro - (vidros_individuais*(quant_vidros[i]-1))), 0))
            for vidro in range(quant_vidros[i]-1):
                vidros_totais.append(vidros_individuais)
            vidros_totais.append(medida_ultimo_vidro)
        else:
            vidros_totais.append(vidros_individuais)
    return vidros_totais


# SUGESTAO: PEGAR AS COORDENAS DEPOIS DO FILLET DE CIMA, CALCULAR AS LINHAS, DEPOIS APAGAR A LINHA INTEIRA E DESENHAR AS INDIVIDUAIS E DAR OFFSET DE 8 PRA BAIXO
# DEPOIS, COM A MEDIDA DOS PERFIS E MATERIAIS, COMECAR A COLOCAR NO ECG COM SELENIUM


    # for index, lado in enumerate(lcs):
    #     folga_esq = folgas_juncoes[index][0]
    #     folga_dir = folgas_juncoes[index][1]

    #     if index == 0 and len(lcs) == 1:
    #         print('1')
    #         folga_ajuste_angulo_esq = gaps_lcs[0]
    #         folga_ajuste_angulo_dir = gaps_lcs[1]
    #     elif 70 < (abs(angs_in[index])) < 110:
    #         if index == 0 and len(lcs) > 1:
    #             print('2')
    #             folga_ajuste_angulo_esq = gaps_lcs[0]
    #             folga_ajuste_angulo_dir = 0
    #         elif index == (len(lcs) -1):
    #             print('3')
    #             folga_ajuste_angulo_esq = 0
    #             folga_ajuste_angulo_dir = 0
    #         else: 
    #             print('4')
    #             folga_ajuste_angulo_esq = 0
    #             folga_ajuste_angulo_dir = gaps_lcs[1]
    #     else:
    #         if index == 0 and len(lcs) > 1:
    #             print('5')
    #             folga_ajuste_angulo_esq = gaps_lcs[0]
    #             folga_ajuste_angulo_dir = calcular_gaps_vidro_vidro(angs_in[index])
    #         elif index == (len(lcs) -1):
    #             print('6')
    #             folga_ajuste_angulo_esq = calcular_gaps_vidro_vidro(angs_in[index-1])
    #             folga_ajuste_angulo_dir = gaps_lcs[1]
    #         else: 
    #             print('7')
    #             folga_ajuste_angulo_esq = calcular_gaps_vidro_vidro(angs_in[index-1])
    #             folga_ajuste_angulo_dir = calcular_gaps_vidro_vidro(angs_in[index])
        
    #     print(f"folga_esq: {folga_esq}, folga_dir: {folga_dir}, folga_ajuste_angulo_esq: {folga_ajuste_angulo_esq}, folga_ajuste_angulo_dir: {folga_ajuste_angulo_dir}")

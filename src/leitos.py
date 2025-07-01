"""
Desenha os leitos, através de offsets chamados via COM e fillets por lisp.
"""
from pyautocad import Autocad, APoint
from src.autocad_conn import get_acad
from math import sqrt, tan, radians

acad2 = Autocad(create_if_not_exists=True)
acad, acad_ModelSpace = get_acad()

def normalizar(vetor):
    vetor_unitario = sqrt(vetor[0]**2 + vetor[1]**2)
    vetor_unitario_x = vetor[0]/vetor_unitario
    vetor_unitario_y = vetor[1]/vetor_unitario
    
    return (vetor_unitario_x, vetor_unitario_y)

def definir_pontos_na_secao(Inicio_secao, vetor_unitario, distancia):
        return (
            Inicio_secao[0] + vetor_unitario[0] * distancia,
            Inicio_secao[1] + vetor_unitario[1] * distancia
        )

def desenhar_guias_leitos(handles_lcs: list, vidros_sacada: list, posicao_dos_vidros: list, folgas_leitos: list):
    for i, linha_de_centro in enumerate(handles_lcs):
        
        ini_linha_de_centro = linha_de_centro.StartPoint
        fim_linha_de_centro = linha_de_centro.EndPoint

        vetor_linha = (fim_linha_de_centro[0] - ini_linha_de_centro[0], fim_linha_de_centro[1] - ini_linha_de_centro[1])
        vetores_unitarios = normalizar(vetor_linha)

        for index in range(0, len(vidros_sacada[i])):
            comeco_vidro = posicao_dos_vidros[i][index][0]
            fim_vidro = posicao_dos_vidros[i][index][1]
            inicio = definir_pontos_na_secao(ini_linha_de_centro, vetores_unitarios, comeco_vidro + folgas_leitos[i][index][1])
            fim = definir_pontos_na_secao(ini_linha_de_centro, vetores_unitarios, fim_vidro - folgas_leitos[i][index][1])
            acad2.model.AddLine(APoint(inicio[0], inicio[1]), APoint(fim[0], fim[1]))

def calcular_gaps_leito(ang):
    '''
    calcula o gap entre os leitos e a linha de centro quando é juncão do tipo vidro-vidro.
    '''
    cat_adj = 14
    gap_leito = round((tan(radians(abs(ang/2))) * cat_adj), 2)
    return gap_leito

def folgas_leitos(vidros, folgas_vidros, angs_in, gaps_lcs):
    '''
    Calcula as folgas dos leitos para cada vidro em cada seção da sacada.
    
    vidros: lista de listas, cada sublista representa os vidros de uma seção
    folgas_vidros: mesma estrutura que vidros, mas com folgas esquerda/direita
    angs_in: lista com ângulos de entrada das seções
    gaps_lcs: lista com valores de gap (folga) por seção e lado
    '''
    folgas_leitos_sacada = []
    for secao in range(len(vidros)):
        folgas_leitos_secao = []
        for index in range(len(vidros[secao])):
            folgas_leitos_vidro = []
            for lado in range(2):
                if lado == 0:
                    if index == 0:
                        if folgas_vidros[secao][index][0] == 2:
                            folga_esq = calcular_gaps_leito(angs_in[secao-1]) - 1
                        elif folgas_vidros[secao][index][0] == -7:
                            folga_esq = calcular_gaps_leito(angs_in[secao-1])
                        elif folgas_vidros[secao][index][0] == 1:
                            folga_esq = gaps_lcs[secao][0]
                            if angs_in[secao-1] < 20:
                                folga_esq += 1.5
                        else:
                            folga_esq = 1.5
                    else:
                        folga_esq = 1.5
                    folgas_leitos_vidro.append(folga_esq)
                if lado == 1:
                    if folgas_vidros[secao][index][1] == 2:
                        folga_dir = calcular_gaps_leito(angs_in[secao]) - 1
                    elif folgas_vidros[secao][index][1] == -7:
                        folga_dir = calcular_gaps_leito(angs_in[secao])
                    elif folgas_vidros[secao][index][1] == 1:
                        folga_dir = gaps_lcs[secao][1]
                        if angs_in[secao-1] < 20:
                            folga_dir += 1.5
                    else:
                        folga_dir = 1.5
                    folgas_leitos_vidro.append(folga_dir)
            folgas_leitos_secao.append(folgas_leitos_vidro)
        folgas_leitos_sacada.append(folgas_leitos_secao)
    return folgas_leitos_sacada

# [
# [[12.0, 337.0], [340.0, 665.0], [668.0, 993.0]], 
# [[-2.0, 395.0], [398.0, 795.0], [798.0, 1195.0], [1198.0, 1595.0], [1598.0, 1997.0]], 
# [[2.66, 396.66], [399.66, 793.66], [796.66, 1190.66], [1193.66, 1587.66], [1590.66, 1987.66]]
# ]

# def desenhar_leitos(folgas_leito, vidros, folgas_vidros, angs_in, gaps_lcs):
#     for linha in acad_ModelSpace:
#         if linha.EntityName == 'AcDbLine' and linha.Layer == '0':
#             ext = linha.Offset(14)
#             handles_leitos['externos'].append(ext.Handle)
#             ext.Layer = 'Leito Externo'
#             int = linha.Offset(-14)
#             handles_leitos['internos'].append(int.Handle)
#             ext.Layer = 'Leito Interno'

#         # if 
#             ext_ini = ext.StartPoint
#             int_ini = int.StartPoint
#             lat_esq = acad2.model.AddLine(APoint(ext_ini[0], ext_ini[1]), APoint(int_ini[0], int_ini[1]))
#             ext_fim = ext.EndPoint
#             int_fim = int.EndPoint
#             lat_dir = acad2.model.AddLine(APoint(ext_fim[0], ext_fim[1]), APoint(int_fim[0], int_fim[1]))
#             int.Layer = lat_esq.Layer = lat_dir.Layer = 'Leito Interno'
#     return handles_leitos


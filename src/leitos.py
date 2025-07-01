"""
Desenha os leitos, através de offsets chamados via COM e fillets por lisp.
"""
from pyautocad import Autocad, APoint
from src.autocad_conn import get_acad
from copy import deepcopy
from math import sqrt

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

def desenhar_guias_leitos(handles_lcs: list, vidros_sacada: list, posicao_dos_vidros: list):
    for i, linha_de_centro in enumerate(handles_lcs):
        
        ini_linha_de_centro = linha_de_centro.StartPoint
        fim_linha_de_centro = linha_de_centro.EndPoint

        vetor_linha = (fim_linha_de_centro[0] - ini_linha_de_centro[0], fim_linha_de_centro[1] - ini_linha_de_centro[1])
        vetores_unitarios = normalizar(vetor_linha)

        for index in range(0, len(vidros_sacada[i])):
            comeco_vidro = posicao_dos_vidros[i][index][0]
            fim_vidro = posicao_dos_vidros[i][index][1]
            inicio = definir_pontos_na_secao(ini_linha_de_centro, vetores_unitarios, comeco_vidro + 1.5)
            fim = definir_pontos_na_secao(ini_linha_de_centro, vetores_unitarios, fim_vidro - 1.5)
            acad2.model.AddLine(APoint(inicio[0], inicio[1]), APoint(fim[0], fim[1]))

# def definir_leitos():
#     folgas_lados = []
#     for secao in folgas_vidros:
#         folgas_leitos_secao = []
#         for index, vidro in enumerate(vidros[secao]):
#             folgas = []
#             for lado in range(2):
#                 if lado == 0:

def offset_leitos(vidros, folgas_vidros, angs_in):
    handles_leitos = {'externos': '', 'internos': ''}
    folgas_lados = []
    for secao in folgas_vidros:
        folgas_leitos_secao = []
        for index, vidro in enumerate(vidros[secao]):
            folgas = []
            for lado in range(2):
                if lado == 0:
                    if index == 0:
                        if folgas_vidros[secao][0] in (0, 12, -12, 7):
                            folgas = [1.5]
                            folgas_leitos_secao.append(folgas)
                        if folgas_vidros[secao][0] == 2:
                            folgas = []
                            #folgas = logica_para_passante_colante()
                            folgas_leitos_secao.append(folgas)
                        if folgas_vidros[secao][0] == -7:
                            folgas = []
                            #folgas = logica_para_passante_colante()
                            folgas_leitos_secao.append(folgas)
                        if folgas_vidros[secao][0] == -1:
                            folgas = []
                            #folgas = logica_para_passante_colante()
                            folgas_leitos_secao.append(folgas)
                    else:
                        pass
                        #logica_para_curvas()
                if lado == 1:

                
                 
    # for linha in acad_ModelSpace:
    #     if linha.EntityName == 'AcDbLine' and linha.Layer == '0':
    #         ext = linha.Offset(14)
    #         handles_leitos['externos'].append(ext.Handle)
    #         ext.Layer = 'Leito Externo'
    #         int = linha.Offset(-14)
    #         handles_leitos['internos'].append(int.Handle)
    #         ext.Layer = 'Leito Interno'

    #     # if 
    #         ext_ini = ext.StartPoint
    #         int_ini = int.StartPoint
    #         lat_esq = acad2.model.AddLine(APoint(ext_ini[0], ext_ini[1]), APoint(int_ini[0], int_ini[1]))
    #         ext_fim = ext.EndPoint
    #         int_fim = int.EndPoint
    #         lat_dir = acad2.model.AddLine(APoint(ext_fim[0], ext_fim[1]), APoint(int_fim[0], int_fim[1]))
    #         int.Layer = lat_esq.Layer = lat_dir.Layer = 'Leito Interno'
    return handles_leitos

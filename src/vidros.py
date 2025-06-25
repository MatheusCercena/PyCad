"""
Desenha os vidros, através de offsets chamados via COM e fillets por lisp.
"""

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

    for secao in handles_lcs():
        secao = acad.doc.HandleToObject(secao)  
        p1 = secao.StartPoint  # ponto inicial (x, y, z)
        p2 = secao.EndPoint    # ponto final

        vetor_linha = (p2[0] - p1[0],p2[1] - p1[1], p2[2] - p1[2])

        def normalizar(vetor):
            mag = sqrt(vetor[0]**2 + vetor[1]**2 + vetor[2]**2)
            return (vetor[0]/mag, vetor[1]/mag, vetor[2]/mag)

        vetor_unitario = normalizar(vetor_linha)

        def ponto_na_secao(Inicio_secao, vetor_unitario, distancia):
                return (
                    Inicio_secao[0] + vetor_unitario[0]*distancia,
                    Inicio_secao[1] + vetor_unitario[1]*distancia,
                    Inicio_secao[2] + vetor_unitario[2]*distancia
                )
            
        for vidro in vidros_sacada[secao]:
            comeco_vidro = posicao_dos_vidros[vidro][0]
            fim_vidro = posicao_dos_vidros[vidro][1]
            inicio = ponto_na_secao(p1, vetor_unitario, comeco_vidro)
            fim = ponto_na_secao(p1, vetor_unitario, fim_vidro)

def pontos_dos_vidros():
    
    
    pass

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
    folga_parede = float(-12) 
    folga_passante = float(2)
    folga_colante = float(-7)
    folga_vidro_vidro = float(-1) 
    juncoes_secoes = deepcopy(juncoes)
    folgas_juncoes = []

    for i in range(0, len(juncoes_secoes)):
        if i == 0:
            folgas_juncoes.append(folga_parede)
        elif i == 1:
            juncoes_secoes[i].append(folga_passante)
        elif par[index] == 2:
            juncoes_secoes[i].append(folga_colante)
        else:
            juncoes_secoes[i].append(folga_vidro_vidro)

    for i in range(0, len(juncoes_secoes)):
        for index in range(0, 2):
            if par[index] == 0 and index == 0:
                folgas_ajuste_de_angulo.append(gaps_lcs[0]) 
            elif par[index] == 0 and index == 1:
                folgas_ajuste_de_angulo.append(gaps_lcs[1]) 
            elif par[index] == 1 or par[index] == 2:
                folgas_ajuste_de_angulo.append(0)
            elif par[index] == 3 and index == 0:
                folgas_ajuste_de_angulo.append(calcular_gaps_vidro_vidro(angs_in[i-1]))
            elif par[index] == 3 and index == 1:
                folgas_ajuste_de_angulo.append(calcular_gaps_vidro_vidro(angs_in[i]))

        folga_ajuste_angulo_esq = folgas_ajuste_de_angulo[0]
        folga_ajuste_angulo_dir = folgas_ajuste_de_angulo[1]
        print(f"Secao: {i} folga_esq: {folga_esq}, folga_dir: {folga_dir}, folga_ajuste_angulo_esq: {folga_ajuste_angulo_esq}, folga_ajuste_angulo_dir: {folga_ajuste_angulo_dir}")


def medida_dos_vidros(lcs:list, quant_vidros: list, folgas):
    folga_vep = float(3)
    folga_esq = folgas[0]
    folga_dir = folgas[1]
    folga_ajuste_angulo_esq = folgas[2]
    folga_ajuste_angulo_dir = folgas[3]
    vidros_secao = []
    vidros_totais = []

    for i, linha_de_centro in enumerate(lcs):
        medida_com_vidro = linha_de_centro + folga_esq + folga_dir - folga_ajuste_angulo_esq - folga_ajuste_angulo_dir 
        print(medida_com_vidro)
        medida_com_vidro -= folga_vep*(quant_vidros[i]-1)
        print(medida_com_vidro)
        vidros_individuais = floor(medida_com_vidro/quant_vidros[i])
        print(vidros_individuais)
        if quant_vidros[i] > 1:
            medida_ultimo_vidro = int(round((medida_com_vidro - (vidros_individuais*(quant_vidros[i]-1))), 0))
            for vidro in range(quant_vidros[i]-1):
                vidros_secao.append(vidros_individuais)
            vidros_secao.append(medida_ultimo_vidro)
        else:
            vidros_secao.append(vidros_individuais)
        vidros_totais.append(vidros_secao)

    return vidros_totais




# SUGESTAO: PEGAR AS COORDENAS DEPOIS DO FILLET DE CIMA, CALCULAR AS LINHAS, DEPOIS APAGAR A LINHA INTEIRA E DESENHAR AS INDIVIDUAIS E DAR OFFSET DE 8 PRA BAIXO
# DEPOIS, COM A MEDIDA DOS PERFIS E MATERIAIS, COMECAR A COLOCAR NO ECG COM SELENIUM

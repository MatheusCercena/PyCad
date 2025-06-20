"""
Realiza uma série de calculos sobre a lista de linhas de centro para definir qual delas será a seção principal a ser usada para realocar as seções após estas serem definidas, para desenhar as linhas seguindo um sentido de visualização idealizado.
"""

from sympy import symbols, Eq, solve
from math import sqrt, pow

x, y, b = symbols('x y b')

def definir_linha_perpendicular(pos_lcs):
    '''
    a partir de uma lista de linhas de centro (pos_lcs) define os pontos da coordenada C, assumindo B como coordenada 0,0 (inicial), B como coordenada do meio da linha guia e assumindo C como as coordenadas pertencentes aos dois valores possiveis da reta AC, perpendicular a reta AB com comprimento de 50.000mm.
    tem o objetivo de permitir verificar qual a linha de centro que intercepta a RETA formada pelos dois pontos de C.
    '''
    l_guia_ini = pos_lcs[0][0], pos_lcs[0][1]
    l_guia_fin = pos_lcs[len(pos_lcs)-1][2], pos_lcs[len(pos_lcs)-1][3]
    ini_reta_perp = [(l_guia_fin[0] - l_guia_ini[0])/2, (l_guia_fin[1] - l_guia_ini[1])/2]
    #calculando vetor_AB
    vetor_AB = ini_reta_perp[0] - l_guia_ini[0], ini_reta_perp[1] - l_guia_ini[1] 
    vetor_AB_perp1 = vetor_AB[1]*-1, vetor_AB[0]
    vetor_AB_perp2 = vetor_AB[1], vetor_AB[0]*-1
    comp_AC = 50000
    #normalizando vetor_AB_perp1 e multiplicando por AC
    vetor_AB1_norm = sqrt(pow(vetor_AB_perp1[0], 2) + pow(vetor_AB_perp1[1], 2))
    vetor_AB1_unit = vetor_AB_perp1[0]/vetor_AB1_norm, vetor_AB_perp1[1]/vetor_AB1_norm
    vetor_AC1 = vetor_AB1_unit[0]*comp_AC, vetor_AB1_unit[1]*comp_AC
    coord_c1 = ini_reta_perp[0] + vetor_AC1[0], ini_reta_perp[1] + vetor_AC1[1]
    #normalizando vetor_AB_perp2 e multiplicando por AC
    vetor_AB2_norm = sqrt(pow(vetor_AB_perp2[0], 2) + pow(vetor_AB_perp2[1], 2))
    vetor_AB2_unit = vetor_AB_perp2[0]/vetor_AB2_norm, vetor_AB_perp2[1]/vetor_AB2_norm
    vetor_AC2 = vetor_AB2_unit[0]*comp_AC, vetor_AB2_unit[1]*comp_AC
    coord_c2 = ini_reta_perp[0] + vetor_AC2[0], ini_reta_perp[1] + vetor_AC2[1]

    return coord_c1[0], coord_c1[1], coord_c2[0], coord_c2[1]

def def_eq_reta(secao):
    '''
    define a equação da reta a ser usada para verificar se a seção intercepta a linha perpendicular
    '''
    valor_m = (secao[3] - secao[1]) / (secao[2] - secao[0])
    y_f = secao[3]
    x_f = secao[2]
    eq_b = Eq(y_f, valor_m*x_f + b)
    valor_b = solve(eq_b, b)[0]

    return Eq(y, valor_m*x + valor_b)
   
def verificar_se_intercepta(secao, interseccao):
    '''
    secao = seção que se quer saber se intercepta a linha guia
    interseccao = dicionario com chaves x e y
    A funcao verifica se os eixos x e y da secao interceptam a guia e retorna true ou false
    '''
    intervalo_x = sorted([secao[0], secao[2]])
    intervalo_y = sorted([secao[1], secao[3]])
    
    condicao1 = intervalo_x[0] <= interseccao[x] <= intervalo_x[1]
    condicao2 = intervalo_y[0] <= interseccao[y] <= intervalo_y[1]

    if condicao1 and condicao2 == True: 
        return True
    else:
        return False

def descobrir_secao_principal(pos_lcs):
    '''
    descobre a linha de centro principal dentro de uma lista de linhas de centro (pos_lcs).
    '''
    # Se houver apenas uma seção, retorna 0 automaticamente
    if len(pos_lcs) == 1:
        return 0
    else:
        coord_c = definir_linha_perpendicular(pos_lcs)
        for secao in range(0, len(pos_lcs)):
            interseccao = solve((def_eq_reta(pos_lcs[secao]), def_eq_reta(coord_c)), (x, y))
            verificacao = verificar_se_intercepta(pos_lcs[secao], interseccao)
            if verificacao == True: 
                return int(secao)
            else:
                continue
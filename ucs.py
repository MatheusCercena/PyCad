from sympy import symbols, Eq, solve
from math import sqrt, pow

x, y, b = symbols('x y b')
pos_lcs = [[0, 0, 1000, 0], [1000, 0, 2879.3852415718166, -684.0402866513374], [2879.3852415718166, -684.0402866513374, 5000.70558513146, -2805.36063021098]]

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
    valor_m = (secao[3] - secao[1]) / (secao[2] - secao[0])
    y_f = secao[3]
    x_f = secao[2]
    eq_b = Eq(y_f, valor_m*x_f + b)
    valor_b = solve(eq_b, b)[0]

    return Eq(y, valor_m*x + valor_b)

def verificar_se_intercepta_x(secao1, secao2, interseccao):
    '''
    secao1 = seção
    secao2 = linha guia perpendicular
    '''

    intervalo_1_x = sorted([secao1[0], secao1[2]])
    intervalo_1_y = sorted([secao1[1], secao1[3]])
    intervalo_2_x = sorted([secao2[0], secao2[2]])
    intervalo_2_y = sorted([secao2[1], secao2[3]])
    interseccao = sorted(interseccao.values())

    condicao1 = intervalo_1_x[0] <= interseccao[0] <= intervalo_1_x[1]
    condicao2 = intervalo_1_y[0] <= interseccao[0] <= intervalo_1_y[1]
    condicao3 = intervalo_2_x[0] <= interseccao[1] <= intervalo_2_x[1]
    condicao4 = intervalo_2_y[0] <= interseccao[1] <= intervalo_2_y[1]

    if condicao1 and condicao2 and condicao3 and condicao4 == True: 
        return True
    else:
        return False
    
def verificar_se_intercepta(secao1, secao2, interseccao):
    '''
    seção = seção
    guia = linha guia perpendicular
    '''
    intervalo_1_x = sorted([secao1[0], secao1[2]])
    intervalo_1_y = sorted([secao1[1], secao1[3]])
    intervalo_2_x = sorted([secao2[0], secao2[2]])
    intervalo_2_y = sorted([secao2[1], secao2[3]])
    interseccao = sorted(interseccao.values())

    condicao1 = intervalo_1_x[0] <= interseccao[0] <= intervalo_1_x[1]
    condicao2 = intervalo_1_y[0] <= interseccao[1] <= intervalo_1_y[1]
    condicao3 = intervalo_2_x[0] <= interseccao[0] <= intervalo_2_x[1]
    condicao4 = intervalo_2_y[0] <= interseccao[1] <= intervalo_2_y[1]

    if condicao1 and condicao2 and condicao3 and condicao4 == True: 
        return True
    else:
        return False


s1 = [0, 0, 1, 2]
s2 = [2, 0, 0, 1]
    
# interseccao = solve((def_eq_reta(s1), def_eq_reta(s2)), (x, y))
# print(verificar_se_intercepta_x(s1, s2, interseccao))
# print(interseccao)



coord_c = definir_linha_perpendicular(pos_lcs)

interseccao = solve((def_eq_reta(pos_lcs[2]), def_eq_reta(coord_c)), (x, y))
v = verificar_se_intercepta(pos_lcs[2], coord_c, interseccao)

print(interseccao)
print(v)

# for linha_de_centro in pos_lcs:
#     interseccao = solve((def_eq_reta(pos_lcs[0]), def_eq_reta(coord_c)), (x, y))
#     verificar_se_intercepta_x(linha_de_centro, s2, interseccao)

from sympy import symbols, Eq, solve

x, y, b = symbols('x y b')

def definir_linha_perpendicular(pos_lcs):
    l_guia_ini = pos_lcs[0][0], pos_lcs[len(pos_lcs-1)][0]
    l_guia_fin = pos_lcs[0][1], pos_lcs[len(pos_lcs-1)][1]
    ini_reta_perp = (l_guia_ini[0] + l_guia_ini[1])/2, (l_guia_fin[0] + l_guia_fin[1])/2
#outras solucoes
#https://www.reddit.com/r/askmath/comments/1inbz4v/how_to_find_coordinates_of_third_point_of_a/?tl=pt-br
#Encontre a equação da reta perpendicular: A reta perpendicular tem um declive que é o inverso negativo da reta original. 

def def_eq_reta(secao):
    valor_m = (secao[3] - secao[1]) / (secao[2] - secao[0])
    y_f = secao[3]
    x_f = secao[2]
    eq_b = Eq(y_f, valor_m*x_f + b)
    valor_b = solve(eq_b, b)[0]

    return Eq(y, valor_m*x + valor_b)


def verificar_se_intercepta_x(secao1, secao2, interseccao):

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

s1 = [0, 0, 1, 2]
s2 = [2, 0, 0, 1]
    

interseccao = solve((def_eq_reta(s1), def_eq_reta(s2)), (x, y))

verificar_se_intercepta_x(s1, s2, interseccao)

for linha_de_centro in pos_lcs:

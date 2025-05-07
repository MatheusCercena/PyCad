from math import cos, sin, radians

pos_lcs = [[0, 0, 1000, 0], [1000, 0, 2879.3852415718166, -684.0402866513374], [2879.3852415718166, -684.0402866513374, 5000.70558513146, -2805.36063021098]]
angs_in = [10, 20]

def readequar_linhas_de_centro(lcs, angs_in):
    '''
    Define as posições iniciais e finais nos eixos x e y para cada uma das linhas de centro entregues no parametro lcs.\n
    lcs: do tipo list(), com as linhas de centro a serem definidas\n
    angs_in: do tipo list(), com os angulos internos entre cada linha de centro. Note que angs_in[0] equivale ao angulo entre lcs[0] e lcs[1]\n
    return: retorna as posições definidas para cada linha de centro.
    '''
    x = 2
    lista_de_LCs = []
    pos_xi = 0
    pos_yi = 0
    pos_xf = lcs[0]
    pos_yf = 0
    lc = [pos_xi, pos_yi, pos_xf, pos_yf]

    lista_de_LCs.append(lc)
    ang_in = 0

    for c in range(x, len(lcs)):
        pos_xi = pos_xf
        pos_yi = pos_yf
        pos_xf += cos(radians(angs_in[c-1] + ang_in))*lcs[c]
        pos_yf += sin(radians(angs_in[c-1] + ang_in))*lcs[c]
        ang_in += angs_in[c-1]
        lc = [pos_xi, pos_yi, pos_xf, pos_yf]
        lista_de_LCs[c] = lc

    pos_xf = 0
    pos_yf = 0
    pos_xi = sin(radians(angs_in[x-1] + ang_in))*lcs[c]
    pos_yi = sin(radians(angs_in[x-1] + ang_in))*lcs[c]
    
    for c in range(0, x, reversed):
        pos_xf = pos_xi[c]
        pos_yf = pos_yi[c]
        pos_xi -= cos(radians(angs_in[c-1] + ang_in))*lcs[c]
        pos_yi -= sin(radians(angs_in[c-1] + ang_in))*lcs[c]
        ang_in += angs_in[c-1]
        lc = [pos_xi, pos_yi, pos_xf, pos_yf]
        lista_de_LCs[c] = lc




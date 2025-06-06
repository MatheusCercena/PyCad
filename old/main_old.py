from pyautocad import Autocad, APoint
from math import radians, sin, cos
from old.find_main_section_old import descobrir_secao_principal

acad = Autocad(create_if_not_exists=True)

lcs = []#linhas de centro
angs_ex = []#angulos externos(1 esq(angs_ex[0]), 1 dir(angs_ex[1]))
angs_in = []#angulos internos(quantidade elementos == len(lcs)-1)
prumos = []#prumos

def pedir_lcs():
    cont = 1
    while True:
        lc_secoes = int(input(f'Digite a linha de centro da S{cont}: '))
        lcs.append(lc_secoes)
        cont +=1
        res = input('Deseja digitar outra linha de centro? Digite enter para sim ou qualquer tecla para não:')
        if res != '':
            break

def pedir_angSecoes(qntd):
    for c in range(0, qntd-1):
        ang_sec = int(input(f'Qual o angulo entre a S{c+1} e a S{c+2}: '))
        angs_in.append(ang_sec*-1)

def definir_linhas_de_centro(lcs, angs_in):
    '''
    Define as posições iniciais e finais nos eixos x e y para cada uma das linhas de centro entregues no parametro lcs.\n
    lcs: do tipo list(), com as linhas de centro a serem definidas\n
    angs_in: do tipo list(), com os angulos internos entre cada linha de centro. Note que angs_in[0] equivale ao angulo entre lcs[0] e lcs[1]\n
    return: retorna as posições definidas para cada linha de centro.
    '''
    lista_de_LCs = []
    pos_xi = 0
    pos_yi = 0
    pos_xf = lcs[0]
    pos_yf = 0
    lc = [pos_xi, pos_yi, pos_xf, pos_yf]
    lista_de_LCs.append(lc)
    ang_in = 0

    for c in range(1, len(lcs)):
        pos_xi = pos_xf
        pos_yi = pos_yf
        pos_xf += cos(radians(angs_in[c-1] + ang_in))*lcs[c]
        pos_yf += sin(radians(angs_in[c-1] + ang_in))*lcs[c]
        ang_in += angs_in[c-1]
        lc = [pos_xi, pos_yi, pos_xf, pos_yf]
        lista_de_LCs.append(lc)

    return lista_de_LCs

def definir_linhas_de_centro_reduzida(lcs, angs_in):
    pass

def readequar_linhas_de_centro(lcs, pos_lcs, angs_in, sec_princ):
    '''
    Define as posições iniciais e finais nos eixos x e y para cada uma das linhas de centro entregues no parametro lcs.\n
    lcs: do tipo list(), com as linhas de centro a serem definidas\n
    angs_in: do tipo list(), com os angulos internos entre cada linha de centro. Note que angs_in[0] equivale ao angulo entre lcs[0] e lcs[1]\n
    return: retorna as posições definidas para cada linha de centro.
    '''
    print(pos_lcs)
    print(sec_princ)
    lista_de_LCs = pos_lcs
    pos_xi = 0
    pos_yi = 0
    pos_xf = lcs[sec_princ]
    pos_yf = 0
    lc = [pos_xi, pos_yi, pos_xf, pos_yf]
    lista_de_LCs[sec_princ] = lc

    ang_in = 0

    if sec_princ < len(pos_lcs)-1:
        for c in range(sec_princ+1, len(lcs)):
            pos_xi = pos_xf
            pos_yi = pos_yf
            pos_xf += cos(radians(angs_in[c-1] + ang_in))*lcs[c]
            pos_yf += sin(radians(angs_in[c-1] + ang_in))*lcs[c]
            ang_in += angs_in[c-1]
            lc = [pos_xi, pos_yi, pos_xf, pos_yf]
            lista_de_LCs[c] = lc

    if sec_princ >= 1:

        pos_xi = cos(radians(angs_in[sec_princ-1]))*lcs[sec_princ-1]*-1
        pos_yi = -sin(radians(angs_in[sec_princ-1]))*lcs[sec_princ-1]*-1
        pos_xf = 0
        pos_yf = 0
        lc = [pos_xi, pos_yi, pos_xf, pos_yf]
        lista_de_LCs[sec_princ-1] = lc

        ang_in = angs_in[sec_princ-1]

    if sec_princ >= 2:
        for c in reversed(range(sec_princ-1)):
            # pos_xf = pos_xi
            # pos_yf = pos_yi
            # pos_xi = cos(radians(angs_in[c] + ang_in))*lcs[c]*-1
            # pos_yi = -sin(radians(angs_in[c] + ang_in))*lcs[c]*-1
            # ang_in += angs_in[c-1]
            # lc = [pos_xi, pos_yi, pos_xf, pos_yf]
            # lista_de_LCs[c] = lc  
            pos_In_x = pos_xi
            pos_In_y = pos_yi
            pos_Fi_x = pos_xi-lcs[c]
            pos_Fi_y = pos_yi
            lc = [pos_In_x, pos_In_y, pos_Fi_x, pos_Fi_y]
            s1 = acad.model.AddLine(APoint(lc[0], lc[1]), APoint(lc[2], lc[3]))
            s1.Rotate(APoint(lc[0], lc[1]), radians(angs_in[c]+ang_in))


    print(lista_de_LCs)
    return lista_de_LCs

def desenhar_linhas_de_centro(pos_lcs):
    '''
    Desenha as linhas de centro da instancia aberta de Autocad, de acordo com as respectivas coordenadas passadas no parametro pos_lcs.\n
    pos_lcs: do tipo list(), com as coordenadas das linhas de centro a serem desenhadas.
    '''
    for lc in pos_lcs:
        acad.model.AddLine(APoint(lc[0], lc[1]), APoint(lc[2], lc[3]))
    

pedir_lcs()
pedir_angSecoes(len(lcs))
pos_lcs = definir_linhas_de_centro(lcs, angs_in)
sec_princ = descobrir_secao_principal(pos_lcs)
pos_lcs = readequar_linhas_de_centro(lcs, pos_lcs, angs_in, sec_princ)
desenhar_linhas_de_centro(pos_lcs)


# def pedir_angParedes():
#     ang_esq = int(input(f'Digite o angulo da extremidade esquerda: '))
#     ang_dir = int(input(f'Digite o angulo da extremidade direita: '))
#     angs_ex.append(ang_esq)
#     angs_ex.append(ang_dir)
# def pedir_prumos():
#     prumo_esq = int(input(f'Digite o angulo da extremidade esquerda: '))
#     prumos.append(prumo_esq)
#     prumo_dir = int(input(f'Digite o angulo da extremidade direita: '))
#     prumos.append(prumo_dir)



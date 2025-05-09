from pyautocad import Autocad, APoint
from math import radians, sin, cos
from find_main_section import descobrir_secao_principal

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
        ang_sec = float(input(f'Qual o angulo entre a S{c+1} e a S{c+2}: '))
        angs_in.append(ang_sec*-1)

def definir_linhas_de_centro(lcs, angs_in):
    '''
    Define as posições iniciais e finais nos eixos x e y para cada uma das linhas de centro entregues no parametro lcs.\n
    lcs: do tipo list(), com as linhas de centro a serem definidas\n
    angs_in: do tipo list(), com os angulos internos entre cada linha de centro. Note que angs_in[0] equivale ao angulo entre lcs[0] e lcs[1]\n
    return: retorna as posições definidas para cada linha de centro.
    '''
    lista_de_LCs = lcs
    linha = acad.model.AddLine(APoint(0, 0), APoint(lcs[0], 0))
    inicio = linha.StartPoint
    final = linha.EndPoint
    angs = 0
    coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
    coord_de_linhas_de_centro = []
    coord_de_linhas_de_centro.append(coord_linhas)
    linha.Delete()


    for l in range(1, len(lista_de_LCs)):
        linha = acad.model.AddLine(APoint(final[0], final[1]), APoint(final[0] + lista_de_LCs[l], final[1]))
        linha.Rotate(APoint(final[0], final[1]), radians(angs_in[l-1] + angs))
        angs += angs_in[l-1]
        inicio = linha.StartPoint
        final = linha.EndPoint
        
        coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
        coord_de_linhas_de_centro.append(coord_linhas)
        linha.Delete()

    return coord_de_linhas_de_centro

def redesenhar_linhas_de_centro(lcs, angs_in, sec_princ):
    '''
    Desenha as linhas de centro na instancia de AutoCad e retorna uma lista com as posições iniciais e finais nos eixos x e y para cada uma das linhas de centro entregues no parametro lcs.\n
    lcs: do tipo list(), com as linhas de centro a serem definidas\n
    angs_in: do tipo list(), com os angulos internos entre cada linha de centro. Note que angs_in[0] equivale ao angulo entre lcs[0] e lcs[1]\n
    return: retorna as posições definidas para cada linha de centro.
    '''
    lista_de_LCs = lcs  
    #desenha a seção principal a partir de (0, 0)
    linha = acad.model.AddLine(APoint(0, 0), APoint(lista_de_LCs[sec_princ], 0))
    inicio = linha.StartPoint
    final = linha.EndPoint
    angs = 0
    coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
    lista_de_LCs[sec_princ] = coord_linhas
 
    #desenha as seções depois da seção principal, SE existirem | se a seção principal for 0 e só tiver uma seção, ignora
    if sec_princ < len(lcs)-1:
        for l in range(sec_princ + 1, len(lista_de_LCs)):
            linha = acad.model.AddLine(APoint(final[0], final[1]), APoint(final[0] + lista_de_LCs[l], final[1]))
            linha.Rotate(APoint(final[0], final[1]), radians(angs_in[l-1] + angs))
            angs += angs_in[l-1]
            inicio = linha.StartPoint
            final = linha.EndPoint
            
            coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
            lista_de_LCs[l] = coord_linhas
    
    #desenha a primeira seção antes da seção principal, SE existirem
    if sec_princ >= 1:
        linha = acad.model.AddLine(APoint(0 - lista_de_LCs[sec_princ-1], 0), APoint(0, 0))
        linha.Rotate(APoint(0, 0), radians(angs_in[sec_princ-1] * -1))
        inicio = linha.StartPoint
        final = linha.EndPoint
        angs = angs_in[sec_princ-1]
        coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
        lista_de_LCs[sec_princ-1] = coord_linhas
    #desenha as seções antes da seção principal, SE existirem
        if sec_princ >= 2:
            for l in reversed(range(sec_princ-1)):
                linha = acad.model.AddLine(APoint(inicio[0] - lista_de_LCs[l], inicio[1]), APoint(inicio[0], inicio[1]))
                linha.Rotate(APoint(inicio[0], inicio[1]), radians((angs_in[l] + angs)*-1))
                angs += angs_in[l]
                inicio = linha.StartPoint
                final = linha.EndPoint
                
                coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
                lista_de_LCs[l] = coord_linhas

    return lista_de_LCs

pedir_lcs()
pedir_angSecoes(len(lcs))
pos_lcs = definir_linhas_de_centro(lcs, angs_in)
if len(pos_lcs) == 1:
    sec_princ = 0
else:
    sec_princ = descobrir_secao_principal(pos_lcs)
pos_lcs = redesenhar_linhas_de_centro(lcs, angs_in, sec_princ)



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



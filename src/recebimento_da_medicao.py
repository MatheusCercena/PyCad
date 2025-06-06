"""
Funções para pedir os dados principais das medições para serem usadas pelas funções de desenho.
"""

def pedir_linhas_de_centro():
    linhas_de_centro = []
    cont = 1
    while True:
        lc_secoes = int(input(f'Digite a linha de centro da S{cont}: '))
        linhas_de_centro.append(lc_secoes)
        cont +=1
        res = input('Deseja digitar outra linha de centro? Digite enter para sim ou qualquer tecla para não:')
        if res != '':
            break
    return linhas_de_centro

def pedir_angSecoes(qntd_secoes: int):
    '''
    Solicita ao usuário os angulos interno e retorna uma lista com os angulos internos no formato: [ang_1, ang_2, ..., ang_n]
    '''
    angs_in = []
    for c in range(0, qntd_secoes-1):
        #inserir o angulo medido no transferidor, sem conversão.
        ang_sec = float(input(f'Qual o angulo entre a S{c+1} e a S{c+2}: '))
        ang_sec = 180-ang_sec
        angs_in.append(ang_sec*-1)
    return angs_in

def pedir_angParedes():
    '''
    Solicita ao usuário os angulos das extremidades direita e esquerda, e retorna uma lista com os angulos externos no formato: [ang_esq, ang_dir]
    '''
    angs_ex = []
    ang_esq = float(input(f'Digite o angulo da extremidade esquerda: '))
    ang_dir = float(input(f'Digite o angulo da extremidade direita: '))
    angs_ex.append(ang_esq)
    angs_ex.append(ang_dir)
    return angs_ex

def pedir_prumos():
    '''
    Solicita ao usuário os prumos das extremidades direita e esquerda, e retorna uma lista com os angulos externos no formato: [prumo_esq, prumo_dir]
    '''
    prumos = []
    prumo_esq = float(input(f'Digite o angulo da extremidade esquerda: '))
    prumos.append(prumo_esq)
    prumo_dir = float(input(f'Digite o angulo da extremidade direita: '))
    prumos.append(prumo_dir)
    return prumos

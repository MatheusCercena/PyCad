"""
Funções para pedir os dados principais das medições para serem usadas pelas funções de desenho.
"""

def pedir_linhas_de_centro():
    linhas_de_centro = []
    cont = 1
    while True:
        try:
            lc_secoes = int(input(f'Digite a linha de centro da S{cont}: '))
        except:
            print(f'[ERRO] O campo "linha de centro" precisa conter apenas numeros inteiros: ')
            continue
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
        while True:
            try:
                ang_sec = float(input(f'Qual o angulo entre a S{c+1} e a S{c+2}: ').replace(',', '.'))
                break
            except:
                print(f'[ERRO] O campo "angulo" precisa conter apenas numeros: ')
        ang_sec = 180-ang_sec
        angs_in.append(ang_sec*-1)
    return angs_in

def pedir_angParedes():
    '''
    Solicita ao usuário os angulos das extremidades direita e esquerda, e retorna uma lista com os angulos externos no formato: [ang_esq, ang_dir]
    '''
    angs_ex = []
    while True:
        try:
            ang_esq = 90 - float(input(f'Digite o angulo da extremidade esquerda: '))
            break
        except:
            print(f'[ERRO] O campo "angulo parede esquerda" precisa conter apenas numeros: ')
    while True:
        try:
            ang_dir = 90 - float(input(f'Digite o angulo da extremidade direita: '))
            break
        except:
            print(f'[ERRO] O campo "angulo parede direita" precisa conter apenas numeros: ')
    angs_ex.append(ang_esq)
    angs_ex.append(ang_dir)
    return angs_ex

def pedir_prumos():
    '''
    Solicita ao usuário os prumos das extremidades direita e esquerda, e retorna uma lista com os angulos externos no formato: [prumo_esq, prumo_dir]
    '''
    prumos = []
    while True:
        try:
            prumo_esq = float(input(f'Digite o angulo da extremidade esquerda: '))
            break
        except:
            print(f'[ERRO] O campo "prumo esquerdo" precisa conter apenas numeros: ')
    while True:
        try:
            prumo_dir = float(input(f'Digite o angulo da extremidade direita: '))
            break
        except:
            print(f'[ERRO] O campo "prumo direita" precisa conter apenas numeros: ')
    prumos.append(prumo_esq)
    prumos.append(prumo_dir)
    return prumos

"""
Funções para pedir os dados principais das medições para serem usadas pelas funções de desenho.
"""

def pedir_linhas_de_centro():
    linhas_de_centro = []

    print(f'''
{' - '*10}LINHAS DE CENTRO{' - '*10}
''')

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

def pedir_quant_vidros(lcs):
    quant_vidros = []
    print(f'''
{' - '*10}QUANTIDADE DE VIDROS{' - '*10}
''')

    for c in range(0, len(lcs)):
        try:
            quant = int(input(f'Digite a quantidade de vidros da S{c+1}: '))
        except:
            print(f'[ERRO] O campo "quantidade de vidros" precisa conter apenas numeros inteiros: ')
            continue
        quant_vidros.append(quant)
    return quant_vidros

def pedir_angSecoes(lcs: int):
    '''
    Solicita ao usuário os angulos interno e retorna uma lista com os angulos internos no formato: [ang_1, ang_2, ..., ang_n]
    '''
    angs_in = []
    print(f'''
{' - '*10}ANGULOS DAS SEÇÕES{' - '*10}
''')

    for c in range(0, len(lcs)-1):
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
    print(f'''
{' - '*10}ANGULOS DAS PAREDES{' - '*10}
''')

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
    print(f'''
{' - '*10}PRUMOS{' - '*10}
''')

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

def definir_juncoes(lcs, angs_in):
    '''
    Retorna uma lista em que cada elemento representa uma secao e cada secao tem 2 elementos com o elemento 0 sendo o tipo de junao do lado esquerdo da secao e o elemento 1 sendo o tipo de juncao do lado direito da secao:
        0 - vidro-parede
        1 - passante
        2 - colante
        3 - vidro-vidro
    '''
    juncoes = []
    for index in range(0, len(lcs)):
        esq_dir = []
        for lado in range(0, 2):
            if index == 0 and lado == 0: #parede esquerda
                esq_dir.append(0)
            elif lado == 0 and juncoes[-1][1] == 1: #se ultimo é passante, este é colante
                esq_dir.append(2)
            elif lado == 0 and juncoes[-1][1] == 2: #se ultimo é colante, este é passante
                esq_dir.append(1)
            elif lado == 0 and juncoes[-1][1] == 3: #se ultimo é vidro-vidro, este é vidro-vidro
                esq_dir.append(3)
            elif len(angs_in) != 0 and index < len(angs_in):
                if 70 < (abs(angs_in[index])) < 110: #passante-colante
                    res = input(f'A juncão entre os vidros do lado {index} e {index+1} será passante e colante, qual deseja que seja o passante? Digite "e" para o vidro do lado {index} ou "d" para o vidro do lado {index + 1}: ')
                    while res not in ['e', 'd']:
                        res = input(f'A juncão entre os vidros do lado {index} e {index+1} será passante e colante, qual deseja que seja o passante? Digite "e" para o vidro do lado {index} ou "d" para o vidro do lado {index + 1}: ')
                    if res == 'e': #se esquerda é passante, este é passante
                        esq_dir.append(1)
                    if res == 'd': #se direita é passante, este é colante
                        esq_dir.append(2)
                else: #vidro-vidro
                    esq_dir.append(3)
            else: #parede direita
                esq_dir.append(0)
        juncoes.append(esq_dir)

    return juncoes

def solicitar_sentido_abertura(quant_vidros: list):
    '''
Retorna uma lista de sublistas em que cada sublista representa uma abertura:
item 0: onde a abertura começa
item 1: onde termina a abertura
item 2: qual vidro é o giratório
item 3: qual o sentido de abertura (direita ou esquerda)
item 4: lista contendo os vidros que são fixos.
    '''
    sentidos = []
    moveis = []
    v_ini = ''
    v_fin = ''
    giratorio = ''
    print(f'''
{' - '*10}SENTIDOS DE ABERTURA{' - '*10}
''')

    cont = 1
    while True:
        if len(moveis) > 0 and max(moveis) >= sum(quant_vidros):
            break
        while True:
            try:
                v_ini = int(input(f'Digite o vidro onde começa a {cont}ª abertura: '))
                if v_ini > sum(quant_vidros):
                    print(f'A sacada tem menos que {v_ini} vidros. Escolha um vidro existente na sacada')
                    continue
                elif v_ini not in moveis and v_ini != 0:
                    break
                else:
                    print('Esse vidro já abre em outro lugar.')
                    continue
            except:
                print(f'[ERRO] O vidro precisa ser numérico.')
        while True:
            try:
                v_fin = int(input(f'Digite o vidro onde termina a {cont}ª abertura: '))
                if v_fin > sum(quant_vidros):
                    print(f'A sacada tem menos que {v_fin} vidros. Escolha um vidro existente na sacada')
                    continue
                elif v_ini not in moveis and v_ini != 0:
                    break
                else:
                    print('Esse vidro já abre em outro lugar.')
                    continue
            except:
                print(f'[ERRO] O vidro precisa ser numérico.')
        while True:
            try:
                giratorio = int(input(f'O vidro giratrio da abertura será no {v_ini} ou no {v_fin}?'))
                if giratorio in [v_ini, v_fin]:
                    break
                else:
                    print(f'O vidro giratório precisa ser o {v_ini} ou o {v_fin}.')
                    continue
            except:
                print(f'[ERRO] O vidro giratório precisa ser numérico.')
        [moveis.append(vidro) for vidro in range(v_ini, v_fin+1)]
        sentido = 'direita' if giratorio == v_fin else 'esquerda'
        print(f'Certo, os vidros da {cont}ª abertura irao abrir para a {sentido}.')
        abertura = [v_ini, v_fin, giratorio, sentido]
        sentidos.append(abertura)
        res = ''
        cont += 1 
        fixos = []
        for vidro in range(1, sum(quant_vidros)+1):
            if vidro not in moveis:
                fixos.append(vidro)
        res = input(f'Deseja informar outra abertura? [s/n]').strip().lower()
        while res not in ['s', 'n']:
            print('A resposta precisa ser "s" ou "n".')
            res = input(f'Deseja informar outra abertura? [s/n]').strip().lower()
        if res == 'n':
            return sentidos, fixos
        if res == 's':
            continue
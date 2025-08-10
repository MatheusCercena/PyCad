''' Funções para gerenciar bocas dos vidros, evitando molas e garantindo abertura correta. '''

from src.calcs_vetor import obter_dados_intervalo

def verificar_se_boca_bate_na_mola(molas, boca, sentido):
    ''' Verifica se a boca está batendo em alguma mola. '''
    for mola in molas:
        if mola-34 <= boca <= mola +34:#boca está batendo na mola
            if sentido == 'esquerda':
                distancia_boca = mola + 45
            else:
                distancia_boca = mola - 45
        else:
            distancia_boca = boca
    return distancia_boca

def verificar_se_vidro_abre_na_boca(vidro, meio, sentido, boca):
    ''' Verifica se o vidro abre na boca. '''
    limite_vidro = meio + vidro*0.6 if sentido == 'esquerda' else meio - vidro*0.6
    if sentido == 'esquerda' and boca <= limite_vidro or sentido == 'direita' and boca >= limite_vidro:
        return False
    else:
        return True

def criar_nova_boca(meio_do_estacionamento, vidro, sentido):
    ''' Cria uma nova boca para o vidro caso a boca atual não esteja adequada. '''
    if sentido == 'esquerda':
        nova_boca = meio_do_estacionamento + (vidro - 15.0) - 15
    else:
        nova_boca = -meio_do_estacionamento - (vidro + 15.0) + 15
    return nova_boca

def definir_bocas(
        sentidos: list[int, int, int, int, tuple[int]],
        medidas_vidros: list[float],
        pontos_vidros: list[list[float]],
        pivos: list[int]
        ):
    ''' Define as bocas para os vidros com base nos sentidos de abertura e medidas. '''
    bocas = []
    for i, sentido in enumerate(sentidos):
        vidro_ini = sentido[0]
        vidro_fim = sentido[1]
        sentido = sentido[4]
        pivo = pivos[i]

        medida_vidros_da_abertura = obter_dados_intervalo(medidas_vidros, vidro_ini, vidro_fim)
        posicao_vidros_da_abertura = obter_dados_intervalo(pontos_vidros, vidro_ini, vidro_fim)
        quant_vidros_da_abertura = vidro_fim - vidro_ini + 1
        giratorio = 0 if sentido == 'esquerda' else quant_vidros_da_abertura-1
        final_do_giratorio = posicao_vidros_da_abertura[giratorio][1] if sentido == 'esquerda' else posicao_vidros_da_abertura[giratorio][0]

        # Definindo o meio dos vidros
        meio_dos_vidros = [pivo]
        contador = 1
        for vidro in range(0, quant_vidros_da_abertura-1):
            meio = pivo + 30*contador if sentido == 'esquerda' else pivo - 30*contador
            meio_dos_vidros.append(meio)
            contador += 1

        # Definindo posicao das molas e espaco que nao pode ir bocas
        molas = []
        for vidro in meio_dos_vidros[::-3]:
            ponto_mola = vidro + 90 if sentido == 'esquerda' else vidro - 90
            molas.append(ponto_mola)

        #definindo boca1
        bocas_lado = []
        boca1 = final_do_giratorio - 30.0 if sentido == 'esquerda' else final_do_giratorio + 30.0
        boca1_final = verificar_se_boca_bate_na_mola(molas, boca1, sentido)
        bocas_lado.append(boca1_final)

        # Definindo as outras bocas
        for i, vidro in enumerate(medida_vidros_da_abertura):
            meio_do_estacionamento = meio_dos_vidros[i]
            ultima_boca = bocas_lado[-1]
            verificacao = verificar_se_vidro_abre_na_boca(vidro, meio_do_estacionamento, sentido, ultima_boca)
            if verificacao is False:
                nova_boca = criar_nova_boca(meio_do_estacionamento, vidro, sentido)
                bocas_lado.append(nova_boca)
            else:
                continue
        bocas.append(bocas_lado)
    return bocas

# def definir_pontos_bocas(bocas: list[float], coord_linhas_centro, sentido):
#     pontos_bocas = []

#     for boca in bocas:
#         for linha_centro in coord_linhas_centro:
#             if sentido


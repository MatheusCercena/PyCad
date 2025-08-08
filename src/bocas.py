from src.calcs_vetor import contar_entre_numeros, obter_dados_intervalo
from src.pivos import definir_pivos

def ver_se_boca_bate_na_mola(molas, boca, sentido):
    for mola in molas:
        if mola-34 <= boca <= mola +34:#boca está batendo na mola
            if sentido == 'esquerda':
                distancia_boca = mola + 45
            else:
                distancia_boca = mola - 45
            return distancia_boca
        else:
            return boca
    
def verificar_se_vidro_abre_na_boca(vidro, meio, sentido, boca):
    limite_vidro = meio - vidro*0.6 if sentido == 'esquerda' else meio + vidro*0.6
    if sentido == 'esquerda' and boca >= limite_vidro or sentido == 'direita' and boca <= limite_vidro:
        return False
    else:
        return True
    
def criar_nova_boca(vidro, sentido):
    if sentido == 'esquerda':
        nova_boca = vidro[0] + 15.0
    else:
        nova_boca = vidro[1] - 15.0
    return nova_boca

def definir_bocas(
        sentidos: list[int, int, int, int, tuple[int]],
        medidas_vidros: list[float], 
        pontos_vidros: list[list[float]], 
        pivos: list[int]
        ):
    for i, sentido in enumerate(sentidos):
        vidro_ini = sentido[0]
        vidro_fim = sentido[1]
        sentido = sentido[4]
        pivo = pivos[i]

        medida_vidros_da_abertura = obter_dados_intervalo(medidas_vidros, vidro_ini, vidro_fim)
        posicao_vidros_da_abertura = obter_dados_intervalo(pontos_vidros, vidro_ini, vidro_fim)
        quant_vidros_da_abertura = contar_entre_numeros(vidro_ini, vidro_fim)
        
        final_do_giratorio = posicao_vidros_da_abertura[0][0] + pivo if sentido == 'esquerda' else posicao_vidros_da_abertura[0][1]
                
        # Definindo o meio dos vidros
        meio_dos_vidros = [pivo]
        contador = 0
        for vidro in range(quant_vidros_da_abertura):
            meio = pivo - 30*contador if sentido == 'esquerda' else pivo + 30*contador
            meio_dos_vidros.append(meio)
        
        # Definindo posicao das molas e espaco que nao pode ir bocas
        molas = []
        for vidro in range(len(meio_dos_vidros), 0, -3):
            ponto_mola = vidro - 90 if sentido == 'esquerda' else vidro + 90
            molas.append(ponto_mola)


        #definindo boca1
        bocas = []
        boca1 = final_do_giratorio + 30.0 if sentido == 'esquerda' else final_do_giratorio - 30.0
        boca1_final = ver_se_boca_bate_na_mola(molas, boca1, sentido)
        bocas.append(boca1_final)

        # Definindo as outras bocas
        for i, vidro in enumerate(medida_vidros_da_abertura):
            meio_do_estacionamento = meio_dos_vidros[i]
            ultima_boca = bocas[-1]
            verificacao = verificar_se_vidro_abre_na_boca(vidro, meio_do_estacionamento, sentido, ultima_boca)
            if verificacao == False:
                nova_boca = criar_nova_boca(vidro, sentido)
                bocas.append(nova_boca)
            else:
                continue
    return bocas

def definir_pontos_bocas(bocas: list[float], coord_linhas_centro, coord_perfis_u):
    pontos_bocas = []
    for boca in bocas:
        for linha_centro in coord_linhas_centro
            
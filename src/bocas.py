from src.calcs_vetor import contar_entre_numeros
from src.aberturas import distribuir_vidros_por_lado

def obter_medidas_intervalo(medidas_vidros: list[float], vidro_inicial: int, vidro_final: int) -> list[float]:
    """
    Retorna as medidas dos vidros entre vidro_inicial e vidro_final (inclusive).
    Assume que o vidro 1 está no índice 0 da lista.

    Exemplo:
    medidas_vidros = [1000, 1010, 1020, 1030, 1040]
    obter_medidas_intervalo(medidas_vidros, 2, 4) -> [1010, 1020, 1030]
    """
    inicio = vidro_inicial - 1
    fim = vidro_final     

    return medidas_vidros[inicio:fim]

def obter_pontos_intervalo(pontos_vidros: list[list[float]], vidro_inicial: int, vidro_final: int) -> list[list[float]]:
    """
    Retorna as medidas dos vidros entre vidro_inicial e vidro_final (inclusive).
    Assume que o vidro 1 está no índice 0 da lista.

    Exemplo:
    medidas_vidros = [1000, 1010, 1020, 1030, 1040]
    obter_medidas_intervalo(medidas_vidros, 2, 4) -> [1010, 1020, 1030]
    """
    inicio = vidro_inicial - 1
    fim = vidro_final     

    return pontos_vidros[inicio:fim]

def definir_pivos(sentidos, juncoes: list[list[int]], medidas_perfis_U: list[list[float]], quant_vidros):
    """
    Para cada vidro, define o valor do pivô (30, 70 ou 85) conforme posição, sentido de abertura e tipo de junção.
    - sentidos: lista de tuplas/listas, cada uma com (vidro_inicial, vidro_final, giratorio, adjacente, direcao),
    - juncoes: lista de listas, cada sub-lista representa os tipos de junção de cada lado (0=parede, 1=passante, 2=colante, 3=vidro-vidro).
    - vidros: lista com medida dos vidros
    - quant_vidros: lista com quantidade de vidros por lado.
    Retorna: lista com os pivôs na ordem dos respectivos giratorios.
    """
    vidros_mapeados = distribuir_vidros_por_lado(quant_vidros)
    pivos = []
    for sentido in sentidos:
        giratorio = sentido[2]
        for i, lado in enumerate(vidros_mapeados):
            # perfis_secao = medidas_perfis_U[i]
            for j, vidro in enumerate(lado):
                if vidro == giratorio:
                    if j == 0:
                        if juncoes[i][0] == 0:
                            pivos.append(70)
                            break
                        else:
                            pivos.append(85)
                            break
                    elif j == len(lado)-1:
                        if juncoes[i][1] == 0:
                            pivos.append(70)
                            break
                        else:
                            pivos.append(85)
                            break
                    else:
                        # Verifica qual das extremidades (início ou fim) está mais próxima do vidro giratório
                        # e puxa o pivô a partir dali (pode ser útil para casos de ajuste fino)
                        # Aqui, vamos comparar a distância do vidro giratório até o início e até o fim do lado
                        # dist_inicio = 
                        # dist_fim = len(lado) - 1 - j
                        # if dist_inicio < dist_fim:
                        #     # Mais próximo do início
                        #     tipo_juncao = juncoes[i][0]
                        #     if tipo_juncao == 0:
                        #         pivos.append(70)
                        #     elif tipo_juncao in (1, 2) and sentido[4] == 'esquerda':
                        #         pivos.append(85)
                        #     else:
                        #         pivos.append(30)
                        # elif dist_fim < dist_inicio:
                        #     # Mais próximo do fim
                        #     tipo_juncao = juncoes[i][1]
                        #     if tipo_juncao == 0:
                        #         pivos.append(70)
                        #     elif tipo_juncao in (1, 2) and sentido[4] == 'direita':
                        #         pivos.append(85)
                        #     else:
                        #         pivos.append(30)
                        # else:
                        #     # Equidistante, padrão 30
                        #     pivos.append(30)
                        

def definir_bocas(sentidos, medidas_vidros: list[float], pontos_vidros: list[list[float]], juncoes: list[list[int]], pivos):
    for i, sentido in enumerate(sentidos):
        vidro_ini = sentido[0]
        vidro_fim = sentido[1]
        pivo = pivos[i]
        medida_vidros_da_abertura = obter_medidas_intervalo(medidas_vidros, vidro_ini, vidro_fim)
        posicao_vidros_da_abertura = obter_pontos_intervalo(pontos_vidros, vidro_ini, vidro_fim)
        quant_vidros_da_abertura = contar_entre_numeros(vidro_ini, vidro_fim)

        def definir_distancia_bocas():
            pass
        def definir_quantidade_bocas():
            pass

        if sentido[4] == 'esquerda':
               
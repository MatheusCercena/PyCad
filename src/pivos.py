from src.aberturas import distribuir_vidros_por_lado

def definir_pivos(
        quant_vidros: list[int],
        sentidos: list[int, int, int, int, tuple[int]],
        juncoes: list[list[int]],
        medidas_perfis_U: list[list[float]],
        pontos_vidros: list[list[float]]
        ):
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
            perfis_secao = medidas_perfis_U[i]
            perfis_linear = []
            inicio = 0
            for perfil in perfis_secao:
                ini_perfil = inicio
                fim_perfil = inicio + perfil
                perfis_linear.append((ini_perfil, fim_perfil))
                inicio += perfil
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
                        # Achar lado que começa o vidro giratório
                        if sentido[4] == 'esquerda':
                            ponto_ini_vidro = pontos_vidros[i][j][0]
                        else:
                            ponto_ini_vidro = pontos_vidros[i][j][1]
                        # Achar em qual perfil está o vidro giratório 
                        secao_do_giratorio = ''
                        for i, perfil in enumerate(perfis_linear):
                            if perfil[0] <= ponto_ini_vidro <= perfil[1]:
                                secao_do_giratorio = perfil
                                break
                        # Verifica qual das extremidades da secao do giratorio está mais próxima do vidro
                        dist_inicio = ponto_ini_vidro - secao_do_giratorio[0] 
                        dist_fim = secao_do_giratorio[1] - ponto_ini_vidro
                        if dist_inicio < dist_fim:
                            distancia_usada = dist_inicio + 30
                        else:
                            distancia_usada = dist_fim - 30
                        pivos.append(30 + distancia_usada)
    return pivos

def definir_alturas(alturas: list[list[int]], niveis: list[list[int]], lcs: list[int]):
    '''Converte as alturas e niveis de listas com sublistas para listas simples.'''

    dist_pedacos =  dist_inteira = 0
    # Redefine de forma inicial as alturas com base no nível
    alturas_redefinidas: list[list][int] = []
    for index, lado in enumerate(alturas):
        for i, altura in enumerate(lado):
            altura_redefinida = altura - niveis[index][i]
            alturas_redefinidas.append(altura_redefinida)

    # Verifica se é necessário readequar a altura mais baixa da parte de cima
    todas_alturas = [altura for lado in alturas for altura in lado]
 
    maior_altura = max(todas_alturas)
    menor_altura = min(todas_alturas)
    diferença_superior = maior_altura - menor_altura
    ponto_mais_baixo_emcima = menor_altura

    diferenças_superiores_normalizadas = []
    for index, lado in enumerate(alturas):
        diferenças_lado = []
        for i, altura in enumerate(lado):
            diferenca = altura - menor_altura
            diferenças_lado.append(diferenca)
        diferenças_superiores_normalizadas.append(diferenças_lado)

    if 12 < diferença_superior:
        print('Necessario usar sucata de trilho em pedaços de qualquer cor na parte superior')
        opt = input('Deseja aumentar a altura dos vidros em +5mm por usar perfil U com calha (PE-1) na parte superior invés de versao sem calha (CEG-235)? [s/n]')
        if opt == 's':
            ponto_mais_baixo_emcima += 5
        diferença_superior -= 5
        if 12 < diferença_superior:
            dist_pedacos, dist_inteira = calcular_sucata(diferenças_superiores_normalizadas, lcs)

    # Verifica se é necessário readequar a altura mais alta na parte de baixo
    todos_niveis = [nivel for lado in niveis for nivel in lado]

    diferença_inferior = abs(min(todos_niveis))
    ponto_mais_alto_embaixo = max(todos_niveis)

    if 12 < diferença_inferior:
        print('Necessario usar sucata de trilho em pedaços de qualquer cor na parte inferior')
        opt = input('Deseja aumentar a altura dos vidros em +3mm por embutir a contrafechadura? [s/n]')
        if opt == 's':
            ponto_mais_alto_embaixo -= 3
            diferença_inferior += 3
        if 12 < diferença_inferior:
            dist_pedacos, dist_inteira = calcular_sucata(niveis, lcs)

    # Definicao de variáveis finais
    altura_vidro = ponto_mais_baixo_emcima - ponto_mais_alto_embaixo
    quantidade_de_pedacos = dist_pedacos / 500 + 1
    sucata = (quantidade_de_pedacos, dist_inteira)

    return maior_altura, menor_altura, altura_vidro, sucata
    
def calcular_sucata(diferencas: list[list[float]], lcs: list[float]) -> tuple[float, float]:
    """
    Calcula a distância total nas seguintes faixas:
    - Entre 12 e 17
    - Acima de 17

    Param:
    - diferencas: lista de sublistas com valores verticais
    - lcs: lista de larguras associadas a cada sublista

    Return:
    - Tupla com distância entre 12 e 17, distância acima de 17)
    """
    diferencas = [[abs(valor) for valor in sublista] for sublista in diferencas]

    limite_inferior = 12.0
    limite_superior = 17.0

    dist_entre_12_17 = 0.0
    dist_acima_17 = 0.0

    for pontos, largura_total in zip(diferencas, lcs):
        if len(pontos) < 2:
            continue

        trechos = len(pontos) - 1
        largura_por_trecho = largura_total / trechos

        for i in range(trechos):
            y1 = pontos[i]
            y2 = pontos[i+1]

            y_min = min(y1, y2)
            y_max = max(y1, y2)

            altura_total = abs(y2 - y1)
            if altura_total == 0:
                continue  # evita divisão por zero

            # Faixa entre 12 e 17
            intersec_min = max(y_min, limite_inferior)
            intersec_max = min(y_max, limite_superior)

            if intersec_min < intersec_max:
                proporcao_12_17 = (intersec_max - intersec_min) / altura_total
                dist_entre_12_17 += proporcao_12_17 * largura_por_trecho

            # Faixa acima de 17
            if y_max > limite_superior:
                altura_acima_17 = y_max - max(y_min, limite_superior)
                proporcao_acima_17 = altura_acima_17 / altura_total
                dist_acima_17 += proporcao_acima_17 * largura_por_trecho

    return dist_entre_12_17, dist_acima_17

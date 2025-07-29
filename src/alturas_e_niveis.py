from typing import List, Tuple

# def definir_alturas(alturas: list[list[int]], niveis: list[list[int]], lcs: list[int]):
#     '''Converte as alturas e niveis de listas com sublistas para listas simples.'''

#     dist_pedacos =  dist_inteira = 0
#     # Redefine de forma inicial as alturas com base no nível
#     alturas_redefinidas: list[list][int] = []
#     for index, lado in enumerate(alturas):
#         for i, altura in enumerate(lado):
#             altura_redefinida = altura - niveis[index][i]
#             alturas_redefinidas.append(altura_redefinida)

#     # Verifica se é necessário readequar a altura mais baixa da parte de cima
#     todas_alturas = [altura for lado in alturas for altura in lado]
 
#     maior_altura = max(todas_alturas)
#     menor_altura = min(todas_alturas)
#     diferença_superior = maior_altura - menor_altura
#     ponto_mais_baixo_emcima = menor_altura

#     diferenças_superiores_normalizadas = []
#     for index, lado in enumerate(alturas):
#         diferenças_lado = []
#         for i, altura in enumerate(lado):
#             diferenca = altura - menor_altura
#             diferenças_lado.append(diferenca)
#         diferenças_superiores_normalizadas.append(diferenças_lado)

#     if 12 < diferença_superior:
#         print('Necessario usar sucata de trilho em pedaços de qualquer cor na parte superior')
#         opt = input('Deseja aumentar a altura dos vidros em +5mm por usar perfil U com calha (PE-1) na parte superior invés de versao sem calha (CEG-235)? [s/n]')
#         if opt == 's':
#             ponto_mais_baixo_emcima += 5
#         diferença_superior -= 5
#         if 12 < diferença_superior:
#             dist_pedacos, dist_inteira = calcular_sucata(diferenças_superiores_normalizadas, lcs)

#     # Verifica se é necessário readequar a altura mais alta na parte de baixo
#     todos_niveis = [nivel for lado in niveis for nivel in lado]

#     diferença_inferior = abs(min(todos_niveis))
#     ponto_mais_alto_embaixo = max(todos_niveis)

#     if 12 < diferença_inferior:
#         print('Necessario usar sucata de trilho em pedaços de qualquer cor na parte inferior')
#         opt = input('Deseja aumentar a altura dos vidros em +3mm por embutir a contrafechadura? [s/n]')
#         if opt == 's':
#             ponto_mais_alto_embaixo -= 3
#             diferença_inferior += 3
#         if 12 < diferença_inferior:
#             dist_pedacos, dist_inteira = calcular_sucata(niveis, lcs)

#     # Definicao de variáveis finais
#     altura_vidro = ponto_mais_baixo_emcima - ponto_mais_alto_embaixo
#     quantidade_de_pedacos = dist_pedacos / 500 + 1
#     sucata = (quantidade_de_pedacos, dist_inteira)

#     return maior_altura, menor_altura, altura_vidro, sucata

def definir_alturas(
    alturas: List[List[int]],
    niveis: List[List[int]],
    lcs: List[int],
    quant_vidros: List[int],
    sentidos_abert: List[List[int]]
) -> Tuple[int, int, int, Tuple[float, float]]:
    """
    Ajusta alturas considerando os pontos mais baixos e mais altos nos giratórios,
    com tolerância de 12mm para limitar variações extremas.

    Args:
        alturas (List[List[int]]): Lista de alturas por lado.
        niveis (List[List[int]]): Lista de níveis por lado.
        lcs (List[int]): Lista de larguras de cada lado.
        quant_vidros (List[int]): Quantidade de vidros por lado.
        sentidos_abert (List[List[int]]): Aberturas definidas pelo usuário.

    Returns:
        Tuple contendo:
            - Maior altura
            - Menor altura
            - Altura do vidro
            - Tupla (distância de pedaços, distância inteira)
    """
    dist_pedacos = dist_inteira = 0

    # Redefine de forma inicial as alturas com base no nível
    alturas_redefinidas: List[List[int]] = [
        [altura + niveis[i][j] for j, altura in enumerate(lado)]
        for i, lado in enumerate(alturas)
    ]

    # Lista com todas as alturas para extremos brutos
    todas_alturas = [altura for lado in alturas_redefinidas for altura in lado]
    maior_altura = max(todas_alturas)
    menor_altura = min(todas_alturas)

    # Obter altura do giratório e aplicar tolerância de 12mm
    alturas_giratorios = obter_altura_giratorios(sentidos_abert, quant_vidros, alturas_redefinidas, lcs)
    ponto_mais_baixo_emcima = ajustar_limite_superior(menor_altura, alturas_redefinidas, alturas_giratorios, 12.0)

    # Diferencas para calcular sucata
    diferencas_superiores_normalizadas = [[altura - ponto_mais_baixo_emcima for altura in lado] for lado in alturas_redefinidas]

    diferenca_superior = max(abs(altura) for lado in diferencas_superiores_normalizadas for altura in lado)

    if diferenca_superior > 12:
        print('Necessário usar sucata de trilho em pedaços na parte superior.')
        opt = input('Deseja aumentar a altura dos vidros em +5mm por usar perfil U com calha? [s/n]').strip().lower()
        if opt == 's':
            ponto_mais_baixo_emcima += 5
            diferenca_superior -= 5
        if diferenca_superior > 12:
            dist_pedacos, dist_inteira = calcular_sucata(diferencas_superiores_normalizadas, lcs)

    # Parte inferior
    todos_niveis = [nivel for lado in niveis for nivel in lado]
    ponto_mais_alto_embaixo_bruto = max(todos_niveis)

    niveis_giratorios = obter_altura_giratorios(sentidos_abert, quant_vidros, niveis, lcs)
    ponto_mais_alto_embaixo = ajustar_limite_inferior(ponto_mais_alto_embaixo_bruto, niveis, niveis_giratorios,12.0)

    # Calcular diferença inferior com base ajustada
    niveis_ajustados = [[nivel - ponto_mais_alto_embaixo for nivel in lado] for lado in niveis]

    diferenca_inferior = diferenca_inferior = min(min(sublista) for sublista in niveis_ajustados)

    if diferenca_inferior > 12:
        print('Necessário usar sucata de trilho em pedaços na parte inferior.')
        opt = input('Deseja aumentar a altura dos vidros em +3mm por embutir a contrafechadura? [s/n]').strip().lower()
        if opt == 's':
            ponto_mais_alto_embaixo -= 3
            diferenca_inferior += 3
        if diferenca_inferior > 12:
            dist_pedacos, dist_inteira = calcular_sucata(niveis, lcs)

    altura_vidro = ponto_mais_baixo_emcima - ponto_mais_alto_embaixo
    quantidade_de_pedacos = dist_pedacos / 500
    if quantidade_de_pedacos != 0:
        quantidade_de_pedacos += 1
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

def mapear_vidro_para_lado(quant_vidros: List[int]) -> dict[int, Tuple[int, int]]:
    """
    Mapeia o número absoluto do vidro para (lado, índice local).

    Args:
        quant_vidros: Lista com quantidade de vidros por lado.

    Returns:
        Mapa: vidro absoluto (1-based) → (lado, índice_local no lado)
    """
    mapa = {}
    contador = 1
    for lado, qtd in enumerate(quant_vidros):
        for i in range(qtd):
            mapa[contador] = (lado, i)
            contador += 1
    return mapa

def interpolar_valor_em_x(pontos: List[float], valores: List[float], x: float) -> float:
    """
    Interpola linearmente o valor em uma posição x a partir de pontos e valores dados.

    Args:
        pontos: Lista de coordenadas X dos pontos (ex: posições dos pontos de medição).
        valores: Lista de alturas ou níveis correspondentes.
        x: A posição X alvo onde queremos saber o valor interpolado.

    Returns:
        Valor interpolado na posição X.
    """
    if len(pontos) == 1:
        return valores[0]

    for i in range(len(pontos) - 1):
        x0, x1 = pontos[i], pontos[i + 1]
        y0, y1 = valores[i], valores[i + 1]
        if x0 <= x <= x1:
            # Interpolação linear
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)

    # Fora da faixa → extrapola no final
    if x <= pontos[0]:
        return valores[0]
    return valores[-1]


def obter_altura_giratorios(
    aberturas: List[List[int]],
    quant_vidros: List[int],
    fonte: List[List[int]],
    lcs: List[int]
) -> List[float]:
    """
    Obtém a altura (ou nível) do ponto do giratório interpolado na posição real do vidro.

    Args:
        aberturas: Lista de abertura com info do vidro giratório.
        quant_vidros: Lista de quantos vidros por lado.
        fonte: Lista de alturas ou níveis por lado.
        lcs: Largura total de cada lado.

    Returns:
        Lista com alturas interpoladas dos giratórios.
    """
    mapa = mapear_vidro_para_lado(quant_vidros)
    resultado = []

    for abertura in aberturas:
        vidro = abertura[2]
        lado, idx_local = mapa[vidro]
        total_vidros = quant_vidros[lado]
        largura_total = lcs[lado]

        # Obter coordenadas X normalizadas da medição
        n_pontos = len(fonte[lado])
        step = largura_total / (n_pontos - 1) if n_pontos > 1 else 0
        pontos_x = [i * step for i in range(n_pontos)]

        # Obter posição real do vidro no eixo X
        largura_vidro = largura_total / total_vidros
        centro_vidro = (idx_local + 0.5) * largura_vidro

        altura_interpolada = interpolar_valor_em_x(pontos_x, fonte[lado], centro_vidro)
        resultado.append(altura_interpolada)

    return resultado

def ajustar_limite_superior(
    base: float,
    alturas: list[list[float]],
    giratorios: list[float],
    limite: float = 12.0
) -> float:
    """
    Ajusta a referência da parte superior para garantir que nenhum ponto esteja
    mais de `limite` mm abaixo da base.

    Args:
        base: valor inicial da referência superior.
        alturas: lista de listas com todas as alturas.
        giratorios: lista com as alturas dos giratórios.
        limite: tolerância máxima permitida (padrão: 12mm).

    Returns:
        Valor ajustado da base superior.
    """
    todos = [p for lado in alturas for p in lado] + giratorios

    for ajuste in range(int(base), int(min(todos)) - 1, -1):
        if all(ajuste - p <= limite for p in todos):
            return ajuste

    return base - limite  # como fallback, rebaixa até o máximo permitido

def ajustar_limite_inferior(
    base: float,
    niveis: list[list[float]],
    giratorios: list[float],
    limite: float = 12.0
) -> float:
    """
    Ajusta a referência da parte inferior para garantir que nenhum ponto esteja
    mais de `limite` mm acima da base.

    Args:
        base: valor inicial da referência inferior.
        niveis: lista de listas com todos os níveis (parte inferior).
        giratorios: lista com os níveis dos giratórios.
        limite: tolerância máxima permitida (padrão: 12mm).

    Returns:
        Valor ajustado da base inferior.
    """
    todos = [p for lado in niveis for p in lado] + giratorios

    for ajuste in range(int(base), int(max(todos)) + 1):
        if all(p - ajuste <= limite for p in todos):
            return ajuste

    return base + limite  # como fallback, eleva até o máximo permitido

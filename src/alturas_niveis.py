

def definir_alturas(
    alturas: list[list[int]],
    niveis: list[list[int]],
    lcs: list[int],
    quant_vidros: list[int],
    sentidos_abert: list[list[int]]
) -> tuple[int, int, int, tuple[float, float]]:
    """
    Ajusta alturas considerando os pontos mais baixo para fixacao do vidro na parte superior e mais alto na parte inferior, com tolerância de 12mm para evitar trilho muito socado.

    Args:
        alturas: Lista de alturas por lado.
        niveis: Lista de níveis por lado.
        lcs: Lista de larguras de cada lado.
        quant_vidros: Quantidade de vidros por lado.
        sentidos_abert: Aberturas definidas pelo usuário.

    Returns:
        Tuple contendo:
            - Maior altura
            - Menor altura
            - Altura do vidro
            - Tupla (distância de pedaços de sucata, distância sucata inteira)
    """
    todas_alturas = [altura for lado in alturas for altura in lado]
    todos_niveis = [nivel for lado in niveis for nivel in lado]
    maior_nivel = max(todos_niveis)
    niveis_base_0 = [[nivel - maior_nivel for nivel in lado] for lado in niveis]
    alturas_com_base_0 = [[altura + niveis_base_0[i][j] for j, altura in enumerate(lado)] for i, lado in enumerate(alturas)]
    
    niveis_giratorios = obter_niveis_giratorios(sentidos_abert, quant_vidros, alturas_com_base_0, lcs)
    maior_nivel_giratório = max(niveis_giratorios)
    if maior_nivel_giratório <= -12:
        diferenca = 12 - maior_nivel_giratório
        maior_nivel_giratório = -12
        niveis_finais = [[nivel + diferenca for nivel in lado] for lado in niveis_base_0]
    else:
        niveis_finais = niveis_base_0

    diferenca_inferior = min(min(sublista) for sublista in niveis_finais)
    if diferenca_inferior <= -12:
        print(f'Diferença de nível de {abs(diferenca_inferior)} e o giraatório mais alto na parte de baixo é o 'x'. Necessário usar sucata de trilho na parte inferior.')
        opt = input('Deseja aumentar a altura dos vidros em +3mm para embutir a contrafechadura? [s/n]').strip().lower()
        if opt == 's':
            diferenca = 3
            niveis_finais = [[nivel + diferenca for nivel in lado] for lado in niveis_finais]
        if diferenca_inferior > 12:
            dist_pedacos, dist_inteira = calcular_sucata(niveis, lcs)

    maior_altura = max(todas_alturas)
    menor_altura = min(todas_alturas)
    altura_vidro = 0
    dist_pedacos = dist_inteira = 0

    return

def calcular_sucata():
    pass

def obter_niveis_giratorios(
        sentidos_abert,
        quant_vidros, 
        alturas_redefinidas, 
        lcs):
    '''
    Obtém o nível de cada giratório interpolado na posição real do vidro.

    Args:
        aberturas: Lista de abertura com info do vidro giratório.
        quant_vidros: Lista de quantos vidros por lado.
        fonte: Lista de alturas ou níveis por lado.
        lcs: Largura total de cada lado.

    Returns
        Lista com alturas interpoladas dos giratórios.
    '''
    pass
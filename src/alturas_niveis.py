def niveis(niveis, lcs, quant_vidros, sentidos_abert):
    def maior_valor(lista):
        return max(max(sublista) for sublista in lista)
    
    # Ajustando niveis para padrao de base 0 
    maior_nivel = maior_valor(niveis)
    niveis_base_0 = [[nivel - maior_nivel for nivel in lado] for lado in niveis]
    
    # Ajustando niveis pelo giratorio
    niveis_giratorios = obter_altura_giratorios(sentidos_abert, quant_vidros, niveis, lcs)
    maior_nivel_giratório = max(niveis_giratorios)
    niveis_base_giratorio = [[nivel + abs(maior_nivel_giratório) for nivel in lado] for lado in niveis_base_0]
    maior_nivel_base_giratorio = maior_valor(niveis_base_giratorio)

    # Reajustando niveis para evitar trilho socado
    if maior_nivel_base_giratorio >= 12:
        diferenca = maior_nivel_base_giratorio - 12
        niveis_finais = [[nivel + diferenca for nivel in lado] for lado in niveis_base_giratorio]
        maior_nivel_base_giratorio = maior_valor(niveis_finais)
    else:
        niveis_finais = niveis_base_giratorio

    # Definição da sucata inferior
    diferenca_inferior = min(min(lado) for lado in niveis_finais)
    if diferenca_inferior <= -12 and maior_nivel_base_giratorio <= 9:
        print(f"Diferença de nível de {abs(diferenca_inferior)} e o ponto com giratório mais alto na parte de baixo é o 'x'. Necessário usar sucata de trilho na parte inferior.")
        opt = input('Deseja aumentar a altura dos vidros em +3mm para embutir a contrafechadura? [s/n]').strip().lower()
        if opt == 's':
            diferenca = 3
            niveis_finais = [[nivel - diferenca for nivel in lado] for lado in niveis_finais]
        elif opt == 'n':
            pass
        else:
            print('Por favor, digite apenas o caracteres "s" ou "n".')
  
    return niveis_finais

def alturas_por_nivel(alturas, niveis_finais):
    alturas_com_base_0 = [[altura + niveis_finais[i][j] for j, altura in enumerate(lado)] for i, lado in enumerate(alturas)]
    return alturas_com_base_0

def diferença_alturas(alturas_com_base_0, lcs, quant_vidros, sentidos_abert):
    # 2.1 Ajustando alturas pelo giratorio    
    alturas_giratorios = obter_altura_giratorios(sentidos_abert, quant_vidros, alturas_com_base_0, lcs)
    menor_altura_giratorio = min(alturas_giratorios)
    diferencas_de_altura = [altura - menor_altura_giratorio for altura in alturas_giratorios]
    menor_altura_ajustada = min(diferencas_de_altura)

    # 2.2 Reajustando alturas para evitar trilho socado
    if menor_altura_ajustada <= -12:
        diferenca = menor_altura_giratorio + 12
        menor_altura_ajustada = 12
        diferencas_finais = [[nivel + diferenca for nivel in lado] for lado in diferencas_de_altura]
    else:
        diferencas_finais = diferencas_de_altura

    # 2.3 Definição de sucata superior
    diferenca_superior = max(diferencas_finais)
    if diferenca_superior >= 12 and menor_altura_ajustada >= -9:
        print(f"Diferença de altura de {abs(diferenca_superior)} e o ponto com giratório mais baixo na parte de cima é o 'x'. Necessário usar sucata de trilho na parte superior.")
        opt = input('Deseja usar perfil U com calha interna na parte de cima e aumentar a altura dos vidros em +5mm para embutir a molinha na calha do perfil U com calha? [s/n]').strip().lower()
        if opt == 's':
            diferenca = 5
            diferencas_finais = [[altura + diferenca for altura in lado] for lado in diferencas_finais]
        elif opt == 'n':
            pass
        else:
            print('Por favor, digite apenas o caracteres "s" ou "n".')

    return diferencas_finais

def folga_altura_vidro(diferenca_superior, diferenca_inferior):
    if diferenca_superior <= 7 and diferenca_inferior >= -7:
        folga_vidro = 165
    else:
        folga_vidro = 160

    return folga_vidro

def necessidade_de_sucata(niveis_finais, alturas_finais, lcs):
    dist_pedacos = 0
    dist_inteira = 0
    
    # Reverificando diferença pra ver se ainda há necessidade da sucata
    diferenca_inferior = min(min(lado) for lado in niveis_finais)
    if diferenca_inferior <= -12:
        sp, si = calcular_sucata(niveis, lcs)
        dist_pedacos += sp
        dist_inteira += si

    # Reverificando diferença pra ver se ainda há necessidade da sucata
    diferenca_superior = max(alturas_finais)
    if diferenca_superior >= 12:
        sp, si = calcular_sucata(alturas_finais, lcs)
        dist_pedacos += sp
        dist_inteira += si

    return dist_pedacos, dist_inteira

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

def mapear_vidro_para_lado(quant_vidros: list[int]) -> dict[int, tuple[int, int]]:
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

def interpolar_valor_em_x(pontos: list[float], valores: list[float], x: float) -> float:
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
    aberturas: list[list[int]],
    quant_vidros: list[int],
    fonte: list[list[int]],
    lcs: list[int]
) -> list[float]:
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

# if __name__ == 'main':
#     niveis()
#     alturas()
#     necessidade_de_sucata()
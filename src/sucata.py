from math import ceil
from src.calcs_vetor import maior_valor, menor_valor

def definir_diferencas(dif_niveis, base_niv, dif_alturas, base_alt):
    diferencas_niv = [[dif - base_niv if dif != base_niv else dif for dif in lado] for lado in dif_niveis]
    diferenca_niv = menor_valor( diferencas_niv)

    diferencas_alt = [[dif + base_alt if dif != base_alt else dif for dif in lado] for lado in dif_alturas]
    diferenca_alt = maior_valor(diferencas_alt)

    return diferenca_niv, diferenca_alt

def necessidade_de_sucata(diferencas, lcs, posicao, base):
    dist_pedacos = 0
    dist_inteira = 0

    if posicao == 'nivel':
        diferencas = [[dif - base if dif != base else dif for dif in lado] for lado in diferencas]
        diferenca = menor_valor( diferencas)

    if posicao == 'altura':
        diferencas = [[dif + base if dif != base else dif for dif in lado] for lado in diferencas]
        diferenca = maior_valor( diferencas)
        
    if diferenca <= -12 or diferenca >= 12:
        sp, si = calcular_sucata(diferencas, lcs)
        dist_pedacos += ceil(sp/500)
        dist_inteira += ceil(si/100)*100

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

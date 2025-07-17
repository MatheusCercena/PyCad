from math import sqrt, tan, radians

def normalizar(vetor: tuple[float, float]) -> tuple[float, float]:
    """Retorna o vetor unitário (normalizado)"""
    norma = sqrt(vetor[0]**2 + vetor[1]**2)
    return (vetor[0]/norma, vetor[1]/norma)

def multiplicar_vetor(vetor: tuple[float, float], escalar: float) -> tuple[float, float]:
    """Multiplica um vetor por um escalar"""
    return (vetor[0] * escalar, vetor[1] * escalar)

def somar_pontos(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float]:
    """Soma dois pontos/vetores 2D"""
    return (p1[0] + p2[0], p1[1] + p2[1])

def ponto_medio(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float]:
    """Retorna o ponto médio entre dois pontos"""
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def definir_pontos_na_secao(Inicio_secao, vetor_unitario, distancia):
        return (
            Inicio_secao[0] + vetor_unitario[0] * distancia,
            Inicio_secao[1] + vetor_unitario[1] * distancia
        )

def dentro_do_intervalo(valor: float, minimo: float, maximo: float, tol: float = 1e-6) -> bool:
    """
    Verifica se um valor está dentro de um intervalo fechado [minimo, maximo], considerando uma margem de tolerância para evitar erros causados por imprecisão de ponto flutuante.

    Parâmetros:
    - valor (float): o valor a ser testado.
    - minimo (float): limite inferior do intervalo.
    - maximo (float): limite superior do intervalo.
    - tol (float, opcional): tolerância permitida na comparação. Default é 1e-6.

    Retorna:
    - bool: True se valor estiver dentro do intervalo (com tolerância), False caso contrário.
    """

    # Garante que minimo e maximo estejam na ordem correta
    limite_inferior = min(minimo, maximo)
    limite_superior = max(minimo, maximo)

    # Verificação com margem de tolerância
    return (limite_inferior - tol) <= valor <= (limite_superior + tol)

def calcular_gaps_paredes(ang):
    '''
    calcula o gap entre a linha de centro e a parede, que é diferente de 0 no caso de paredes anguladas.
    '''
    cat_adj = 18
    gap_lcs = round((tan(radians(abs(ang))) * cat_adj), 0)
    return gap_lcs

def calcular_gaps_leito(ang):
    '''
    calcula o gap entre os leitos e a linha de centro quando é juncão do tipo vidro-vidro.
    '''
    cat_adj = 14
    gap_leito = round((tan(radians(abs(ang/2))) * cat_adj), 2)
    return gap_leito

def calcular_gaps_vidro(ang, espessura_vidro):
    '''
    calcula o gap entre o vidro e a linha de centro quando é juncão do tipo vidro-vidro.
    '''
    cat_adj = espessura_vidro/2
    gap_vidro = round((tan(radians(abs(ang/2))) * cat_adj), 2)
    return gap_vidro

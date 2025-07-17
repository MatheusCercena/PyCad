from math import sqrt, tan, radians, atan2, cos, sin 

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

def angulo_do_vetor(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Retorna o ângulo (em radianos) do vetor formado por p1 -> p2 em relação ao eixo X."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return atan2(dy, dx)

def vetor_perpendicular_unitario(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float]:
    """Retorna o vetor unitário perpendicular ao vetor formado por p1 -> p2"""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    mod = sqrt(dx**2 + dy**2)
    return (-dy / mod, dx / mod)

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

def obter_pontos_medida_total(perfil: list[tuple[float, float, float]]) -> tuple[tuple[float, float], tuple[float, float]]:
    """
    Dado um perfil com 4 pontos [(x0,y0,z0), (x1,y1,z1), (x2,y2,z2), (x3,y3,z3)] ou em outras palavras [(ini_int), (fim_int), (ini_ext), (fim_ext)] e um offset,
    retorna dois pontos (x, y) que definem corretamente a cota entre os extremos, com offset perpendicular ao vetor base e rotação compensada.
    Retorna: (ponto_inicio, ponto_fim)
    """
    # 1. Vetor base: ponto 0 (início interno) até ponto 1 (fim interno)
    base = perfil[0]
    direcao = perfil[1]
    dx = direcao[0] - base[0]
    dy = direcao[1] - base[1]
    theta = -atan2(dy, dx)  # rotação para alinhar com eixo X

    # 2. Rotaciona todos os pontos para normalizar
    rotacionados = []
    for i, ponto in enumerate(perfil):
        x, y = ponto[:2] 
        xt = x - base[0]
        yt = y - base[1]
        xr = xt * cos(theta) - yt * sin(theta)
        yr = xt * sin(theta) + yt * cos(theta)
        rotacionados.append((i, xr, yr))

    # 3. Identifica os extremos (menor e maior X)
    extremos = sorted(rotacionados, key=lambda p: p[1])
    ponto_ini_idx, x_ini, y_ini = extremos[0]
    ponto_fim_idx, x_fim, y_fim = extremos[-1]

    # ponto início corrigido
    x_rot = x_ini * cos(-theta)
    y_rot = x_ini * sin(-theta)
    
    ponto_inicio = (x_rot + base[0], y_rot + base[1])

    # ponto fim permanece sem offset
    x_rot_fim = x_fim * cos(-theta) - y_fim * sin(-theta)
    y_rot_fim = x_fim * sin(-theta) + y_fim * cos(-theta)
    ponto_fim = (x_rot_fim + base[0], y_rot_fim + base[1])

    return ponto_inicio, ponto_fim

"""
Módulo de funções matemáticas e geométricas auxiliares para cálculos de projetos CAD.

Inclui operações com vetores, pontos, ângulos, distâncias, gaps e manipulação de coordenadas para uso em outros módulos do projeto.
"""
from math import sqrt, tan, radians, atan2, cos, sin 
from math import atan2, cos, sin, radians, degrees
from typing import Tuple, List
import numpy as np

Ponto3D = Tuple[float, float, float]
Ponto2D = Tuple[float, float]

def vetor_entre_pontos(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float]:
    """Calcula o vetor que vai de p1 até p2.
    
    Args:
        p1: Ponto inicial (x, y).
        p2: Ponto final (x, y).
    
    Returns:
        tuple: Vetor (dx, dy) que vai de p1 até p2.
    """
    return (p2[0] - p1[0], p2[1] - p1[1])

def normalizar(vetor: tuple[float, float]) -> tuple[float, float]:
    """Normaliza um vetor para obter o vetor unitário.
    
    Args:
        vetor: Vetor a ser normalizado (x, y).
    
    Returns:
        tuple: Vetor unitário normalizado.
    """
    norma = sqrt(vetor[0]**2 + vetor[1]**2)
    return (vetor[0]/norma, vetor[1]/norma)

def distancia_2d(p1: tuple, p2: tuple) -> float:
    """Calcula a distância euclidiana entre dois pontos 2D.
    
    Args:
        p1: Primeiro ponto (x, y).
        p2: Segundo ponto (x, y).
    
    Returns:
        float: Distância entre os pontos.
    """
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def multiplicar_vetor(vetor: tuple[float, float], escalar: float) -> tuple[float, float]:
    """Multiplica um vetor por um escalar.
    
    Args:
        vetor: Vetor a ser multiplicado (x, y).
        escalar: Valor escalar para multiplicação.
    
    Returns:
        tuple: Vetor resultante da multiplicação.
    """
    return (vetor[0] * escalar, vetor[1] * escalar)

def somar_pontos(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float]:
    """Soma dois pontos/vetores 2D.
    
    Args:
        p1: Primeiro ponto/vetor (x, y).
        p2: Segundo ponto/vetor (x, y).
    
    Returns:
        tuple: Soma dos pontos/vetores.
    """
    return (p1[0] + p2[0], p1[1] + p2[1])

def ponto_medio(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float]:
    """Calcula o ponto médio entre dois pontos.
    
    Args:
        p1: Primeiro ponto (x, y).
        p2: Segundo ponto (x, y).
    
    Returns:
        tuple: Ponto médio entre p1 e p2.
    """
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def angulo_do_vetor(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Calcula o ângulo do vetor formado por p1 -> p2 em relação ao eixo X.
    
    Args:
        p1: Ponto inicial (x, y).
        p2: Ponto final (x, y).
    
    Returns:
        float: Ângulo em radianos do vetor p1 -> p2.
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return atan2(dy, dx)

def vetor_perpendicular_unitario(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float]:
    """Calcula o vetor unitário perpendicular ao vetor formado por p1 -> p2.
    
    Args:
        p1: Ponto inicial (x, y).
        p2: Ponto final (x, y).
    
    Returns:
        tuple: Vetor unitário perpendicular ao vetor p1 -> p2.
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    mod = sqrt(dx**2 + dy**2)
    return (-dy / mod, dx / mod)

def definir_pontos_na_secao(Inicio_secao: tuple[float, float], vetor_unitario: tuple[float, float], distancia: float) -> tuple[float, float]:
    """Define um ponto em uma seção a partir de um ponto inicial, vetor unitário e distância.
    
    Args:
        Inicio_secao: Ponto inicial da seção (x, y).
        vetor_unitario: Vetor unitário da direção (x, y).
        distancia: Distância a partir do ponto inicial.
    
    Returns:
        tuple: Ponto calculado na seção (x, y).
    """
    return (
        Inicio_secao[0] + vetor_unitario[0] * distancia,
        Inicio_secao[1] + vetor_unitario[1] * distancia
    )

def dentro_do_intervalo(valor: float, minimo: float, maximo: float, tol: float = 1e-6) -> bool:
    """Verifica se um valor está dentro de um intervalo fechado.
    
    Considera uma margem de tolerância para evitar erros causados por imprecisão de ponto flutuante.
    
    Args:
        valor: Valor a ser testado.
        minimo: Limite inferior do intervalo.
        maximo: Limite superior do intervalo.
        tol: Tolerância permitida na comparação. Padrão: 1e-6.
    
    Returns:
        bool: True se valor estiver dentro do intervalo (com tolerância), False caso contrário.
    """

    # Garante que minimo e maximo estejam na ordem correta
    limite_inferior = min(minimo, maximo)
    limite_superior = max(minimo, maximo)

    # Verificação com margem de tolerância
    return (limite_inferior - tol) <= valor <= (limite_superior + tol)

def calcular_gaps_paredes(ang: float) -> float:
    """Calcula o gap entre a linha de centro e a parede.
    
    O gap é diferente de 0 no caso de paredes anguladas.
    
    Args:
        ang: Ângulo da parede em graus.
    
    Returns:
        float: Gap calculado entre a linha de centro e a parede.
    """
    cat_adj = 18
    gap_lcs = round((tan(radians(abs(ang))) * cat_adj), 0)
    return gap_lcs

def calcular_gaps_leito(ang: float) -> float:
    """Calcula o gap entre os leitos e a linha de centro.
    
    Usado quando é junção do tipo vidro-vidro.
    
    Args:
        ang: Ângulo da junção em graus.
    
    Returns:
        float: Gap calculado entre os leitos e a linha de centro.
    """
    cat_adj = 14
    gap_leito = round((tan(radians(abs(ang/2))) * cat_adj), 2)
    return gap_leito

def calcular_gaps_vidro(ang: float, espessura_vidro: int) -> float:
    """Calcula o gap entre o vidro e a linha de centro.
    
    Usado quando é junção do tipo vidro-vidro.
    
    Args:
        ang: Ângulo da junção em graus.
        espessura_vidro: Espessura do vidro em milímetros.
    
    Returns:
        float: Gap calculado entre o vidro e a linha de centro.
    """
    cat_adj = espessura_vidro/2
    gap_vidro = round((tan(radians(abs(ang/2))) * cat_adj), 2)
    return gap_vidro

def obter_pontos_medida_total(perfil: list[tuple[float, float, float]]) -> tuple[list[int], tuple[float, float], tuple[float, float]]:
    """Obtém os pontos para cota de medida total de um perfil.
    
    Dado um perfil com 4 pontos [(x0,y0,z0), (x1,y1,z1), (x2,y2,z2), (x3,y3,z3)] 
    ou em outras palavras [(ini_int), (fim_int), (ini_ext), (fim_ext)], retorna 
    dois pontos (x, y) que definem corretamente a cota entre os extremos, com 
    offset perpendicular ao vetor base e rotação compensada.
    
    Args:
        perfil: Lista com 4 pontos 3D do perfil.
    
    Returns:
        tuple: Tupla contendo:
            - Lista com índices dos pontos extremos
            - Ponto de início da cota (x, y)
            - Ponto de fim da cota (x, y)
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
    extremos = rotacionados
    extremos_sorted = sorted(extremos, key=lambda p: p[1])
    ponto_ini_idx, x_ini, y_ini = extremos_sorted[0]
    ponto_fim_idx, x_fim, y_fim = extremos_sorted[-1]

    # pontos corrigidos
    pontos = [ponto_ini_idx, ponto_fim_idx]
    x_rot_ini = x_ini * cos(-theta)
    y_rot_ini = x_ini * sin(-theta)
    ponto_inicio = (x_rot_ini + base[0], y_rot_ini + base[1])

    x_rot_fim = x_fim * cos(-theta)
    y_rot_fim = x_fim * sin(-theta)

    ponto_fim = (x_rot_fim + base[0], y_rot_fim + base[1])

    return pontos, ponto_inicio, ponto_fim
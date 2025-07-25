"""
Módulo de funções matemáticas e geométricas auxiliares para cálculos de projetos CAD.

Inclui operações com vetores, pontos, ângulos, distâncias, gaps e manipulação de coordenadas para uso em outros módulos do projeto.
"""
from math import sqrt, atan2

def vetor_entre_pontos(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float]:
    """Calcula o vetor que vai de p1 até p2."""
    return (p2[0] - p1[0], p2[1] - p1[1])

def normalizar(vetor: tuple[float, float]) -> tuple[float, float]:
    """Normaliza um vetor para obter o vetor unitário."""
    norma = sqrt(vetor[0]**2 + vetor[1]**2)
    return (vetor[0]/norma, vetor[1]/norma)

def distancia_2d(p1: tuple, p2: tuple) -> float:
    """Calcula a distância entre dois pontos 2D."""
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def multiplicar_vetor(vetor: tuple[float, float], escalar: float) -> tuple[float, float]:
    """Multiplica um vetor por um escalar."""
    return (vetor[0] * escalar, vetor[1] * escalar)

def somar_pontos(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float]:
    """Soma dois pontos/vetores 2D."""
    return (p1[0] + p2[0], p1[1] + p2[1])

def ponto_medio(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float]:
    """Calcula o ponto médio entre dois pontos."""
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def angulo_do_vetor(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Calcula o ângulo em radianos do vetor formado por p1 -> p2 em relação ao eixo X."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return atan2(dy, dx)

def normalizar_coordenadas(ponto_inicial: tuple[float, float], p1: tuple[float, float], p2: tuple[float, float]) -> tuple[int, int]:
    '''
    Retorna as coordenadas de p1 e p2 como a distancia linear delas em relação ao ponto inicial.
    '''
    novo_p1 = distancia_2d(ponto_inicial, p1)
    novo_p2 = distancia_2d(ponto_inicial, p2)
    return novo_p1, novo_p2

def esta_entre(a: float, x: float, y: float) -> bool:
    if a >= min(x, y) and a <= max(x, y):
        return True
    else: 
        return False

def vetor_perpendicular_unitario(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float]:
    """Calcula o vetor unitário perpendicular ao vetor formado por p1 -> p2."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    mod = sqrt(dx**2 + dy**2)
    return (-dy / mod, dx / mod)

def linha_paralela_com_offset(p1: tuple[float, float], p2: tuple[float, float], offset: float) -> tuple[tuple[float, float], tuple[float, float]]:
    """Retorna os dois pontos de uma linha paralela deslocada por um offset perpendicular"""
    vetor_perp = vetor_perpendicular_unitario(p1, p2)
    deslocamento = multiplicar_vetor(vetor_perp, offset)

    novo_p1 = somar_pontos(p1, deslocamento)
    novo_p2 = somar_pontos(p2, deslocamento)

    return novo_p1, novo_p2

def deslocar_pontos_direcao(p1: tuple[float, float], p2: tuple[float, float], desloc_p1: float, desloc_p2: float) -> tuple[tuple[float, float], tuple[float, float]]:
    """Retorna dois pontos deslocados ao longo da direção do vetor p1 → p2, com deslocamentos independentes para cada extremidade."""
    vetor = vetor_entre_pontos(p1, p2)
    vetor_unitario = normalizar(vetor)

    novo_p1 = somar_pontos(p1, multiplicar_vetor(vetor_unitario, desloc_p1))
    novo_p2 = somar_pontos(p2, multiplicar_vetor(vetor_unitario, desloc_p2))

    return novo_p1, novo_p2

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

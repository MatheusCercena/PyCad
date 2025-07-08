from pyautocad import Autocad, APoint
from math import sqrt#, tan, radians
# from time import sleep

acad2 = Autocad(create_if_not_exists=True)

# def ponto_offset_perpendicular(p1: APoint, p2: APoint, distancia: float):
#     # vetor da linha p1 -> p2
#     dx = p2.x - p1.x
#     dy = p2.y - p1.y

#     # vetor perpendicular: (-dy, dx) ou (dy, -dx)
#     perp_x = -dy
#     perp_y = dx

#     # normaliza o vetor perpendicular
#     norm = sqrt(perp_x**2 + perp_y**2)
#     if norm == 0:
#         return APoint(p1.x, p1.y + distancia)  # fallback pra vertical

#     unit_x = perp_x / norm
#     unit_y = perp_y / norm

#     # ponto médio da linha
#     mx = (p1.x + p2.x) / 2
#     my = (p1.y + p2.y) / 2

#     # ponto deslocado
#     loc_x = mx + unit_x * distancia
#     loc_y = my + unit_y * distancia

#     return APoint(loc_x, loc_y)

# def puxar_cotas_vidro(coordenadas_vidros):
#     offset = 200
#     for linha in coordenadas_vidros:
#         inicio_linha = APoint(linha[0])
#         fim_linha = APoint(linha[1])

#         loc = ponto_offset_perpendicular(inicio_linha, fim_linha, offset)

#         dim = acad2.model.AddDimAligned(inicio_linha, fim_linha, loc)
#         dim.StyleName = 'Vidro'

from math import sqrt, atan2

def calcular_dist(p1, p2):
    return sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def vetor_para_angulo_rad(p1, p2):
    return atan2(p2[1] - p1[1], p2[0] - p1[0])  # já retorna em radianos

def cotar_maior_lado(leito):
    # leito é uma lista com 4 pontos (x, y)
    lados = [
        (leito[0], leito[1]),
        (leito[1], leito[2]),
        (leito[2], leito[3]),
        (leito[3], leito[0])
    ]
    
    # encontra o lado com maior distância
    lado_mais_longo = max(lados, key=lambda lado: calcular_dist(*lado))
    p1, p2 = APoint(*lado_mais_longo[0]), APoint(*lado_mais_longo[1])
    comprimento = calcular_dist(lado_mais_longo[0], lado_mais_longo[1])
    
    # calcula ângulo e ponto médio
    angulo = vetor_para_angulo_rad(lado_mais_longo[0], lado_mais_longo[1])
    mx = (p1.x + p2.x) / 2
    my = (p1.y + p2.y) / 2

    # desloca cota perpendicularmente ao lado
    offset = -400
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    perp_x = -dy
    perp_y = dx
    norm = sqrt(perp_x**2 + perp_y**2)
    unit_x = perp_x / norm
    unit_y = perp_y / norm
    loc = APoint(mx + unit_x * offset, my + unit_y * offset)

    # desenha a cota com o ângulo correto
    dim = acad2.model.AddDimRotated(p1, p2, loc, angulo)
    dim.StyleName = 'Vidro'

def puxar_cotas_leito(lista_de_leitos):
    for leito in lista_de_leitos:
        cotar_maior_lado(leito)

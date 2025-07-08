from pyautocad import Autocad, APoint
# from math import sqrt, tan, radians
# from time import sleep

acad2 = Autocad(create_if_not_exists=True)

# def puxar_cotas_vidro(coordenadas_vidros):
#     for linha in coordenadas_vidros:
#         inicio_linha = APoint(linha[0])
#         fim_linha = APoint(linha[1])
#         offset = 200
#         loc = APoint( (inicio_linha.x + fim_linha.x)/2, (inicio_linha.y + fim_linha.y)/2+offset)
#         acad2.model.AddDimAligned(inicio_linha, fim_linha, loc)


from math import sqrt
from pyautocad import APoint

def ponto_offset_perpendicular(p1: APoint, p2: APoint, distancia: float):
    # vetor da linha p1 -> p2
    dx = p2.x - p1.x
    dy = p2.y - p1.y

    # vetor perpendicular: (-dy, dx) ou (dy, -dx)
    perp_x = -dy
    perp_y = dx

    # normaliza o vetor perpendicular
    norm = sqrt(perp_x**2 + perp_y**2)
    if norm == 0:
        return APoint(p1.x, p1.y + distancia)  # fallback pra vertical

    unit_x = perp_x / norm
    unit_y = perp_y / norm

    # ponto médio da linha
    mx = (p1.x + p2.x) / 2
    my = (p1.y + p2.y) / 2

    # ponto deslocado
    loc_x = mx + unit_x * distancia
    loc_y = my + unit_y * distancia

    return APoint(loc_x, loc_y)

def puxar_cotas_vidro(coordenadas_vidros):
    offset = 200
    for linha in coordenadas_vidros:
        inicio_linha = APoint(linha[0])
        fim_linha = APoint(linha[1])

        loc = ponto_offset_perpendicular(inicio_linha, fim_linha, offset)

        dim = acad2.model.AddDimAligned(inicio_linha, fim_linha, loc)
        dim.StyleName = 'Vidro'

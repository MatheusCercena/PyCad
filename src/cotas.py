from pyautocad import Autocad, APoint
from src.autocad_conn import get_acad
from math import sqrt, tan, radians
from time import sleep

acad2 = Autocad(create_if_not_exists=True)
acad, acad_ModelSpace = get_acad()

def puxar_cotas_vidro(linhas):
    linhas_convertidas = [acad.HandleToObject(item) for item in linhas]
    for linha in linhas_convertidas:
        p1 = APoint(linha.StartPoint)
        p2 = APoint(linha.EndPoint)

        # Calcula posição da linha de cota deslocando no eixo Y
        offset = 200
        mid_y = (p1.y + p2.y) / 2 + offset
        dim_line_loc = APoint((p1.x + p2.x) / 2, mid_y)

        acad_ModelSpace.AddDimAligned(p1, p2, dim_line_loc)

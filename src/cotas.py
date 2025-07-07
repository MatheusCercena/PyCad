from pyautocad import Autocad, APoint
from src.autocad_conn import get_acad
from math import sqrt, tan, radians
from time import sleep

acad2 = Autocad(create_if_not_exists=True)
acad, acad_ModelSpace = get_acad()

def puxar_cotas_vidro(coord):
    for linha in coord:
        inicio_linha = APoint(linha[0])
        fim_linha = APoint(linha[1])
        offset = 200

        loc = APoint( ((inicio_linha.x + fim_linha.x)+offset)/2, ((inicio_linha.y + fim_linha.y)+offset)/2  )

        print(inicio_linha)
        print(fim_linha)
        print(loc)
        acad2.model.AddDimAligned(inicio_linha, fim_linha, loc)

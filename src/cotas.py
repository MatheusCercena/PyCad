from pyautocad import Autocad, APoint
from math import sqrt,atan2
from src.calcs import obter_pontos_medida_total, ponto_medio, somar_pontos, multiplicar_vetor, vetor_perpendicular_unitario, angulo_do_vetor

acad = Autocad(create_if_not_exists=True)

def cotar_medida_total(perfis, tipo_cota='ISO-25', offset=200):
    for perfil in perfis:
        p1, p2 = obter_pontos_medida_total(perfil)
        a1 = APoint(*p1)
        a2 = APoint(*p2)

        # Ângulo da cota (do vetor do lado interno)
        x0, y0, _ = perfil[0]
        x1, y1, _ = perfil[1]
        ang = angulo_do_vetor((x0, y0), (x1, y1))

        # Vetor perpendicular unitário
        v_perp = vetor_perpendicular_unitario(p1, p2)

        # Ponto médio com offset perpendicular
        meio = ponto_medio(p1, p2)
        deslocado = somar_pontos(meio, multiplicar_vetor(v_perp, offset))
        loc = APoint(*deslocado)

        # Criar a cota
        dim = acad.model.AddDimRotated(a1, a2, loc, ang)
        dim.TextRotation = ang
        dim.StyleName = tipo_cota
        dim.TextMovement = 0
        dim.TextOutsideAlign = False
        dim.TextInsideAlign = True

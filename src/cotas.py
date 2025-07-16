from pyautocad import Autocad, APoint
from math import sqrt,atan2, cos, sin, hypot

acad = Autocad(create_if_not_exists=True)

def cotar_medida_total(perfis, tipo_cota='ISO-25', offset=200):
    for perfil in perfis:
        p1, p2 = obter_pontos_para_cota_corrigida(perfil)
        a1 = APoint(p1[0], p1[1])
        a2 = APoint(p2[0], p2[1])

        # Calcula ângulo da cota (mesmo do vetor base interno)
        dx = perfil[1][0] - perfil[0][0]
        dy = perfil[1][1] - perfil[0][1]
        ang = atan2(dy, dx)

        # vetor base da cota (direção do perfil)
        dx = a2.x - a1.x
        dy = a2.y - a1.y
        mod = sqrt(dx**2 + dy**2)

        # vetor perpendicular unitário
        vx = -dy / mod
        vy =  dx / mod

        # aplica offset de 200mm na direção perpendicular
        loc_x = (a1.x + a2.x) / 2 + vx * offset
        loc_y = (a1.y + a2.y) / 2 + vy * offset
        loc = APoint(loc_x, loc_y)

        dim = acad.model.AddDimRotated(a1, a2, loc, ang)
        dim.TextRotation = ang
        dim.StyleName = tipo_cota
        dim.TextInsideAlign = True     
        dim.TextMovement = 0
        dim.TextOutsideAlign = False  # evita forçar pra fora
        dim.TextInsideAlign = True    # tenta centralizar o texto
        
def obter_pontos_para_cota_corrigida(perfil):
    """
    Dado um leito com 4 pontos [(x0,y0,z0), (x1,y1,z1), (x2,y2,z2), (x3,y3,z3)] e um offset,
    Dado um leito com 4 pontos [(ini_int), (fim_int), (ini_ext), (fim_ext)] e um offset,
    retorna dois pontos (x, y) que definem corretamente a cota entre os extremos,
    com offset perpendicular ao vetor base e rotação compensada.
    [(12.0, 4.0, 0.0), (337.0, 4.0, 0.0)], 
    [0.0, 0.0, 1000.0, 0.0]
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

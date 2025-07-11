from pyautocad import Autocad, APoint
from math import sqrt,atan2, cos, sin, degrees
from src.ucs import definir_ucs
acad2 = Autocad(create_if_not_exists=True)

def cotar_medida_total(perfis, offset=28):
    for i, perfil in enumerate(perfis):
        print(f'perfil {perfil}')
        p1 = perfil[0]
        p2 = perfil[-1]
        print(f'p1 {p1}')
        print(f'p2 {p2}')
        definir_ucs(i, p1, p2)

        p1, p2 = obter_pontos_para_cota_corrigida(perfil, offset)
        a1 = APoint(*p1)
        a2 = APoint(*p2)

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
        offset = 200
        loc_x = (a1.x + a2.x) / 2 + vx * offset
        loc_y = (a1.y + a2.y) / 2 + vy * offset
        loc = APoint(loc_x, loc_y)

        for i, (p1, p2) in enumerate(perfis):
            acad2.model.AddDimRotated(a1, a2, loc, ang)


def obter_pontos_para_cota_corrigida(leito, offset=28):
    """
    Dado um leito com 4 pontos [(x0,y0), (x1,y1), (x2,y2), (x3,y3)] e um offset,
    retorna dois pontos (x, y) que definem corretamente a cota entre os extremos,
    com offset perpendicular ao vetor base e rotação compensada.
    
    Retorna: (ponto_inicio, ponto_fim)
    """

    # 1. Vetor base: ponto 0 (início interno) até ponto 1 (fim interno)
    base = leito[0]
    direcao = leito[1]
    dx = direcao[0] - base[0]
    dy = direcao[1] - base[1]
    theta = -atan2(dy, dx)  # rotação para alinhar com eixo X

    # 2. Rotaciona todos os pontos para normalizar
    rotacionados = []
    for i, ponto in enumerate(leito):
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
        


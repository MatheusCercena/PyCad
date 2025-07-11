from pyautocad import Autocad
import pythoncom
import win32com.client
import math
from src.autocad_conn import get_acad

pythoncom.CoInitialize()
acad = Autocad()
doc = acad.doc
acad2, acad_ModelSpace = get_acad()

def vetor_unitario(p1, p2):
    """Calcula vetor unitário entre dois pontos"""
    dx, dy, dz = [p2[i] - p1[i] for i in range(3)]
    mag = math.sqrt(dx**2 + dy**2 + dz**2)
    return (dx / mag, dy / mag, dz / mag)

def vetor_perpendicular_2d(v):
    """Retorna vetor perpendicular no plano XY (Z=0)"""
    return (-v[1], v[0], 0.0)

def para_variant(pt):
    """Converte tupla com floats em VARIANT aceito pelo AutoCAD"""
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, tuple(float(x) for x in pt))

def arredondar_vetor(v, casas=6):
    return tuple(round(float(x), casas) for x in v)

def definir_ucs(indice, p1, p2):
    '''
    Define um UCS baseado nos pontos inicial (p1) e final (p2) de um perfil.

    - p1: ponto de origem do UCS
    - p2: ponto ao longo do eixo Y (direção do perfil)
    - Um ponto px perpendicular é calculado automaticamente para compor o eixo X.
    '''
    # Converte para tupla de 3 floats (se só veio x, y)
    if len(p1) == 2:
        p1 = (*p1, 0.0)
    if len(p2) == 2:
        p2 = (*p2, 0.0)

    # Arredonda os pontos
    p1 = tuple(round(c, 6) for c in p1)
    p2 = tuple(round(c, 6) for c in p2)

    # Calcula ponto no eixo X a partir da perpendicular 2D a p1 → p2
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    px = (p1[0] + dy, p1[1] - dx, p1[2])  # deslocamento ortogonal no plano XY

    nome_ucs = f"PerfilUCS_{indice}"

    # Deleta UCS anterior com mesmo nome (evita erro)
    for ucs in doc.UserCoordinateSystems:
        if ucs.Name == nome_ucs:
            ucs.Delete()
            break

    ucs = doc.UserCoordinateSystems.Add(p1, px, p2, nome_ucs)
    viewport = doc.ActiveViewport
    viewport.UCS = ucs
    doc.ActiveViewport = viewport
    doc.Regen(1)


def definir_ucs_por_pontos(p0, px, py, nome="MeuUCS"):
    """
    Define um UCS no AutoCAD com base em três pontos:
    - p0: ponto de origem
    - px: ponto ao longo do eixo X
    - py: ponto ao longo do eixo Y
    """
    p0 = tuple(round(c, 6) for c in p0)
    px = tuple(round(c, 6) for c in px)
    py = tuple(round(c, 6) for c in py)

    # Deleta UCS anterior se existir
    for ucs in doc.UserCoordinateSystems:
        if ucs.Name == nome:
            ucs.Delete()
            break

    ucs = doc.UserCoordinateSystems.Add(p0, px, py, nome)
    doc.ActiveViewport.UCS = ucs
    doc.ActiveViewport = doc.ActiveViewport
    doc.Regen(1)

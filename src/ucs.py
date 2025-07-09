from pyautocad import Autocad
import pythoncom
import win32com.client
import math

pythoncom.CoInitialize()
acad = Autocad()
doc = acad.doc

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
    param indice: usado para o nome do ucs dentro da funcao
    param p1: coordenadas x e y do começo do perfil
    param p2: coordenadas x e y do final do perfil
    '''
    origem = p1
    eixo_x = vetor_unitario(p1, p2)
    eixo_y = vetor_perpendicular_2d(eixo_x)
    
    # Converte para VARIANTs
    origem = arredondar_vetor(origem)
    eixo_x  = arredondar_vetor(eixo_x)
    eixo_y  = arredondar_vetor(eixo_y)

    print(f"Origem: {origem}")
    print(f"Eixo X: {eixo_x}")
    print(f"Eixo Y: {eixo_y}")

    for u in doc.UserCoordinateSystems:
        if u.Name == nome_ucs:
            u.Delete()
            break

    if sum(abs(c) for c in eixo_x) < 1e-6 or sum(abs(c) for c in eixo_y) < 1e-6:
        print(f"[ERRO] Vetores nulos no UCS {indice}. Pulando.")
        return
    # Cria UCS com nome único
    nome_ucs = f"PerfilUCS_{indice}"
    ucs = doc.UserCoordinateSystems.Add(origem, eixo_x, eixo_y, nome_ucs)

    # Aplica no viewport ativo
    viewport = doc.ActiveViewport
    viewport.UCS = ucs
    doc.ActiveViewport = viewport
    doc.Regen(1)
"""
Desenha os perfis U, através de offsets chamados via COM e fillets por lisp.
"""

from copy import deepcopy
from src.autocad_conn import get_acad

acad, acad_ModelSpace = get_acad()

def offset_perfis_U(handles_lcs):
    offset_ext = 20
    offset_int = 32

    handles = {'externos': [], 'internos': []}
    for linha in handles_lcs:
        linha_ext = linha.Offset(offset_ext)#.Offset retorna uma tupla
        linha_ext[0].Layer = 'Perfil U Externo'
        handles['externos'].append(linha_ext[0].Handle)

        linha_int = linha.Offset(-offset_int)
        linha_int[0].Layer = 'Perfil U Interno'
        handles['internos'].append(linha_int[0].Handle)
    return handles

def fillet_perfis_U(handles):
    linhas_externas = deepcopy(handles['externos'])
    linhas_internas = deepcopy(handles['internos'])

    for index in range(0, len(linhas_externas)-1):
        acad.SendCommand(f'(c:custom_fillet "{linhas_externas[index]}" "{linhas_externas[index+1]}")\n')
        acad.SendCommand(f'(c:custom_fillet "{linhas_internas[index]}" "{linhas_internas[index+1]}")\n')

def definir_coord_perfis_U(handles):
    linhas_externas = deepcopy(handles['externos'])
    linhas_internas = deepcopy(handles['internos'])
    coordenadas = []
    for linha in range(len(linhas_externas)):
        coord = []
        
        linha_ext = acad.HandleToObject(linhas_externas[linha])
        coord.append(linha_ext.StartPoint)
        coord.append(linha_ext.EndPoint)
    
        linha_int = acad.HandleToObject(linhas_internas[linha])
        coord.append(linha_int.StartPoint)
        coord.append(linha_int.EndPoint)

        coordenadas.append(coord)
    return coordenadas
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

def definir_coord_perfis_U(handles, aberturas_por_lado):
    linhas_externas = deepcopy(handles['externos'])
    linhas_internas = deepcopy(handles['internos'])
    coordenadas = []

    for linha in range(len(linhas_externas)):

        if aberturas_por_lado[linha] != 0:
            #adicionar if pra caso o lado seja maior que 1980 e menor que elevador, definir a medida
            pass

        coord = []
        
        linha_ext = acad.HandleToObject(linhas_externas[linha])
        coord.append(linha_ext.StartPoint)
        coord.append(linha_ext.EndPoint)
    
        linha_int = acad.HandleToObject(linhas_internas[linha])
        coord.append(linha_int.StartPoint)
        coord.append(linha_int.EndPoint)

        coordenadas.append(coord)
    return coordenadas

def distribuir_vidros_por_lado(quant_vidros):
    """
    Recebe uma lista com a quantidade de vidros por lado e retorna uma lista de sublistas,
    cada uma contendo os números sequenciais dos vidros de cada lado.

    Exemplo:
    Entrada: [3, 5, 2]
    Saída: [[1, 2, 3], [4, 5, 6, 7, 8], [9, 10]]
    """
    todos_vidros = []
    cont = 1

    for qtd in quant_vidros:
        vidros_lado = list(range(cont, cont + qtd))
        todos_vidros.append(vidros_lado)
        cont += qtd

    return todos_vidros

def associar_aberturas_aos_lados(quant_vidros, aberturas):
    '''
    param quant_vidros: lista com quantidade de vidros por lado
    param aberturas: lista com valores de cada abertura conforme funcao "solicitar sentido de abertura"
    '''
    todos_vidros = distribuir_vidros_por_lado(quant_vidros)
    resultado = []
    for abertura in aberturas:
        for lado in todos_vidros:
            if abertura[2] in lado:
                resultado.append(abertura[4])
                break
            else:
                resultado.append(0)
    return resultado


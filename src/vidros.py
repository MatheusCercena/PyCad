"""
Desenha os vidros, através de offsets chamados via COM e fillets por lisp.
"""

from src.autocad_conn import get_acad
from copy import deepcopy

acad, acad_ModelSpace = get_acad()

def offset_vidros(handles_lcs):
    offset_ext = 4
    offset_int = 4

    handles = {'externos': [], 'internos': []}
    for linha in handles_lcs:
        linha_ext = linha.Offset(offset_ext)#.Offset retorna uma tupla
        linha_ext[0].Layer = 'Vidro Externo'
        handles['externos'].append(linha_ext[0].Handle)

        linha_int = linha.Offset(-offset_int)
        linha_int[0].Layer = 'Vidro Interno'
        handles['internos'].append(linha_int[0].Handle)
    return handles

def fillet_vidros(handles):
    linhas_externas = deepcopy(handles['externos'])
    linhas_internas = deepcopy(handles['internos'])

    for index in range(0, len(linhas_externas)-1):
        acad.SendCommand(f'(c:custom_fillet "{linhas_externas[index]}" "{linhas_externas[index+1]}")\n')
        acad.SendCommand(f'(c:custom_fillet "{linhas_internas[index]}" "{linhas_internas[index+1]}")\n')

# SUGESTAO: PEGAR AS COORDENAS DEPOIS DO FILLET DE CIMA, CALCULAR AS LINHAS, DEPOIS APAGAR A LINHA INTEIRA E DESENHAR AS INDIVIDUAIS E DAR OFFSET DE 8 PRA BAIXO
# DEPOIS, COM A MEDIDA DOS PERFIS E MATERIAIS, COMECAR A COLOCAR NO ECG COM SELENIUM

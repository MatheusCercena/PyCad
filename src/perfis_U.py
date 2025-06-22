"""
Desenha os perfis U, através de offsets chamados via COM e fillets por lisp.
"""

import win32com.client
import os
from time import sleep
from src.linhas_de_centro import ordem_lcs
from copy import deepcopy

# Conecta ao AutoCAD
acad = win32com.client.Dispatch("AutoCAD.Application").ActiveDocument
acad_ModelSpace = acad.ModelSpace

def carregar_comando_fillet():
    '''
    Futuramente, caso precise fazer novos comandos, adicionar no lisp_code e corrigir nomes das funcoes para algo como "carregar_comandos_customizados"
    '''
    lisp_code = f'''
(defun c:custom_fillet ( h1 h2 / linha1 linha2)
    (setq linha1 (handent h1))
    (setq linha2 (handent h2))
    (command "_.fillet" linha1 linha2)
    (princ "\nComando")
    (princ)
)
'''
    #__file__ retorna a pasta atual, lisp é a pasta a ser criada, os.path.join junta os 2 caminhos
    dir_base = os.path.join(os.path.dirname(__file__), 'lisp')
    os.makedirs(dir_base, exist_ok=True)
    dir_lisp = os.path.join(dir_base, "custom_fillet_perfil_U.lsp")

    with open(dir_lisp, "w") as file:
        file.write(lisp_code.strip())
    caminho_lisp = os.path.normpath(dir_lisp).replace("\\", "\\\\")
    acad.SendCommand(f'(load "{caminho_lisp}")\n')
    sleep(3)

def offset_perfis_U():
    offset_ext = 20
    offset_int = 32
    linhas = []
    
    for linha in acad_ModelSpace:
        if linha.EntityName == 'AcDbLine' and linha.Layer == 'Linha de Centro':
            linhas.append(linha)

    handles = {'externos': [], 'internos': []}
    for linha in linhas:
        # método .Offset sempre retorna tuplas mesmo que com 1 elemento.
        linha_ext = linha.Offset(offset_ext)
        linha_ext[0].Layer = 'Perfil U Externo'
        handles['externos'].append(linha_ext[0].Handle)

        linha_int = linha.Offset(-offset_int)
        linha_int[0].Layer = 'Perfil U Interno'
        handles['internos'].append(linha_int[0].Handle)
    return handles

def fillet_perfis_U(handles, ordem: list):
    linhas_externas = deepcopy(handles['externos'])
    linhas_internas = deepcopy(handles['internos'])

    for index, value in enumerate(ordem):
        linhas_externas[value] = handles['externos'][index]
        linhas_internas[value] = handles['internos'][index]

    for index in range(0, len(ordem)-1):
        acad.SendCommand(f'(c:custom_fillet "{linhas_externas[index]}" "{linhas_externas[index+1]}")\n')
        acad.SendCommand(f'(c:custom_fillet "{linhas_internas[index]}" "{linhas_internas[index+1]}")\n')


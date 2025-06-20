"""
Desenha os perfis U, através de offsets chamados via COM e fillets por lisp.
"""

import win32com.client
import os
from time import sleep
from src.linhas_de_centro import ordem_lcs

# Conecta ao AutoCAD
acad = win32com.client.Dispatch("AutoCAD.Application").ActiveDocument
acad_ModelSpace = acad.ModelSpace

def dar_fillet(handle1: int, handle2: int):
    lisp_code = f'''
(defun c:custom_fillet ( / linha1 linha2)
    (setq linha1 (handent "{handle1}"))
    (setq linha2 (handent "{handle2}"))
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
    sleep(1)
    acad.SendCommand('custom_fillet\n')
    

def offset_perfis_U(lcs, sec_princ):
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

def fillet_perfis_U(handles, sec_princ):
    #Converter para fillet
    linhas_externas = []
    for index, linha in enumerate(reversed(handles['externos'])):
        if index < sec_princ:
            linhas_externas.append(linha)
    linhas_externas.append(handles['externos'][sec_princ])
    for index, linha in enumerate(handles['externos']):
        if index > sec_princ:
            linhas_externas.append(linha)
    print(linhas_externas)
    for index in range(0, len(linhas_externas)-1):
        dar_fillet(linhas_externas[index], linhas_externas[index+1])

    #Converter para fillet
    linhas_internas = []
    for index, linha in enumerate(reversed(handles['internos'])):
        if index < sec_princ:
            linhas_internas.append(linha)
    linhas_internas.append(handles['internos'][sec_princ])
    for index, linha in enumerate(handles['internos']):
        if index > sec_princ:
            linhas_internas.append(linha)
    print(linhas_internas)
    for index in range(0, len(linhas_internas)-1):
        dar_fillet(linhas_internas[index], linhas_internas[index+1])

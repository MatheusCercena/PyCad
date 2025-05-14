"""
Desenha os perfis U, através de offsets chamados via COM e fillets por lisp.
"""

import win32com.client
import os
from time import sleep

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
    print("Caminho LISP:", repr(os.path.normpath(dir_lisp)))
    caminho_lisp = os.path.normpath(dir_lisp).replace("\\", "\\\\")
    print(caminho_lisp)
    try:
        acad.SendCommand(f'(load "{caminho_lisp}")\n')

    except:
        print('nope')
    sleep(1.5)
    try:
        acad.SendCommand('(custom_fillet)\n')
    except:
        print('nope2')


def offset_perfis_U():
    offset_ext = 20
    offset_int = 32
    handles = []

    for linha in acad_ModelSpace:
        if linha.EntityName == 'AcDbLine' and linha.Layer == 'Linha de Centro':
            #método offset sempre retorna uma tupla, então e preciso iterar sobre ela, mesmo que possua apenas 1 elemento
            linha_ext = linha.Offset(offset_ext)
            linha_int = linha.Offset(-offset_int)

            for linha in linha_ext:
                linha.Layer = 'Perfil U Externo'
                handle = linha.Handle
                handles.append(handle)

            for linha in linha_int:
                linha.Layer = 'Perfil U Interno'
                handle = linha.Handle
                handles.append(handle)
                
    dar_fillet(handles[0], handles[2])

    dar_fillet(handles[1], handles[3])

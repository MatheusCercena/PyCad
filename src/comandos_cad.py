"""
Módulo para carregamento de comandos customizados no AutoCAD.

Inclui função para carregar rotinas LISP personalizadas, facilitando operações como fillet automatizado entre entidades.
"""
import os
from time import sleep
from src.autocad_conn import get_acad

acad, acad_ModelSpace = get_acad()

def carregar_comandos() -> None:
    """Carrega comandos customizados no AutoCAD.
    
    Carrega comandos customizados no AutoCAD. Usar preferivelmente no começo do código, 
    para evitar erros de difícil identificação.
    
    Returns:
        None: Função carrega comandos no AutoCAD sem retorno.
    """
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

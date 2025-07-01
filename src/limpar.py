from pyautocad import Autocad
from src.autocad_conn import get_acad
from time import sleep

acad2 = Autocad(create_if_not_exists=True)
acad, acad_ModelSpace = get_acad()

def limpar_tudo():
    for linha in acad_ModelSpace:
        linha.Delete()
    sleep(1)

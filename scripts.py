from pyautocad import Autocad, APoint
from math import pi
# Conectar ao AutoCAD
acad = Autocad(create_if_not_exists=True)
print("Conectado ao AutoCAD:", acad.app.Name)

lcs = []
angs_ex = []
angs_in = []
conv_rad = angs_in*(pi/180)
def pedir_lcs():
    cont = 0
    while True:
        lc_secoes = input(f'Digite a linha de centro da S{cont+1}: ')
        lcs.append(lc_secoes)
        cont +=1
        res = input('Ha outra linha de centro? ')
        if res != '':
            break
def pedir_angParedes():
    ang_esq = input(f'Digite o angulo da extremidade esquerda: ')
    ang_dir = input(f'Digite o angulo da extremidade direita: ')
    angs_ex.append(ang_esq)
    angs_ex.append(ang_dir)
def pedir_angSecoes(qntd):
    for c in range(0, qntd):
        ang_sec = input(f'Qual o angulo entre a S{c+1} e a S{c+2}: ')
        angs_in.append(ang_sec)
pedir_lcs()
pedir_angSecoes(len(lcs)-1)
print(angs_in )
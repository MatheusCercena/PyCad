from pyautocad import Autocad, APoint
from math import pi, sin, cos

acad = Autocad(create_if_not_exists=True)
print("Conectado ao AutoCAD:", acad.app.Name)

lcs = []
angs_ex = []
angs_in = []
prumos = []
def conv_rad(ang: float):
    return ang*(pi/180)
def pedir_lcs():
    cont = 0
    while True:
        lc_secoes = int(input(f'Digite a linha de centro da S{cont+1}: '))
        lcs.append(lc_secoes)
        cont +=1
        res = input('Deseja digitar outra linha de centro?')
        if res == '':
            break
def pedir_angSecoes(qntd):
    for c in range(0, qntd-1):
        ang_sec = int(input(f'Qual o angulo entre a S{c+1} e a S{c+2}: '))
        angs_in.append(ang_sec)
pedir_lcs()
pedir_angSecoes(len(lcs))

lcs1_xf = lcs[0]
lcs1_yf = 0
lc1 = acad.model.AddLine(APoint(0, 0), APoint(lcs1_xf, lcs1_yf))
lcs2_xf = lcs1_xf + cos(conv_rad(angs_in[0]))*lcs[1]
lcs2_yf = lcs1_xf + sin(conv_rad(angs_in[0]))*lcs[1]
lc2 = acad.model.AddLine(APoint(lcs1_xf, lcs1_yf), APoint(lcs2_xf, lcs2_yf))

lcs3_xf = lcs2_xf + cos(conv_rad(angs_in[1]))*lcs[2]
lcs3_yf = lcs2_yf + sin(conv_rad(angs_in[1]))*lcs[2]
lc3 = acad.model.AddLine(APoint(lcs2_xf, lcs2_yf), APoint(lcs3_xf, lcs3_yf))

lcs4_xf = lcs3_xf + cos(conv_rad(angs_in[2]))*lcs[3]
lcs4_yf = lcs3_yf + sin(conv_rad(angs_in[2]))*lcs[3]
lc4 = acad.model.AddLine(APoint(lcs3_xf, lcs3_yf), APoint(lcs4_xf, lcs4_yf))





# def pedir_angParedes():
#     ang_esq = int(input(f'Digite o angulo da extremidade esquerda: '))
#     ang_dir = int(input(f'Digite o angulo da extremidade direita: '))
#     angs_ex.append(ang_esq)
#     angs_ex.append(ang_dir)
# def pedir_prumos():
#     prumo_esq = int(input(f'Digite o angulo da extremidade esquerda: '))
#     prumos.append(prumo_esq)
#     prumo_dir = int(input(f'Digite o angulo da extremidade direita: '))
#     prumos.append(prumo_dir)
# def desenhar_linhas_de_centro():
#     s1 = acad.model.AddLine(APoint(xi, yi), APoint(xf, yf))
# # def rotacionar_linhas(seção1, seção2, angulo):
# #     ponto_dir_seção1 = 
# #     ponto_esq_seção1 = 

"""
Desenha as paredes, através de offsets chamados via COM e fillets por lisp.
"""
import pythoncom
from pyautocad import Autocad, APoint
from src.autocad_conn import get_acad
from math import radians
from time import sleep

acad, acad_ModelSpace = get_acad()
acad2 = Autocad(create_if_not_exists=True)

def fazer_parede_esq(lcs, perfil_U_ext, perfil_U_int, angulo):
    '''
    Desenha a parede esquerda sem dar fillet com os perfis U e retorna o handle dela
    return: Handle (str)
    '''
    for tentativa in range(5):
        try:
            pythoncom.PumpWaitingMessages()
            ini = acad.HandleToObject(perfil_U_ext).StartPoint
            fim = acad.HandleToObject(perfil_U_int).StartPoint
            break
        except:
            sleep(0.5)
    linha = acad2.model.AddLine(APoint(ini[0], ini[1]), APoint(fim[0], fim[1]))
    linha.Rotate(APoint(lcs[0], lcs[1]), radians(angulo * 1))
    linha.Layer = 'Paredes'
    return linha.Handle

def fazer_parede_dir(handles_lcs, perfil_U_ext, perfil_U_int, angulo):
    '''
    Desenha a parede direita sem dar fillet com os perfis U e retorna o handle dela
    return: Handle (str)
    '''
    for tentativa in range(5):
        try:
            pythoncom.PumpWaitingMessages()
            ini = acad.HandleToObject(perfil_U_ext).EndPoint
            fim = acad.HandleToObject(perfil_U_int).EndPoint
            break
        except:
            sleep(0.5)
    linha = acad2.model.AddLine(APoint(ini[0], ini[1]), APoint(fim[0], fim[1]))
    linha.Rotate(APoint(handles_lcs[2], handles_lcs[3]), radians(angulo * -1))
    linha.Layer = 'Paredes'
    return linha.Handle

def fillet_paredes(handle_perfil_U_ext, handle_perfil_U_int, handle_parede):
    '''
    Dá fillet nos perfis U com o handle da parede.
    '''
    acad.SendCommand(f'(c:custom_fillet "{handle_perfil_U_ext}" "{handle_parede}")\n')
    acad.SendCommand(f'(c:custom_fillet "{handle_parede}" "{handle_perfil_U_int}")\n')
    
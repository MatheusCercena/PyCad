from src.achar_secao_principal import descobrir_secao_principal
from src.recebimento_da_medicao import pedir_linhas_de_centro, pedir_angSecoes, pedir_angParedes, pedir_prumos
from src.linhas_de_centro import definir_linhas_de_centro, redesenhar_linhas_de_centro, ordem_lcs
from src.perfis_U import offset_perfis_U, fillet_perfis_U
from src.leitos import offset_leitos, fillet_leitos
from src.vidros import offset_vidros, fillet_vidros
from src.paredes import fazer_parede_esq, fazer_parede_dir, fillet_paredes
from src.comandos import carregar_comandos
from time import sleep


if __name__ == "__main__":
    lcs = [1000, 2000, 3000, 2000, 1000]
    angs_in = [-20, -20, -20, -20]
    angs_paredes = [10, -10]
    prumos = [5, -5]
    # lcs = pedir_linhas_de_centro()
    # angs_in = pedir_angSecoes(len(lcs))
    # angs_paredes = pedir_angParedes()
    # prumos = pedir_prumos()

    carregar_comandos()

    pos_lcs = definir_linhas_de_centro(lcs, angs_in)
    sec_princ = descobrir_secao_principal(pos_lcs)
    pos_lcs, handles_lcs = redesenhar_linhas_de_centro(lcs, angs_in, sec_princ)

    handles_perfis_U = offset_perfis_U(handles_lcs)
    fillet_perfis_U(handles_perfis_U)

    parede_esq = fazer_parede_esq(pos_lcs[0], handles_perfis_U['externos'][0], handles_perfis_U['internos'][0], angs_paredes[0])
    parede_dir = fazer_parede_dir(pos_lcs[-1], handles_perfis_U['externos'][-1], handles_perfis_U['internos'][-1], angs_paredes[1])

    fillet_paredes(handles_perfis_U['externos'][0], handles_perfis_U['internos'][0], parede_esq)
    fillet_paredes(handles_perfis_U['externos'][-1], handles_perfis_U['internos'][-1], parede_dir)

    handles_vidros = offset_vidros(handles_lcs)
    fillet_vidros(handles_vidros)

    handles_leitos = offset_leitos(handles_lcs)
    fillet_leitos(handles_leitos)

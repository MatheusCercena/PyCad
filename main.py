from src.achar_secao_principal import descobrir_secao_principal
from src.recebimento_da_medicao import pedir_linhas_de_centro, pedir_quant_vidros, pedir_angSecoes, pedir_angParedes, pedir_prumos, definir_juncoes
from src.linhas_de_centro import definir_linhas_de_centro, redesenhar_linhas_de_centro
from src.perfis_U import offset_perfis_U, fillet_perfis_U
from src.leitos import offset_leitos, fillet_leitos
from src.vidros import offset_vidros, fillet_vidros, medida_dos_vidros, definir_folgas_vidros, pontos_dos_vidros
from src.paredes import fazer_parede_esq, fazer_parede_dir, fillet_paredes
from src.comandos import carregar_comandos
from src.cant_ajustes_angulo import necessidade_cant_ajuste, infos_cant_ajuste


if __name__ == "__main__":
    lcs = pedir_linhas_de_centro()
    quant_vidros = pedir_quant_vidros(lcs)
    angs_in = pedir_angSecoes(lcs)
    angs_paredes = pedir_angParedes()
    # prumos = pedir_prumos()
    juncoes = definir_juncoes(lcs, angs_in)

    carregar_comandos()

    pos_lcs = definir_linhas_de_centro(lcs, angs_in)
    sec_princ = descobrir_secao_principal(pos_lcs)
    pos_lcs, handles_lcs = redesenhar_linhas_de_centro(lcs, angs_in, sec_princ)

    handles_perfis_U = offset_perfis_U(handles_lcs)
    fillet_perfis_U(handles_perfis_U)

    parede_esq = fazer_parede_esq(pos_lcs[0], handles_perfis_U['externos'][0], handles_perfis_U['internos'][0], angs_paredes[0])
    fillet_paredes(handles_perfis_U['externos'][0], handles_perfis_U['internos'][0], parede_esq)

    parede_dir = fazer_parede_dir(pos_lcs[-1], handles_perfis_U['externos'][-1], handles_perfis_U['internos'][-1], angs_paredes[1])
    fillet_paredes(handles_perfis_U['externos'][-1], handles_perfis_U['internos'][-1], parede_dir)

    gap_lcs_parede_esq, gap_cant_esq, necessidade_cant_esq = necessidade_cant_ajuste(angs_paredes[0], True)
    gap_lcs_parede_dir, gap_cant_dir, necessidade_cant_dir = necessidade_cant_ajuste(angs_paredes[1], False)

    gaps_lcs = [gap_lcs_parede_esq, gap_lcs_parede_dir]
    if necessidade_cant_esq == True:
        info_cant_esq = infos_cant_ajuste(gap_cant_esq)
        print(f'Info cant esq: {info_cant_esq}')
    if necessidade_cant_dir == True:
        info_cant_dir = infos_cant_ajuste(gap_cant_dir)
        print(f'Info cant dir: {necessidade_cant_dir}')

    folgas = definir_folgas_vidros(juncoes, gaps_lcs, angs_in)
    vidros = medida_dos_vidros(lcs, quant_vidros, folgas)
    print(f'Vidros sacada = {vidros}')
    cont = 1
    for secao in vidros:
        for medida in secao:
            print(f'V{cont}: {medida}. ', end='')
            cont += 1
    pontos_vidros = pontos_dos_vidros(vidros, folgas)
    print(f'Pontos vidros = {pontos_vidros}')
    handles_vidros = offset_vidros(handles_lcs, vidros, pontos_vidros)
    fillet_vidros(handles_vidros)

    handles_leitos = offset_leitos(handles_lcs)
    fillet_leitos(handles_leitos)

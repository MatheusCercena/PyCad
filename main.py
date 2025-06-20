from src.achar_secao_principal import descobrir_secao_principal
from src.recebimento_da_medicao import pedir_linhas_de_centro, pedir_angSecoes, pedir_angParedes, pedir_prumos
from src.linhas_de_centro import definir_linhas_de_centro, redesenhar_linhas_de_centro
from src.perfis_U import offset_perfis_U, fillet_perfis_U

lcs = pedir_linhas_de_centro()
angs_in = pedir_angSecoes(len(lcs))
# pedir_angParedes()
# pedir_prumos()
pos_lcs = definir_linhas_de_centro(lcs, angs_in)
sec_princ = descobrir_secao_principal(pos_lcs)
pos_lcs = redesenhar_linhas_de_centro(lcs, angs_in, sec_princ)
handles_perfis_U = offset_perfis_U(lcs, sec_princ)
print(handles_perfis_U)
fillet_perfis_U(handles_perfis_U, sec_princ)


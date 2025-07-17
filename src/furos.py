from src.autocad_conn import get_acad

acad, acad_ModelSpace = get_acad()

def definir_pontos_furos(handles_perfis_U):
    for perfil_U in handles_perfis_U:
        acad.HandleToObject(perfil_U).Offset(700)
        #pegar medidas dos vidros pelas posicoes vidros e calcular a partir daí 
        #ou, antes, fazer a função pra dividir os trilhos

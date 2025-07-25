from perfis_U import distribuir_perfis_U_por_lado
from 

def definir_coord_drenos(coord_perfis_U, medidas_perfis_u, espessura_v):
    coordenadas = []
    offset = 700-espessura_v/2

    distribuir_perfis_U_por_lado(def definir_coord_drenos(coord_perfis_U, medidas_perfis_u, espessura_v):
, coord_perfis_U,)
    for index, lado in enumerate(coord_perfis_U):
        p1 = vidro[0]
        p2 = vidro[1]
        novo_p1, novo_p2 = linha_paralela_com_offset(p1, p2, offset)

        p1_final, p2_final = deslocar_pontos_direcao(novo_p1, novo_p2, desloc_p1, desloc_p2)
        coord.append(p1_final)
        coord.append(p2_final)
        coordenadas.append(coord)
        quant_lado += 1

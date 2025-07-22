"""
Módulo responsável por definir pontos de furação nos perfis U com base nas medidas dos perfis e posições dos vidros.

Este módulo interage com o AutoCAD para criar offsets nos perfis U conforme a necessidade do projeto.
"""
from src.autocad_conn import get_acad
from src.calcs_vetor import linha_paralela_com_offset, deslocar_pontos_direcao
from pyautocad import APoint
from src.aberturas import distribuir_vidros_por_lado
from src.calcs_cad import calcular_gaps_furos, calcular_gaps_vidro

acad, acad_ModelSpace = get_acad()

def definir_pontos_furos(coord_vidros: list[list[tuple[float, float, float]]], folgas_vidros: list[list[int, int]], quant_vidros, angs_in, angs_paredes, espessura_v) -> list[list[tuple[float, float, float]]]:
    """Define os pontos para furação dos perfis U.
    
    Args:
        medidas_perfis_U: Lista contendo as medidas dos perfis U.
        pontos_vidros: Lista contendo os pontos dos vidros.
    
    Returns:
        None: Função executa operações no AutoCAD sem retorno.
    """

    folga_parede = -12
    folga_passante = 2
    folga_colante = -7
    folga_vidro_vidro = -1

    offset = 696
    coordenadas = []

    distribuicao = distribuir_vidros_por_lado(quant_vidros)

    coord_vidros_reorganizada = []
    for lado in distribuicao:
        vidros_lado = [coord_vidros[i - 1] for i in lado]
        coord_vidros_reorganizada.append(vidros_lado)

    for index, lado in enumerate(coord_vidros_reorganizada):
        for i, vidro in enumerate(lado):
            coord = []
            coord_50 = []
            p1 = vidro[0]
            p2 = vidro[1]
            novo_p1, novo_p2 = linha_paralela_com_offset(p1, p2, offset)
            cota_de_50_p1 = ''
            cota_de_50_p2 = ''

            #lado esquerdo (desloc_p1)
            if i == 0 and folgas_vidros[index][0] == folga_parede:
                desloc_p1 = folga_parede - calcular_gaps_furos(angs_paredes[0])
            elif i == 0 and folgas_vidros[index][0] == folga_passante:
                desloc_p1 = calcular_gaps_furos(angs_in[index-1]) + folga_passante + 50
                cota_de_50_p2 = desloc_p1
            elif i == 0 and folgas_vidros[index][0] == folga_colante:
                desloc_p1 = calcular_gaps_furos(angs_in[index-1]) + folga_colante + 50
                cota_de_50_p2 = desloc_p1
            elif i == 0 and folgas_vidros[index][0] == folga_vidro_vidro:
                desloc_p1 = calcular_gaps_furos(angs_in[index-1]) - calcular_gaps_vidro(angs_in[index-1], espessura_v) + folga_vidro_vidro + 50
                cota_de_50_p2 = desloc_p1
            else:
                desloc_p1 = -1.5

            #lado direito  (desloc_p2)
            if i == len(lado)-1 and folgas_vidros[index][1] == folga_parede:
                desloc_p2 = folga_parede*-1 + calcular_gaps_furos(angs_paredes[1]) 
            elif i == len(lado)-1 and folgas_vidros[index][1] == folga_passante:
                desloc_p2 = calcular_gaps_furos(angs_in[index])*-1 + folga_passante - 50
                cota_de_50_p1 = desloc_p2
            elif i == len(lado)-1 and folgas_vidros[index][1] == folga_colante:
                desloc_p2 = calcular_gaps_furos(angs_in[index])*-1 + folga_colante*-1 - 50
                cota_de_50_p1 = desloc_p2
            elif i == len(lado)-1 and folgas_vidros[index][1] == folga_vidro_vidro:
                desloc_p2 = calcular_gaps_furos(angs_in[index])*-1 + calcular_gaps_vidro(angs_in[index], espessura_v) + folga_vidro_vidro*-1 - 50
                cota_de_50_p1 = desloc_p2
            else:
                desloc_p2 = 1.5


            p1_final, p2_final = deslocar_pontos_direcao(novo_p1, novo_p2, desloc_p1, desloc_p2)
            coord.append(APoint(*p1_final))
            coord.append(APoint(*p2_final))
            coordenadas.append(coord)

            if cota_de_50_p2:
                p2_50_ini = deslocar_pontos_direcao(p1_final, p2_final, -50, 0)[0]
                p2_50_fim = p1_final
                coord_50.append(APoint(*p2_50_ini))
                coord_50.append(APoint(*p2_50_fim))
                coordenadas.append(coord_50)

            if cota_de_50_p1:
                p2_50_ini = p2_final
                p2_50_fim = deslocar_pontos_direcao(p1_final, p2_final, 0, +50)[1]
                coord_50.append(APoint(*p2_50_ini))
                coord_50.append(APoint(*p2_50_fim))
                coordenadas.append(coord_50)
    return coordenadas

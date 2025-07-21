"""
Módulo responsável por definir pontos de furação nos perfis U com base nas medidas dos perfis e posições dos vidros.

Este módulo interage com o AutoCAD para criar offsets nos perfis U conforme a necessidade do projeto.
"""
from src.autocad_conn import get_acad
from src.calcs_vetor import linha_paralela_com_offset, deslocar_pontos_direcao
from pyautocad import APoint
from src.aberturas import distribuir_vidros_por_lado

acad, acad_ModelSpace = get_acad()

def definir_pontos_furos(coord_vidros: list[list[tuple[float, float, float]]], folgas_vidros: list[list[int, int]], quant_vidros) -> list[list[tuple[float, float, float]]]:
    """Define os pontos para furação dos perfis U.
    
    Args:
        medidas_perfis_U: Lista contendo as medidas dos perfis U.
        pontos_vidros: Lista contendo os pontos dos vidros.
    
    Returns:
        None: Função executa operações no AutoCAD sem retorno.
    """
    offset = 700
    coordenadas = []

    distribuicao = distribuir_vidros_por_lado(quant_vidros)

    coord_vidros_reorganizada = []
    for lado in distribuicao:
        # Ajusta os índices (de 1-based para 0-based)
        vidros_lado = [coord_vidros[i - 1] for i in lado]
        coord_vidros_reorganizada.append(vidros_lado)

    for vidro in coord_vidros:
        coord = []
        p1 = vidro[0]
        p2 = vidro[1]
        novo_p1, novo_p2 = linha_paralela_com_offset(p1, p2, offset)


        desloc_p1 = folgas_vidros
        desloc_p2 = 0

        #continuar com IFs para determinar os pontos de deslocamento
        p1_final, p2_final = deslocar_pontos_direcao(novo_p1, novo_p2, desloc_p1, desloc_p2)

        coord.append(APoint(*p1_final))
        coord.append(APoint(*p2_final))
        coordenadas.append(coord)

    return coordenadas


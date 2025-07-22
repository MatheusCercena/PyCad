"""
Módulo responsável por definir pontos de furação nos perfis U com base nas medidas dos perfis e posições dos vidros.

Este módulo interage com o AutoCAD para criar offsets nos perfis U conforme a necessidade do projeto.
"""
from src.autocad_conn import get_acad
from src.calcs_vetor import linha_paralela_com_offset, deslocar_pontos_direcao, distancia_2d
from pyautocad import APoint
from src.aberturas import distribuir_vidros_por_lado
from src.calcs_cad import calcular_gaps_furos, calcular_gaps_vidro

acad, acad_ModelSpace = get_acad()

def definir_pontos_furos(coord_vidros: list[list[tuple[float, float, float]]], coord_perfis_U: list[list[float]], folgas_vidros: list[list[int, int]], quant_vidros: list[list[int]], angs_in: list[float], angs_paredes: list[float], espessura_v: int) -> list[list[tuple[float, float, float]]]:
    """Define os pontos para furação dos perfis U.
    
    Args:
        medidas_perfis_U: Lista contendo as medidas dos perfis U.
        pontos_vidros: Lista contendo os pontos dos vidros.
    
    Returns:
        None: Função executa operações no AutoCAD sem retorno.
    """

    folga_parede = -12
    folga_passante = 2
    folga_colante = -3-espessura_v/2
    folga_vidro_vidro = -1
    offset = 700-espessura_v/2

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
    
    coordenadas_finais = redefinir_pontos_furos(coordenadas, coord_perfis_U, offset, espessura_v)

    return coordenadas_finais

def normalizar_coordenadas(ponto_inicial: tuple[float, float], p1: tuple[float, float], p2: tuple[float, float]) -> tuple[int, int]:
    '''
    Retorna as coordenadas de p1 e p2 como a distancia linear delas em relação ao ponto inicial.
    '''
    novo_p1 = distancia_2d(ponto_inicial, p1)
    novo_p2 = distancia_2d(ponto_inicial, p2)
    return novo_p1, novo_p2

def esta_entre(a: float, x: float, y: float) -> bool:
    if a > min(x, y) and a < max(x, y):
        return True
    else: 
        return False

def redefinir_pontos_furos(coord_furos: list[list[tuple[float, float, float]]], coord_perfis_U: list[list[float]], offset: int, espessura_v: int) -> list[list[tuple[float, float, float]]]:
    offset_corrigido = offset + espessura_v - espessura_perfil_U
    espessura_perfil_U = 20

    coordenadas_redefinidas = []
    for lado in range(len(coord_perfis_U)):
        perfis_u_lado = coord_perfis_U[lado]
        furos_lado = coord_furos[lado]

        coordenadas_lado_redefinidas = []
        perfis_U_normalizados = []
        furos_normalizados = []
        for perfil in perfis_u_lado:
            ini_nova, fim_nova = linha_paralela_com_offset(perfil[0], perfil[1], offset_corrigido)
            perfil_normalizado = normalizar_coordenadas(perfis_u_lado[0], ini_nova, fim_nova)
            perfis_U_normalizados.append(perfil_normalizado)

        for furo in furos_lado:
            furo_normalizado = normalizar_coordenadas(perfis_u_lado[0], furo[0], furo[1])
            furos_normalizados.append(furo_normalizado)
            
        for i, furo in enumerate(furos_normalizados):
            perfil_tocado = [] 
            for ponto in furo:
                for index, perfil in enumerate(perfis_U_normalizados):
                    if esta_entre(ponto, perfil[0], perfil[1]) == True:
                        perfil_tocado.append(index)
                    break
            if perfil_tocado[0] == perfil_tocado[1]:
                coord_nova_1 = [] #definir
                coord_nova_2 = [] #definir

                coordenadas_lado_redefinidas.extend(coord_nova_1, coord_nova_2)
            else:
                coordenadas_lado_redefinidas.append(furos_lado[i])

        coordenadas_redefinidas.append(coordenadas_lado_redefinidas)
    
    return coordenadas_redefinidas
        

            
"""
Módulo para desenho e manipulação de perfis U no AutoCAD.

Inclui funções para criar offsets, aplicar fillets, distribuir vidros, associar aberturas e calcular coordenadas dos perfis U.
"""
"""
Desenha os perfis U, através de offsets chamados via COM e fillets por lisp.
"""

from copy import deepcopy
from src.autocad_conn import get_acad
from src.calcs_vetor import distancia_2d, normalizar, definir_pontos_na_secao, vetor_entre_pontos
from src.calcs_cad import obter_pontos_medida_total
from pyautocad import APoint

acad, acad_ModelSpace = get_acad()

def offset_perfis_U(handles_lcs: list) -> dict[str, list[str]]:
    """Cria offsets dos perfis U externos e internos.
    
    Args:
        handles_lcs: Lista de handles das linhas de centro.
    
    Returns:
        dict: Dicionário com handles dos perfis U externos e internos.
            - 'externos': Lista de handles dos perfis U externos
            - 'internos': Lista de handles dos perfis U internos
    """
    offset_ext = 20
    offset_int = 32

    handles = {'externos': [], 'internos': []}
    for linha in handles_lcs:
        linha_ext = linha.Offset(offset_ext)#.Offset retorna uma tupla
        linha_ext[0].Layer = 'Perfil U Externo'
        handles['externos'].append(linha_ext[0].Handle)

        linha_int = linha.Offset(-offset_int)
        linha_int[0].Layer = 'Perfil U Interno'
        handles['internos'].append(linha_int[0].Handle)
    return handles

def fillet_perfis_U(handles: dict[str, list[str]]) -> None:
    """Aplica fillets nos perfis U externos e internos.
    
    Args:
        handles: Dicionário contendo handles dos perfis U externos e internos.
    
    Returns:
        None: Função executa comandos no AutoCAD sem retorno.
    """
    linhas_externas = deepcopy(handles['externos'])
    linhas_internas = deepcopy(handles['internos'])

    for index in range(0, len(linhas_externas)-1):
        acad.SendCommand(f'(c:custom_fillet "{linhas_externas[index]}" "{linhas_externas[index+1]}")\n')
        acad.SendCommand(f'(c:custom_fillet "{linhas_internas[index]}" "{linhas_internas[index+1]}")\n')

def definir_coord_perfis_U(handles: dict[str, list[str]]) -> list[list[tuple[float, float, float]]]:
    """Define as coordenadas dos perfis U.
    
    Args:
        handles: Dicionário contendo handles dos perfis U externos e internos.
    
    Returns:
        list: Lista de sublistas que contém 4 tuplas com os pontos x, y, z de cada extremidade do perfil U.
    """
    linhas_externas = deepcopy(handles['externos'])
    linhas_internas = deepcopy(handles['internos'])
    coordenadas = []

    for linha in range(len(linhas_externas)):
        coord = []
        
        linha_ext = acad.HandleToObject(linhas_externas[linha])
        coord.append(linha_ext.StartPoint)
        coord.append(linha_ext.EndPoint)
    
        linha_int = acad.HandleToObject(linhas_internas[linha])
        coord.append(linha_int.StartPoint)
        coord.append(linha_int.EndPoint)

        coordenadas.append(coord)
    return coordenadas

def redefinir_coord_perfis_U(coord_perfis_U: list[list[tuple[float, float, float]]], aberturas_por_lado: list, elevador: int) -> tuple[list[list[float]], list[float]]:
    """Redefine as coordenadas dos perfis U considerando aberturas e elevador.
    
    Args:
        coord_perfis_U: Lista com coordenadas dos perfis U.
        aberturas_por_lado: Lista com aberturas por lado.
        elevador: Altura máxima do elevador.
    
    Returns:
        tuple: Tupla contendo:
            - Lista de listas com medidas dos perfis por seção
            - Lista com coordenadas dos perfis redefinidos
    """
    #corrigir funcao pra que tenha 4 elementos, no caso o 2 internos e 2 externos.

    medidas = []
    coordenadas = []
    for i, lado in enumerate(coord_perfis_U):
        pontos = obter_pontos_medida_total(lado)
        p1 = pontos[1]
        p2 = pontos[2]
        
        comprimento_perfil = distancia_2d(p1, p2)
        comprimento_restante = comprimento_perfil

        perfis_secao = []
        while True:
            if elevador < comprimento_restante > 2800:
                secao_nova = 1980
                perfis_secao.append(secao_nova)
                comprimento_restante -= secao_nova
            elif elevador < comprimento_restante <= 2800:
                secao_nova = comprimento_restante/2
                perfis_secao.append(secao_nova)
                comprimento_restante -= secao_nova
            else:#comprimento_restante < elevador
                if aberturas_por_lado[i] == 'esquerda':
                    if comprimento_restante > 1980:
                        perfis_secao.append(comprimento_restante)
                    else:
                        perfis_secao.insert(0, comprimento_restante)
                elif aberturas_por_lado[i] == 'direita':
                    if comprimento_restante > 1980:
                        perfis_secao.insert(0, comprimento_restante)
                    else:
                        perfis_secao.append(comprimento_restante)
                else:
                    perfis_secao.insert(0, comprimento_restante)
                    #mais tarde fazer funcao pra levar em conta o angulo da sacada.
                break
        medidas.append(perfis_secao)
        vetor = vetor_entre_pontos(p1, p2)
        vetor_unitario = normalizar(vetor)
        ini_perfil = p1
        distancia = 0
        for perfil in perfis_secao:
            distancia += perfil
            coord_perfil = []
            coord_perfil.append(ini_perfil)

            fim_perfil = definir_pontos_na_secao(p1, vetor_unitario, distancia)
            coord_perfil.append(fim_perfil)
            
            ini_perfil = fim_perfil
            coordenadas.append(coord_perfil)
    return medidas, coordenadas

"""
Módulo responsável por definir pontos de furação nos perfis U com base nas medidas dos perfis e posições dos vidros.

Este módulo interage com o AutoCAD para criar offsets nos perfis U conforme a necessidade do projeto.
"""
from src.autocad_conn import get_acad

acad, acad_ModelSpace = get_acad()

def definir_pontos_furos(medidas_perfis_U: list, pontos_vidros: list) -> None:
    """Define os pontos para furação dos perfis U.
    
    Args:
        medidas_perfis_U: Lista contendo as medidas dos perfis U.
        pontos_vidros: Lista contendo os pontos dos vidros.
    
    Returns:
        None: Função executa operações no AutoCAD sem retorno.
    """
    for perfil_U in medidas_perfis_U:
        acad.HandleToObject(perfil_U).Offset(700)
        #pegar medidas dos vidros pelas posicoes vidros e calcular a partir daí 


12,
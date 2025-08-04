'''
NÃO ESTÁ FUNCIONANDO
'''

# from pyautocad import Autocad, APoint
# from src.calcs_vetor import ponto_medio

# acad = Autocad()

# def definir_centro(pos_lcs: list) -> tuple[float, float, float, float]:
#     ponto_ini = (pos_lcs[0][0], pos_lcs[0][1])
#     ponto_fim = (pos_lcs[-1][2], pos_lcs[-1][3])
#     x, y, z = ponto_medio(ponto_ini, ponto_fim)
#     ponto_base = APoint(x, y)
#     return ponto_base

# def get_first_viewport():
#     for obj in acad.doc.PaperSpace:
#         if obj.ObjectName == 'AcDbViewport':
#             return obj
#     return None

# # === Passo 3: centralizar e ajustar escala ===
# def centralizar_viewport(lcs):
#     posicao = definir_centro(lcs)
#     vp = get_first_viewport()
#     vp.Center = posicao
#     vp.DisplayLocked = True
#     vp.Update()


from src.calcs_vetor import ponto_perpendicular_a_vetor, ponto_medio, vetor_entre_pontos, normalizar, angulo_do_vetor
from src.comandos_cad import adicionar_mtext_modelspace, adicionar_texto_modelspace
from pyautocad import APoint

def posicionar_pivos(pos_lcs, sec_princ, pivos: list[int], giratorios: list[int]):
    """
    Posiciona os pivos no CAD.
    """
    ponto_ini = (pos_lcs[sec_princ][0], pos_lcs[sec_princ][1])
    ponto_fim = (pos_lcs[sec_princ][2], pos_lcs[sec_princ][3])
    ponto_base = ponto_medio(ponto_ini, ponto_fim)
    ponto_base = (ponto_base[0] - 450, ponto_base[1])
    ponto_base_pivo = ponto_perpendicular_a_vetor(ponto_base, ponto_ini, ponto_fim, -600)

    linhas = []

    for pivo, giratorio in zip(pivos, giratorios):
        if pivo not in [70, 85, 30, -70, -85, -30]:
            if pivo < 0:
                extra = "puxar da esquerda"
            elif pivo > 0:
                extra = "puxar da direita"
            else:
                extra = ""
        else:
            extra = ""

        linhas.append(f"Pivo V{giratorio}: {abs(pivo)} mm {extra}")

    texto_final = "\n".join(linhas)
    texto = adicionar_mtext_modelspace(texto_final, APoint(*ponto_base_pivo), 70, 1700)
    texto.AttachmentPoint = 2
    ponto_base_pivo = (ponto_base_pivo[0] + 600, ponto_base_pivo[1])
    texto.InsertionPoint = APoint(*ponto_base_pivo)  # reposiciona após mudar o AttachmentPoint


def posicionar_alturas(
        pos_lcs: list[list[float, float, float, float]],
        sec_princ: int,
        maior_altura: int,
        menor_altura: int,
        altura_vidro: int
        ):
    """Posiciona alturas de vidro, vao e painel no CAD.
    """
    ponto_ini = (pos_lcs[sec_princ][0], pos_lcs[sec_princ][1])
    ponto_fim = (pos_lcs[sec_princ][2], pos_lcs[sec_princ][3])
    ponto_base = ponto_medio(ponto_ini, ponto_fim)
    ponto_base = (ponto_base[0] - 450, ponto_base[1])

    ponto_base_vidro = ponto_perpendicular_a_vetor(ponto_base, ponto_ini, ponto_fim, 1200)
    adicionar_texto_modelspace(f'Altura do vidro: {altura_vidro}', APoint(*ponto_base_vidro), 70)

    ponto_base_painel = ponto_perpendicular_a_vetor(ponto_base, ponto_ini, ponto_fim, 1320)
    adicionar_texto_modelspace(f'Altura do painel: {altura_vidro+33}', APoint(*ponto_base_painel), 70)

    ponto_base_vao = ponto_perpendicular_a_vetor(ponto_base, ponto_ini, ponto_fim, -500)
    adicionar_texto_modelspace(f'Alturas do vão: {maior_altura} / {menor_altura}', APoint(*ponto_base_vao), 70)

def posicionar_angulos(pos_lcs, angulos):
    angulo_real_lcs = []
    inicios = []
    lcss = []
    for i, linha in enumerate(pos_lcs):
        x_ini, y_ini, x_fim, y_fim = linha
        p1 = (x_ini, y_ini)
        p2 = (x_fim, y_fim)
        angulo_lcs = angulo_do_vetor(p1, p2)
        angulo_real_lcs.append(angulo_lcs)
        inicios.append(p1)
        lcss.append((p1, p2))

    for i, angulo in enumerate(angulos):
        angulo_lcs_anterior = angulo_real_lcs[i]
        angulo_lcs_posterior = angulo_real_lcs[i + 1]
        angulo_medio = (angulo_lcs_anterior + angulo_lcs_posterior) / 2
        p1 = lcss[i][0]
        p2 = lcss[i + 1][1]
        ponto_base = inicios[i+1]
        ponto_texto = ponto_perpendicular_a_vetor(ponto_base, p1, p2, -125)

        if not 70 < abs(angulo) < 110:
            texto = adicionar_mtext_modelspace(angulo/2, APoint(*ponto_texto), 50, 200)
            texto.AttachmentPoint = 5
            # ponto_base = (ponto_base_pivo[0] + 600, ponto_base_pivo[1])
            # texto.InsertionPoint = APoint(*ponto_base_pivo)  # reposiciona após mudar o AttachmentPoint

            # texto.InsertionPoint = ponto_inicial
            texto.Rotation = angulo_medio

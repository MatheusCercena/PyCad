from src.calcs import calcular_gaps_paredes
    
def necessidade_cant_ajuste(ang, abre_ali: bool):
    '''
    Esperado valor 0 para abertura para dentro e 1 para abertura para fora
    '''
    if abre_ali == True:
        quant_cant = 1
    else:
        quant_cant = 2

    gap_lcs = calcular_gaps_paredes(ang)

    if ang > 0: #espaco vazio pra fora
        if quant_cant == 1:
            gap_cant = gap_lcs
            necessidade = False
        if quant_cant == 2:
            gap_cant = gap_lcs*2
            if gap_cant <= 7:
                necessidade = False
            else:
                necessidade = True
    elif ang < 0: #espaco vazio pra dentro
        if quant_cant == 1:
            gap_cant = gap_lcs
            if gap_cant <= 7:
                necessidade = False
            else:
                necessidade = True
        if quant_cant == 2:
            gap_cant = gap_lcs*2
            if gap_cant <= 7:
                necessidade = False
            else:
                necessidade = True
    else: #90 graus, reto, ang 0
        gap_cant = 0
        necessidade = False

    if necessidade == True:
        gap_lcs = gap_lcs + 2
    else:
        gap_lcs = gap_lcs

    return gap_lcs, gap_cant, necessidade

def infos_cant_ajuste(gap_cant):
    '''
    Retorna modelo da cantoneira necessária, se precisa refilar e a medida das paredes dela caso haja necessidade de refilar
    '''
    if 7 < gap_cant < 15:
        mod = 'ct-005'
        refilada = True
        medida_int = 15
        medida_ext = gap_cant - 2
    elif gap_cant == 15:
        mod = 'ct-005'
        refilada = False
        medida_int = 15
        medida_ext = 15
    elif 15 < gap_cant < 25:
        mod = 'ct-025'
        refilada = True
        medida_int = 25
        medida_ext = gap_cant - 2
    elif gap_cant == 25:
        mod = 'ct-025'
        refilada = False
        medida_int = 25
        medida_ext = 25
    elif 25 < gap_cant < 38:
        mod = 'ct-026'
        refilada = True
        medida_int = 38
        medida_ext = gap_cant - 2
    elif gap_cant == 38:
        mod = 'ct-026'
        refilada = False
        medida_int = 38
        medida_ext = 38
    elif 38 < gap_cant < 50:
        mod = 'ct-050'
        refilada = True
        medida_int = 38 #nao cabe mais no perfil U
        medida_ext = gap_cant - 2
    elif gap_cant == 50:
        mod = 'ct-050'
        refilada = False
        medida_int = 38 #nao cabe mais no perfil U
        medida_ext = 50
    else:
        mod = None
        refilada = None
        medida_int = None
        medida_ext = None

    return mod, refilada, medida_int, medida_ext

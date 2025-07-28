from src.perfis_U import distribuir_perfis_U_por_lado
from src.calcs_vetor import deslocar_pontos_direcao, linha_paralela_com_offset, distancia_2d

def calculo_dreno(medida_lado) -> list[int]:
    '''Calcula a medida entre os drenos e a quantidade de drenos.'''
    sobra_dreno = (medida_lado-400)
    medida_drenos = float()

    if sobra_dreno < 600:
        medida_drenos = sobra_dreno
        quantidade = 1
    elif 800 < sobra_dreno < 1200:
        medida_drenos = sobra_dreno/2
        quantidade = 2
    else:
        quantidade = 1
        medida_drenos_provisoria = 0
        while True:
            medida_drenos = sobra_dreno/quantidade
            if 600 <= medida_drenos <= 800:
                break
            elif medida_drenos_provisoria > 800 and medida_drenos < 600:
                break
            quantidade +=1
            medida_drenos_provisoria = medida_drenos

    if medida_lado < 600:
        medida_drenos = medida_lado/2
        quantidade = 2
        medidas = [medida_drenos]*quantidade
    else:
        medidas = [200] + [int(round(medida_drenos, 0))]*quantidade + [200]

    return medidas

def normalizar_drenos(medidas, medida_lado) -> list[int]:
    ini = 0
    coodenadas_normalizadas = []
    for i, dreno in enumerate(medidas):
        if medida_lado >= 600 and i == len(medidas) - 2:
            coord_ini_norm = ini
            coord_fim_norm = medida_lado - 200
        elif medida_lado >= 600 and i == len(medidas) - 1:
            coord_ini_norm = medida_lado - 200
            coord_fim_norm = medida_lado
        else:
            coord_ini_norm = ini
            coord_fim_norm = coord_ini_norm + dreno
        coodenadas_normalizadas.append((coord_ini_norm, coord_fim_norm))
        ini = coord_fim_norm

    return coodenadas_normalizadas

def definir_coord_drenos(coord_perfis_U, medidas_perfis_u, espessura_ext_perfil_U):
    coordenadas = []
    coordenadas_drenos_por_lado = []
    offset = 850-espessura_ext_perfil_U
    perfis_U = distribuir_perfis_U_por_lado(medidas_perfis_u, coord_perfis_U)

    for lado in perfis_U:
        coordenadas_lado = []
        p1 = lado[0][0] # inicio do primeiro perfil 
        p2 = lado[-1][1] # fim do ultimo perfil
        novo_p1, novo_p2 = linha_paralela_com_offset(p1, p2, offset)

        medida_lado = distancia_2d(novo_p1, novo_p2)

        medidas_drenos = calculo_dreno(medida_lado)
        drenos_normalizados = normalizar_drenos(medidas_drenos, medida_lado)
        
        for dreno in drenos_normalizados:
            p1_final, p2_final = deslocar_pontos_direcao(novo_p1, novo_p2, dreno[0], dreno[1], True)
            coordenadas_lado.append((p1_final, p2_final))

        coordenadas_drenos_por_lado.append(coordenadas_lado)
            
    coordenadas = [coord for lado in coordenadas_drenos_por_lado for coord in lado]
    return coordenadas_drenos_por_lado, coordenadas

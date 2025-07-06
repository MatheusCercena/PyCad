"""
Desenha os leitos, através de offsets chamados via COM e fillets por lisp.
"""
from pyautocad import Autocad, APoint
from src.autocad_conn import get_acad
from math import sqrt, tan, radians
from sympy import symbols, Eq, solve


acad2 = Autocad(create_if_not_exists=True)
acad, acad_ModelSpace = get_acad()

x, y, b = symbols('x y b')

def normalizar(vetor):
    vetor_unitario = sqrt(vetor[0]**2 + vetor[1]**2)
    vetor_unitario_x = vetor[0]/vetor_unitario
    vetor_unitario_y = vetor[1]/vetor_unitario
    
    return (vetor_unitario_x, vetor_unitario_y)

def definir_pontos_na_secao(Inicio_secao, vetor_unitario, distancia):
        return (
            Inicio_secao[0] + vetor_unitario[0] * distancia,
            Inicio_secao[1] + vetor_unitario[1] * distancia
        )

def desenhar_guias_leitos(handles_lcs: list, vidros_sacada: list, posicao_dos_vidros: list, folgas_leitos: list):
    handles_guias_leitos = []
    for i, linha_de_centro in enumerate(handles_lcs):
        
        ini_linha_de_centro = linha_de_centro.StartPoint
        fim_linha_de_centro = linha_de_centro.EndPoint

        vetor_linha = (fim_linha_de_centro[0] - ini_linha_de_centro[0], fim_linha_de_centro[1] - ini_linha_de_centro[1])
        vetores_unitarios = normalizar(vetor_linha)

        for index in range(0, len(vidros_sacada[i])):
            comeco_vidro = posicao_dos_vidros[i][index][0]
            fim_vidro = posicao_dos_vidros[i][index][1]
            inicio = definir_pontos_na_secao(ini_linha_de_centro, vetores_unitarios, comeco_vidro + folgas_leitos[i][index][0])
            fim = definir_pontos_na_secao(ini_linha_de_centro, vetores_unitarios, fim_vidro - folgas_leitos[i][index][1])
            guia = acad2.model.AddLine(APoint(inicio[0], inicio[1]), APoint(fim[0], fim[1]))
            handles_guias_leitos.append(acad.HandleToObject(guia.Handle))
    return handles_guias_leitos

def calcular_gaps_leito(ang):
    '''
    calcula o gap entre os leitos e a linha de centro quando é juncão do tipo vidro-vidro.
    '''
    cat_adj = 14
    gap_leito = round((tan(radians(abs(ang/2))) * cat_adj), 2)
    return gap_leito

def folgas_leitos(vidros, folgas_vidros, angs_in):
    '''
    Calcula as folgas dos leitos para cada vidro em cada seção da sacada.
    
    vidros: lista de listas, cada sublista representa os vidros de uma seção
    folgas_vidros: mesma estrutura que vidros, mas com folgas esquerda/direita
    angs_in: lista com ângulos de entrada das seções
    gaps_lcs: lista com valores de gap (folga) por seção e lado
    '''
    folgas_leitos_sacada = []
    for secao in range(len(vidros)):
        folgas_leitos_secao = []
        for index in range(len(vidros[secao])):
            folgas_leitos_vidro = []
            for lado in range(2):
                if lado == 0:
                    if index == 0:
                        if folgas_vidros[secao][0] == 2:
                            folga_esq = calcular_gaps_leito(angs_in[secao-1]) + 3 
                        elif folgas_vidros[secao][0] == -7:
                            folga_esq = calcular_gaps_leito(angs_in[secao-1]) - 7
                        elif folgas_vidros[secao][0] == -1:
                            if abs(angs_in[secao-1])/2 < 20:
                                folga_esq = 1.5
                            else: 
                                folga_esq = 0
                        else:
                            folga_esq = 1.5
                    else:
                        folga_esq = 1.5
                    folgas_leitos_vidro.append(folga_esq)
                if lado == 1:
                    if index+1 == len(vidros[secao]):                            
                        if folgas_vidros[secao][1] == 2:
                            folga_dir = calcular_gaps_leito(angs_in[secao]) + 3
                        elif folgas_vidros[secao][1] == -7:
                            folga_dir = calcular_gaps_leito(angs_in[secao]) - 7
                        elif folgas_vidros[secao][1] == -1:
                            if abs(angs_in[secao-1])/2 < 20:
                                folga_dir = 1.5
                            else: 
                                folga_dir = 0
                        else:
                            folga_dir = 1.5
                    else:
                        folga_dir = 1.5

                    folgas_leitos_vidro.append(folga_dir)
            folgas_leitos_secao.append(folgas_leitos_vidro)
        folgas_leitos_sacada.append(folgas_leitos_secao)
    return folgas_leitos_sacada

def converter_ordem_para_secoes(vidros, lista):
    lista_nova = []
    cont = 0
    for secao in vidros:
        lista_secao = []
        for vidro in secao:
            lista_secao.append(lista[cont])
            cont += 1
        lista_nova.append(lista_secao)
    return lista_nova

def def_eq_reta_leitos(ponto_a, ponto_b):
    '''
    define a equação da reta a ser usada para verificar se a seção intercepta a linha perpendicular
    '''
    x1 = ponto_a[0]
    y1 = ponto_a[1]
    x2 = ponto_b[0]
    y2 = ponto_b[1]

    if x2 == x1:
        return Eq(x, x1)
    else:
        valor_m = (ponto_b[1] - ponto_a[1]) / (ponto_b[0] - ponto_a[0])
        y_f = ponto_b[1]
        x_f = ponto_b[0]
        eq_b = Eq(y_f, valor_m*x_f + b)
        valor_b = solve(eq_b, b)[0]

        return Eq(y, valor_m*x + valor_b)

def desenhar_leitos(handles_guias, vidros, angs, giratorios, adjacentes, sentidos):
    handles_leitos = {'externos': [], 'internos': [], 'lat_esq': [], 'lat_dir': []}
    handles_guias = converter_ordem_para_secoes(vidros, handles_guias)
    
    pos_vidro = 1
    pos_sentido = 0

    for index, secao in enumerate(handles_guias):
        for i, linha_guia in enumerate(secao):
            #Offsets
            ext = linha_guia.Offset(14)[0]
            handles_leitos['externos'].append(acad.HandleToObject(ext.Handle))
            ext.Layer = 'Leito Externo'

            int = linha_guia.Offset(-14)[0]
            handles_leitos['internos'].append(acad.HandleToObject(int.Handle))
            int.Layer = 'Leito Interno'
            
            #Guias
            guia_int = linha_guia.Offset(4)[0]
            guia_ext = linha_guia.Offset(-4)[0]
            coord_guia_interna_x = guia_int.EndPoint
            coord_guia_interna_y = guia_int.EndPoint
            coord_guia_externa_x = guia_ext.StartPoint
            coord_guia_externa_y = guia_ext.EndPoint

            #Laterais
            ext_ini = ext.StartPoint
            ext_fim = ext.EndPoint
            int_ini = int.StartPoint
            int_fim = int.EndPoint

            lat_esq = acad2.model.AddLine(APoint(ext_ini[0], ext_ini[1]), APoint(int_ini[0], int_ini[1]))
            lat_esq.Layer = 'Leito Interno'
            handles_leitos['lat_esq'].append(acad.HandleToObject(lat_esq.Handle))
            coord_lat_esq_x = lat_esq.StartPoint
            coord_lat_esq_y = lat_esq.EndPoint

            lat_dir = acad2.model.AddLine(APoint(ext_fim[0], ext_fim[1]), APoint(int_fim[0], int_fim[1]))
            lat_dir.Layer = 'Leito Interno'
            handles_leitos['lat_dir'].append(acad.HandleToObject(lat_dir.Handle))
            coord_lat_dir_x = lat_dir.StartPoint
            coord_lat_dir_y = lat_dir.EndPoint

            #Intersecoes para rotacao
            interseccao_esq_inf = solve((def_eq_reta_leitos(coord_guia_interna_x, coord_guia_interna_y), def_eq_reta_leitos(coord_lat_esq_x, coord_lat_esq_y)), (x, y))
            interseccao_dir_inf  = solve((def_eq_reta_leitos(coord_guia_interna_x, coord_guia_interna_y), def_eq_reta_leitos(coord_lat_dir_x, coord_lat_dir_y)), (x, y))
            interseccao_esq_sup  = solve((def_eq_reta_leitos(coord_guia_externa_x, coord_guia_externa_y), def_eq_reta_leitos(coord_lat_esq_x, coord_lat_esq_y)), (x, y))
            interseccao_dir_sup = solve((def_eq_reta_leitos(coord_guia_externa_x, coord_guia_externa_y), def_eq_reta_leitos(coord_lat_dir_x, coord_lat_dir_y)), (x, y))
            
            # rotacoes lado esquerdo
            if index != 0:
                if not (70 < abs(angs[index-1]) < 110):
                    if i == 0 and angs[index-1] > 0:
                        lat_esq.Rotate(APoint(float(interseccao_esq_inf[x]), float(interseccao_esq_inf[y])), radians((angs[index-1])/2))
                    elif i == 0 and angs[index-1] < 0:
                        lat_esq.Rotate(APoint(float(interseccao_esq_sup[x]), float(interseccao_esq_sup[y])), radians((angs[index-1])/2))
            
            # rotacoes lado direito
            if index != len(handles_guias)-1:
                if i == len(secao) and angs[index] > 0:
                    lat_dir.Rotate(APoint(float(interseccao_dir_inf[x]), float(interseccao_dir_inf[y])), radians((angs[index])/2))            
                elif i == len(secao) and angs[index] > 0:
                    lat_dir.Rotate(APoint(float(interseccao_dir_sup[x]), float(interseccao_dir_sup[y])), radians((angs[index])/2))
            
            # rotacoes giratorios
            if pos_vidro in giratorios:
                if sentidos[pos_sentido] == 'direita':
                    lat_esq.Rotate(APoint(float(interseccao_esq_inf[x]), float(interseccao_esq_inf[y])), radians(5))
                else:
                    lat_dir.Rotate(APoint(float(interseccao_dir_inf[x]), float(interseccao_dir_inf[y])), radians(5))
                if pos_vidro-1 in adjacentes:
                    pos_sentido += 1

            # rotacoes vidros adjacentes aos giratorios
            if pos_vidro in adjacentes:
                if sentidos[pos_sentido] == 'direita':
                    handles_leitos['lat_dir'][-1].Rotate(APoint(float(interseccao_esq_sup[x]), float(interseccao_esq_sup[y])), radians(5))
                elif sentidos[pos_sentido-1] == 'esquerda':
                    handles_leitos['lat_esq'][-1].Rotate(APoint(float(interseccao_dir_sup[x]), float(interseccao_dir_sup[y])), radians(5))
                if pos_vidro-1 in giratorios:
                    pos_sentido += 1
            pos_vidro += 1

    return handles_leitos

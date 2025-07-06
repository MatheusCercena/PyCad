"""
Desenha os leitos, através de offsets chamados via COM e fillets por lisp.
"""
from pyautocad import Autocad, APoint
from src.autocad_conn import get_acad
from math import sqrt, tan, radians

acad2 = Autocad(create_if_not_exists=True)
acad, acad_ModelSpace = get_acad()

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
            handles_guias_leitos.append(guia.Handle)
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
                            print(f'Lado {0} Index {index} folga {folga_esq}')
                            print('entrei no 1 - 1')
                        elif folgas_vidros[secao][0] == -7:
                            folga_esq = calcular_gaps_leito(angs_in[secao-1]) - 7
                            print(f'Lado {0} Index {index} folga {folga_esq}')
                            print('entrei no 1 - 2')
                        elif folgas_vidros[secao][0] == -1:
                            print(abs(angs_in[secao-1])/2)
                            if abs(angs_in[secao-1])/2 < 20:
                                folga_esq = 1.5
                            else: 
                                folga_esq = 0
                            print(f'Lado {0} Index {index} folga {folga_esq}')
                            print('entrei no 1 - 3')
                        else:
                            folga_esq = 1.5
                            print(f'Lado {0} Index {index} folga {folga_esq}')
                            print('entrei no 1 - 4')
                    else:
                        folga_esq = 1.5
                        print(f'Lado {0} Index {index} folga {folga_esq}')
                        print('entrei no 1 - 5')
                    folgas_leitos_vidro.append(folga_esq)
                    print(f'Folga leitos vidro s{secao} {folgas_leitos_vidro}')
                if lado == 1:
                    if index+1 == len(vidros[secao]):                            
                        if folgas_vidros[secao][1] == 2:
                            folga_dir = calcular_gaps_leito(angs_in[secao]) + 3
                            print(f'Lado {1} Index {index} folga {folga_dir}')
                            print('entrei no 2 - 1')
                        elif folgas_vidros[secao][1] == -7:
                            folga_dir = calcular_gaps_leito(angs_in[secao]) - 7
                            print(f'Lado {1} Index {index} folga {folga_dir}')
                            print('entrei no 2 - 2')
                        elif folgas_vidros[secao][1] == -1:
                            print(abs(angs_in[secao-1])/2)
                            if abs(angs_in[secao-1])/2 < 20:
                                folga_dir = 1.5
                            else: 
                                folga_dir = 0
                            print(f'Lado {1} Index {index} folga {folga_dir}')
                            print('entrei no 2 - 3')
                        else:
                            folga_dir = 1.5
                            print(f'Lado {1} Index {index} folga {folga_dir}')
                            print('entrei no 2 - 4')
                    else:
                        folga_dir = 1.5
                        print(f'Lado {1} Index {index} folga {folga_dir}')
                        print('entrei no 2 - 5')

                    folgas_leitos_vidro.append(folga_dir)
                    print(f'Folga leitos vidro s{secao} {folgas_leitos_vidro}')
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

# def definir_graus_leitos(folgas_leitos, giratorios, angs, sentido):
    

#     cont = 0
#     for secao in folgas_leitos:
#         for leito in secao:
#             for i in range(2):
#                 if i == 0 and folgas_leitos[secao][leito][i] == 1.5:

#                 if leito in giratório_esq

#                 if leito in giratório_esq
                
#                 if leito in pseudo_giratório_dir
                
#                 if leito in pseudo_giratórios_dir
#         cont += 1

def desenhar_leitos(vidros, angs, giratorios, sentidos):
    handles_leitos = {'externos': [], 'internos': []}
    handles_guias = converter_ordem_para_secoes(vidros, handles_guias)
    
    pos_vidro = 1
    pos_giratorio = 0
    pos_sentido = 0

    for secao in handles_guias:
        for index, linha_guia in enumerate(secao):
            ext = linha_guia.Offset(14)
            handles_leitos['externos'].append(ext[0].Handle)
            ext.Layer = 'Leito Externo'

            int = linha_guia.Offset(-14)
            handles_leitos['internos'].append(int[0].Handle)
            int.Layer = 'Leito Interno'

            ext_ini = ext.StartPoint
            int_ini = int.StartPoint
            lat_esq = acad2.model.AddLine(APoint(ext_ini[0], ext_ini[1]), APoint(int_ini[0], int_ini[1]))
            lat_esq.Layer = 'Leito Interno'

            ext_fim = ext.EndPoint
            int_fim = int.EndPoint
            lat_dir = acad2.model.AddLine(APoint(ext_fim[0], ext_fim[1]), APoint(int_fim[0], int_fim[1]))
            lat_dir.Layer = 'Leito Interno'

            if index == 0 and angs(index) > 0:
                lat_esq.Rotate()
            if index == 0 and angs(index) < 0:
                lat_esq.Rotate()
            if index == len(linha_guia) and angs(index) > 0:
                lat_dir.Rotate()            
            if index == len(linha_guia) and angs(index) > 0:
                lat_dir.Rotate()
            if pos_vidro in giratorios:
                if pos_sentido == 'direta':
                    lat_esq.Rotate()
                else:
                    lat_dir.Rotate()

        pos_sentido += 1
        pos_vidro += 1

    return handles_leitos


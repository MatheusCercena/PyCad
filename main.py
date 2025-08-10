from src.aberturas import associar_aberturas_aos_lados
from src.alturas_niveis import definir_niveis, alturas_por_nivel, diferenca_alturas, folga_altura_vidro
from src.achar_secao_principal import descobrir_secao_principal
from src.cant_ajustes_angulo import necessidade_cant_ajuste, infos_cant_ajuste
from src.comandos_cad import carregar_comandos, remover_guias
from src.calcs_vetor import menor_valor, maior_valor
from src.cotas import cotar_medida_total
from src.drenos import definir_coord_drenos
from src.furos import definir_pontos_furos
from src.leitos import folgas_leitos, desenhar_guias_leitos, desenhar_leitos
from src.limpar import limpar_tudo
from src.linhas_de_centro import definir_linhas_de_centro, redesenhar_linhas_de_centro, definir_coord_lcs
from src.paredes import fazer_parede_esq, fazer_parede_dir, fillet_paredes
from src.perfis_U import offset_perfis_U, fillet_perfis_U, definir_coord_perfis_U, redefinir_coord_perfis_U
# from src.recebimento_da_medicao import pedir_linhas_de_centro, pedir_quant_vidros, pedir_angSecoes, pedir_angParedes, pedir_prumos, definir_juncoes, solicitar_sentido_abertura, pedir_elevador, pedir_alturas, pedir_niveis
from src.sucata import necessidade_de_sucata, definir_diferencas
from src.vidros import offset_vidros, medida_dos_vidros, definir_folgas_vidros, pontos_dos_vidros, desenhar_guias_vidros
# from src.ferragens import *
from src.bocas import definir_bocas
from src.pivos import definir_pivos

if __name__ == "__main__":

    # Informações de entrada
    limpar_tudo()

    # lcs = pedir_linhas_de_centro()
    lcs = [1000, 3000, 2000]
    # lcs = [590, 2505]

    # alturas = pedir_alturas(lcs)
    alturas = [[1570, 1574], [1575, 1578, 1582, 1579], [1577, 1580]]
    # alturas = [[1137, 1138], [1138, 1141]]

    # niveis = pedir_niveis(alturas)
    niveis = [[0, -2], [-4, -9, -12, -12], [-12, -9]]
    # niveis = [[5, 0], [0, -5]]

    # quant_vidros = pedir_quant_vidros(lcs)
    quant_vidros = [2, 6, 4]
    # quant_vidros = [2, 5]

    # sentidos_abert, fixos = solicitar_sentido_abertura(quant_vidros)
    # sentidos_abert = [[1, 12, 1, 2, 'esquerda']]
    sentidos_abert = [[1, 5, 1, 2, 'esquerda'], [6, 12, 12, 11, 'direita']]
    # sentidos_abert = [[1, 2, 2, 1, 'direita'], [3, 7, 3, 4, 'esquerda']]

    giratorios = [sentido[2] for sentido in sentidos_abert]
    adjacentes = [sentido[3] for sentido in sentidos_abert]
    sentidos = [sentido[4] for sentido in sentidos_abert]

    # angs_in = pedir_angSecoes(lcs)
    angs_in = [-90.0, -90.0]
    # angs_in = [-89.6]

    # angs_paredes = pedir_angParedes()
    # print(f'Angulos de paredes: {angs_paredes}')
    angs_paredes = [0.0, 0.0]

    # prumos = pedir_prumos()

    # juncoes = definir_juncoes(lcs, angs_in)
    juncoes = [[0, 2], [1, 1], [2, 0]]
    # juncoes = [[0, 2], [1, 0]]


    # elevador = pedir_elevador()
    elevador = 2600

    espessura_vidro = int(8)
    espessura_ext_perfil_U = int(20)
    carregar_comandos()

    # Linhas de centro
    pos_lcs = definir_linhas_de_centro(lcs, angs_in)
    sec_princ = descobrir_secao_principal(pos_lcs)
    pos_lcs, handles_lcs = redesenhar_linhas_de_centro(lcs, angs_in, sec_princ)
    coord_lcs = definir_coord_lcs(pos_lcs)

    # Início perfis U
    handles_perfis_U = offset_perfis_U(handles_lcs)
    fillet_perfis_U(handles_perfis_U)

    # Paredes
    parede_esq = fazer_parede_esq(pos_lcs[0], handles_perfis_U['externos'][0], handles_perfis_U['internos'][0], angs_paredes[0])
    fillet_paredes(handles_perfis_U['externos'][0], handles_perfis_U['internos'][0], parede_esq)

    parede_dir = fazer_parede_dir(pos_lcs[-1], handles_perfis_U['externos'][-1], handles_perfis_U['internos'][-1], angs_paredes[1])
    fillet_paredes(handles_perfis_U['externos'][-1], handles_perfis_U['internos'][-1], parede_dir)

    # Reajustando perfis U
    coord_perfis_U = definir_coord_perfis_U(handles_perfis_U)
    aberturas_por_lado = associar_aberturas_aos_lados(quant_vidros, sentidos_abert)
    medidas_perfis_U, coord_perfis_U = redefinir_coord_perfis_U(coord_perfis_U, aberturas_por_lado, elevador)

    # Ajustes de angulos de paredes
    gap_lcs_parede_esq, gap_cant_esq, necessidade_cant_esq = necessidade_cant_ajuste(angs_paredes[0], True)
    gap_lcs_parede_dir, gap_cant_dir, necessidade_cant_dir = necessidade_cant_ajuste(angs_paredes[1], False)

    gaps_lcs = [gap_lcs_parede_esq, gap_lcs_parede_dir]
    if necessidade_cant_esq is True:
        info_cant_esq = infos_cant_ajuste(gap_cant_esq)
        print(f'Info cant esq: {info_cant_esq}')
    if necessidade_cant_dir is True:
        info_cant_dir = infos_cant_ajuste(gap_cant_dir)
        print(f'Info cant dir: {info_cant_dir}')

    # Vidros
    folgas_vidros = definir_folgas_vidros(juncoes, gaps_lcs, angs_in, espessura_vidro)
    vidros = medida_dos_vidros(lcs, quant_vidros, folgas_vidros)
    pontos_vidros = pontos_dos_vidros(vidros, folgas_vidros)
    desenhar_guias_vidros(handles_lcs, vidros, pontos_vidros)
    handles_vidros, coord_vidros = offset_vidros(espessura_vidro)
    remover_guias()

    # Leitos
    folga_leitos = folgas_leitos(vidros, folgas_vidros, angs_in, sentidos_abert)
    handles_guias_leitos = desenhar_guias_leitos(handles_lcs, vidros, pontos_vidros, folga_leitos)
    handle_leitos, coord_leitos = desenhar_leitos(handles_guias_leitos, vidros, angs_in, giratorios, adjacentes, sentidos)
    remover_guias()

    # Furos
    coord_furos = definir_pontos_furos(coord_vidros, folgas_vidros, quant_vidros, angs_in, angs_paredes, espessura_vidro)

    # Drenos
    coord_drenos_por_lado, coord_drenos = definir_coord_drenos(coord_perfis_U, medidas_perfis_U, espessura_ext_perfil_U)

    #Cotas
    cotar_medida_total(coord_vidros, 'Vidro', 246)
    cotar_medida_total(coord_leitos, 'Leito', 386)
    cotar_medida_total(coord_lcs, 'Linha de centro', 550)
    cotar_medida_total(coord_perfis_U, 'Perfis U', 680)
    cotar_medida_total(coord_furos, 'Furos', 150)
    cotar_medida_total(coord_drenos, 'Drenos', 150)

    # Alturas
    dif_niveis, nivel_base = definir_niveis(niveis, lcs, quant_vidros, sentidos_abert)
    alturas_finais = alturas_por_nivel(alturas, dif_niveis)
    dif_altura, altura_base = diferenca_alturas(alturas_finais, lcs, quant_vidros, sentidos_abert)
    altura_vao = round(menor_valor(alturas_finais), 0) + altura_base - nivel_base
    maior_altura = maior_valor(alturas)
    menor_altura = menor_valor(alturas)
    print(f'A altura do vão para o calculo do vidro é {altura_vao}')
    print(f'A maior altura do vão é: {maior_altura}')
    print(f'A menor altura do vão é: {menor_altura}')
    dif_superior, dif_inferior = definir_diferencas(dif_niveis, nivel_base, dif_altura, altura_base)
    folga_vidro = folga_altura_vidro(dif_superior, dif_inferior)
    altura_vidro = altura_vao - folga_vidro
    altura_painel = altura_vidro + 33
    altura_pe3 = altura_painel + 98
    print(f'A altura do vidro é: {altura_vidro}')
    print(f'A altura do painel é: {altura_painel}')
    print(f'A medida da cantoneira com escova é: {altura_pe3}')

    # Definir sucata
    sucata_pedacos_inferior, sucata_inteira_inferior = necessidade_de_sucata(dif_niveis, lcs, 'nivel', nivel_base)
    sucata_pedacos_superior, sucata_inteira_superior = necessidade_de_sucata(dif_altura, lcs, 'altura', altura_base)
    sucata_pedacos = sucata_pedacos_inferior + sucata_pedacos_superior
    sucata_inteira = sucata_inteira_inferior + sucata_inteira_superior
    print(f'A quantidade de sucata em pedaços necessária é {sucata_pedacos}, sendo {sucata_pedacos_inferior} para a parte inferior e {sucata_pedacos_superior} para a parte superior.')
    print(f'A quantidade de sucata interira necessária é {sucata_inteira}, sendo {sucata_inteira_superior} para a parte inferior e {sucata_inteira_inferior} para a parte superior.')

    # posicao = APoint(-5.6, 3.6, 0)
    # tampa_leito = formula_tampa_de_leito(juncoes)
    # adicionar_texto(tampa_leito, posicao)
    pivos = definir_pivos(quant_vidros, sentidos_abert, juncoes, medidas_perfis_U, pontos_vidros)
    print(f'Pivos: {pivos}')
    bocas = definir_bocas(sentidos_abert, vidros, pontos_vidros, pivos)
    print(bocas)

    input('A sacada foi desenhada no autocad, aperte qualquer tecla pra fechar essa janela: ')

    # ja esta fazendo o calculo das bocas agora tem que desenhar elas e puxar as medidas
    # corrgir buga para bocas sentido direito
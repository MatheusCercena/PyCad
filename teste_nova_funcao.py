"""
Teste da nova função redefinir_coord_perfis_U com múltiplos pedaços
"""

from math import sqrt, atan2, cos, sin

def normalizar(vetor):
    """Retorna o vetor unitário (normalizado)"""
    norma = sqrt(vetor[0]**2 + vetor[1]**2)
    return (vetor[0]/norma, vetor[1]/norma)

def definir_pontos_na_secao(inicio_secao, vetor_unitario, distancia):
    return (
        inicio_secao[0] + vetor_unitario[0] * distancia,
        inicio_secao[1] + vetor_unitario[1] * distancia
    )

def obter_pontos_para_cota_corrigida(perfil):
    """
    Função auxiliar para calcular os pontos extremos de um perfil U.
    """
    # Usa os pontos internos como base (primeiro e segundo pontos)
    base = perfil[0]  # início interno
    direcao = perfil[1]  # fim interno
    
    # Calcula o vetor base
    dx = direcao[0] - base[0]
    dy = direcao[1] - base[1]
    theta = -atan2(dy, dx)  # rotação para alinhar com eixo X
    
    # Rotaciona todos os pontos para normalizar
    rotacionados = []
    for i, ponto in enumerate(perfil):
        x, y = ponto[:2]
        xt = x - base[0]
        yt = y - base[1]
        xr = xt * cos(theta) - yt * sin(theta)
        yr = xt * sin(theta) + yt * cos(theta)
        rotacionados.append((i, xr, yr))
    
    # Identifica os extremos (menor e maior X)
    extremos = sorted(rotacionados, key=lambda p: p[1])
    ponto_ini_idx, x_ini, y_ini = extremos[0]
    ponto_fim_idx, x_fim, y_fim = extremos[-1]
    
    # Converte de volta para coordenadas originais
    x_rot = x_ini * cos(-theta)
    y_rot = x_ini * sin(-theta)
    ponto_inicio = (x_rot + base[0], y_rot + base[1])
    
    x_rot_fim = x_fim * cos(-theta) - y_fim * sin(-theta)
    y_rot_fim = x_fim * sin(-theta) + y_fim * cos(-theta)
    ponto_fim = (x_rot_fim + base[0], y_rot_fim + base[1])
    
    return ponto_inicio, ponto_fim

def redefinir_coord_perfis_U(coord_perfis_U, aberturas_por_lado, elevador):
    """
    Redefine as coordenadas dos perfis U baseado na medida total e altura do elevador.
    """
    resultado = []
    
    for i, perfil in enumerate(coord_perfis_U):
        # Calcula a medida total do perfil
        p1, p2 = obter_pontos_para_cota_corrigida(perfil)
        medida_total = sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        
        print(f"Perfil {i+1}: medida_total = {medida_total:.1f}mm")
        
        # Se a medida for menor que 1980mm ou menor que o elevador, mantém o perfil inteiro
        if medida_total <= 1980 or medida_total <= elevador:
            print(f"  -> Mantém perfil inteiro")
            resultado.append(perfil)
            continue
        
        print(f"  -> Divide perfil")
        
        # Se chegou aqui, precisa dividir o perfil
        # Determina qual lado tem giratório
        lado_giratorio = aberturas_por_lado[i] if i < len(aberturas_por_lado) else 0
        
        # Calcula quantos pedaços de 1980mm cabem na medida total
        num_pedacos_1980 = int(medida_total // 1980)
        medida_sobra = medida_total - (num_pedacos_1980 * 1980)
        
        # Se a sobra é maior que o elevador, adiciona mais um pedaço de 1980mm
        if medida_sobra > elevador:
            num_pedacos_1980 += 1
            medida_sobra = medida_total - (num_pedacos_1980 * 1980)
        
        print(f"    Pedaços de 1980mm: {num_pedacos_1980}")
        print(f"    Medida sobra: {medida_sobra:.1f}mm")
        
        # Obtém os pontos extremos do perfil
        p1, p2 = obter_pontos_para_cota_corrigida(perfil)
        
        # Calcula o vetor direção do perfil
        vetor_direcao = (p2[0] - p1[0], p2[1] - p1[1])
        vetor_unitario = normalizar(vetor_direcao)
        
        # Define a ordem dos pedaços baseado no lado do giratório
        if lado_giratorio == 'direita':
            # Pedaços de 1980mm ficam na esquerda, sobra fica na direita
            pedacos_1980_esquerda = num_pedacos_1980
            pedacos_1980_direita = 0
        else:
            # Pedaços de 1980mm ficam na direita, sobra fica na esquerda
            pedacos_1980_esquerda = 0
            pedacos_1980_direita = num_pedacos_1980
        
        # Cria os pedaços
        perfil_atual = perfil.copy()
        medida_acumulada = 0
        
        # Cria pedaços de 1980mm na esquerda (se houver)
        for j in range(pedacos_1980_esquerda):
            # Calcula o ponto de divisão para 1980mm
            ponto_divisao_1980 = definir_pontos_na_secao(p1, vetor_unitario, medida_acumulada + 1980)
            
            # Calcula a proporção para os perfis interno e externo
            proporcao = (medida_acumulada + 1980) / medida_total
            
            # Calcula os pontos de divisão nos perfis
            ext_ini = perfil_atual[0]
            ext_fim = perfil_atual[1]
            int_ini = perfil_atual[2]
            int_fim = perfil_atual[3]
            
            vetor_ext = (ext_fim[0] - ext_ini[0], ext_fim[1] - ext_ini[1])
            vetor_int = (int_fim[0] - int_ini[0], int_fim[1] - int_ini[1])
            
            ponto_divisao_ext = (
                ext_ini[0] + vetor_ext[0] * proporcao,
                ext_ini[1] + vetor_ext[1] * proporcao,
                0.0
            )
            
            ponto_divisao_int = (
                int_ini[0] + vetor_int[0] * proporcao,
                int_ini[1] + vetor_int[1] * proporcao,
                0.0
            )
            
            # Cria o pedaço de 1980mm
            pedaco_1980 = [
                ext_ini,
                ponto_divisao_ext,
                int_ini,
                ponto_divisao_int
            ]
            
            resultado.append(pedaco_1980)
            
            # Atualiza o perfil atual para o próximo pedaço
            perfil_atual = [
                ponto_divisao_ext,
                ext_fim,
                ponto_divisao_int,
                int_fim
            ]
            
            medida_acumulada += 1980
            
            # Verifica a medida do pedaço criado
            p1_pedaco, p2_pedaco = obter_pontos_para_cota_corrigida(pedaco_1980)
            medida_pedaco = sqrt((p2_pedaco[0] - p1_pedaco[0])**2 + (p2_pedaco[1] - p1_pedaco[1])**2)
            print(f"      Pedaço {j+1} (esquerda): {medida_pedaco:.1f}mm")
        
        # Cria pedaços de 1980mm na direita (se houver)
        for j in range(pedacos_1980_direita):
            # Calcula o ponto de divisão para 1980mm
            ponto_divisao_1980 = definir_pontos_na_secao(p1, vetor_unitario, medida_acumulada + 1980)
            
            # Calcula a proporção para os perfis interno e externo
            proporcao = (medida_acumulada + 1980) / medida_total
            
            # Calcula os pontos de divisão nos perfis
            ext_ini = perfil_atual[0]
            ext_fim = perfil_atual[1]
            int_ini = perfil_atual[2]
            int_fim = perfil_atual[3]
            
            vetor_ext = (ext_fim[0] - ext_ini[0], ext_fim[1] - ext_ini[1])
            vetor_int = (int_fim[0] - int_ini[0], int_fim[1] - int_ini[1])
            
            ponto_divisao_ext = (
                ext_ini[0] + vetor_ext[0] * proporcao,
                ext_ini[1] + vetor_ext[1] * proporcao,
                0.0
            )
            
            ponto_divisao_int = (
                int_ini[0] + vetor_int[0] * proporcao,
                int_ini[1] + vetor_int[1] * proporcao,
                0.0
            )
            
            # Cria o pedaço de 1980mm
            pedaco_1980 = [
                ext_ini,
                ponto_divisao_ext,
                int_ini,
                ponto_divisao_int
            ]
            
            resultado.append(pedaco_1980)
            
            # Atualiza o perfil atual para o próximo pedaço
            perfil_atual = [
                ponto_divisao_ext,
                ext_fim,
                ponto_divisao_int,
                int_fim
            ]
            
            medida_acumulada += 1980
            
            # Verifica a medida do pedaço criado
            p1_pedaco, p2_pedaco = obter_pontos_para_cota_corrigida(pedaco_1980)
            medida_pedaco = sqrt((p2_pedaco[0] - p1_pedaco[0])**2 + (p2_pedaco[1] - p1_pedaco[1])**2)
            print(f"      Pedaço {j+1} (direita): {medida_pedaco:.1f}mm")
        
        # Adiciona o pedaço final (sobra)
        if medida_sobra > 0:
            resultado.append(perfil_atual)
            p1_sobra, p2_sobra = obter_pontos_para_cota_corrigida(perfil_atual)
            medida_sobra_calc = sqrt((p2_sobra[0] - p1_sobra[0])**2 + (p2_sobra[1] - p1_sobra[1])**2)
            print(f"      Pedaço sobra: {medida_sobra_calc:.1f}mm")
    
    return resultado

def testar_funcao():
    # Dados de teste
    coord_perfis_U = [
        # Perfil 1: 10000mm (muito maior que 1980 e elevador)
        [
            (0.0, 0.0, 0.0),      # ext_ini
            (10000.0, 0.0, 0.0),  # ext_fim
            (0.0, 20.0, 0.0),     # int_ini
            (10000.0, 20.0, 0.0)  # int_fim
        ],
        # Perfil 2: 2500mm (maior que 1980 e elevador)
        [
            (0.0, 100.0, 0.0),    # ext_ini
            (2500.0, 100.0, 0.0), # ext_fim
            (0.0, 120.0, 0.0),    # int_ini
            (2500.0, 120.0, 0.0)  # int_fim
        ],
        # Perfil 3: 1500mm (menor que 1980)
        [
            (0.0, 200.0, 0.0),    # ext_ini
            (1500.0, 200.0, 0.0), # ext_fim
            (0.0, 220.0, 0.0),    # int_ini
            (1500.0, 220.0, 0.0)  # int_fim
        ]
    ]
    
    aberturas_por_lado = ['direita', 'esquerda', 0]  # Primeiro lado tem giratório para direita, segundo para esquerda
    elevador = 2200  # Elevador de 2200mm
    
    print("Testando nova função redefinir_coord_perfis_U...")
    print(f"Coordenadas originais: {len(coord_perfis_U)} perfis")
    print(f"Aberturas por lado: {aberturas_por_lado}")
    print(f"Elevador: {elevador}mm")
    print()
    
    # Testa a função
    resultado = redefinir_coord_perfis_U(coord_perfis_U, aberturas_por_lado, elevador)
    
    print(f"\nResultado final: {len(resultado)} perfis")
    
    # Verifica se todos os pedaços estão corretos
    for i, perfil in enumerate(resultado):
        p1, p2 = obter_pontos_para_cota_corrigida(perfil)
        medida = sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        print(f"Perfil final {i+1}: {medida:.1f}mm")

if __name__ == "__main__":
    testar_funcao() 
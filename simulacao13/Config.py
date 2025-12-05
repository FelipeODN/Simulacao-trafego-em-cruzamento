import pygame

# Inicialização do Pygame
pygame.init()

# Configurações de cores
ASFALTO = (15, 15, 15)
VERDE_ESCURO = (0, 35 , 0)
# Dimensões da tela e ruas
G = 7
C, L = 1500, 800
C_RUA, L_RUA = C, L/2.8
PX_RUA, PY_RUA = 0, (L - L_RUA)/2
PY_RUA2 = (L+L_RUA)/2
C_CARRO, L_CARRO = 90, 45
# Configurações das vias
VIA1 = (C + 1, (PY_RUA + L_RUA/4) - 2 * G)
VIA2 = (-C_CARRO, PY_RUA + 3 * L_RUA/4)
VIA3 = ((C - L_RUA)/2 + L_RUA/4 - 2 * G, -C_CARRO)
VIA4 = ((C - L_RUA)/2 + 3 * L_RUA/4 - G, L + 1)
VIAS = (VIA1, VIA2, VIA3, VIA4)
# POSIÇÃO LEGENDAS
PX_LEG1, PY_LEG1 = 20, 20
PX_LEG2, PY_LEG2 = (C-130) , L-120
# Configurações das faixas
FAIXA_BRANCA1 = ((C + L_RUA)/2 + G, PY_RUA + 2)
FAIXA_BRANCA2 = ((C - L_RUA)/2 - G, L/2 + 3 * G)
FAIXA_BRANCA3 = ((C - L_RUA)/2, PY_RUA - G)
FAIXA_BRANCA4 = (C/2 + 20, (L + L_RUA)/2)
# DISTÂNCIAS PARA SEMÁFOROS
DISTANCIA_SEMAFORO1 = FAIXA_BRANCA1[0] + 100
DISTANCIA_SEMAFORO2 = FAIXA_BRANCA2[0] - 100
DISTANCIA_SEMAFORO3 = FAIXA_BRANCA3[1] - 80
DISTANCIA_SEMAFORO4 = FAIXA_BRANCA4[1] + 80
# DISTÂNCIAS ENTRE CARROS
DISTANCIA_SEGURA = 80
DS_MIN = DISTANCIA_MINIMA_SPAWN = 120  # Para vias horizontais
DS_MIN_Y = DISTANCIA_MINIMA_SPAWN_VERTICAL = 40  # Para vias verticais
# CONFIGURAÇÕES DE ACELERAÇÃO E FRENAGEM
ACELERACAO_LENTA = 0.02
ACELERACAO_MEDIA = 0.04
ACELERACAO_RAPIDA = 0.065
FRENAGEM_LENTA = 0.2
FRENAGEM_MEDIA = 0.5
FRENAGEM_RAPIDA = 1.0
FRENAGEM_VERTICAL_LENTA = 0.4
FRENAGEM_VERTICAL_MEDIA = 0.8
FRENAGEM_VERTICAL_RAPIDA = 1.5
# LIMITES DE VELOCIDADE PARA MUDANÇA DE ACELERAÇÃO
LIMITE_VELOCIDADE_BAIXA = 20  # Km/h
LIMITE_VELOCIDADE_MEDIA = 40  # Km/h
# TEMPOS PARA BUZINA
TEMPO_PARADO_PARA_BUZINAR = 2.0  # segundos
TEMPO_ENTRE_BUZINAS = 5.0  # segundos
#TEMPOS P/ CRIAR CARROS
TP_1 = 750
TP_2 = 1000
TP_3 = 2500
M1 = MAX_CARROS_VIA1 = 6
M2 = MAX_CARROS_VIA2 = 6
M3 = MAX_CARROS_VIA3 = 4
M4 = MAX_CARROS_VIA4 = 4

# Configurações da tela
TELA = pygame.display.set_mode((C, L), pygame.RESIZABLE)
pygame.display.set_caption("Simulação versão 13 - Cruzamento com Semáforos")
FONTE = pygame.font.Font(None, 36)
FONTE_PEQUENA = pygame.font.Font(None, 24)

# Configurações de velocidade
DADOS_VELOCIDADE = {
    'Probabilidade Acumulada': [0.1, 0.3, 0.6, 0.85, 0.95, 1],
    'Velocidade Min': [3.09, 4.62, 6.17, 7.71, 9.25, 10.80],
    'Velocidade Max': [4.61, 6.16, 7.70, 9.24, 10.79, 16.96]
}

# Cores dos carros
CORES_CARROS = [
    "branco", "policia3", "vermelho", "azul", "verde", "amarelo", 
    "cinza", "marrom", "cinza2", "azul2", "preto", "caramelo", 
    "azul_metalico", "laranja"
]
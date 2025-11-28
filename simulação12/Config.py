import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configurações de cores
ASFALTO = (35, 35, 35)
VERDE_ESCURO = (0, 75, 0)

# Dimensões da tela e ruas
G = 7
C, L = 1500, 800
C_RUA, L_RUA = C, L/2.8
PX_RUA, PY_RUA = 0, (L - L_RUA)/2
C_CARRO, L_CARRO = 90, 45

# Configurações das vias
VIA1 = (C + 1, (PY_RUA + L_RUA/4) - 2 * G)
VIA2 = (-C_CARRO, PY_RUA + 3 * L_RUA/4)
VIA3 = ((C - L_RUA)/2 + L_RUA/4 - 2 * G, -C_CARRO)
VIA4 = ((C - L_RUA)/2 + 3 * L_RUA/4 - G, L + 1)
VIAS = (VIA1, VIA2, VIA3, VIA4)

# Configurações das faixas
FAIXA_BRANCA1 = ((C + L_RUA)/2 + G, PY_RUA + 2)
FAIXA_BRANCA2 = ((C - L_RUA)/2 - G, L/2 + 3 * G)
FAIXA_BRANCA3 = ((C - L_RUA)/2, PY_RUA - G)
FAIXA_BRANCA4 = (C/2 + 20, (L + L_RUA)/2)

# Configurações da tela
TELA = pygame.display.set_mode((C, L), pygame.RESIZABLE)
pygame.display.set_caption("Simulação versão 12 - Modularizada")
FONTE = pygame.font.Font(None, 36)

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
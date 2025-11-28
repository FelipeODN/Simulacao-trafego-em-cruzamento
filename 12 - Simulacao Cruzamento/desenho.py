import pygame
from Config import *

def desenhar_rua(tela):
    # Rua horizontal
    pygame.draw.rect(tela, ASFALTO, (PX_RUA, PY_RUA, C_RUA, L_RUA))
    
    # Faixas horizontais
    pygame.draw.rect(tela, 'yellow', (PX_RUA, L/2 - G, (C - L_RUA)/2, G))
    pygame.draw.rect(tela, 'yellow', ((C + L_RUA)/2, L/2 - G, (C - L_RUA)/2 + 1, G))
    pygame.draw.rect(tela, 'yellow', (PX_RUA, L/2 + G, (C - L_RUA)/2, G))
    pygame.draw.rect(tela, 'yellow', ((C + L_RUA)/2, L/2 + G, (C - L_RUA)/2 + 1, G))
    
    # Rua vertical
    pygame.draw.rect(tela, ASFALTO, ((C - L_RUA)/2, 0, L_RUA, L))
    
    # Faixas verticais
    pygame.draw.rect(tela, 'yellow', ((C - L_RUA)/2 + L_RUA/2 - G, 0, G, (L - L_RUA)/2))
    pygame.draw.rect(tela, 'yellow', ((C - L_RUA)/2 + L_RUA/2 + G, 0, G, (L - L_RUA)/2))
    pygame.draw.rect(tela, 'yellow', ((C - L_RUA)/2 + L_RUA/2 - G, (L + L_RUA)/2, G, (L - L_RUA)/2))
    pygame.draw.rect(tela, 'yellow', ((C - L_RUA)/2 + L_RUA/2 + G, (L + L_RUA)/2, G, (L - L_RUA)/2))
    
    # Faixas brancas redutoras
    pygame.draw.rect(tela, 'white', ((C + L_RUA)/2, PY_RUA + 2, G, L_RUA/2 - 2 * G))
    pygame.draw.rect(tela, 'white', ((C - L_RUA)/2 - G, L/2 + 3 * G, G, L_RUA/2 - 2 * G - 10))
    pygame.draw.rect(tela, 'white', ((C - L_RUA)/2 + 2, PY_RUA - G, L_RUA/2 - 2 * G, G))
    pygame.draw.rect(tela, 'white', (C/2 + 3 * G, (L + L_RUA)/2, L_RUA/2 - 3 * G - 3, G))

def desenhar_legendas(tela, fonte, tempo_decorrido, contador_colisoes, tempo_semaforo1, tempo_semaforo2):
    # Legenda tempo
    tempo_texto = f"Tempo: {tempo_decorrido:.2f} s"
    texto_renderizado = fonte.render(tempo_texto, True, 'white')
    
    # Legenda contador colisões
    texto_contador = f"Colisões: {contador_colisoes}"
    texto_colisao = fonte.render(texto_contador, True, 'white')
    
    # Legenda semáforos
    tp1 = f"{tempo_semaforo1:.1f}s"
    texto_tempo_semaforo1 = fonte.render(tp1, True, 'white')
    tp2 = f"{tempo_semaforo2:.1f}s"
    texto_tempo_semaforo2 = fonte.render(tp2, True, 'white')
    
    # Instruções
    mudar_semaforo1 = "esquerdo mouse troca o sinal -->"
    texto_mudar_semaforo1 = fonte.render(mudar_semaforo1, True, 'black')
    mudar_semaforo2 = "<-- direito do mouse troca o sinal"
    texto_mudar_semaforo2 = fonte.render(mudar_semaforo2, True, 'black')
    
    # Comandos limpar
    limpar_via1 = "aperte '1' para limpar via 1"
    texto_limpar1 = fonte.render(limpar_via1, True, 'red')
    limpar_via2 = "aperte '2' para limpar via 2"
    texto_limpar2 = fonte.render(limpar_via2, True, 'lightblue')
    limpar_via3 = "aperte '3' para limpar via 3"
    texto_limpar3 = fonte.render(limpar_via3, True, 'green')
    limpar_via4 = "aperte '4' para limpar via 4"
    texto_limpar4 = fonte.render(limpar_via4, True, 'yellow')
    limpar_tudo = "aperte 'c' para limpar tudo"
    texto_limpar_tudo = fonte.render(limpar_tudo, True, 'purple')
    
    # Desenhar todas as legendas
    tela.blit(texto_renderizado, (20, 20))
    tela.blit(texto_colisao, (820, 20))
    tela.blit(texto_mudar_semaforo1, ((C - L_RUA - 900)/2, PY_RUA + L_RUA + 50))
    tela.blit(texto_mudar_semaforo2, ((C + L_RUA + 120)/2, PY_RUA - 80))
    tela.blit(texto_limpar1, (820, 600))
    tela.blit(texto_limpar2, (820, 630))
    tela.blit(texto_limpar3, (820, 660))
    tela.blit(texto_limpar4, (820, 690))
    tela.blit(texto_limpar_tudo, (820, 720))
    tela.blit(texto_tempo_semaforo1, ((C - L_RUA)/2 - 48, PY_RUA + L_RUA + 140))
    tela.blit(texto_tempo_semaforo2, ((C + L_RUA)/2 + 5, 100))
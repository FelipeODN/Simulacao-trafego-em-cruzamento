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
    pygame.draw.rect(tela, 'white', (FAIXA_BRANCA1[0],FAIXA_BRANCA1[1], G, L_RUA/2 - 2 * G))
    pygame.draw.rect(tela, 'white', (FAIXA_BRANCA2[0],FAIXA_BRANCA2[1], G, L_RUA/2 - 2 * G - 10))
    pygame.draw.rect(tela, 'white', (FAIXA_BRANCA3[0],FAIXA_BRANCA3[1], L_RUA/2 - 2 * G, G))
    pygame.draw.rect(tela, 'white', (FAIXA_BRANCA4[0],FAIXA_BRANCA4[1], L_RUA/2 - 3 * G - 3, G))
    
def desenhar_legendas(tela, fonte, fonte2, tempo_decorrido, contador_colisoes, tempo_semaforo1, tempo_semaforo2, estado_semaforo1,estado_semaforo2, 
                      total_carros,total_carros_via1,total_carros_via2,total_carros_via3,total_carros_via4):
    CORES_SEMAFORO = {'vermelho': 'red','amarelo': 'yellow','verde': 'green'}
    
    # Usa a cor correspondente ao estado
    cor_semaforo1 = CORES_SEMAFORO.get(estado_semaforo1, 'white')
    cor_semaforo2 = CORES_SEMAFORO.get(estado_semaforo2, 'white')

    caixa = pygame.Surface((160, 155), pygame.SRCALPHA)
    caixa.fill((*ASFALTO, 255))  # RGB + alpha (0-255, menor = mais transparente)
    tela.blit(caixa, (10, 55))

    # Contador total de carros
    texto_total1 = f"Carros via1  =   {total_carros_via1}"
    texto_total1 = fonte2.render(texto_total1, True, (220, 0, 0))
    texto_total2 = f"Carros via2  =   {total_carros_via2}"
    texto_total2 = fonte2.render(texto_total2, True, 'light blue')
    texto_total3 = f"Carros via3  =   {total_carros_via3}"
    texto_total3 = fonte2.render(texto_total3, True, 'green')
    texto_total4 = f"Carros via4  =   {total_carros_via4}"
    texto_total4 = fonte2.render(texto_total4, True, 'yellow')
    texto_total = f"Total Carros =  {total_carros}"
    texto_total = fonte2.render(texto_total, True, 'purple')
    # Legenda tempo
    tempo_texto = f"Tempo: {tempo_decorrido:.2f} s"
    texto_renderizado = fonte.render(tempo_texto, True, 'light green', (0,25,25))
    # Legenda contador colisões
    texto_contador = f"Colisões: {contador_colisoes}"
    texto_colisao = fonte.render(texto_contador, True, (50,100,100), (15,30,30))
    # Legenda semáforos
    tp1 = f"{tempo_semaforo1:.1f}s"
    texto_tempo_semaforo1 = fonte.render(tp1, True, cor_semaforo1)
    tp2 = f"{tempo_semaforo2:.1f}s"
    texto_tempo_semaforo2 = fonte.render(tp2, True, cor_semaforo2)
    # Instruções
    mudar_semaforo1 = "esquerdo mouse muda sinal ->"
    texto_mudar_semaforo1 = fonte.render(mudar_semaforo1, True, ( 150,150,150), (25,25,25))
    mudar_semaforo2 = "<- direito mouse muda sinal"
    texto_mudar_semaforo2 = fonte.render(mudar_semaforo2, True, (150, 150, 150), (25,25,25))
    # Mutar
    mutar = "'m' - mutar"
    texto_mutar = fonte2.render(mutar,True,'orange',(50,50,50))
    # Comandos limpar
    limpar_via1 = "'1' - limpar via 1"
    texto_limpar1 = fonte2.render(limpar_via1, True, 'red', (50,0,0))
    limpar_via2 = "'2' - limpar via 2"
    texto_limpar2 = fonte2.render(limpar_via2, True, 'lightblue', (0,0,50))
    limpar_via3 = "'3' - limpar via 3"
    texto_limpar3 = fonte2.render(limpar_via3, True, 'green', (0,2,0))
    limpar_via4 = "'4' - limpar via 4"
    texto_limpar4 = fonte2.render(limpar_via4, True, 'yellow', (50,50,0))
    limpar_tudo = "'c' - limpar tudo"
    texto_limpar_tudo = fonte2.render(limpar_tudo, True, 'purple', (50,0,50))
    
    # Desenhar todas as legendas
    tela.blit(texto_renderizado,     (20, 20))
    tela.blit(texto_colisao,         (PX_LEG2-30, 20))
    tela.blit(texto_mudar_semaforo1, ((C - L_RUA - 840)/2, PY_RUA + L_RUA + 50))
    tela.blit(texto_mudar_semaforo2, ((C + L_RUA + 120)/2, PY_RUA - 80))
    tela.blit(texto_mutar  ,         (PX_LEG2, PY_LEG2))
    tela.blit(texto_limpar1,         (PX_LEG2,  PY_LEG2+20))
    tela.blit(texto_limpar2,         (PX_LEG2, PY_LEG2+40))
    tela.blit(texto_limpar3,         (PX_LEG2, PY_LEG2+60))
    tela.blit(texto_limpar4,         (PX_LEG2, PY_LEG2+80))
    tela.blit(texto_limpar_tudo,     (PX_LEG2, PY_LEG2+100))
    tela.blit(texto_tempo_semaforo1, ((C - L_RUA)/2 - 48, PY_RUA + L_RUA + 140))
    tela.blit(texto_tempo_semaforo2, ((C + L_RUA)/2 + 5, 100))
    tela.blit(texto_total1,          (20, 60))
    tela.blit(texto_total2,          (20, 90))
    tela.blit(texto_total3,          (20, 120))
    tela.blit(texto_total4,          (20, 150))
    tela.blit(texto_total ,          (20, 180))
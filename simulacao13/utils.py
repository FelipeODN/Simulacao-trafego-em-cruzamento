import pygame
from Config import *

def verificar_colisoes(carros, pares_colididos_anteriores):
    """Verifica colisões e retorna apenas as NOVAS colisões"""
    pares_colididos_frame = set()
    novas_colisoes = 0
    
    for i, carro in enumerate(carros):
        rect_carro = pygame.Rect(carro.x, carro.y, carro.c_carro, carro.l_carro)
        for j, outro_carro in enumerate(carros[i+1:], start=i+1):
            rect_outro = pygame.Rect(outro_carro.x, outro_carro.y, outro_carro.c_carro, outro_carro.l_carro)
            
            if rect_carro.colliderect(rect_outro):
                par = frozenset({id(carro), id(outro_carro)})
                pares_colididos_frame.add(par)
                
                # Conta apenas se é uma colisão NOVA (não estava no frame anterior)
                if par not in pares_colididos_anteriores:
                    novas_colisoes += 1
    
    return novas_colisoes, pares_colididos_frame

def limpar_carros_fora_tela(lista_carros):
    return [carro for carro in lista_carros if -C_CARRO <= carro.x <= C and -C_CARRO <= carro.y <= L]

def processar_eventos(carros_via1, carros_via2, carros_via3, carros_via4, gerador,sistema_som):
    a = 0
    rodando = True

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        keys = pygame.key.get_pressed()
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_KP_PLUS:
                carros_via1.append(gerador.criar_carro_aleatorio(VIAS[0]))
                carros_via2.append(gerador.criar_carro_aleatorio(VIAS[1]))
                carros_via3.append(gerador.criar_carro_aleatorio(VIAS[2]))
                carros_via4.append(gerador.criar_carro_aleatorio(VIAS[3]))
                sistema_som.aumentar_volume()
            
            if evento.key == pygame.K_KP_MINUS:
                if carros_via1: carros_via1.pop()
                if carros_via2: carros_via2.pop()
                if carros_via3: carros_via3.pop()
                if carros_via4: carros_via4.pop()
                sistema_som.diminuir_volume()

            if evento.key == pygame.K_m:
                sistema_som.alternar_mute() # Alterna estado de mudo
                
        if keys[pygame.K_1] or keys[pygame.K_c]:
            carros_via1.clear()
        if keys[pygame.K_1] or keys[pygame.K_c]:
            carros_via1.clear()
        if keys[pygame.K_2] or keys[pygame.K_c]:
            carros_via2.clear()
        if keys[pygame.K_3] or keys[pygame.K_c]:
            carros_via3.clear()
        if keys[pygame.K_4] or keys[pygame.K_c]:
            carros_via4.clear()
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: a = 1
            if evento.button == 3: a = 3
            if evento.button == 2: a = 2
        
        if evento.type == pygame.MOUSEWHEEL:
            for carro in carros_via1 + carros_via2 + carros_via3 + carros_via4:
                if evento.y > 0:  # Scroll para cima
                    carro.velocidade_x *= 1.2
                    carro.velocidade_y *= 1.2
                elif evento.y < 0:  # Scroll para baixo
                    carro.velocidade_x *= 0.8
                    carro.velocidade_y *= 0.8
    
    return rodando, a
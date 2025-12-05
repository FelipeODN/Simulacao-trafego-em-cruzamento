import pygame
import random
from Config import *
from SistemaSom import SistemaSom

class Carro:
    def __init__(self, cor, x, y, c_carro, l_carro, velocidade_x, velocidade_y, rotacao, virar):
        self.cor = cor
        self.cores = pygame.transform.scale(pygame.transform.rotate(cor, rotacao), (c_carro, l_carro))
        self.x, self.y = float(x), float(y)
        self.c_carro, self.l_carro = c_carro, l_carro
        self.velocidade_x, self.velocidade_y, self.virar = velocidade_x/2, velocidade_y/2, virar
        self.ultimo_tempo = pygame.time.get_ticks()
        self.tempo_parado = 0
        self.buzinou = False
        self.ultima_buzina = 0
        self.sistema_som = None 

    def desenhar(self, tela):
        tela.blit(self.cores, (int(self.x), int(self.y)))
    
    def set_sistema_som(self, sistema_som):
        """Configura o sistema de som para este carro"""
        self.sistema_som = sistema_som
    
    def mostrar_velocidade(self, tela, fonte,carros_via1, carros_via2):
        centro_x = self.x + self.c_carro/2
        centro_y = self.y + self.l_carro/2
        velocidade_kmh = abs(self.velocidade_x + self.velocidade_y)*6.48 # /((1000/30)/60)*(3.6)) = /(1000/1800)*3.6 = *18/10 * 3.6 = 1.8*3.6 = 6.48
        velocidade_texto = f"{velocidade_kmh:.2f}Km/h"
        
        # Obter a cor predominante da imagem do carro
        cor_carro = self._obter_cor_predominante()
        texto = fonte.render(velocidade_texto, True, cor_carro)
        
        if self in carros_via1 or self in carros_via2: 
            # se colocar assim: self in [carros_via1, carros_via2]:
            # O que o Python entende:
            # "self está na lista que contém carros_via1 e carros_via2?"
            # Isso verifica se self É IGUAL A carros_via1 OU carros_via2
            # Mas self é um Carro, e carros_via1 é uma lista!
            # Isso verifica: carro1 == carros_via1? ou carro1 == carros_via2?
            # Um Carro nunca será igual a uma lista!
            tela.blit(texto, (centro_x - 35, centro_y - 50))
        else:tela.blit(texto, (centro_x - 30, centro_y - 70))
    
    def _obter_cor_predominante(self):
        """Obtém a cor predominante da imagem do carro"""
        try:
            # Redimensiona a imagem para uma amostra menor para melhor performance
            amostra = pygame.transform.scale(self.cores, (10, 10))
            pixels = pygame.surfarray.array3d(amostra)
            
            # Calcula a cor média
            r = int(pixels[:,:,0].mean())
            g = int(pixels[:,:,1].mean())
            b = int(pixels[:,:,2].mean())
            
            return (r, g, b)
        except:
            # Fallback para branco se houver erro
            return (255, 255, 255)
 
    def movimento(self, carros_via1, carros_via2, carros_via3, carros_via4, estado1,estado2):
        
        DISTANCIA_SEMAFORO1 = FAIXA_BRANCA1[0] + 100
        DISTANCIA_SEMAFORO2 = FAIXA_BRANCA2[0] - 100
        DISTANCIA_SEMAFORO3 = FAIXA_BRANCA3[1] - 80
        DISTANCIA_SEMAFORO4 = FAIXA_BRANCA4[1] + 80
        DISTANCIA_SEGURA = 80
        parar = False
        vel_x = abs(self.velocidade_x*6.48) # mesmo parâmetro de vel que o q é mostrado
        vel_y = abs(self.velocidade_y*6.48)
        P = random.uniform(1,1.2)
        ACELERAR = (   P*0.065 if 0 <= vel_x <= 20
                    else P*0.04  if 20 < vel_x <= 40
                    else P*0.02                           ) if self in [carros_via1,carros_via2] else (

                        P*0.04  if 0 <= vel_y <= 20
                    else P*0.02                           )

        FREAR = ( P*0.35 if 0 <= vel_x <= 20                # FREAR deve necesseriamente ser mais forte que ACELERAR
                else P*0.5 if 20 < vel_x  <= 40
                else P*0.6                               ) if self in [carros_via1,carros_via2] else (

                    P*0.35 if 0 <= vel_y <= 20
                else P*0.5 if 20 < vel_y < 40
                else P*0.6                               )
        
        #VIA 1 - ESQUERDA PARA DIREITA
        if self in carros_via1:
            if estado1 in ['vermelho','amarelo']:
                if FAIXA_BRANCA1[0] <= self.x < DISTANCIA_SEMAFORO1: # o primeiro a chegar perto da faixa para no vermelho
                    parar = True
            for carro in carros_via1:
                if self != carro:
                    dx = abs(self.x - carro.x - C_CARRO)
                    if self.x > carro.x and dx <= DISTANCIA_SEGURA : # O carro de trás para quando perto do carro da frente
                        parar = True
            
        #VIA 2 - DIREITA PARA ESQUERDA
        if self in carros_via2:
            if estado1 in ['vermelho','amarelo']:
                if DISTANCIA_SEMAFORO2 < self.x+C_CARRO <= FAIXA_BRANCA2[0] : 
                    parar = True
            for carro in carros_via2:
                if self != carro:
                    dx = abs(self.x + C_CARRO - carro.x )
                    if self.x < carro.x and dx <= DISTANCIA_SEGURA :
                        parar = True

        #VIA 3 - CIMA PARA BAIXO
        if self in carros_via3:
            if estado2 in ['vermelho','amarelo']:
                if DISTANCIA_SEMAFORO3 < self.y + C_CARRO <= FAIXA_BRANCA3[1] :
                    parar = True
            for carro in carros_via3:
                if self != carro:        
                    dy = abs(self.y + C_CARRO - carro.y )
                    if self.y < carro.y and dy <= DISTANCIA_SEGURA :
                        parar = True
            
        #VIA 4 - BAIXO PARA CIMA
        if self in carros_via4:
            if estado2 in ['vermelho','amarelo']:
                if FAIXA_BRANCA4[1] <= self.y < DISTANCIA_SEMAFORO4 :
                    parar = True
            for carro in carros_via4:
                if self != carro:
                    dy = abs(self.y - carro.y - C_CARRO)
                    if self.y > carro.y and dy <= DISTANCIA_SEGURA :
                        parar = True

        # Se não está parado no semáforo, acelera
        if self in carros_via1:
            if parar:
                if self.velocidade_x < 0 : self.velocidade_x += FREAR
                if self.velocidade_x > 0 : self.velocidade_x = 0
            else: self.velocidade_x -= ACELERAR

        if self in carros_via2:
            if parar:
                if self.velocidade_x > 0 : self.velocidade_x -= FREAR
                if self.velocidade_x < 0 : self.velocidade_x = 0
            else: self.velocidade_x += ACELERAR
        
        if self in carros_via3:
            if parar:
                if self.velocidade_y > 0 : self.velocidade_y -= FREAR
                if self.velocidade_y < 0 : self.velocidade_y = 0
            else: self.velocidade_y += ACELERAR

        if self in carros_via4:
            if parar:
                if self.velocidade_y < 0 : self.velocidade_y += FREAR
                if self.velocidade_y > 0 : self.velocidade_y = 0
            else: self.velocidade_y -= ACELERAR

        # MOVIMENTO
        self.x += self.velocidade_x
        self.y += self.velocidade_y

        if self in carros_via1 or self in carros_via2:
            velocidade_abs = vel_x
        else:
            velocidade_abs = vel_y
        
        # Se está parado ou quase parado
        if  velocidade_abs < 0.1 :  # Quase parado
            self.tempo_parado += 1/60  # Assumindo 60 FPS
            
            # Se parado por mais de 2 segundos e não buzinou recentemente
            tempo_atual = pygame.time.get_ticks()
            if (self.tempo_parado > 2.0 and 
                not self.buzinou and 
                tempo_atual - self.ultima_buzina > 5000):  # Só a cada 5 segundos
                
                self.buzinar()
        else:
            self.tempo_parado = 0
            self.buzinou = False
    
    def buzinar(self):
        """Toca a buzina deste carro"""
        if self.sistema_som:
            self.sistema_som.tocar_buzina()
            self.buzinou = True
            self.ultima_buzina = pygame.time.get_ticks()
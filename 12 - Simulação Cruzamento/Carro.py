import pygame
from Config import *

class Carro:
    def __init__(self, cor, x, y, c_carro, l_carro, velocidade_x, velocidade_y, rotacao, virar):
        self.cor = cor
        self.cores = pygame.transform.scale(pygame.transform.rotate(cor, rotacao), (c_carro, l_carro))
        self.x, self.y = float(x), float(y)
        self.c_carro, self.l_carro = c_carro, l_carro
        self.velocidade_x, self.velocidade_y, self.virar = velocidade_x/2, velocidade_y, virar

    def desenhar(self, tela):
        tela.blit(self.cores, (int(self.x), int(self.y)))
    
    def mostrar_velocidade(self, tela, fonte):
        centro_x = self.x + self.c_carro/2
        centro_y = self.y + self.l_carro/2
        velocidade_kmh = abs(self.velocidade_x + self.velocidade_y)/((1000/30)/60)*(3.6)
        velocidade_texto = f"{velocidade_kmh:.2f}Km/h"
        texto = fonte.render(velocidade_texto, True, 'white')
        
        if self.velocidade_x != 0:
            tela.blit(texto, (centro_x - 35, centro_y - 50))
        else:
            tela.blit(texto, (centro_x - 30, centro_y - 70))
    
    def movimento(self, carros_via1, carros_via2, carros_via3, carros_via4, estado1, estado2):
        parado_semaforo = False
        
        # Para carros horizontais (via1 e via2)
        if self.velocidade_x != 0:
            if estado1 == 'vermelho' or estado1 == 'amarelo':
                if self.velocidade_x < 0:  # Via1 (indo para esquerda)
                    if FAIXA_BRANCA1[0] <= self.x < FAIXA_BRANCA1[0] + C_CARRO/2:
                        parado_semaforo = True
                    for carro in carros_via1:
                        if self != carro:
                            dx = abs(self.x - carro.x)
                            if self.x > carro.x and dx < C_CARRO*1.2 and FAIXA_BRANCA1[0] <= self.x < C:
                                parado_semaforo = True
                else:  # Via2 (indo para direita)
                    if FAIXA_BRANCA2[0] - C_CARRO/2 <= self.x + C_CARRO < FAIXA_BRANCA2[0]:
                        parado_semaforo = True
                    for carro in carros_via2:
                        if self != carro:
                            dx = abs(self.x - carro.x)
                            if self.x < carro.x and dx < C_CARRO*1.2 and 0 <= self.x < FAIXA_BRANCA2[0]:
                                parado_semaforo = True
        
        # Para carros verticais (via3 e via4)
        elif estado2 == 'vermelho' or estado2 == 'amarelo':
            if self.velocidade_y > 0:  # Via3 (indo para baixo)
                if FAIXA_BRANCA3[1] - C_CARRO/4 <= self.y + C_CARRO < FAIXA_BRANCA3[1]:
                    parado_semaforo = True
                for carro in carros_via3:
                    if self != carro:
                        dy = abs(self.y - carro.y)
                        if self.y < carro.y and dy < C_CARRO*1.2 and 0 <= self.y + C_CARRO < FAIXA_BRANCA3[1]:
                            parado_semaforo = True
            else:  # Via4 (indo para cima)
                if FAIXA_BRANCA4[1] <= self.y < FAIXA_BRANCA4[1] + C_CARRO/4:
                    parado_semaforo = True
                for carro in carros_via4:
                    if self != carro:
                        dy = abs(self.y - carro.y)
                        if self.y > carro.y and dy < C_CARRO*1.2 and FAIXA_BRANCA4[1] <= self.y < L:
                            parado_semaforo = True
        
        # Se não está parado no semáforo, move normalmente
        if not parado_semaforo:
            self.x += self.velocidade_x
            self.y += self.velocidade_y

        # Lógica de aceleração/desaceleração (mantida do seu código original)
        aceleracao = 0.000001
        desaceleracao = 0.000001

        # Sua lógica complexa de movimento entre carros...
        for outro_carro in carros_via1:
            if outro_carro != self:
                dx = abs(self.x - outro_carro.x)
                if estado1 == 'verde' or self.x < FAIXA_BRANCA1[0]:
                    if dx <= C_CARRO*1.3 and self.x > outro_carro.x:
                        self.velocidade_x += (dx/dx**2)
                    if dx <= C_CARRO*1.3 and self.x < outro_carro.x:
                        self.velocidade_x -= (dx/dx**2)
                    if dx > C_CARRO*2 and self.x > outro_carro.x:
                        self.velocidade_x -= aceleracao
                    if dx > C_CARRO*2 and self.x < outro_carro.x:
                        self.velocidade_x -= aceleracao
                
                if estado1 == 'vermelho':
                    if FAIXA_BRANCA1[0] <= self.x:
                        self.velocidade_x += 0.001

                    if parado_semaforo:
                        if self.velocidade_x > 0:
                            self.velocidade_x = max(0, self.velocidade_x - desaceleracao)
                        elif self.velocidade_x < 0:
                            self.velocidade_x = min(0, self.velocidade_x + desaceleracao)
                        if self.velocidade_y > 0:
                            self.velocidade_y = max(0, self.velocidade_y - desaceleracao)
                        elif self.velocidade_y < 0:
                            self.velocidade_y = min(0, self.velocidade_y + desaceleracao)
        
        if len(carros_via1) == 1 and (self.x <= FAIXA_BRANCA1[0] or estado1 == 'verde'):
            self.velocidade_x -= aceleracao

    def mudar_via(self, carros_via1, carros_via2, carros_via3, carros_via4):
        # Implementação da mudança de via (mantida do seu código)
        from gerador_carros import criar_carro_na_via
        
        # Via1 para outras vias
        if self in carros_via1 and self.virar == 'via4':
            if FAIXA_BRANCA4[0] + 10 <= self.x <= FAIXA_BRANCA4[0] + 50:
                return criar_carro_na_via('via4', self, carros_via1, carros_via4)
        
        if self in carros_via1 and self.virar == 'via3':
            if FAIXA_BRANCA3[0] + 50 <= self.x + self.c_carro <= FAIXA_BRANCA3[0] + 80:
                return criar_carro_na_via('via3', self, carros_via1, carros_via3)
        
        # Via2 para outras vias
        if self in carros_via2 and self.virar == 'via4':
            if FAIXA_BRANCA4[0] + 10 <= self.x <= FAIXA_BRANCA4[0] + 50:
                return criar_carro_na_via('via4', self, carros_via2, carros_via4, velocidade_invertida=True)
        
        if self in carros_via2 and self.virar == 'via3':
            if FAIXA_BRANCA3[0] + 50 <= self.x + self.c_carro <= FAIXA_BRANCA3[0] + 80:
                return criar_carro_na_via('via3', self, carros_via2, carros_via3)
        
        # Via3 para outras vias
        if self in carros_via3 and self.virar == 'via1':
            if FAIXA_BRANCA1[1] + 10 <= self.y + self.c_carro <= FAIXA_BRANCA1[1] + 50:
                return criar_carro_na_via('via1', self, carros_via3, carros_via1)
        
        if self in carros_via3 and self.virar == 'via2':
            if FAIXA_BRANCA2[1] + 50 <= self.y <= FAIXA_BRANCA2[1] + 80:
                return criar_carro_na_via('via2', self, carros_via3, carros_via2)
        
        # Via4 para outras vias
        if self in carros_via4 and self.virar == 'via1':
            if FAIXA_BRANCA1[1] + 10 <= self.y + self.c_carro <= FAIXA_BRANCA1[1] + 50:
                return criar_carro_na_via('via1', self, carros_via4, carros_via1)
        
        if self in carros_via4 and self.virar == 'via2':
            if FAIXA_BRANCA2[1] + 50 <= self.y <= FAIXA_BRANCA2[1] + 80:
                return criar_carro_na_via('via2', self, carros_via4, carros_via2, velocidade_invertida=True)
        
        return None
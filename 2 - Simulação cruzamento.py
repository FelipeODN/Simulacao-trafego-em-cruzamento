import pygame
import random
import tkinter as tk
import numpy as np
import pandas as pd
# Cores:
branco =  255 , 255 , 255 
preto = 0
cinza = 127,127,127
asfalto =  35 , 35 , 35 
vermelho =  255 , 0 , 0
azul =  0 , 0 , 255 
verde =  0 , 255 , 0
roxo =  60 , 000 , 60 
amarelo =  255 , 255 , 0
verde_escuro =  0, 75 ,0 
cores = [branco,preto,cinza,vermelho,azul,verde,roxo,amarelo]

# Tamanhos:
c,l = 800,600
tela = pygame.display.set_mode(( c, l ), pygame.RESIZABLE)
titulo = pygame.display.set_caption("Simulação 2")
c_rua,l_rua =  c , l/2.2
px_rua,py_rua =  0 , (l-l_rua)/2
g = 7
l_carro,c_carro = 40 , 80
via1 = (py_rua + l_rua/4) - 2*g
via2 = (l/2) + l_rua/4 -2*g
via3 = via3_x,via3_y = ((c-l_rua)/2 + l_rua/4 -2*g, -l_carro)
via4 = via4_x,via4_y = ((c-l_rua)/2 + 3*l_rua/4 -g, l+l_carro)
vias = (via1,via2,via3,via4)
carro_imagem = pygame.image.load("Car64.png").convert_alpha()

class Carro:
    def __init__( self , cor , x , y , c_carro, l_carro, velocidade_x , velocidade_y , rotação):
        self.cores = cor
        self.x = x
        self.y = y
        self.c_carro, self.l_carro = c_carro,l_carro
        self.velocidade_x = velocidade_x
        self.velocidade_y = velocidade_y
        self.carro_imagem = pygame.transform.rotate(carro_imagem, rotação)
        self.imagem = pygame.transform.scale(self.carro_imagem, (c_carro, l_carro))
    def desenhar(self,tela):
        tela.blit(self.imagem, (self.x, self.y))
        
    def movimento(self):    
            self.x += self.velocidade_x
            self.y += self.velocidade_y

# initialize data of lists.
data = {'Probabilidade Relativa': [0.1, 0.2, 0.5, 0.2],
        'Probabilidade Acumulada': [0.1,0.3,0.8,1.0],
        'Velocidade Min': [1.85,2.78,3.70,4.63],
        'Velocidade Max': [2.77,3.69,4.62,5.55]}
# Create DataFrame
df = pd.DataFrame(data)
Prob_Acum = df["Probabilidade Acumulada"]
def gerar_velocidade():
    x = np.random.rand()
    i=0
    for prob_acum in Prob_Acum:
        if prob_acum > x:
            break
        i += 1
    min = df['Velocidade Min'][i]
    max = df['Velocidade Max'][i]
    v = random.uniform(min,max)
    return v
#tamanhos = {
    #"pequeno": (random.randint(70, 85), random.randint(32, 35)),
    #"medio": (random.randint(85, 100), random.randint(35, 40)),
    #"grande": (random.randint(100, 110), random.randint(40, 45)),}

#tipo_carro = random.choice(list(tamanhos.keys()))
#c_carro, l_carro = tamanhos[tipo_carro]

carros = []
def criar_carros_aleatorios():
    cor = random.choice(cores)
    y = random.choice(vias)
    if y == via1:
        c_carro,l_carro = 80 , 40
        x = c_rua
        velocidade_x = -1*gerar_velocidade()
        velocidade_y = 0
        rotação = 180
    elif y == via2:
        c_carro,l_carro = 80 , 40
        x = -80
        velocidade_x = gerar_velocidade()
        velocidade_y = 0
        rotação = 0
    elif y == via3:
        c_carro,l_carro = 40 , 80
        x,y = via3
        velocidade_x = 0
        velocidade_y = gerar_velocidade()
        rotação = 270
    else :
        c_carro,l_carro = 40 , 80
        x,y = via4
        velocidade_x = 0
        velocidade_y = -1*gerar_velocidade()
        rotação = 90
    
    return (Carro( cor , x , y, c_carro, l_carro, velocidade_x,velocidade_y,rotação))

tempo_proximo_carro = 100
ultimo_tempo = pygame.time.get_ticks()
clock = pygame.time.Clock()
dt = 0
rodando = True
while rodando:
    
    tela.fill(verde_escuro)
    rua1 = pygame.draw.rect( tela , asfalto ,( px_rua , py_rua , c_rua , l_rua ))
    faixa1 = pygame.draw.rect( tela , amarelo , ( px_rua , l/2-g , (c-l_rua)/2 , g ))
    faixa1_2 = pygame.draw.rect( tela , amarelo , ( (c+l_rua)/2 , l/2-g , c , g ))
    faixa2 = pygame.draw.rect( tela , amarelo , ( px_rua , l/2+g , (c-l_rua)/2 , g ))
    faixa2_2 = pygame.draw.rect( tela , amarelo , ( (c+l_rua)/2 , l/2+g , c , g ))

    rua2 = pygame.draw.rect( tela , asfalto ,( (c-l_rua)/2 , 0 , l_rua , l ))
    faixa3 = pygame.draw.rect( tela , amarelo , ( (c-l_rua)/2 + l_rua/2 - g , 0 , g , (l-l_rua)/2 ))
    faixa3_2 = pygame.draw.rect( tela , amarelo , ( (c-l_rua)/2 + l_rua/2 + g, 0 , g , (l-l_rua)/2 ))
    faixa4 = pygame.draw.rect( tela , amarelo , ( (c-l_rua)/2 + l_rua/2 - g , (l+l_rua)/2 , g , (l-l_rua)/2 ))
    faixa4_2 = pygame.draw.rect( tela , amarelo , ( (c-l_rua)/2 + l_rua/2 + g, (l+l_rua)/2 , g , (l-l_rua)/2 ))

    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ultimo_tempo > tempo_proximo_carro: 
        carros.append(criar_carros_aleatorios())
        tempo_proximo_carro = random.randint(200,2000)
        ultimo_tempo = tempo_atual

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    for carro in carros:
        carro.desenhar(tela)
        carro.movimento()
    
    carros = [carro for carro in carros if -c_carro <= carro.x <= c +c_carro and -c_carro <= carro.y <= l+c_carro]
    pygame.display.flip()
    dt = clock.tick(60)
pygame.quit()
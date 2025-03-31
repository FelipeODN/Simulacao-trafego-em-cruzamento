import pygame
import random
import tkinter as tk
import numpy as np
import pandas as pd
import time
pygame.init()
# Cores:
branco =  pygame.image.load("Car64.png")
preto = pygame.image.load("CarPolice.png")
asfalto =  35 , 35 , 35 
vermelho =  pygame.image.load("CarRED64.png")
azul =  pygame.image.load("CarBlue64.png")
verde =  pygame.image.load("CarGreen64.png")
amarelo =  pygame.image.load("CarYellow64.png")
verde_escuro =  0, 75 ,0 
cores = [branco,preto,vermelho,azul,verde,amarelo]
# Tamanhos:
c,l = 1000,600
tela = pygame.display.set_mode(( c, l ), pygame.RESIZABLE)
titulo = pygame.display.set_caption("Simulação 4")
c_rua,l_rua =  c , l/2.2
px_rua,py_rua =  0 , (l-l_rua)/2
g = 7
l_carro,c_carro = 40 , 80
via1 = via1_x,via1_y = c+1, (py_rua + l_rua/4) - 2*g
via2 = via2_x,via2_y = -1 , py_rua+3*l_rua/4
via3 = via3_x,via3_y = ((c-l_rua)/2 + l_rua/4 -2*g, -1)
via4 = via4_x,via4_y = ((c-l_rua)/2 + 3*l_rua/4 -g, l+1)
vias = (via1,via2,via3,via4)
fonte = pygame.font.Font(None, 36)

class Carro:
    def __init__( self , cor , x , y , c_carro, l_carro, velocidade_x , velocidade_y , rotação, via):
        self.cores = pygame.transform.rotate(cor, rotação)
        self.cores = pygame.transform.scale(self.cores, (c_carro, l_carro))
        self.x = float(x) if isinstance(x, (int, float)) else float(x[0])
        self.y = float(y) if isinstance(y, (int, float)) else float(y[1])
        self.c_carro, self.l_carro = c_carro,l_carro
        self.velocidade_x = velocidade_x
        self.velocidade_y = velocidade_y
        self.via = via
        
    def desenhar(self,tela):
        tela.blit(self.cores, (int(self.x), int(self.y)))
        
    def movimento(self):    

            if self.velocidade_x > 0  :
                if 300 <= self.x +c_carro < (c-l_rua)/2 -g and estado=='vermelho':
                        self.x += 0
                else   :
                    self.x += self.velocidade_x
            if self.velocidade_x < 0 :
                if (c+l_rua)/2 +g <= self.x < (c+l_rua)/2 + 100 and estado=='vermelho' and self.velocidade_x <0 :
                        self.x -= 0
                else   :
                    self.x += self.velocidade_x

            for outro_carro in carros:
                    if outro_carro != self :
                        if outro_carro.velocidade_x > 0 and self.velocidade_x >0:
                            d_x = abs(self.x - outro_carro.x)
                            if d_x < 50:
                                self.x = self.x -100
                                self.velocidade_x = outro_carro.velocidade_x
                        if outro_carro.velocidade_x < 0 and self.velocidade_x < 0:
                            d_x = abs(self.x - outro_carro.x)
                            if d_x < 50:
                                self.x = self.x + 100
                                self.velocidade_x = outro_carro.velocidade_x
                   

                    

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


carros = []
carros_via1 = []
carros_via2 = []
carros_via3 = []
carros_via4 = []

def criar_carros_aleatorios(z):
    cor = random.choice(cores)
    z = random.choice([via1,via2])
    if z == via1:
        c_carro,l_carro = 80 , 40
        x,y = via1
        velocidade_x = -1*gerar_velocidade()
        velocidade_y = 0
        rotação = 180
        via = 1
    elif z == via2:
        c_carro,l_carro = 80 , 40
        x,y = via2
        velocidade_x = gerar_velocidade()
        velocidade_y = 0
        rotação = 0
        via = 2
    elif z == via3:
        c_carro,l_carro = 40 , 80
        x,y = via3
        velocidade_x = 0
        velocidade_y = gerar_velocidade()
        rotação = 270
        via = 3
    else :
        c_carro,l_carro = 40 , 80
        x,y = via4
        velocidade_x = 0
        velocidade_y = -1*gerar_velocidade()
        rotação = 90
        via = 4
    
    return (Carro( cor , x , y, c_carro, l_carro, velocidade_x , velocidade_y , rotação, via))

def desenhar_semaforo(cor):
    pygame.draw.rect(tela, 0, ((c-l_rua)/2-50, py_rua+l_rua-1, 50, 130))  # Semáforo
    pygame.draw.circle(tela, 'red' if cor == "vermelho" else (50, 0, 0), ((c-l_rua-50)/2+1, py_rua+l_rua-1+25), 15)
    pygame.draw.circle(tela, 'yellow' if cor == "amarelo" else (50, 50, 0), ((c-l_rua-50)/2+1, py_rua+l_rua-1+65), 15)
    pygame.draw.circle(tela,  'green' if cor == "verde" else (0, 50, 0), ((c-l_rua-50)/2+1, py_rua+l_rua-1+105), 15)
    
def desenhar_rua():
    pygame.draw.rect( tela , asfalto ,( px_rua , py_rua , c_rua , l_rua )) #rua horizontal
    pygame.draw.rect( tela , 'yellow' , ( px_rua , l/2-g , (c-l_rua)/2 , g )) #faixa horizontal 1
    pygame.draw.rect( tela , 'yellow' , ( (c+l_rua)/2 , l/2-g , c , g )) #faixa horizontal 1_2
    pygame.draw.rect( tela , 'yellow' , ( px_rua , l/2+g , (c-l_rua)/2 , g )) #faixa horizontal 2
    pygame.draw.rect( tela , 'yellow' , ( (c+l_rua)/2 , l/2+g , c , g )) #faixa horizontal 2_1
    pygame.draw.rect( tela , asfalto ,( (c-l_rua)/2 , 0 , l_rua , l )) #rua vertical
    pygame.draw.rect( tela , 'yellow' , ( (c-l_rua)/2 + l_rua/2 - g , 0 , g , (l-l_rua)/2 )) #faixa horizontal 3
    pygame.draw.rect( tela , 'yellow' , ( (c-l_rua)/2 + l_rua/2 + g, 0 , g , (l-l_rua)/2 )) #faixa horizontal 3_2
    pygame.draw.rect( tela , 'yellow' , ( (c-l_rua)/2 + l_rua/2 - g , (l+l_rua)/2 , g , (l-l_rua)/2 )) #faixa horizontal 4
    pygame.draw.rect( tela , 'yellow' , ( (c-l_rua)/2 + l_rua/2 + g, (l+l_rua)/2 , g , (l-l_rua)/2 )) #faixa horizontal 4_2
    pygame.draw.rect( tela , 'white' , ( (c+l_rua)/2 , py_rua , g , l_rua/2 -2*g)) # faixa branca redutora 1
    pygame.draw.rect( tela , 'white' , ( (c-l_rua)/2 -g, l/2+2*g , g , l_rua/2 -2*g)) # faixa branca redutora 2

    pygame.draw.rect( tela , 'white' , ( (c-l_rua)/2 -g, l/2+2*g , g , l_rua/2 -2*g)) # faixa branca redutora 2
    pygame.draw.rect( tela , 'white' , ( (c-l_rua)/2 -g, l/2+2*g , g , l_rua/2 -2*g)) # faixa branca redutora 2

tempo_proximo_carro = 100
ultimo_tempo = pygame.time.get_ticks()
clock = pygame.time.Clock()
dt = 0
rodando = True
tempo_anterior = time.time()
inicio = time.time()
duracoes = {"vermelho": 6, "amarelo": 1, "verde": 6}
estado = random.choice(['vermelho','amarelo','verde'])
i=0


while rodando:
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

#criação carros

    #carros1
    
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ultimo_tempo > tempo_proximo_carro:
                
                if len(carros)<6 and estado=='verde' : 
                    carros.append(criar_carros_aleatorios(via1))
                    tempo_proximo_carro = random.randint(1000,2000)
                    ultimo_tempo = tempo_atual
                if len(carros)<3 and estado!='verde':
                    dx = 0 
                    for outro_carro in carros :
                        if outro_carro.velocidade_x > 0:
                            dx = abs(750 - outro_carro.x)
                            if dx > 100 or dx < 0 :
                                break
                    if dx > 100 or dx < 0 :
                        carros.append(criar_carros_aleatorios(via1))
                        tempo_proximo_carro = random.randint(1000,2000)
                        ultimo_tempo = tempo_atual
#carros2






#timer semaforos
    if time.time() - tempo_anterior > duracoes[estado]:
        if estado == "vermelho":
            estado = "verde"
        elif estado == "verde":
            estado = "amarelo"
        elif estado == "amarelo":
            estado = "vermelho"
        tempo_anterior = time.time()
#legenda tempo
    tempo_decorrido = time.time() - inicio
    tempo_texto = f"Tempo: {tempo_decorrido:.2f} s"
    texto_renderizado = fonte.render(tempo_texto, True, (255, 255, 255))
    tela.blit(texto_renderizado, (20, 20))
#desenhar
    tela.fill(verde_escuro)
    desenhar_rua()
    desenhar_semaforo(estado)
    tela.blit(texto_renderizado, (20, 20))



    for carro in carros:
        carro.movimento()
        carro.desenhar(tela)

    carros = [carro for carro in carros if -c_carro <= carro.x <= c+100 and -c_carro <= carro.y <= l+1]
    '''carros_via1 = [carro for carro in carros_via1 if -c_carro <= carro.x <= c+100 and -c_carro <= carro.y <= l+1]
    carros_via2 = [carro for carro in carros_via2 if -c_carro <= carro.x <= c+100 and -c_carro <= carro.y <= l+1]
    carros_via3 = [carro for carro in carros_via3 if -c_carro <= carro.x <= c+100 and -c_carro <= carro.y <= l+1]
    carros_via4 = [carro for carro in carros_via4 if -c_carro <= carro.x <= c+100 and -c_carro <= carro.y <= l+1]'''

    pygame.display.flip()
    dt = clock.tick(60)
pygame.quit()
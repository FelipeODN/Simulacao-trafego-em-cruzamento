import pygame
import random
import tkinter as tk
import numpy as np
import pandas as pd
import time
pygame.init()
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
titulo = pygame.display.set_caption("Simulação 3")
c_rua,l_rua =  c , l/2.2
px_rua,py_rua =  0 , (l-l_rua)/2
g = 7
l_carro,c_carro = 40 , 80
via1 = (py_rua + l_rua/4) - 2*g
via2 = via2_x,via2_y = (l/2) + l_rua/4 -2*g , py_rua+3*l_rua/4
via3 = via3_x,via3_y = ((c-l_rua)/2 + l_rua/4 -2*g, -l_carro)
via4 = via4_x,via4_y = ((c-l_rua)/2 + 3*l_rua/4 -g, l+l_carro)
vias = (via1,via2,via3,via4)
semaforo = s_x,s_y = 200,500
carro_imagem = pygame.image.load("Car64.png").convert_alpha()
fonte = pygame.font.Font(None, 36)
class Carro:
    def __init__( self , cor , x , y , c_carro, l_carro, velocidade_x , velocidade_y , rotação):
        self.cores = cor
        self.x = float(x) if isinstance(x, (int, float)) else float(x[0])  # Pegando apenas o número
        self.y = float(y) if isinstance(y, (int, float)) else float(y[1])
        self.c_carro, self.l_carro = c_carro,l_carro
        self.velocidade_x = velocidade_x
        self.velocidade_y = velocidade_y
        self.carro_imagem = pygame.transform.rotate(carro_imagem, rotação)
        self.imagem = pygame.transform.scale(self.carro_imagem, (c_carro, l_carro))
    def desenhar(self,tela):
        tela.blit(self.carro_imagem, (int(self.x), int(self.y)))
        
    def movimento(self):    
            if 200 <= self.x +c_carro < 280 and estado=='vermelho' and self.velocidade_x >0 :
                self.x += 0
            else   :
                self.x += self.velocidade_x
            self.y += self.velocidade_y

            for outro_carro in carros:
                if outro_carro != self  and  outro_carro.velocidade_x > 0 and self.velocidade_x >0:
                    d_x = abs(self.x - outro_carro.x)
                    if d_x < 50:
                       self.x = self.x -100
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
#tamanhos = {
    #"pequeno": (random.randint(70, 85), random.randint(32, 35)),
    #"medio": (random.randint(85, 100), random.randint(35, 40)),
    #"grande": (random.randint(100, 110), random.randint(40, 45)),}

#tipo_carro = random.choice(list(tamanhos.keys()))
#c_carro, l_carro = tamanhos[tipo_carro]

carros = []
def criar_carros_aleatorios():
    cor = random.choice(cores)
    #y = random.choice(vias)
    y = via2
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

def desenhar_semaforo(cor):
    pygame.draw.rect(tela, preto, (215, 435, 48, 140))  # Estrutura
    # Luzes do semáforo
    pygame.draw.circle(tela, vermelho if cor == "vermelho" else (50, 0, 0), (240,460), 15)
    pygame.draw.circle(tela, amarelo if cor == "amarelo" else (50, 50, 0), (240, 505), 15)
    pygame.draw.circle(tela, verde if cor == "verde" else (0, 50, 0), (240, 550), 15)
    
def desenhar_rua():
    pygame.draw.rect( tela , asfalto ,( px_rua , py_rua , c_rua , l_rua )) #rua horizontal
    pygame.draw.rect( tela , amarelo , ( px_rua , l/2-g , (c-l_rua)/2 , g )) #faixa horizontal 1
    pygame.draw.rect( tela , amarelo , ( (c+l_rua)/2 , l/2-g , c , g )) #faixa horizontal 1_2
    pygame.draw.rect( tela , amarelo , ( px_rua , l/2+g , (c-l_rua)/2 , g )) #faixa horizontal 2
    pygame.draw.rect( tela , amarelo , ( (c+l_rua)/2 , l/2+g , c , g )) #faixa horizontal 2_1
    pygame.draw.rect( tela , asfalto ,( (c-l_rua)/2 , 0 , l_rua , l )) #rua vertical
    pygame.draw.rect( tela , amarelo , ( (c-l_rua)/2 + l_rua/2 - g , 0 , g , (l-l_rua)/2 )) #faixa horizontal 3
    pygame.draw.rect( tela , amarelo , ( (c-l_rua)/2 + l_rua/2 + g, 0 , g , (l-l_rua)/2 )) #faixa horizontal 3_2
    pygame.draw.rect( tela , amarelo , ( (c-l_rua)/2 + l_rua/2 - g , (l+l_rua)/2 , g , (l-l_rua)/2 )) #faixa horizontal 4
    pygame.draw.rect( tela , amarelo , ( (c-l_rua)/2 + l_rua/2 + g, (l+l_rua)/2 , g , (l-l_rua)/2 )) #faixa horizontal 4_2
tempo_proximo_carro = 100
ultimo_tempo = pygame.time.get_ticks()
clock = pygame.time.Clock()
dt = 0
rodando = True
estado = "vermelho"
tempo_anterior = time.time() #segundos
duracoes = {"vermelho": 6, "amarelo": 1, "verde": 6}
inicio = time.time() # time.time(), Retorna o tempo atual em segundos desde 01/01/1970 (Epoch time).



while rodando:
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    tela.fill(verde_escuro)
    
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ultimo_tempo > tempo_proximo_carro:
        if len(carros)<3 and estado=='verde': 
            carros.append(criar_carros_aleatorios())
            tempo_proximo_carro = random.randint(1000,2000)
            ultimo_tempo = tempo_atual
        if len(carros)<3 and estado=='vermelho':
            dx = 0 
            for outro_carro in carros:
                if outro_carro.velocidade_x > 0:
                    dx = abs(215 - outro_carro.x)
                    if dx > 150 or dx < 0 :
                        break
            if dx > 150 or dx < 0 :
                carros.append(criar_carros_aleatorios())
                tempo_proximo_carro = random.randint(1000,2000)
                ultimo_tempo = tempo_atual


    #semaforo
    if time.time() - tempo_anterior > duracoes[estado]:
        if estado == "vermelho":
            estado = "verde"
        elif estado == "verde":
            estado = "amarelo"
        elif estado == "amarelo":
            estado = "vermelho"
        tempo_anterior = time.time()
        print('tempo atual - tempo_anterior >', duracoes[estado])
    #print("\ntp é",time.time()-inicio)
    #print("ta é",tempo_anterior-inicio)
    
    tempo_decorrido = time.time() - inicio
    tempo_texto = f"Tempo: {tempo_decorrido:.2f} s"
    texto_renderizado = fonte.render(tempo_texto, True, (255, 255, 255))
    tela.blit(texto_renderizado, (20, 20))
    desenhar_semaforo(estado)
    desenhar_rua()
    for carro in carros:
        carro.desenhar(tela)
        carro.movimento()
    
    carros = [carro for carro in carros if -c_carro <= carro.x <= c +c_carro and -c_carro <= carro.y <= l+c_carro]
    pygame.display.flip()
    dt = clock.tick(60) #pygame.time.Clock(), Controla a taxa de quadros por segundo (FPS) no Pygame.
pygame.quit()


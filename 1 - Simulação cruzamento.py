import pygame
import random
import tkinter as tk
import numpy as np
import pandas as pd
print (5/5+1)
# Cores:
branco =  255 , 255 , 255 
preto = 0
cinza = 127,127,127
asfalto =  75 , 75 , 75 
vermelho =  255 , 0 , 0
azul =  0 , 0 , 255 
verde =  0 , 255 , 0
roxo =  60 , 000 , 60 
amarelo =  255 , 255 , 0
laranja =  255 , 75 , 0 
marrom = 60, 35 , 15 
vinho =  35 , 0 , 25
azul_escuro	=	(0, 0, 139)
verde_escuro =  0, 75 ,0 
verde_alga =  0 , 30 , 20 
verde_musgo =  50 , 50 , 0
azul_marinho =   18 , 10 , 143 
água_marinha = 127, 255, 212
cores = [branco,preto,cinza,vermelho,azul,verde,roxo,amarelo,laranja,marrom,vinho,azul_escuro,verde_alga,verde_musgo,azul_marinho,água_marinha]

# Tamanhos:
c,l = 1250,750
tela = pygame.display.set_mode(( c, l ), pygame.RESIZABLE)
titulo = pygame.display.set_caption("Simulação 1")
c_rua,l_rua =  c , 300 
px_rua,py_rua =  0 , (l-l_rua)/2
g = 7
l_carro,c_carro = 40 , 80
via1 = (py_rua + l_rua/4)
via2 = (l/2) + l_rua/4 - g
via3 = via3_x,via3_y = ((c-l_rua)/2 + l_rua/4, -l_carro)
via4 = via4_x,via4_y = ((c-l_rua)/2 + 3*l_rua/4, l+l_carro)
vias = (via1,via2,via3,via4)

carro_imagem = pygame.image.load("Car64.png")  # Substitua pelo caminho correto do arquivo
carro_imagem = pygame.transform.scale(carro_imagem, (c_carro, l_carro))  # Ajustar tamanho

class Carro:
    def __init__( self , cor , x , y , c_carro, l_carro, velocidade_x , velocidade_y ):
        self.cores = cor
        self.x = x
        self.y = y
        self.c_carro, self.l_carro = c_carro,l_carro
        self.velocidade_x = velocidade_x
        self.velocidade_y = velocidade_y
        
    def desenhar(self,tela):
        pygame.draw.rect(tela,self.cores,( self.x , self.y , self.c_carro, self.l_carro))
        
    def movimento(self):    
            self.x += self.velocidade_x
            self.y += self.velocidade_y

# initialize data of lists.
data = {'Name': ['Faixa 1', 'Faixa 2', 'Faixa 3', 'Faixa 4'],
        'Probabilidade Relativa': [0.1, 0.2, 0.5, 0.2],
        'Probabilidade Acumulada': [0.1,0.3,0.8,1.0],
        'Velocidade Min': [20.0,30.0,40.0,50.0],
        'Velocidade Max': [29.9,39.9,49.9,59.9]}
# Create DataFrame
df = pd.DataFrame(data)
#print(df)
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
def criar_carros_aleatorios():
    cor = random.choice(cores)
    y = random.choice(vias)
    if y == via1:
        c_carro,l_carro = -80 , 40
        x = c_rua
        velocidade_x = -0.1*gerar_velocidade()
        velocidade_y = 0
    elif y == via2:
        c_carro,l_carro = 80 , 40
        x = -80
        velocidade_x = 0.1*gerar_velocidade()
        velocidade_y = 0
    elif y == via3:
        c_carro,l_carro = 40 , 80
        x,y = via3
        velocidade_x = 0
        velocidade_y = 0.1*gerar_velocidade()
    else :
        c_carro,l_carro = -40 , -80
        x,y = via4
        velocidade_x = 0
        velocidade_y = -0.1*gerar_velocidade()

    print(velocidade_x,velocidade_y)
    return (Carro( cor , x , y, c_carro, l_carro, velocidade_x,velocidade_y))

tempo_proximo_carro = 100
ultimo_tempo = pygame.time.get_ticks()
clock = pygame.time.Clock()
dt = 0
rodando = True
while rodando:
    
    tela.fill('dark green')
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
    
    carros = [carro for carro in carros if -c_carro <= carro.x <= c +c_carro]
    pygame.display.flip()
    dt = clock.tick(60)
#fecha o pygame dentro do while se rodando = false
pygame.quit() # se o de cima é verdade, por fim finaliza o algoritmo

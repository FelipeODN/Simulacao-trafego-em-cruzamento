import pygame
import random
import matplotlib.pyplot as plt
import numpy as np
import io
pygame.init()

# Tamanhos:
c,a = ( 1200 , 700 )                             
c_rua,a_rua = ( c , 300 )
px_rua,py_rua = ( 0 , (a-a_rua)//2)             
l_carro,c_carro = 40,90
y,x = (a - l_carro) /2, -c_carro
tela = pygame.display.set_mode((c,a))
pygame.display.set_caption("TESTE 3")
# Cores:
branco = ( 255 , 255 , 255 )
preto = ( 0 , 0 , 0)
cinza = ( 75 , 75 , 75 )
vermelho = ( 255 , 0 , 0)
azul = ( 0 , 0 , 255 )
verde = ( 0 , 255 , 0)
amarelo = ( 255 , 255 , 0)
laranja = ( 255 , 75 , 0 )
ciano = ( 0 , 255 , 255)
verde_escuro = ( 0 , 20 , 20 )
cores= [branco,preto,cinza,vermelho,azul,verde,amarelo,laranja,ciano,verde_escuro]              
faixa = pygame.draw.rect(tela,'red',(400, py_rua, 5, a_rua))  

class Carro:
    def __init__(self,cor,x,y, velocidade):
        self.cor = cor
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.historico = []  # guarda as velocidades ao longo do tempo

    def desenhar(self,tela):
        pygame.draw.rect(tela,self.cor,(self.x, y ,c_carro,l_carro))

    def movimento(self):
            self.x += self.velocidade

    def acelerar(self):
        pos_x = self.x+c_carro
        i = faixa.x - 150
        j = faixa.x - 50
        
        if i < pos_x < faixa.x :
            if self.velocidade >= 2 :
                self.velocidade -= 0.25
            if self.velocidade <= 0:
                self.velocidade += 0.05
        else:
            self.velocidade += 0.1

historicos_passados = []
velocidades = []
tempos = []
t = 0
carros = []                                                                 
clock = pygame.time.Clock()
rodando = True
while rodando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                carros.append(Carro(random.choice(cores),x,y,random.uniform(3,5)))
            if evento.button == 2:
                p = pygame.mouse.get_pos()
                a=2
            if evento.button == 3:
                carros.remove(carros[0]) if carros else None
        keys = pygame.key.get_pressed()
                

    tela.fill('dark green')
    pygame.draw.rect(tela,(50,50,50),( px_rua , py_rua , c_rua , a_rua ))
    pygame.draw.rect(tela,'red',(400, py_rua, 5, a_rua))
    i = pygame.draw.rect(tela,'blue',(faixa.x -150, py_rua, 5, a_rua))
    j = pygame.draw.rect(tela,'green',(faixa.x - 50, py_rua, 5, a_rua))
    pygame.draw.line(tela, (200, 200, 200), (50, 350), (550, 350), 2)  # eixo x
    pygame.draw.line(tela, (200, 200, 200), (50, 50), (50, 350), 2)

    # atualizar carros ativos
    novos_carros = []
    for carro in carros:
        carro.movimento()
        carro.desenhar(tela)
        carro.acelerar()
        carro.historico.append(carro.velocidade)

        # só mantém se não saiu da tela
        if carro.x < c:
            novos_carros.append(carro)
        else:
            historicos_passados.append((carro.historico, carro.cor))
    carros = novos_carros


    # eixos do gráfico
    pygame.draw.line(tela, (200, 200, 200), (50, 350), (550, 350), 2)  # eixo x
    pygame.draw.line(tela, (200, 200, 200), (50, 50), (50, 350), 2)
    
    # desenhar gráficos de carros ativos
    for carro in carros:
        pontos = [(50+i, 350 - int(vel*20)) for i, vel in enumerate(carro.historico)
                  if 50+i < 550 and 50 <= 350-int(vel*20) < 350]
        if len(pontos) > 1:
            pygame.draw.lines(tela, carro.cor, False, pontos, 2)

    # desenhar gráficos de carros que já saíram
    for historico, cor in historicos_passados:
        pontos = [(50+i, 350 - int(vel*20)) for i, vel in enumerate(historico)
                  if 50+i < 550 and 50 <= 350-int(vel*20) < 350]
        if len(pontos) > 1:
            pygame.draw.lines(tela, cor, False, pontos, 2)

    carros = [carro for carro in carros if carro.x < c]  # remove carros que saíram da tela
    pygame.display.flip()
    dt = clock.tick(60)/1000
    t += dt
pygame.quit()
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
titulo = pygame.display.set_caption("Simulação 5")
c_rua,l_rua =  c , l/2.2
px_rua,py_rua =  0 , (l-l_rua)/2
g = 7
l_carro,c_carro = 40 , 80
via1 = via1_x,via1_y = c+1, (py_rua + l_rua/4) - 2*g
via2 = via2_x,via2_y = -c_carro , py_rua+3*l_rua/4
via3 = via3_x,via3_y = ((c-l_rua)/2 + l_rua/4 -2*g, -1)
via4 = via4_x,via4_y = ((c-l_rua)/2 + 3*l_rua/4 -g, l+1)
vias = (via1,via2,via3,via4)
fonte = pygame.font.Font(None, 36)
faixa_branca1 = (c+l_rua)/2 +g
faixa_branca2 = (c-l_rua)/2 -g
print((c+l_rua)/2 +g)
print((c-l_rua)/2 -g)


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

            if self.velocidade_x < 0 :
                if faixa_branca1 <= self.x < faixa_branca1 + c_carro/2 and estado=='vermelho':
                        self.x -= 0
                else   :
                    self.x += self.velocidade_x

            if self.velocidade_x > 0  :
                if faixa_branca2 - c_carro/2 <= self.x +c_carro < faixa_branca2 and estado=='vermelho':
                        self.x += 0
                else   :
                    self.x += self.velocidade_x
            

            for outro_carro in carros:
                    if outro_carro != self :
                        if outro_carro.velocidade_x < 0 and self.velocidade_x < 0:
                            d_x = abs(self.x - outro_carro.x)
                            if d_x < 50 and self.x > outro_carro.x :
                                self.x = self.x + c_carro*0.7
                                self.velocidade_x = outro_carro.velocidade_x
                        if outro_carro.velocidade_x > 0 and self.velocidade_x >0:
                            d_x = abs(self.x - outro_carro.x)
                            if d_x < 50 and self.x < outro_carro.x :
                                self.x = self.x - c_carro*0.7
                                self.velocidade_x = outro_carro.velocidade_x
                








# inicializar data das listas.
data = {'Probabilidade Relativa': [0.1, 0.2, 0.5, 0.2],
        'Probabilidade Acumulada': [0.1,0.3,0.8,1.0],
        'Velocidade Min': [1.85,2.78,3.70,4.63],
        'Velocidade Max': [2.77,3.69,4.62,5.55]}
# Criar DataFrame
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
    #z = random.choice(vias)
    if z == via1:
        c_carro,l_carro = 80 , 40
        x,y = via1
        velocidade_x = -1*gerar_velocidade()
        velocidade_y = 0
        rotação = 180
        via = 1
    elif z == via2:
        c_carro,l_carro = 80 , 40
        x,y = via2_x,via2_y
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

tempo_proximo_carro1 = random.randint(1000,2000)
tempo_proximo_carro2 = random.randint(1000,2000)
ultimo_tempo1 = pygame.time.get_ticks()
ultimo_tempo2 = pygame.time.get_ticks()

clock = pygame.time.Clock()
dt = 0
rodando = True
tempo_anterior = time.time()
inicio = time.time()
duracoes = {"vermelho": 6, "amarelo": 1, "verde": 6}
estado = random.choice(['vermelho','amarelo','verde'])
pares_colididos = set()  # Armazena pares de carros que já colidiram
contador_colisoes = 0    # Contador total de colisões
a = 0
while rodando:
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        #timer semaforos
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                a = 1
    if time.time() - tempo_anterior > duracoes[estado] or a == 1:
            if estado == "vermelho":
                estado = "verde"
            elif estado == "verde":
                estado = "amarelo"
            elif estado == "amarelo":
                estado = "vermelho"
            tempo_anterior = time.time()
    a = 0


#criação carros

#carros1
    
    tempo_atual1 = pygame.time.get_ticks()
    if tempo_atual1 - ultimo_tempo1 > tempo_proximo_carro1:
            
        if len(carros_via1)<7 and estado == 'verde': 
            carros_via1.append(criar_carros_aleatorios(via1))
            tempo_proximo_carro1 = random.randint(1000,2000)
            ultimo_tempo1 = tempo_atual1
        if len(carros_via1)<3 and estado == 'vermelho':
            dx = 0 
            for outro_carro in carros_via1 :
                    dx = abs( faixa_branca1 + c_carro - outro_carro.x)
                    if dx < 100 :
                        break
            if dx < 100 :
                carros_via1.append(criar_carros_aleatorios(via1))
                tempo_proximo_carro1 = random.randint(1000,2000)
                ultimo_tempo1 = tempo_atual1
#carros2
    tempo_atual2 = pygame.time.get_ticks()
    if tempo_atual2 - ultimo_tempo2 > tempo_proximo_carro2:

        if len(carros_via2)<7 and estado == 'verde': 
            carros_via2.append(criar_carros_aleatorios(via2))
            tempo_proximo_carro2 = random.randint(1000,2000)
            ultimo_tempo2 = tempo_atual2

        if len(carros_via2)<3 and estado == 'vermelho':
            dx = 0 
            for carro in carros_via2 :
                if carro.velocidade_x > 0:
                    dx = abs(faixa_branca2 - c_carro*1.5 - carro.x)
                    if dx < 100 :
                        break
            if dx < 100 :
                carros_via2.append(criar_carros_aleatorios(via2))
                tempo_proximo_carro2 = random.randint(1000,2000)
                ultimo_tempo2 = tempo_atual2















#legenda tempo
    tempo_decorrido = time.time() - inicio
    tempo_texto = f"Tempo: {tempo_decorrido:.2f} s"
    texto_renderizado = fonte.render(tempo_texto, True, (255, 255, 255))
    tela.blit(texto_renderizado, (20, 20))
#legenda colisão
# Resetar os pares colididos a cada frame
    pares_colididos_frame = set()

    for i, carro in enumerate(carros):
    # Criar retângulo de colisão para o carro atual
        rect_carro = pygame.Rect(carro.x, carro.y, carro.c_carro, carro.l_carro)
    
        for j, outro_carro in enumerate(carros[i+1:], start=i+1):
        # Criar retângulo de colisão para o outro carro
            rect_outro = pygame.Rect(outro_carro.x, outro_carro.y, outro_carro.c_carro, outro_carro.l_carro)
        
        # Verificar colisão
            if rect_carro.colliderect(rect_outro):
            # Criar identificador único para o par de carros
                par = frozenset({id(carro), id(outro_carro)})
            
            # Verificar se já registramos essa colisão neste frame
                if par not in pares_colididos_frame:
                    pares_colididos_frame.add(par)
                
                # Verificar se é uma nova colisão (não registrada antes)
                    if par not in pares_colididos:
                        pares_colididos.add(par)
                        contador_colisoes += 1
                        print(f"Colisão detectada! Total: {contador_colisoes}")
    colisao_texto = f"Colisões: {contador_colisoes}"
    texto_colisao = fonte.render(colisao_texto, True, (255, 255, 255))
#desenhar
    tela.fill(verde_escuro)
    desenhar_rua()
    desenhar_semaforo(estado)
    tela.blit(texto_renderizado, (20, 20))
    tela.blit(texto_colisao, (800, 20))

    carros = carros_via1+carros_via2+carros_via3+carros_via4
    for carro in carros:
        carro.movimento()
        carro.desenhar(tela)

    #carros = [carro for carro in carros if -c_carro <= carro.x <= c+100 and -c_carro <= carro.y <= l+100]
    carros_via1 = [carro for carro in carros_via1 if -c_carro <= carro.x <= c+100 and -c_carro <= carro.y <= l+100]
    carros_via2 = [carro for carro in carros_via2 if -c_carro <= carro.x <= c+100 and -c_carro <= carro.y <= l+100]
    carros_via3 = [carro for carro in carros_via3 if -c_carro <= carro.x <= c+100 and -c_carro <= carro.y <= l+100]
    carros_via4 = [carro for carro in carros_via4 if -c_carro <= carro.x <= c+100 and -c_carro <= carro.y <= l+100]

    pygame.display.flip()
    dt = clock.tick(60)
pygame.quit()
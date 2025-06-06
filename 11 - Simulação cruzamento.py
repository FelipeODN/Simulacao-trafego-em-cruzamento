import pygame
import random
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import math as math
pygame.init()
# Cores:
asfalto =  35 , 35 , 35
verde_escuro =  0, 75 ,0 
branco =  pygame.image.load("carros/Carro_branco.png")
polícia = pygame.image.load("carros/carro_policia3.png")
vermelho =  pygame.image.load("carros/Carro_Vermelho.png")
azul =  pygame.image.load("carros/Carro_azul.png")
verde =  pygame.image.load("carros/carro_verde.png")
amarelo =  pygame.image.load("carros/Carro_Amarelo.png")
cinza = pygame.image.load("carros/Carro_cinza.png")
marrom = pygame.image.load("carros/Carro_marrom.png")
cinza2 = pygame.image.load("carros/carro_cinza2.png")
azul2 = pygame.image.load("carros/Carro_azul2.png")
preto = pygame.image.load("carros/preto.png")
caramelo = pygame.image.load("carros/caramelo.png")
azul_metalico = pygame.image.load("carros/carro_azul_metalico.png")
laranja = pygame.image.load("carros/laranja.png")
cores = [branco,polícia,vermelho,azul,verde,amarelo,cinza,marrom,cinza2,azul2,preto,caramelo,azul_metalico,laranja]
# DIMENSÕES:
c,l = 1200,800
tela = pygame.display.set_mode(( c, l ), pygame.RESIZABLE)
titulo = pygame.display.set_caption("Simulação 11")
c_rua,l_rua =  c , l/2.8
px_rua,py_rua =  0 , (l-l_rua)/2
g = 7
c_carro,l_carro = 90 , 45
via1 = via1_x,via1_y = c+1, (py_rua + l_rua/4) - 2*g
via2 = via2_x,via2_y = -c_carro , py_rua+3*l_rua/4
via3 = via3_x,via3_y = ((c-l_rua)/2 + l_rua/4 -2*g, -c_carro)
via4 = via4_x,via4_y = ((c-l_rua)/2 + 3*l_rua/4 -g, l+1)
vias = (via1,via2,via3,via4)
fonte = pygame.font.Font(None, 36)
faixa_branca1 = faixa_branca1_x,faixa_branca1_y = (c+l_rua)/2 +g , py_rua+2
faixa_branca2 = faixa_branca2_x,faixa_branca2_y = (c-l_rua)/2 -g , l/2+3*g
faixa_branca3 = faixa_branca3_x,faixa_branca3_y = (c-l_rua)/2  , py_rua - g
faixa_branca4 = faixa_branca4_x,faixa_branca4_y = c/2 + 20 , (l+l_rua)/2

class Carro:
    def __init__( self , cor , x , y , c_carro, l_carro, velocidade_x , velocidade_y , rotação , virar ):
        self.cor = cor
        self.cores = pygame.transform.rotate(self.cor, rotação)
        self.cores = pygame.transform.scale(self.cores, (c_carro, l_carro))
        self.x = float(x) if isinstance(x, (int, float)) else float(x[0])
        self.y = float(y) if isinstance(y, (int, float)) else float(y[1])
        self.c_carro, self.l_carro = c_carro,l_carro
        self.velocidade_x = velocidade_x
        self.velocidade_y = velocidade_y
        self.virar = virar

    def desenhar(self,tela):
        tela.blit(self.cores, (int(self.x), int(self.y)))

    def mostrar_velocidade(self, tela):
        centro_x = self.x + self.c_carro/2
        centro_y = self.y + self.l_carro/2
        fim_x = centro_x + self.velocidade_x * 20
        fim_y = centro_y + self.velocidade_y * 20
        pygame.draw.line(tela, (255, 255, 255), (centro_x, centro_y), (fim_x, fim_y), 2)
        velocidade_texto = f"{abs(self.velocidade_x + self.velocidade_y)/((1000/30)/60)*(3.6):.2f}Km/h"
        texto = fonte.render(velocidade_texto, True, 'white')
        if self.velocidade_x != 0:
            tela.blit(texto, (centro_x - 35 , centro_y - 50 ))
        else :
            tela.blit(texto, (centro_x - 30 , centro_y - 70 ))
                            
    def ajustar_velocidade(self):
        '''for carro in carros_via1:
            for self in carros_via1:
                if carro != self:
                    dx = abs(carro.x - self.x)
                    if 0 < dx < 100 and abs(self.velocidade_x) > abs(carro.velocidade_x) and self.x > carro.x:
                            self.velocidade_x *= 0.9  # Desacelera
                    else:
                            self.velocidade_x *= 1.1  # Acelera'''

    def movimento(self):    
        parado_semaforo = False
    # Para carros horizontais (via1 e via2)
        if self.velocidade_x != 0:
            if estado1 == 'vermelho' or estado1 == 'amarelo':
                if self.velocidade_x < 0:  # Via1 (indo para esquerda)
                    if faixa_branca1_x <= self.x < faixa_branca1_x + c_carro/2:
                        parado_semaforo = True
                    for carro in carros_via1:
                        if self != carro :
                            dx = abs(self.x - carro.x)
                            if self.x > carro.x and dx < c_carro*1.2 and faixa_branca1_x <= self.x < c:
                                parado_semaforo = True
                else: # Via1 (indo para direita)
                    if faixa_branca2_x - c_carro/2 <= self.x+c_carro < faixa_branca2_x:
                        parado_semaforo = True
                    for carro in carros_via2:
                        if self != carro :
                            dx = abs(self.x - carro.x)
                            if self.x < carro.x and dx < c_carro*1.2 and 0 <= self.x < faixa_branca2_x:
                                parado_semaforo = True
        # Para carros verticais (via3 e via4)
        elif estado2 == 'vermelho' or estado2 == 'amarelo':
            if self.velocidade_y > 0:  # Via3 (indo para baixo)
                if faixa_branca3_y - c_carro/4 <= self.y+c_carro < faixa_branca3_y:
                    parado_semaforo = True
                for carro in carros_via3:
                    if self != carro :
                        dy = abs(self.y - carro.y)
                        if self.y < carro.y and dy < c_carro*1.2 and 0 <= self.y+c_carro < faixa_branca3_y:
                            parado_semaforo = True
            else:  # Via4 (indo para cima)
                if faixa_branca4_y <= self.y < faixa_branca4_y + c_carro/4:
                    parado_semaforo = True
                for carro in carros_via4:
                    if self != carro :
                        dy = abs(self.y - carro.y)
                        if self.y > carro.y and dy < c_carro*1.2 and faixa_branca4_y <= self.y < l:
                            parado_semaforo = True
        # Se não está parado no semáforo, move normalmente
        if not parado_semaforo:
            self.x += self.velocidade_x
            self.y += self.velocidade_y

        # Distância segura:
        for outro_carro in carros:
            if outro_carro != self :
                if outro_carro.velocidade_x < 0 and self.velocidade_x < 0:
                    dx = abs(self.x - outro_carro.x)
                    if dx < c_carro*1.05 and self.x > outro_carro.x :
                        self.x = self.x + 50
                        self.velocidade_x = outro_carro.velocidade_x
                if outro_carro.velocidade_x > 0 and self.velocidade_x > 0:
                    dx = abs(self.x - outro_carro.x)
                    if dx < c_carro*1.05 and self.x < outro_carro.x :
                        self.x = self.x - 50
                        self.velocidade_x = outro_carro.velocidade_x      
                if outro_carro.velocidade_y > 0 and self.velocidade_y > 0:
                        dy = abs(self.y - outro_carro.y)
                        if dy < c_carro*1.05 and self.y < outro_carro.y :
                            self.y = self.y - 50
                            self.velocidade_y = outro_carro.velocidade_y
                if outro_carro.velocidade_y < 0 and self.velocidade_y < 0:
                        dy = abs(self.y - outro_carro.y)
                        if dy < c_carro*1.05 and self.y > outro_carro.y :
                            self.y = self.y + 50
                            self.velocidade_y = outro_carro.velocidade_y

    def mudar_via(self):
        # mudança de via para carros na via1
        if self in carros_via1 and self.virar == 'via4':
            if faixa_branca4_x+10 <= self.x <= faixa_branca4_x+50:
                novo_carro = Carro(self.cor,via4_x,self.y,45,90,0,self.velocidade_x,90,None)
                carros_via4.append(novo_carro)
                carros_via1.remove(self)
                return novo_carro
        if self in carros_via1 and self.virar == 'via3':
            if faixa_branca3_x+50 <= self.x+c_carro <= faixa_branca3_x+80:
                novo_carro = Carro(self.cor,via3_x,self.y,45,90,0,-self.velocidade_x,-90,None)
                carros_via3.append(novo_carro)
                carros_via1.remove(self)
                return novo_carro
        # mudança de via para carros na via2
        if self in carros_via2 and self.virar == 'via4':
            if faixa_branca4_x+10 <= self.x <= faixa_branca4_x+50:
                novo_carro = Carro(self.cor,via4_x,self.y,45,90,0,-self.velocidade_x,90,None)
                carros_via4.append(novo_carro)
                carros_via2.remove(self)
                return novo_carro
        if self in carros_via2 and self.virar == 'via3':
            if faixa_branca3_x+50 <= self.x+self.c_carro <= faixa_branca3_x+80:
                novo_carro = Carro(self.cor,via3_x,self.y,45,90,0,self.velocidade_x,-90,None)
                carros_via3.append(novo_carro)
                carros_via2.remove(self)
                return novo_carro
        # mudança de via para carros na via3
        if self in carros_via3 and self.virar == 'via1':
            if faixa_branca1_y+10 <= self.y+self.c_carro<= faixa_branca1_y+50:
                novo_carro = Carro(self.cor,self.x,via1_y,90,45,-self.velocidade_y,0,180,None)
                carros_via1.append(novo_carro)
                carros_via3.remove(self)
                return novo_carro
        if self in carros_via3 and self.virar == 'via2':
            if faixa_branca2_y+50 <= self.y <= faixa_branca2_y+80:
                novo_carro = Carro(self.cor,self.x,via2_y,90,45,self.velocidade_y,0,360,None)
                carros_via2.append(novo_carro)
                carros_via3.remove(self)
                return novo_carro
        # mudança de via para carros na via4
        if self in carros_via4 and self.virar == 'via1':
            if faixa_branca1_y+10 <= self.y+self.c_carro<= faixa_branca1_y+50:
                novo_carro = Carro(self.cor,self.x,via1_y,90,45,self.velocidade_y,0,180,None)
                carros_via1.append(novo_carro)
                carros_via4.remove(self)
                return novo_carro
        if self in carros_via4 and self.virar == 'via2':
            if faixa_branca2_y+50 <= self.y <= faixa_branca2_y+80:
                novo_carro = Carro(self.cor,self.x,via2_y,90,45,-self.velocidade_y,0,0,None)
                carros_via2.append(novo_carro)
                carros_via4.remove(self)
                return novo_carro

# Sistema unificado de escolha de via
def escolher_via(via_origem):
    x = np.random.rand()
    
    if via_origem == 'via1':
        if x <= 0.5:
            return random.choice(['via3', 'via4'])
        else:
            return 'via1'
    
    elif via_origem == 'via2':
        if x <= 0.5:
            return random.choice(['via3', 'via4'])
        else:
            return 'via2'
    
    elif via_origem == 'via3':
        if x <= 0.5:
            return random.choice(['via1', 'via2'])
        else:
            return 'via3'
    
    elif via_origem == 'via4':
        if x <= 0.5:
            return random.choice(['via2', 'via1'])
        else:
            return 'via4'

# inicializar data das listas.
data = {'Probabilidade Acumulada': [ 0.1 , 0.3 , 0.6 , 0.85 , 0.95 , 1],
        'Velocidade Min': [ 3.09 , 4.63 , 6.17 , 7.72 , 9.26 , 10.80 ],
        'Velocidade Max': [ 4.61 , 6.16 , 7.70 , 9.24 , 10.79 , 16.96 ]}
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

# iniciar listas carros
carros = []
carros_via1 = []
carros_via2 = []
carros_via3 = []
carros_via4 = []

def criar_carros_aleatorios(z):
    cor = random.choice(cores)
    #z = random.choice(vias)
    if z == via1:
        c_carro,l_carro = 90,45
        x,y = via1
        velocidade_x = -1*gerar_velocidade()
        velocidade_y = 0
        rotação = 180
        virar = escolher_via('via1')
    elif z == via2:
        c_carro,l_carro = 90,45
        x,y = via2_x,via2_y
        velocidade_x = gerar_velocidade()
        velocidade_y = 0
        rotação = 0
        virar = escolher_via('via2')
    elif z == via3:
        c_carro,l_carro = 45,90
        x,y = via3
        velocidade_x = 0
        velocidade_y = gerar_velocidade()
        rotação = 270
        virar = escolher_via('via3')
    else :
        c_carro,l_carro = 45,90
        x,y = via4
        velocidade_x = 0
        velocidade_y = -1*gerar_velocidade()
        rotação = 90
        virar = escolher_via('via4')
    return (Carro( cor , x , y, c_carro, l_carro, velocidade_x , velocidade_y , rotação , virar ))


def desenhar_semaforo1(cor):
    pygame.draw.rect(tela, 0, ((c-l_rua)/2-50, py_rua+l_rua, 50, 130))  # Semáforo 1
    pygame.draw.circle(tela, 'red' if cor == "vermelho" else (50, 0, 0), ((c-l_rua-50)/2+1, py_rua+l_rua-1+25), 15)
    pygame.draw.circle(tela, 'yellow' if cor == "amarelo" else (50, 50, 0), ((c-l_rua-50)/2+1, py_rua+l_rua-1+65), 15)
    pygame.draw.circle(tela,  'green' if cor == "verde" else (0, 50, 0), ((c-l_rua-50)/2+1, py_rua+l_rua-1+105), 15)
def desenhar_semaforo2(cor):
    pygame.draw.rect(tela, 0, ((c+l_rua)/2, py_rua-130, 50, 130))  # Semáforo 2
    pygame.draw.circle(tela, 'red' if cor == "vermelho" else (50, 0, 0), ((c+l_rua+50)/2, py_rua-130+25), 15)
    pygame.draw.circle(tela, 'yellow' if cor == "amarelo" else (50, 50, 0), ((c+l_rua+50)/2, py_rua-130+65), 15)
    pygame.draw.circle(tela,  'green' if cor == "verde" else (0, 50, 0), ((c+l_rua+50)/2, py_rua-130+105), 15)
    
def desenhar_rua():
    pygame.draw.rect( tela , asfalto ,  ( px_rua , py_rua , c_rua , l_rua ))                            #rua horizontal
    pygame.draw.rect( tela , 'yellow' , ( px_rua , l/2-g , (c-l_rua)/2 , g ))                           #faixa horizontal 1_1
    pygame.draw.rect( tela , 'yellow' , ( (c+l_rua)/2 , l/2-g , (c-l_rua)/2+1 , g ))                    #faixa horizontal 1_2
    pygame.draw.rect( tela , 'yellow' , ( px_rua , l/2+g , (c-l_rua)/2 , g ))                           #faixa horizontal 2_1
    pygame.draw.rect( tela , 'yellow' , ( (c+l_rua)/2 , l/2+g , (c-l_rua)/2+1 , g ))                    #faixa horizontal 2_2
    pygame.draw.rect( tela , asfalto ,  ( (c-l_rua)/2 , 0 , l_rua , l ))                                #rua vertical
    pygame.draw.rect( tela , 'yellow' , ( (c-l_rua)/2 + l_rua/2 - g , 0 , g , (l-l_rua)/2 ))            #faixa horizontal 3_1
    pygame.draw.rect( tela , 'yellow' , ( (c-l_rua)/2 + l_rua/2 + g, 0 , g , (l-l_rua)/2 ))             #faixa horizontal 3_2
    pygame.draw.rect( tela , 'yellow' , ( (c-l_rua)/2 + l_rua/2 - g , (l+l_rua)/2 , g , (l-l_rua)/2 ))  #faixa horizontal 4_1
    pygame.draw.rect( tela , 'yellow' , ( (c-l_rua)/2 + l_rua/2 + g, (l+l_rua)/2 , g , (l-l_rua)/2 ))   #faixa horizontal 4_2
    pygame.draw.rect( tela , 'white' ,  ( (c+l_rua)/2 , py_rua+2 , g , l_rua/2 -2*g))                   # faixa branca redutora 1
    pygame.draw.rect( tela , 'white' ,  ( (c-l_rua)/2 -g, l/2+3*g , g , l_rua/2 -2*g-10))               # faixa branca redutora 2
    pygame.draw.rect( tela , 'white' ,  ( (c-l_rua)/2 +2, py_rua - g , l_rua/2 -2*g , g))               # faixa branca redutora 3
    pygame.draw.rect( tela , 'white' ,  ( c/2 +3*g, (l+l_rua)/2 , l_rua/2 -3*g-3 , g))                  # faixa branca redutora 4

tempo_proximo_carro1 = random.randint(1000,2000)
tempo_proximo_carro2 = random.randint(1000,2000)
tempo_proximo_carro3 = random.randint(1000,2000)
tempo_proximo_carro4 = random.randint(1000,2000)
ultimo_tempo1 = pygame.time.get_ticks()
ultimo_tempo2 = pygame.time.get_ticks()
ultimo_tempo3 = pygame.time.get_ticks()
ultimo_tempo4 = pygame.time.get_ticks()
clock = pygame.time.Clock()
rodando = True
tempo_anterior1,tempo_anterior2 = time.time(),time.time()
inicio = time.time()
duracoes = {"vermelho": 6, "amarelo": 3 , "verde": 6}
estado1= random.choice(['vermelho','amarelo','verde'])
if estado1 == 'vermelho':
    estado2 = 'verde'
elif estado1 == 'verde':
    estado2 = 'vermelho'
else:  # se estado1 == 'amarelo'
    estado2 = 'verde'
pares_colididos = set()
contador_colisoes,dt,a = 0,0,0

# LOOP : 
while rodando:
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1] or keys[pygame.K_c]:
            carros_via1.clear()
        if keys[pygame.K_2] or keys[pygame.K_c]:
            carros_via2.clear()
        if keys[pygame.K_3] or keys[pygame.K_c]:
            carros_via3.clear()
        if keys[pygame.K_4] or keys[pygame.K_c]:
            carros_via4.clear()
        '''if keys[pygame.K_p]:
            pygame.mixer_music.pause()'''
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                a = 1
            if evento.button == 3:
                a = 2

# Timer semaforos:

# Semaforo 1 vias horizontais
    if time.time() - tempo_anterior1 > duracoes[estado1] or a == 1:
        if estado1 == "vermelho":
            estado1 = "verde"
        elif estado1 == "verde":
            estado1 = "amarelo"
        elif estado1 == "amarelo":
            estado1 = "vermelho"
        tempo_anterior1 = time.time()
    if a == 1 :
        tempo_anterior1 = time.time()
        tempo_semaforo1 = time.time()-tempo_anterior1
    tempo_semaforo1 = time.time()-tempo_anterior1
# Semaforo 2 vias verticais
    if time.time() - tempo_anterior2 > duracoes[estado2] or a == 2:
        if estado2 == "vermelho":
            estado2 = "verde"
        elif estado2 == "verde":
            estado2 = "amarelo"
        elif estado2 == "amarelo":
            estado2 = "vermelho"
        tempo_anterior2 = time.time()
    if a == 2 :
        tempo_anterior2 = time.time()
        tempo_semaforo2 = time.time()-tempo_anterior2
    a = 0
    tempo_semaforo2 = time.time()-tempo_anterior2

# CRIAÇÃO CARROS:

    # carros1 
    tempo_atual1 = pygame.time.get_ticks()
    if tempo_atual1 - ultimo_tempo1 > tempo_proximo_carro1:     
        if len(carros_via1)<9 and estado1 == 'verde': 
            carros_via1.append(criar_carros_aleatorios(via1))
            tempo_proximo_carro1 = random.randint(750,1500)
            ultimo_tempo1 = tempo_atual1
        if len(carros_via1)<4 and estado1 == ('vermelho' or 'amarelo'):
            dx = 0 
            for carro in carros_via1 :
                dx = abs( faixa_branca1_x - carro.x)
                if dx < 100 :
                    break
            if dx < 100 :
                carros_via1.append(criar_carros_aleatorios(via1))
                tempo_proximo_carro1 = random.randint(1500,2200)
                ultimo_tempo1 = tempo_atual1
    # carros2
    tempo_atual2 = pygame.time.get_ticks()
    if tempo_atual2 - ultimo_tempo2 > tempo_proximo_carro2:
        if len(carros_via2)<9 and estado1 == 'verde' : 
            carros_via2.append(criar_carros_aleatorios(via2))
            tempo_proximo_carro2 = random.randint(750,1500)
            ultimo_tempo2 = tempo_atual2
        if len(carros_via2)<4 and (estado1 == 'vermelho' or 'amarelo'):
            dx = 0 
            for carro in carros_via2 :
                if carro.velocidade_x > 0:
                    dx = abs(faixa_branca2_x - c_carro*1.5 - carro.x)
                    if dx < 100 :
                        break
            if dx < 100 :
                carros_via2.append(criar_carros_aleatorios(via2))
                tempo_proximo_carro2 = random.randint(1500,2200)
                ultimo_tempo2 = tempo_atual2
    # carros3
    tempo_atual3 = pygame.time.get_ticks()
    if tempo_atual3 - ultimo_tempo3 > tempo_proximo_carro3:
        if len(carros_via3)<6 and estado2 == 'verde': 
            carros_via3.append(criar_carros_aleatorios(via3))
            tempo_proximo_carro3 = random.randint(750,1500)
            ultimo_tempo3 = tempo_atual3
        if len(carros_via3)<3 and estado2 == ('vermelho' or 'amarelo'):
            dy = 0 
            for carro in carros_via3 :
                if carro.velocidade_y > 0:
                    dy = abs(faixa_branca3_y - c_carro/2 - carro.y)
                    if dy < 100 :
                        break
            if dy < 100 :
                carros_via3.append(criar_carros_aleatorios(via3))
                tempo_proximo_carro3 = random.randint(1500,2200)
                ultimo_tempo3 = tempo_atual3
    # carros4
    tempo_atual4 = pygame.time.get_ticks()
    if tempo_atual4 - ultimo_tempo4 > tempo_proximo_carro4:
        if len(carros_via4)<6 and estado2 == 'verde': 
            carros_via4.append(criar_carros_aleatorios(via4))
            tempo_proximo_carro4 = random.randint(750,1500)
            ultimo_tempo4 = tempo_atual4
        if len(carros_via4)<3 and estado2 == ('vermelho' or 'amarelo'):
            dy = 0 
            for carro in carros_via4 :
                if carro.velocidade_y < 0:
                    dy = abs(faixa_branca4_y  - carro.y)
                    if dy < 100 :
                        break
            if dy < 100 :
                carros_via4.append(criar_carros_aleatorios(via4))
                tempo_proximo_carro4 = random.randint(1500,2200)
                ultimo_tempo4 = tempo_atual4

# Colisão
    pares_colididos_frame = set()
    for i, carro in enumerate(carros):
        rect_carro = pygame.Rect(carro.x, carro.y, carro.c_carro, carro.l_carro)
        for j, outro_carro in enumerate(carros[i+1:], start=i+1):
            rect_outro = pygame.Rect(outro_carro.x, outro_carro.y, outro_carro.c_carro, outro_carro.l_carro)
            if rect_carro.colliderect(rect_outro):
                par = frozenset({id(carro), id(outro_carro)})
                if par not in pares_colididos_frame:
                    pares_colididos_frame.add(par)
                    if par not in pares_colididos:
                        pares_colididos.add(par)
                        contador_colisoes += 1

# Legenda comandos:

    # legenda tempo
    tempo_decorrido = time.time() - inicio
    tempo_texto = f"Tempo: {tempo_decorrido:.2f} s"
    texto_renderizado = fonte.render(tempo_texto, True, 'white')
    # legenda contador colisões
    texto_contador = f"Colisões: {contador_colisoes}"
    texto_colisao = fonte.render(texto_contador, True, 'white')
    #legenda semáforos
    tp1 = f"{tempo_semaforo1:.1f}s"
    texto_tempo_semaforo1 = fonte.render(tp1,True,'white')
    tp2 = f"{tempo_semaforo2:.1f}s"
    texto_tempo_semaforo2 = fonte.render(tp2,True,'white')
    mudar_semaforo1 = "esquerdo mouse troca o sinal -->"
    texto_mudar_semaforo1 = fonte.render(mudar_semaforo1,True,'black')
    mudar_semaforo2 = "<-- direito do mouse troca o sinal"
    texto_mudar_semaforo2 = fonte.render(mudar_semaforo2,True,'black')
    # legenda comandos limpar
    limpar_via1 = "aperte '1' para limpar via 1"
    texto_limpar1 = fonte.render(limpar_via1,True,'red')
    limpar_via2 = "aperte '2' para limpar via 2"
    texto_limpar2 = fonte.render(limpar_via2,True,'lightblue')
    limpar_via3 = "aperte '3' para limpar via 3"
    texto_limpar3 = fonte.render(limpar_via3,True,'green')
    limpar_via4 = "aperte '4' para limpar via 4"
    texto_limpar4 = fonte.render(limpar_via4,True,' yellow')
    limpar_tudo = "aperte 'c' para limpar tudo"
    texto_limpar_tudo = fonte.render(limpar_tudo,True,'purple')

#desenhar
    tela.fill(verde_escuro)
    desenhar_rua()
    desenhar_semaforo1(estado1)
    desenhar_semaforo2(estado2)
    tela.blit(texto_renderizado, (20, 20))
    tela.blit(texto_colisao, (820, 20))
    tela.blit(texto_mudar_semaforo1, ( (c-l_rua-900)/2 , py_rua+l_rua+50 ) )
    tela.blit(texto_mudar_semaforo2, ( (c+l_rua+120)/2 , py_rua-80 ))
    tela.blit(texto_limpar1, (820, 600))
    tela.blit(texto_limpar2, (820, 630))
    tela.blit(texto_limpar3, (820, 660))
    tela.blit(texto_limpar4, (820, 690))
    tela.blit(texto_limpar_tudo, (820, 720))
    tela.blit(texto_tempo_semaforo1, ((c-l_rua)/2-48, py_rua+l_rua+140))
    tela.blit(texto_tempo_semaforo2, ((c+l_rua)/2+5, 100))

    carros = carros_via1+carros_via2+carros_via3+carros_via4
    for carro in carros:
        carro.movimento()
        carro.ajustar_velocidade()
        carro.desenhar(tela)
        carro.mostrar_velocidade(tela)
        carro.mudar_via()

# Remvover carros fora do limite visível :
    carros_via1 = [carro for carro in carros_via1 if -c_carro <= carro.x <= c and -c_carro <= carro.y <= l]
    carros_via2 = [carro for carro in carros_via2 if -c_carro <= carro.x <= c and -c_carro <= carro.y <= l]
    carros_via3 = [carro for carro in carros_via3 if -c_carro <= carro.x <= c and -c_carro <= carro.y <= l]
    carros_via4 = [carro for carro in carros_via4 if -c_carro <= carro.x <= c and -c_carro <= carro.y <= l]

    pygame.display.flip()
    dt = clock.tick(60)

# Fim da Simulação
'''texto = texto_unificado = (
    "Você rodou a Simulação 11:\n\n"
    "A simulação durou %.2f segundos\n\n"
    "Houve %d colisões na simulação" ) % (tempo_decorrido, contador_colisoes)
plt.text(0.5, 0.5, texto, color="black", fontsize=12, ha='center')
plt.axis('off')'''
plt.show()
pygame.quit()

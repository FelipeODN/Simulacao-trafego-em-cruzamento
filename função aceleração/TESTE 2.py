import pygame
import random
pygame.init()

# Tamanhos:
c,a = ( 1200 , 700 )                             
c_rua,a_rua = ( c , 300 )
px_rua,py_rua = ( 0 , (a-a_rua)//2)             
l_carro,c_carro = 40,90
y = (a - l_carro) /2
x = -c_carro


tela = pygame.display.set_mode((c,a))
pygame.display.set_caption("TESTE 2")

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
        self.cores = cor
        self.x = x
        self.y = y
        self.velocidade = velocidade
        pos_x = self.x+c_carro

    def desenhar(self,tela):
        pygame.draw.rect(tela,self.cores,(self.x, y ,c_carro,l_carro))

    def movimento(self):
            #vel += acc * dt          # v = v0 + a*t
            #pos += vel * dt          # s = s0 + v*t
            #self.velocidade += 0.05*dt
            #self.x += self.velocidade
            self.x = self.x + self.velocidade
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

    pontos = []
    for p in range(0, t):
        X = 50 + p       # desloca no gráfico
        Y = 350 - (p**2)//50
        if 50 <= X < 550 and 50 <= Y < 350:
            pontos.append((X, Y))

    if len(pontos) > 1:
        pygame.draw.lines(tela, (0, 255, 0), False, pontos, 2)
            
    for carro in carros:
        carro.movimento()
        carro.desenhar(tela)
        carro.acelerar()
    
    pygame.display.flip()
    dt = clock.tick(60)
    t += 1
pygame.quit()
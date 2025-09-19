import pygame
import random
import matplotlib.pyplot as plt
import io

pygame.init()

# Config tela
LARGURA, ALTURA = 1200, 800
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Simulação com Gráfico")

# Config rua
LARGURA_RUA, ALTURA_RUA = LARGURA, 300
X_RUA, Y_RUA = 0, (ALTURA - ALTURA_RUA)
L_CARRO, C_CARRO = 40, 90
faixa = pygame.draw.rect(tela,'red',(400, X_RUA, 5, Y_RUA))

# Cores
CORES = [
    (255,255,255), (0,0,0), (75,75,75), (255,0,0), (0,0,255),
    (0,255,0), (255,255,0), (255,75,0), (0,255,255), (0,20,20)
]

# Classe carro
class Carro:
    def __init__(self, cor, x, y, velocidade):
        self.cor = cor
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.historico_x = []
        self.historico_y = []
        self.historico_velocidade = []
        self.historico_tempo = []
    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, C_CARRO, L_CARRO))

    def movimento(self):
        self.x += self.velocidade
        pos_x = self.x+C_CARRO
        i = faixa.x - 150
        j = faixa.x - 50
        
        if i < pos_x < faixa.x :
            if self.velocidade >= 2 :
                self.velocidade -= 0.25
            if self.velocidade <= 0:
                self.velocidade += 0.05
        else:
            self.velocidade += 0.1

    def registrar_historico(self):
        self.historico_velocidade.append(self.velocidade*50)
        self.historico_tempo.append(tempo)
        self.historico_x.append(self.x)
        self.historico_y.append(self.y)

# Função para gerar gráfico
def gerar_grafico(carros):
    plt.clf()
    for carro in carros:
        plt.plot(carro.historico_x, carro.historico_y, marker="o", markersize=2, label=f"Carro {id(carro)%1000}")

    plt.xlabel("Posição X (px)",color='white')
    plt.ylabel("Posição Y (px)",color='white')
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.title("Histórico dos Carros",color='white')
    plt.grid(True)
    plt.xlim(0, LARGURA)
    plt.ylim(0, ALTURA)
    plt.legend(fontsize=6)

    buf = io.BytesIO()
    plt.savefig(buf, format="PNG",transparent=True)
    buf.seek(0)
    grafico = pygame.image.load(buf)
    buf.close()
    return pygame.transform.scale(grafico, (600, 500))

def gerar_grafico_velocidade(carros):
    plt.clf()
    for carro in carros:
        plt.plot(carro.historico_tempo, carro.historico_velocidade, marker="o", markersize=2, label=f"Carro {id(carro)%1000}")

    plt.xlabel("Posição X (px)",color='white')
    plt.ylabel("Posição Y (px)",color='white')
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.title("Histórico dos Carros",color='white')
    plt.grid(True)
    plt.xlim(0, LARGURA)
    plt.ylim(0, ALTURA)
    plt.legend(fontsize=6)

    buf = io.BytesIO()
    plt.savefig(buf, format="PNG",transparent=True)
    buf.seek(0)
    grafico = pygame.image.load(buf)
    buf.close()
    return pygame.transform.scale(grafico, (600, 500))

# Loop principal
carros = []
clock = pygame.time.Clock()
rodando = True
t = 0
estado = 1
while rodando:
    
    # Atualizar carros
    for carro in carros:
        carro.movimento()
        carro.registrar_historico()

    # Remover carros fora da tela
    carros = [carro for carro in carros if carro.x < LARGURA]

    # Desenhar ambiente
    tela.fill((30, 30, 30))
    pygame.draw.rect(tela, (50,50,50), (X_RUA, Y_RUA, LARGURA_RUA, ALTURA_RUA))

    for carro in carros:
        carro.desenhar(tela)
    if carros:
        if estado == 1:
            grafico = gerar_grafico(carros)
            tela.blit(grafico, (0, 20))
            grafico2 = gerar_grafico_velocidade(carros)
            tela.blit(grafico2,(600,20))
    
    # Desenhar gráfico
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # botão esquerdo -> adiciona carro
                carros.append(Carro(random.choice(CORES), 0, random.randint(Y_RUA,ALTURA), random.uniform(2, 5)))
            if evento.button == 2:
                if estado == 0:
                    estado = 1
            if evento.button == 3:  # botão direito -> remove primeiro carro
                print("evento3")
                if estado == 1:
                    estado = 0
                


    pygame.display.flip()
    dt = clock.tick(60)
    t += dt
    tempo = t/100

pygame.quit()


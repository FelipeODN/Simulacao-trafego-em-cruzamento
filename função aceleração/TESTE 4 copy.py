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

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, C_CARRO, L_CARRO))

    def movimento(self):
        self.x += self.velocidade

    def registrar_historico(self):
        self.historico_x.append(self.x)
        self.historico_y.append(self.y)

# Função para gerar gráfico
def gerar_grafico(carros):
    plt.clf()
    for carro in carros:
        plt.plot(carro.historico_x, carro.historico_y, marker="o", markersize=2, label=f"Carro {id(carro)%1000}")

    plt.xlabel("Posição X (px)")
    plt.ylabel("Posição Y (px)")
    plt.title("Histórico dos Carros")
    plt.grid(True)
    plt.xlim(0, LARGURA)
    plt.ylim(0, ALTURA)
    plt.legend(fontsize=6)

    buf = io.BytesIO()
    plt.savefig(buf, format="PNG")
    buf.seek(0)
    grafico = pygame.image.load(buf)
    buf.close()
    return pygame.transform.scale(grafico, (400, 300))

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
        a = 1
            
    
    # Desenhar gráfico
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # botão esquerdo -> adiciona carro
                carros.append(Carro(random.choice(CORES), 0, ALTURA-(ALTURA_RUA-L_CARRO)/2, random.uniform(2, 5)))
            if evento.button == 3:  # botão direito -> remove primeiro carro
                print("evento3")
                grafico = gerar_grafico(carros)
                tela.blit(grafico, (400, 20))
                


    pygame.display.flip()
    dt = clock.tick(60)
    t += dt

pygame.quit()


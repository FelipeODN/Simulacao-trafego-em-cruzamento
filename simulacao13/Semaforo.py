import time
import random
from Config import *

class Semaforo:
    def __init__(self):
        self.duracoes = {"vermelho": 12, "amarelo": 3, "verde": 12}
        self.estado1 = random.choice(['vermelho', 'amarelo', 'verde'])
        self.estado2 = 'verde' if self.estado1 == 'vermelho' else 'vermelho' if self.estado1 == 'verde' else 'verde'
        self.tempo_anterior1 = time.time()
        self.tempo_anterior2 = time.time()
        self.tempo_semaforo1 = 0
        self.tempo_semaforo2 = 0
    
    def atualizar(self, a=0):
        # Semaforo 1 - vias horizontais
        if time.time() - self.tempo_anterior1 > self.duracoes[self.estado1] or a == 1:
            self.estado1 = {"vermelho": "verde", "verde": "amarelo", "amarelo": "vermelho"}[self.estado1]
            self.tempo_anterior1 = time.time()
        
        if a == 1:
            self.tempo_anterior1 = time.time()
        
        self.tempo_semaforo1 = time.time() - self.tempo_anterior1
        
        # Semaforo 2 - vias verticais
        if time.time() - self.tempo_anterior2 > self.duracoes[self.estado2] or a == 3:
            self.estado2 = {"vermelho": "verde", "verde": "amarelo", "amarelo": "vermelho"}[self.estado2]
            self.tempo_anterior2 = time.time()
        
        if a == 3:
            self.tempo_anterior2 = time.time()
        
        if a == 2:
            self.tempo_anterior1 = time.time()
            self.tempo_anterior2 = time.time()
            self.estado1 = 'verde'
            self.estado2 = 'verde'
            self.tempo_semaforo1 = 0
            self.tempo_semaforo2 = 0
        
        self.tempo_semaforo2 = time.time() - self.tempo_anterior2
        
        return self.tempo_semaforo1, self.tempo_semaforo2
    
    def desenhar_semaforo1(self, tela, cor):
        pygame.draw.rect(tela, 0, ((C - L_RUA)/2 - 50, PY_RUA + L_RUA, 50, 130))
        pygame.draw.circle(tela, 'red' if cor == "vermelho" else (50, 0, 0), 
                          ((C - L_RUA - 50)/2 + 1, PY_RUA + L_RUA - 1 + 25), 15)
        pygame.draw.circle(tela, 'yellow' if cor == "amarelo" else (50, 50, 0), 
                          ((C - L_RUA - 50)/2 + 1, PY_RUA + L_RUA - 1 + 65), 15)
        pygame.draw.circle(tela, 'green' if cor == "verde" else (0, 50, 0), 
                          ((C - L_RUA - 50)/2 + 1, PY_RUA + L_RUA - 1 + 105), 15)
    
    def desenhar_semaforo2(self, tela, cor):
        pygame.draw.rect(tela, 0, ((C + L_RUA)/2, PY_RUA - 130, 50, 130))
        pygame.draw.circle(tela, 'red' if cor == "vermelho" else (50, 0, 0), 
                          ((C + L_RUA + 50)/2, PY_RUA - 130 + 25), 15)
        pygame.draw.circle(tela, 'yellow' if cor == "amarelo" else (50, 50, 0), 
                          ((C + L_RUA + 50)/2, PY_RUA - 130 + 65), 15)
        pygame.draw.circle(tela, 'green' if cor == "verde" else (0, 50, 0), 
                          ((C + L_RUA + 50)/2, PY_RUA - 130 + 105), 15)
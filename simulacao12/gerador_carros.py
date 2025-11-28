import random
import numpy as np
import pandas as pd
from Carro import Carro
from Config import *

class GeradorCarros:
    def __init__(self):
        self.data = pd.DataFrame(DADOS_VELOCIDADE)
        self.cores = self._carregar_cores()
    
    def _carregar_cores(self):
        return [pygame.image.load(f"carros/{cor}.png") for cor in CORES_CARROS]
    
    def gerar_velocidade(self):
        x = np.random.rand()
        prob_acum = self.data["Probabilidade Acumulada"]
        
        for i, prob in enumerate(prob_acum):
            if prob > x:
                min_vel = self.data['Velocidade Min'][i]
                max_vel = self.data['Velocidade Max'][i]
                return random.uniform(min_vel, max_vel)
        return random.uniform(3.09, 4.61)
    
    def escolher_via(self, via_origem):
        x = np.random.rand()
        
        if via_origem == 'via1':
            return random.choice(['via3', 'via4']) if x <= 0.5 else 'via1'
        elif via_origem == 'via2':
            return random.choice(['via3', 'via4']) if x <= 0.5 else 'via2'
        elif via_origem == 'via3':
            return random.choice(['via1', 'via2']) if x <= 0.5 else 'via3'
        elif via_origem == 'via4':
            return random.choice(['via2', 'via1']) if x <= 0.5 else 'via4'
    
    def criar_carro_aleatorio(self, via):
        cor = random.choice(self.cores)
        
        if via == VIA1:
            config = (90, 45, -1 * self.gerar_velocidade(), 0, 180, 'via1')
        elif via == VIA2:
            config = (90, 45, self.gerar_velocidade(), 0, 0, 'via2')
        elif via == VIA3:
            config = (45, 90, 0, self.gerar_velocidade(), 270, 'via3')
        else:  # VIA4
            config = (45, 90, 0, -1 * self.gerar_velocidade(), 90, 'via4')
        
        c_carro, l_carro, vel_x, vel_y, rotacao, via_origem = config
        virar = self.escolher_via(via_origem)
        
        return Carro(cor, via[0], via[1], c_carro, l_carro, vel_x, vel_y, rotacao, virar)

def criar_carro_na_via(via_destino, carro_original, lista_origem, lista_destino, velocidade_invertida=False):
    """Função auxiliar para criar carro em nova via durante mudança"""
    configs = {
        'via1': (carro_original.x, VIA1[1], 90, 45, -carro_original.velocidade_y if velocidade_invertida else carro_original.velocidade_y, 0, 180),
        'via2': (carro_original.x, VIA2[1], 90, 45, carro_original.velocidade_y if velocidade_invertida else -carro_original.velocidade_y, 0, 0),
        'via3': (VIA3[0], carro_original.y, 45, 90, 0, -carro_original.velocidade_x if velocidade_invertida else carro_original.velocidade_x, -90),
        'via4': (VIA4[0], carro_original.y, 45, 90, 0, carro_original.velocidade_x if velocidade_invertida else -carro_original.velocidade_x, 90)
    }
    
    x, y, c_carro, l_carro, vel_x, vel_y, rotacao = configs[via_destino]
    novo_carro = Carro(carro_original.cor, x, y, c_carro, l_carro, vel_x, vel_y, rotacao, None)
    
    lista_destino.append(novo_carro)
    lista_origem.remove(carro_original)
    
    return novo_carro
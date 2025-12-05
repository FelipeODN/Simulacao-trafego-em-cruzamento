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
        return random.uniform(3.09, 16.96)
    
    def criar_carro_aleatorio(self, via):
        cor = random.choice(self.cores)
        
        if via == VIA1:
            config = (C_CARRO, L_CARRO, -1 * self.gerar_velocidade(), 0, 180, 'via1')
        elif via == VIA2:
            config = (C_CARRO, L_CARRO, self.gerar_velocidade(), 0, 0, 'via2')
        elif via == VIA3:
            config = (L_CARRO, C_CARRO, 0, self.gerar_velocidade(), 270, 'via3')
        else:  # VIA4
            config = (L_CARRO, C_CARRO, 0, -1 * self.gerar_velocidade(), 90, 'via4')
        
        c_carro, l_carro, vel_x, vel_y, rotacao, via_origem = config
        #virar = self.escolher_via(via_origem)
        
        return Carro(cor, via[0], via[1], c_carro, l_carro, vel_x, vel_y, rotacao, virar=None)
    
    def gerar_carro_via1(self, carros_via1, tempo_atual_pygame, ultimo_tempo, proximo_tempo, max_carros, espaco_minimo):
        """Gera carro na via1 se houver espaço e condições"""
        # Verifica timer e quantidade máxima
        if (tempo_atual_pygame - ultimo_tempo > proximo_tempo and 
            len(carros_via1) < max_carros):
            
            # Verifica espaço disponível (último carro não está muito perto do spawn)
            if carros_via1:
                ultimo_carro = max(carros_via1, key=lambda carro: carro.x)  # Maior X = mais à direita,# Lambda retorna: carro.x para cada carro,# max() compara esses valores de x
                traseira = ultimo_carro.x + C_CARRO
                limite = VIA1[0] - espaco_minimo
                
                if traseira > limite:
                    return ultimo_tempo, proximo_tempo, False
                # se o x é maior que o limite, não cria o carro, retorna falso, logica invertid
                #VERIFICAÇÃO: "O último carro está BLOQUEANDO o spawn?"
                #Se SIM (condição True) → return False (não cria)
                #Se NÃO (condição False) → continue (pode criar)

            #Se traseira > limite for True → entra no return False → função termina
            #Se não → continua e cria o carro

            # Cria o carro
            carros_via1.append(self.criar_carro_aleatorio(VIA1))
            
            # Retorna novos tempos
            return tempo_atual_pygame, random.randint(TP_1, TP_3), True
        
        return ultimo_tempo, proximo_tempo, False
    
    def gerar_carro_via2(self, carros_via2, tempo_atual_pygame, ultimo_tempo, proximo_tempo, max_carros, espaco_minimo):
        """Gera carro na via2 se houver espaço e condições"""
        if (tempo_atual_pygame - ultimo_tempo > proximo_tempo and 
            len(carros_via2) < max_carros):
            
            if carros_via2:
                ultimo_carro = min(carros_via2, key=lambda carro: carro.x)  # Menor X = mais à esquerda
                traseira = ultimo_carro.x
                limite = VIA2[0] + espaco_minimo
                if traseira < limite:
                    return ultimo_tempo, proximo_tempo, False
            
            carros_via2.append(self.criar_carro_aleatorio(VIA2))
            return tempo_atual_pygame, random.randint(TP_1, TP_3), True
        return ultimo_tempo, proximo_tempo, False

    def gerar_carro_via3(self, carros_via3, tempo_atual_pygame, ultimo_tempo, proximo_tempo, max_carros, espaco_minimo):
        """Gera carro na via3 se houver espaço e condições"""
        if (tempo_atual_pygame - ultimo_tempo > proximo_tempo and 
            len(carros_via3) < max_carros):
            
            if carros_via3:
                ultimo_carro = min(carros_via3, key=lambda carro: carro.y)  # Menor Y = mais acima
                traseira = ultimo_carro.y
                limite = VIA3[1] + C_CARRO +espaco_minimo
                if traseira < limite:
                    return ultimo_tempo, proximo_tempo, False
            
            carros_via3.append(self.criar_carro_aleatorio(VIA3))
            return tempo_atual_pygame, random.randint(TP_1, TP_3), True
        
        return ultimo_tempo, proximo_tempo, False

    def gerar_carro_via4(self, carros_via4, tempo_atual_pygame, ultimo_tempo, proximo_tempo, max_carros, espaco_minimo):
        """Gera carro na via4 se houver espaço e condições"""
        if (tempo_atual_pygame - ultimo_tempo > proximo_tempo and 
            len(carros_via4) < max_carros):
            
            if carros_via4:
                ultimo_carro = max(carros_via4, key=lambda carro: carro.y) # Maior Y = mais abaixo
                traseira = ultimo_carro.y + C_CARRO
                limite = VIA4[1] - espaco_minimo
                if traseira > limite:
                    return ultimo_tempo, proximo_tempo, False
            
            carros_via4.append(self.criar_carro_aleatorio(VIA4))
            return tempo_atual_pygame, random.randint(TP_1, TP_3), True
        
        return ultimo_tempo, proximo_tempo, False



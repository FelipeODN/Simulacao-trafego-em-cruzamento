import pygame
import time
import random
from Config import *
from Carro import Carro
from Semaforo import Semaforo
from gerador_carros import GeradorCarros
from desenho import *
from utils import *

def main():
    # Inicialização
    clock = pygame.time.Clock()
    rodando = True
    
    # Gerenciadores
    semaforo_manager = Semaforo()
    gerador_carros = GeradorCarros()
    
    # Listas de carros
    carros_via1, carros_via2, carros_via3, carros_via4 = [], [], [], []
    
    # Variáveis de controle
    inicio = time.time()
    contador_colisoes = 0
    pares_colididos = set()
    
    # Timers para geração de carros
    timers_carros = {
        'via1': {'ultimo_tempo': 0, 'proximo_tempo': random.randint(1000, 2000)},
        'via2': {'ultimo_tempo': 0, 'proximo_tempo': random.randint(1000, 2000)},
        'via3': {'ultimo_tempo': 0, 'proximo_tempo': random.randint(1000, 2000)},
        'via4': {'ultimo_tempo': 0, 'proximo_tempo': random.randint(1000, 2000)}
    }

    # LOOP PRINCIPAL
    while rodando:
        tempo_atual_pygame = pygame.time.get_ticks()
        tempo_decorrido = time.time() - inicio
        
        # Processar eventos
        rodando, a = processar_eventos(carros_via1, carros_via2, carros_via3, carros_via4, gerador_carros)
        if not rodando:
            break
        
        # Atualizar semáforos
        tempo_semaforo1, tempo_semaforo2 = semaforo_manager.atualizar(a)
        
        # Gerar carros na via1 (exemplo)
        if (tempo_atual_pygame - timers_carros['via1']['ultimo_tempo'] > 
            timers_carros['via1']['proximo_tempo'] and 
            len(carros_via1) < 8 and 
            semaforo_manager.estado1 == 'verde'):
            
            carros_via1.append(gerador_carros.criar_carro_aleatorio(VIAS[0]))
            timers_carros['via1']['ultimo_tempo'] = tempo_atual_pygame
            timers_carros['via1']['proximo_tempo'] = random.randint(750, 1500)
        
        # Atualizar todos os carros
        todos_carros = carros_via1 + carros_via2 + carros_via3 + carros_via4
        
        for carro in todos_carros:
            carro.movimento(carros_via1, carros_via2, carros_via3, carros_via4, 
                           semaforo_manager.estado1, semaforo_manager.estado2)
        
        # Verificar colisões
        novas_colisoes, novos_pares = verificar_colisoes(todos_carros)
        contador_colisoes += novas_colisoes
        pares_colididos.update(novos_pares)
        
        # RENDERIZAÇÃO
        TELA.fill(VERDE_ESCURO)
        desenhar_rua(TELA)
        semaforo_manager.desenhar_semaforo1(TELA, semaforo_manager.estado1)
        semaforo_manager.desenhar_semaforo2(TELA, semaforo_manager.estado2)
        desenhar_legendas(TELA, FONTE, tempo_decorrido, contador_colisoes, tempo_semaforo1, tempo_semaforo2)
        
        # Desenhar carros
        for carro in todos_carros:
            carro.desenhar(TELA)
            carro.mostrar_velocidade(TELA, FONTE)
        
        # Limpar carros fora da tela
        carros_via1 = limpar_carros_fora_tela(carros_via1)
        carros_via2 = limpar_carros_fora_tela(carros_via2)
        carros_via3 = limpar_carros_fora_tela(carros_via3)
        carros_via4 = limpar_carros_fora_tela(carros_via4)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
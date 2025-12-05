import pygame
import time
import random
from Config import *
from Carro import Carro
from Semaforo import Semaforo
from gerador_carros import GeradorCarros
from desenho import *
from utils import *
from SistemaSom import SistemaSom

def main():
    # Inicialização
    clock = pygame.time.Clock()
    rodando = True
    # Gerenciadores
    semaforo_manager = Semaforo()
    gerador_carros = GeradorCarros()
    sistema_som = SistemaSom()
    sistema_som.iniciar_musica_ambiente() #só puxa 1 vez, agora coloca dentro do while pra ver
    # Listas de carros
    carros_via1, carros_via2, carros_via3, carros_via4 = [], [], [], []
    # Variáveis de controle
    inicio = pygame.time.get_ticks()/1000
    contador_colisoes = 0
    pares_colididos = set()
    
    # Timers para geração de carros
    timers_carros = {
        'via1': {'ultimo_tempo1': 0, 'proximo_tempo1': random.randint(1000, 2000)},
        'via2': {'ultimo_tempo2': 0, 'proximo_tempo2': random.randint(1000, 2000)},
        'via3': {'ultimo_tempo3': 0, 'proximo_tempo3': random.randint(1000, 2000)},
        'via4': {'ultimo_tempo4': 0, 'proximo_tempo4': random.randint(1000, 1000)}
    }
    # LOOP PRINCIPAL
    while rodando:
        tempo_atual_pygame = pygame.time.get_ticks()
        tempo_decorrido = pygame.time.get_ticks()/1000 - inicio
        
        # Processar eventos
        rodando, a = processar_eventos(carros_via1, carros_via2, carros_via3, carros_via4, gerador_carros, sistema_som)
        if a == 1 or a == 2 or a== 3:
            sistema_som.sons['semáforo'].play()
        if not rodando:
            break
        
        # Atualizar semáforos
        tempo_semaforo1, tempo_semaforo2 = semaforo_manager.atualizar(a)
        
        # Gerar carros na via1
        ultimo_tempo1, proximo_tempo1, carro_criado1 = gerador_carros.gerar_carro_via1(carros_via1, 
        tempo_atual_pygame,timers_carros['via1']['ultimo_tempo1'],timers_carros['via1']['proximo_tempo1'],M1, DS_MIN)
        # Gerar carros na via2
        ultimo_tempo2, proximo_tempo2, carro_criado2 = gerador_carros.gerar_carro_via2(carros_via2, 
        tempo_atual_pygame,timers_carros['via2']['ultimo_tempo2'],timers_carros['via2']['proximo_tempo2'],M2, DS_MIN)
        # Gerar carros na via3
        ultimo_tempo3, proximo_tempo3, carro_criado3 = gerador_carros.gerar_carro_via3(carros_via3, 
        tempo_atual_pygame,timers_carros['via3']['ultimo_tempo3'],timers_carros['via3']['proximo_tempo3'],M3, DS_MIN_Y)
        # Gerar carros na via4
        ultimo_tempo4, proximo_tempo4, carro_criado4 = gerador_carros.gerar_carro_via4(carros_via4, 
        tempo_atual_pygame,timers_carros['via4']['ultimo_tempo4'],timers_carros['via4']['proximo_tempo4'],M4, DS_MIN_Y)
        
        # Atualiza os timers apenas se um carro foi criado
        if carro_criado1:
            timers_carros['via1']['ultimo_tempo1'] = ultimo_tempo1
            timers_carros['via1']['proximo_tempo1'] = proximo_tempo1
        if carro_criado2:
            timers_carros['via2']['ultimo_tempo2'] = ultimo_tempo2
            timers_carros['via2']['proximo_tempo2'] = proximo_tempo2
        if carro_criado3:
            timers_carros['via3']['ultimo_tempo3'] = ultimo_tempo3
            timers_carros['via3']['proximo_tempo3'] = proximo_tempo3
        if carro_criado4:
            timers_carros['via4']['ultimo_tempo4'] = ultimo_tempo4
            timers_carros['via4']['proximo_tempo4'] = proximo_tempo4
        
        # Atualizar todos os carros
        todos_carros = carros_via1 + carros_via2 + carros_via3 + carros_via4

        # Verificar colisões (apenas novas)
        novas_colisoes, pares_colididos_frame = verificar_colisoes(todos_carros, pares_colididos)
        contador_colisoes += novas_colisoes

        if novas_colisoes > 0:
            sistema_som.tocar_colisao()
        
        # Atualiza o conjunto de pares colididos para o próximo frame
        pares_colididos = pares_colididos_frame
        
        # RENDERIZAÇÃO
        TELA.fill(VERDE_ESCURO)
        desenhar_rua(TELA)
        semaforo_manager.desenhar_semaforo1(TELA, semaforo_manager.estado1)
        semaforo_manager.desenhar_semaforo2(TELA, semaforo_manager.estado2)
        desenhar_legendas(TELA, FONTE,FONTE_PEQUENA, tempo_decorrido, contador_colisoes, tempo_semaforo1, tempo_semaforo2,
                          estado_semaforo1=semaforo_manager.estado1,
                          estado_semaforo2=semaforo_manager.estado2,
                          total_carros=len(todos_carros),
                          total_carros_via1=len(carros_via1),
                          total_carros_via2=len(carros_via2),
                          total_carros_via3=len(carros_via3),
                          total_carros_via4=len(carros_via4))
        
        # Desenhar carros
        for carro in todos_carros:
            carro.movimento(carros_via1, carros_via2, carros_via3, carros_via4, 
                           semaforo_manager.estado1, semaforo_manager.estado2)
            carro.desenhar(TELA)
            carro.mostrar_velocidade(TELA, FONTE,carros_via1, carros_via2)
            carro.set_sistema_som(sistema_som)
        
        # Limpar carros fora da tela
        carros_via1 = limpar_carros_fora_tela(carros_via1)
        carros_via2 = limpar_carros_fora_tela(carros_via2)
        carros_via3 = limpar_carros_fora_tela(carros_via3)
        carros_via4 = limpar_carros_fora_tela(carros_via4)
        
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__": # Essa condição é o que roda tudo
    main()
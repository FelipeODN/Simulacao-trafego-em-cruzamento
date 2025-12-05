import pygame
import os

class SistemaSom:
    def __init__(self):
        # Inicializa mixer se não estiver inicializado
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
        
        # Cria pasta de sons se não existir
        if not os.path.exists("sons"):
            os.makedirs("sons")
        
        self.volume_geral = 0.7  # 70% volume padrão
        self.mute = False  # ← ADICIONE ESTA LINHA!
        self.volume_antes_mute = self.volume_geral
        # Carrega sons
        self.sons = {}
        self.carregar_sons()
        self.atualizar_volume_geral()
    
    def tocar_som(self, nome_som, volume_extra=1.0):
        """Toca qualquer som com o volume atual configurado"""
        if nome_som in self.sons:
            # Calcula volume final
            if self.mute:
                volume_final = 0.0
            else:
                volume_final = self.volume_geral * volume_extra
            
            # Aplica volume e toca
            som = self.sons[nome_som]
            som.set_volume(volume_final)
            som.play()
            return True
        return False
    
    def carregar_sons(self):
        """Carrega todos os sons do jogo"""

        self.sons['buzina'] = pygame.mixer.Sound("sons/buzina.wav")
        self.sons['colisao'] = pygame.mixer.Sound("sons/colisao.wav")
        self.sons['motor'] = pygame.mixer.Sound("sons/motor.wav")
        self.sons['semáforo'] = pygame.mixer.Sound("sons/bip.wav")
        self.sons['ambiente'] = pygame.mixer.Sound("sons/ambiente.mp3")

    def tocar_colisao(self,volume=0.1):
        """Toca som de colisão"""
        if 'colisao' in self.sons:
            # Aplica volume atual ANTES de tocar
            self.sons['colisao'].set_volume(0.0 if self.mute else self.volume_geral*volume)
            self.sons['colisao'].play()
    
    def tocar_buzina(self,volume=0.08):
        """Toca som de buzina"""
        if 'buzina' in self.sons:
            # Aplica volume atual ANTES de tocar
            self.sons['buzina'].set_volume(0.0 if self.mute else self.volume_geral * volume)
            self.sons['buzina'].play()
    
    def iniciar_musica_ambiente(self, volume=1):
        """Inicia música de fundo"""
        # Aplica volume (considera mute e volume_geral)
        if 'ambiente' in self.sons:
            # Aplica volume atual ANTES de tocar
            self.sons['ambiente'].set_volume(0.0 if self.mute else self.volume_geral * volume)
            self.sons['ambiente'].play(loops=-1) # Loop infinito

    # Funções de controle de volume
    def aumentar_volume(self, incremento=0.1):
        """Aumenta volume geral"""
        self.volume_geral = min(1.0, self.volume_geral + incremento)
        self.mute = False  # Sai do mute se aumentar volume
        self.atualizar_volume_geral()
        print(f"Volume: {int(self.volume_geral * 100)}%")
    
    def diminuir_volume(self, decremento=0.1):
        """Diminui volume geral"""
        self.volume_geral = max(0.0, self.volume_geral - decremento)
        self.atualizar_volume_geral()
        print(f"Volume: {int(self.volume_geral * 100)}%")
    
    def alternar_mute(self):
        """Liga/desliga mute"""
        self.mute = not self.mute
        if self.mute:
            self.volume_antes_mute = self.volume_geral
            print("Mute: ON")
        else:
            self.volume_geral = self.volume_antes_mute
            print("Mute: OFF")
        self.atualizar_volume_geral()

    def atualizar_volume_geral(self):
        """Atualiza volume de todos os sons baseado em volume_geral e mute"""
        if self.mute:
            volume_atual = 0.0
        else:
            volume_atual = self.volume_geral
        
        # Aplica a todos os sons
        for nome, som in self.sons.items():
            try:
                som.set_volume(volume_atual)
            except:
                pass  # Ignora erros
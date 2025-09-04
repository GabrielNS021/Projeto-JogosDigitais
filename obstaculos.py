import pygame
from pygame.locals import *
import random
from tela import *
import time
from player import *
from pygame.mask import from_surface

class Barreira(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super(Barreira, self).__init__()
        self.all_sprites = all_sprites
        self.largura_original = 201
        self.altura_original = 15
        self.num_partes = 3

        self.image_original = pygame.image.load('imgs/Barreira.png')
        self.image_original = pygame.transform.scale(self.image_original, (self.largura_original, self.altura_original))

        self.temp_image = self.image_original.copy()
        self.parte_largura = self.largura_original // self.num_partes
        espaco_vazio = random.randint(0, self.num_partes - 1)

        for i in range(self.num_partes):
            if i == espaco_vazio:
                pygame.draw.rect(self.temp_image, (0, 0, 0, 0), (i * self.parte_largura, 0, self.parte_largura, self.altura_original))

        self.image = self.temp_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 4))
        self.mask = from_surface(self.image)
        self.speed = VELOCIDADE - 7
        self.escala_maxima = 8
        self.passed = False
        self.colidiu = False

    def update(self):
        self.rect.y += self.speed
        distancia_inicial = SCREEN_HEIGHT // 2
        distancia_final = SCREEN_HEIGHT - self.altura_original
        distancia_atual = max(0, distancia_final - self.rect.y)

        fator_escala = max(1, 1 + ((self.escala_maxima - 1) * (1 - distancia_atual / distancia_inicial)))
        nova_largura = int(self.largura_original * fator_escala)
        nova_altura = int(self.altura_original * fator_escala)

        self.image = pygame.transform.scale(self.temp_image, (nova_largura, nova_altura))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = from_surface(self.image)

        if not self.passed and self.rect.top > SCREEN_HEIGHT:
            self.passed = True
            if not self.colidiu:
                for sprite in self.all_sprites:
                    if isinstance(sprite, Player):
                        sprite.increase_score(10)

        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                if self.rect.bottom >= sprite.rect.bottom:
                    if pygame.sprite.collide_mask(self, sprite):
                        sprite.decrease_life()
                        self.colidiu = True
                        break

        if self.rect.top > SCREEN_HEIGHT + 50:
            self.kill()

class Rampa(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super(Rampa, self).__init__()
        self.all_sprites = all_sprites
        self.largura_original = 253
        self.altura_original = 50
        self.image_original = pygame.image.load('imgs/Rampa.png')
        self.image_original = pygame.transform.scale(self.image_original, (self.largura_original, self.altura_original))

        self.image = self.image_original
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 4))
        self.mask = from_surface(self.image)
        self.speed = VELOCIDADE - 7
        self.escala_maxima = 6
        self.passed = False
        self.colidiu = False

    def update(self):
        self.rect.y += self.speed
        distancia_inicial = SCREEN_HEIGHT // 2
        distancia_final = SCREEN_HEIGHT - self.altura_original
        distancia_atual = max(0, distancia_final - self.rect.y)

        fator_escala = max(1, 1 + ((self.escala_maxima - 1) * (1 - distancia_atual / distancia_inicial)))
        nova_largura = int(self.largura_original * fator_escala)
        nova_altura = int(self.altura_original * fator_escala)

        self.image = pygame.transform.scale(self.image_original, (nova_largura, nova_altura))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = from_surface(self.image)

        if not self.passed and self.rect.top > SCREEN_HEIGHT:
            self.passed = True
            if not self.colidiu:
                for sprite in self.all_sprites:
                    if isinstance(sprite, Player):
                        sprite.increase_score(10)

        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                if self.rect.bottom >= sprite.rect.bottom:
                    if pygame.sprite.collide_mask(self, sprite):
                        keys = pygame.key.get_pressed()
                        if not (keys[K_s] or keys[K_DOWN]):
                            if not self.colidiu:
                                sprite.decrease_life()
                                self.colidiu = True
                                break

        if self.rect.top > SCREEN_HEIGHT + 50:
            self.kill()


class Semaforo(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Semaforo, self).__init__()
        self.screen = screen
        self.imagem_amarelo = pygame.image.load('imgs/semaforo_amarelo.png')
        self.imagem_verde = pygame.image.load('imgs/semaforo_verde.png')
        self.image = self.imagem_amarelo
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.start_time = time.time()
        self.reaction_time = None
        self.current_color = "yellow"
        self.key_pressed = False
        self.visible = True

    def update(self):
        current_time = time.time()
        if self.current_color == "yellow" and current_time - self.start_time >= 2:
            self.current_color = "green"
            self.image = self.imagem_verde
            self.green_start_time = current_time
            self.key_pressed = False
            self.visible = True

        if not self.visible:
            self.kill()

    def handle_key_press(self, event, player):
        if not self.key_pressed and self.current_color == "green" and event.type == KEYDOWN:
            if event.key in (K_w, K_UP):
                self.reaction_time = time.time() - self.green_start_time
                self.key_pressed = True
                self.visible = False
                player.adicionar_tempo_semaforo(self.reaction_time)

    def draw(self):
        if self.visible:
            self.screen.blit(self.image, self.rect)
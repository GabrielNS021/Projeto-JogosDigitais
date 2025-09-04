import pygame
from pygame.locals import *
from tela import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.largura = 70
        self.altura = 200

        self.image_normal = pygame.image.load('imgs/PNormal.png')
        self.image_normal = pygame.transform.scale(self.image_normal, (self.largura, self.altura))
        self.image_left = pygame.image.load('imgs/PLeft.png')
        self.image_left = pygame.transform.scale(self.image_left, (self.largura, self.altura))
        self.image_right = pygame.image.load('imgs/PRight.png')
        self.image_right = pygame.transform.scale(self.image_right, (self.largura, self.altura))

        self.image = self.image_normal

        self.rect = self.image.get_rect()
        self.speed = VELOCIDADE

        self.rect.x = SCREEN_WIDTH // 2 - self.largura // 2
        self.rect.y = SCREEN_HEIGHT - self.altura - 3

        self.lives = 3
        self.invincible = False
        self.invincible_start_time = 0
        self.invincible_duration = 2500
        self.pontos = 0
        self.tempos_semaforo = []

    def update(self):
        keys = pygame.key.get_pressed()

        self.rect.y = SCREEN_HEIGHT - self.altura - 3 

        if keys[K_LEFT] or keys[K_a]:
            self.rect.x -= self.speed
            self.image = self.image_left
        elif keys[K_RIGHT] or keys[K_d]:
            self.rect.x += self.speed
            self.image = self.image_right
        else:
            self.image = self.image_normal

        if self.rect.x < 0: 
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - self.largura:
            self.rect.x = SCREEN_WIDTH - self.largura

        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_start_time > self.invincible_duration:
                self.invincible = False
                self.image.set_alpha(255)
            else:
                if (current_time // 100) % 2 == 0:
                    self.image.set_alpha(128)
                else:
                    self.image.set_alpha(255)

    def decrease_life(self):
        if not self.invincible:
            if self.lives > 0:
                self.lives -= 1
                self.invincible = True
                self.invincible_start_time = pygame.time.get_ticks()

    def increase_score(self, points):
        self.pontos += points

    def adicionar_tempo_semaforo(self, tempo):
        self.tempos_semaforo.append(tempo)
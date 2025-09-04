import pygame
from pygame.locals import *

NOME_JOGO = 'TEA Game Skate'
VELOCIDADE = 10

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(NOME_JOGO)

class Base:
    def __init__(self, screen, background_image_path):
        self.screen = screen
        self.running = True
        self.background_image = pygame.image.load(background_image_path)
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw_background(self):
        self.screen.blit(self.background_image, (0, 0))
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw_background()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

    def update(self):
        pass

class Dia(Base):
    def __init__(self, screen):
        super().__init__(screen, 'imgs/Dia.png')

class Tarde(Base):
    def __init__(self, screen):
        super().__init__(screen, 'imgs/Tarde.png')

class Noite(Base):
    def __init__(self, screen):
        super().__init__(screen, 'imgs/Noite.png')

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('agency fb', 60, bold=True)
        self.options = ["Jogar", "Sair"]
        self.running = True
        self.background_image = pygame.image.load('imgs/fundoMenu.png')
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        self.option_rects = []

        for index, option in enumerate(self.options):
            text = self.font.render(option, True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH/2, (SCREEN_HEIGHT/2) + index * 200))
            box_rect = pygame.Rect(
                text_rect.left - 20,
                text_rect.top - 10,
                text_rect.width + 40,
                text_rect.height + 20
            )
            pygame.draw.rect(self.screen, (178, 102, 255), box_rect)

            if box_rect.collidepoint(mouse_pos):
                text_color = (0, 0, 0)
            else:
                text_color = (255, 255, 255)

            text = self.font.render(option, True, text_color)
            self.screen.blit(text, text_rect)
            self.option_rects.append(box_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.draw()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        for index, rect in enumerate(self.option_rects):
                            if rect.collidepoint(mouse_pos):
                                if index == 0:
                                    return "play"
                                elif index == 1:
                                    return "exit"

class Pause:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('agency fb', 60, bold=True)
        self.options = ["Continuar", "Reiniciar", "Menu", "Sair"]
        self.running = True
        self.background_color = (255, 255, 255)

    def draw(self):
        self.screen.fill(self.background_color)
        mouse_pos = pygame.mouse.get_pos()
        self.option_rects = []

        for index, option in enumerate(self.options):
            text = self.font.render(option, True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH/2, (SCREEN_HEIGHT/3) + index * 100))
            box_rect = pygame.Rect(
                text_rect.left - 20,
                text_rect.top - 10,
                text_rect.width + 40,
                text_rect.height + 20
            )
            pygame.draw.rect(self.screen, (178, 102, 255), box_rect)

            if box_rect.collidepoint(mouse_pos):
                text_color = (0, 0, 0)
            else:
                text_color = (255, 255, 255)

            text = self.font.render(option, True, text_color)
            self.screen.blit(text, text_rect)
            self.option_rects.append(box_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.draw()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    return "exit"

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return "continue"

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        for index, rect in enumerate(self.option_rects):
                            if rect.collidepoint(mouse_pos):
                                if index == 0:
                                    return "continue"
                                elif index == 1:
                                    return "restart"
                                elif index == 2:
                                    return "menu"
                                elif index == 3:
                                    return "quit"
                                
class HUD:
    def __init__(self, screen, player):
        self.screen = screen
        self.font = pygame.font.SysFont('agency fb', 40, bold=True)
        self.player = player

        self.hud_background = pygame.image.load('imgs/hud_background.png')
        self.hud_background = pygame.transform.scale(self.hud_background, (250, 150))

    def draw(self):
        hud_x = SCREEN_WIDTH - self.hud_background.get_width() - 20
        hud_y = 20

        self.screen.blit(self.hud_background, (hud_x, hud_y))

        score_text = self.font.render(f"Pontos: {self.player.pontos}", True, (255, 255, 255))
        score_rect = score_text.get_rect(topleft=(hud_x + 20, hud_y + 20))
        self.screen.blit(score_text, score_rect)

        lives_text = self.font.render(f"Vidas: {self.player.lives}", True, (255, 0, 0))
        lives_rect = lives_text.get_rect(topleft=(hud_x + 20, hud_y + 75))
        self.screen.blit(lives_text, lives_rect)

def calcada_rua(screen, frame_count):
    horizontal = SCREEN_HEIGHT * 2 // 4
    rua_final = SCREEN_WIDTH // 6

    cima_esquerda = (SCREEN_WIDTH // 2 - rua_final // 2, horizontal)
    cima_direita = (SCREEN_WIDTH // 2 + rua_final // 2, horizontal)
    baixo_esquerda = (0, SCREEN_HEIGHT)
    baixo_direita = (SCREEN_WIDTH, SCREEN_HEIGHT)

    cor_calcada = (130, 130, 130)

    pygame.draw.rect(screen, cor_calcada, (0, horizontal, SCREEN_WIDTH // 2 - rua_final // 2, SCREEN_HEIGHT - horizontal))
    pygame.draw.rect(screen, cor_calcada, (SCREEN_WIDTH // 2 + rua_final // 2, horizontal, SCREEN_WIDTH // 2, SCREEN_HEIGHT - horizontal))

    pygame.draw.polygon(screen, (50, 50, 50), [baixo_esquerda, baixo_direita, cima_direita, cima_esquerda])

    cor_linha = (255, 255, 255)
    linha_tamanho = 70
    linha_espacamento = 80
    linha_total = linha_tamanho + linha_espacamento

    linha_x = SCREEN_WIDTH // 2
    comeco_y = 20 - horizontal + (frame_count % linha_total)

    for y in range(comeco_y, SCREEN_HEIGHT, linha_total):
        pygame.draw.line(screen, cor_linha, (linha_x, y), (linha_x, y + linha_tamanho), 10)

class Game_Over:
    def __init__(self, screen, pontos_totais, tempos_semaforo):
        self.screen = screen
        self.pontos_totais = pontos_totais
        self.tempos_semaforo = tempos_semaforo
        self.fonte = pygame.font.SysFont('agency fb', 60, bold=True)

        self.background_image = pygame.image.load('imgs/Game_Over.png')
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))

        self.calcular_tempos()
        self.running = True

    def calcular_tempos(self):
        if self.tempos_semaforo:
            self.menor_tempo = min(self.tempos_semaforo)
            self.maior_tempo = max(self.tempos_semaforo)
            self.tempo_medio = sum(self.tempos_semaforo) / len(self.tempos_semaforo)
        else:
            self.menor_tempo = 0.0
            self.maior_tempo = 0.0
            self.tempo_medio = 0.0

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        rendered_text = self.fonte.render(text, True, color)
        text_rect = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.screen.blit(rendered_text, text_rect)

    def draw_button(self, text, rect, color=(178, 102, 255), text_color=(255, 255, 255), hover_color=(0, 0, 0)):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)

        pygame.draw.rect(self.screen, color, rect)
        button_text_color = hover_color if is_hovered else text_color
        button_text = self.fonte.render(text, True, button_text_color)
        text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, text_rect)

    def run(self):
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 150, 200, 60)

        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        return "menu"

            self.screen.blit(self.background_image, (0, 0))

            self.draw_text(f"Pontuação Total: {self.pontos_totais}", SCREEN_HEIGHT // 2 - 100, SCREEN_HEIGHT // 2 - 100)
            self.draw_text(f"Menor Tempo: {self.menor_tempo:.2f}s", SCREEN_HEIGHT // 2 - 50, SCREEN_HEIGHT // 2 - 50)
            self.draw_text(f"Maior Tempo: {self.maior_tempo:.2f}s", SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2)
            self.draw_text(f"Tempo Médio: {self.tempo_medio:.2f}s", SCREEN_HEIGHT // 2 + 50, SCREEN_HEIGHT // 2 + 50)

            self.draw_button("Menu", button_rect)

            pygame.display.flip()

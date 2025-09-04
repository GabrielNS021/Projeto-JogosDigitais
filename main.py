import pygame
from pygame.locals import *
from obstaculos import *
from player import *
from tela import *
import random

pygame.init()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    menu = Menu(screen)
    game_running = True
    frame_count = 0

    while game_running:
        opcao_menu = menu.run()

        if opcao_menu == "play":
            def iniciar_jogo():
                all_sprites = pygame.sprite.Group()
                player = Player()
                all_sprites.add(player)

                imagem_fundo_jogo = pygame.image.load('imgs/Dia.png')
                imagem_fundo_jogo = pygame.transform.scale(imagem_fundo_jogo, (SCREEN_WIDTH, SCREEN_HEIGHT * 2 // 4))

                hud = HUD(screen, player)

                return all_sprites, player, imagem_fundo_jogo, hud

            all_sprites, player, imagem_fundo_jogo, hud = iniciar_jogo()

            pause = False
            clock = pygame.time.Clock()
            running = True

            while running:
                frame_count += 2

                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                        game_running = False
                        break

                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pause = True
                        for sprite in all_sprites:
                            if isinstance(sprite, Semaforo):
                                sprite.handle_key_press(event, player)

                if pause:
                    pause_menu = Pause(screen)
                    opcao_pause = pause_menu.run()

                    if opcao_pause == "continue":
                        pause = False
                    elif opcao_pause == "restart":
                        all_sprites, player, imagem_fundo_jogo, hud = iniciar_jogo()
                        pause = False
                    elif opcao_pause == "menu":
                        running = False
                        break
                    elif opcao_pause == "quit":
                        running = False
                        game_running = False
                        break

                if not pause:
                    if frame_count % 120 == 0:
                        obstaculo_presente = any(isinstance(sprite, (Barreira, Rampa, Semaforo)) and sprite.rect.top < SCREEN_HEIGHT for sprite in all_sprites)

                        if not obstaculo_presente:
                            if player.pontos < 100:
                                barreira = Barreira(all_sprites)
                                all_sprites.add(barreira)

                            elif 100 <= player.pontos < 200:
                                if random.random() < 0.5:
                                    barreira = Barreira(all_sprites)
                                    all_sprites.add(barreira)
                                else:
                                    rampa = Rampa(all_sprites)
                                    all_sprites.add(rampa)

                            elif player.pontos >= 200:
                                rand_value = random.random()
                                if rand_value < 0.35:
                                    barreira = Barreira(all_sprites)
                                    all_sprites.add(barreira)
                                elif rand_value < 0.7:
                                    rampa = Rampa(all_sprites)
                                    all_sprites.add(rampa)
                                else:
                                    semaforo = Semaforo(screen)
                                    all_sprites.add(semaforo)

                    all_sprites.update()

                    screen.fill((255, 255, 255))

                    calcada_rua(screen, frame_count)

                    screen.blit(imagem_fundo_jogo, (0, 0))

                    if player.pontos >= 200:
                        imagem_fundo_jogo = pygame.image.load('imgs/Noite.png')
                        imagem_fundo_jogo = pygame.transform.scale(imagem_fundo_jogo, (SCREEN_WIDTH, SCREEN_HEIGHT * 2 // 4))
                    elif player.pontos >= 100:
                        imagem_fundo_jogo = pygame.image.load('imgs/Tarde.png')
                        imagem_fundo_jogo = pygame.transform.scale(imagem_fundo_jogo, (SCREEN_WIDTH, SCREEN_HEIGHT * 2 // 4))

                    all_sprites.draw(screen)

                    screen.blit(player.image, player.rect)

                    hud.draw()

                    pygame.display.flip()
                    clock.tick(60)
                
                if player.lives <= 0:
                    game_over_screen = Game_Over(screen, player.pontos, player.tempos_semaforo)
                    opcao_game_over = game_over_screen.run()
                    if opcao_game_over == "menu":
                        running = False

        elif opcao_menu == "exit":
            game_running = False

    pygame.quit()

if __name__ == "__main__":
    main()

import pygame.draw


from functions import *


def render_splash_screen(screen, engine_screen_width, engine_screen_height):
    screen.fill(BLACK)

    title_font = pygame.font.SysFont("monospace", 100, bold=True)
    title = 'Gravity Sim v2'
    text_width, text_height = title_font.size(title)
    screen.blit(title_font.render(title,
                                  True,
                                  WHITE),
                (engine_screen_width // 2 - text_width // 2, text_height - 10))

    # should fade in or something
    credits_font = pygame.font.SysFont("monospace", 50)
    title = 'By Lucas Peliciari'
    text_width, text_height = credits_font.size(title)
    screen.blit(credits_font.render(title,
                                    True,
                                    WHITE),
                (engine_screen_width // 2 - text_width // 2, 5 * text_height - 10))

    font = pygame.font.SysFont("monospace", 25)
    text = 'Press any key to continue'
    text_width, text_height = font.size(text)
    screen.blit(font.render(text, True, WHITE),
                (engine_screen_width // 2 - text_width // 2, engine_screen_height - 2 * text_height - 10)) # 10 is arbitrary vertical offset

    text = 'Press F1 during simulation for help'
    text_width, text_height = font.size(text)
    screen.blit(font.render(text, True, WHITE),
                (engine_screen_width // 2 - text_width // 2, engine_screen_height - text_height - 10)) # 10 is arbitrary vertical offset

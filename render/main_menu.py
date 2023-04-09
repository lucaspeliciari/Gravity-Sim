import pygame.draw


from functions import *


def render_main_menu(screen, engine_screen_width, engine_screen_height):
    screen.fill(BLACK)

    title_font = pygame.font.SysFont("monospace", 100, bold=True)
    title = 'Gravity Sim v2'
    text_width, text_height = title_font.size(title)
    screen.blit(title_font.render(title,
                                  True,
                                  WHITE),
                (engine_screen_width // 2 - text_width // 2, text_height - 10))

    font = pygame.font.SysFont("monospace", 25)
    text = 'Press any key to continue'
    text_width, text_height = font.size(text)
    screen.blit(font.render(text, True, WHITE),
                (engine_screen_width // 2 - text_width // 2, engine_screen_height - 2 * text_height - 10))  # 10 is arbitrary vertical offset

    texts_left = [f'Start simulation',
                  f'Load simulation',
                  f'Options',
                  f'Credits',
                  f'Quit',
                  ]

    for i, text in enumerate(texts_left):
        text_width, text_height = font.size(text)
        screen.blit(font.render(text, True, WHITE), (10, engine_screen_height - (i + 1) * text_height))

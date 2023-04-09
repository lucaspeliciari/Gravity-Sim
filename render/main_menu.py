import pygame.draw

from functions import *


def render_main_menu(screen, engine_screen_width, engine_screen_height, option_index):
    screen.fill(BLACK)

    title_font = pygame.font.SysFont("monospace", 100, bold=True)
    title = 'Gravity Sim v2'
    text_width, text_height = title_font.size(title)
    screen.blit(title_font.render(title,
                                  True,
                                  WHITE),
                (engine_screen_width // 2 - text_width // 2, text_height - 10))

    font = pygame.font.SysFont("monospace", 25)

    # main_menu_texts = [
    #     f'Quit',
    #     f'Credits',
    #     f'Options',
    #     f'Load simulation',
    #     f'Start simulation',
    # ]
    MARGIN = 3

    for i, text in enumerate(MAIN_MENU_OPTIONS):
        text_width, text_height = font.size(text)

        if i == option_index:
            pygame.draw.rect(screen,
                             WHITE,
                             (engine_screen_width // 2 - text_width // 2 - MARGIN,
                              engine_screen_height // 2 - (i + 1) * text_height,
                              text_width + MARGIN * 2,
                              text_height),
                             1)

        screen.blit(font.render(text, True, WHITE), (engine_screen_width // 2 - text_width // 2, engine_screen_height // 2 - (i + 1) * text_height))

    text = 'BETA 0.1'
    text_width, text_height = font.size(text)
    screen.blit(font.render(text, True, WHITE), (0, engine_screen_height - text_height))

    text = 'Press F1 during simulation for help'
    text_width, text_height = font.size(text)
    screen.blit(font.render(text, True, WHITE),
                (engine_screen_width // 2 - text_width // 2, engine_screen_height - text_height - 10))  # 10 is arbitrary vertical offset

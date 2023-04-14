import pygame.draw

from functions import *


def render_main_menu(screen, engine_screen_width, engine_screen_height, option_index, template_index, template_name, save_name, recording_name):
    screen.fill(BLACK)

    title_font = pygame.font.SysFont("monospace", 100, bold=True)
    title = 'Gravity Sim v2'
    text_width, text_height = title_font.size(title)
    screen.blit(title_font.render(title,
                                  True,
                                  WHITE),
                (engine_screen_width // 2 - text_width // 2, text_height - 10))

    font = pygame.font.SysFont("monospace", 25)

    MARGIN = 3

    for i, text in enumerate(MAIN_MENU_OPTIONS):
        text_width, text_height = font.size(text)

        # if text == 'Start simulation':
        # if MAIN_MENU_OPTIONS[i] == 'Start simulation' or MAIN_MENU_OPTIONS[i] == 'Start recording':
        #     text += f': {template_name}'

        if i == option_index:
            pygame.draw.rect(screen,
                             WHITE,
                             (engine_screen_width // 2 - text_width // 2 - MARGIN,
                              engine_screen_height // 2 - (i + 1) * text_height,
                              text_width + MARGIN * 2,
                              text_height),
                             1)

            if MAIN_MENU_OPTIONS[i] == 'Start simulation' or MAIN_MENU_OPTIONS[i] == 'Start recording':
                text += f' {template_name}'

            elif MAIN_MENU_OPTIONS[i] == 'Load simulation':
                text += f' {save_name}'

            elif MAIN_MENU_OPTIONS[i] == 'Load recording':
                text += f' {recording_name}'

        screen.blit(font.render(text, True, WHITE), (engine_screen_width // 2 - text_width // 2, engine_screen_height // 2 - (i + 1) * text_height))

    text = 'BETA 0.1'
    text_width, text_height = font.size(text)
    screen.blit(font.render(text, True, WHITE), (0, engine_screen_height - text_height))

    explanation_texts = [
        'Press left / right or A / D to select template for new simulation',
        'Press enter to select highlighted option',
        'Press up / down or W / A to highlight option',
    ]
    for i, text in enumerate(explanation_texts):
        text_width, text_height = font.size(text)
        screen.blit(font.render(text, True, WHITE),
                    (engine_screen_width // 2 - text_width // 2, engine_screen_height - text_height - (i + 1) * text_height))

    text = 'Press F1 during simulation for help'
    text_width, text_height = font.size(text)
    screen.blit(font.render(text, True, WHITE),
                (engine_screen_width // 2 - text_width // 2, engine_screen_height - text_height))

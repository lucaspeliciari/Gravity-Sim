import pygame.draw

from constants import BLACK, WHITE
from file_handler import DEFAULT_SETTINGS


def render_options_menu(screen, font, screen_width, screen_height, option_index):
    screen.fill(BLACK)

    MARGIN = 3

    i = 0
    for option, value in DEFAULT_SETTINGS.items():
        print(option, value)
        text = f'{option}: {value}'
        text_width, text_height = font.size(text)

        if i == option_index:
            pygame.draw.rect(screen,
                             WHITE,
                             (screen_width // 2 - text_width // 2 - MARGIN,
                              screen_height // 2 - (i + 1) * text_height,
                              text_width + MARGIN * 2,
                              text_height),
                             1)

        screen.blit(font.render(text, True, WHITE), (screen_width // 2 - text_width // 2, screen_height // 2 - (i + 1) * text_height))

        i += 1

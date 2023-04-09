from file_handler import default_settings


def render_options_menu():
    for i, option, value in enumerate(default_settings.items()):
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
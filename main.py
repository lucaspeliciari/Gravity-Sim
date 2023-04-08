# GRAVITY SIM V2
# STARTED: 19/04/2022

import pygame

from constants import *
import event_handler
from engine import Engine
from file_handler import *
from game import Game
from prefabs.templates import templates
from simulation import Simulation


def main():
    pygame.init()
    pygame.display.set_caption('Gravity Sim v2')

    pygame.joystick.init()

    settings_check = check_settings()

    settings = read_settings()
    window_size = (settings['windowed_res_x'], settings['windowed_res_Y'])
    templates_index = settings['start_template_index']
    bg_stars_radius = (settings['bg_star_avg_radius'], settings['bg_star_radius_deviation'])
    body_trail_settings = (settings['trail_interval'], settings['max_trail_length'], settings['min_distance_to_trail'])

    sim = Simulation(templates, templates_index, bg_stars_radius, settings['autosave_on_exit'])  # , True
    engine = Engine(sim, window_size, settings['fullscreen'], body_trail_settings, settings['max_messages_in_log'])
    engine.set_octrees(sim)
    game = Game(state=REPLAY)

    if game.state == REPLAY:
        sim.is_recording = True

    game.sim = sim

    red_font_size = 17
    if settings_check == 1:
        engine.messenger.add('settings.json is missing', color=RED, message_time=10, font_size=red_font_size,
                             sticky=True)
        engine.messenger.add('Default settings restored', color=RED, message_time=10, font_size=red_font_size,
                             sticky=True)
        engine.messenger.add('', message_time=10, font_size=red_font_size, sticky=True)
    elif settings_check == 2:
        engine.messenger.add('settings.json is corrupted or has invalid values', color=RED, message_time=10,
                             font_size=red_font_size, sticky=True)
        engine.messenger.add('Default settings restored', color=RED, message_time=10, font_size=red_font_size,
                             sticky=True)
        engine.messenger.add('', message_time=10, font_size=red_font_size, sticky=True)

    if check_saves():
        engine.messenger.add('Save folder not found', color=RED, message_time=10, font_size=red_font_size, sticky=True)
        engine.messenger.add('Created a new folder', color=RED, message_time=10, font_size=red_font_size, sticky=True)
        engine.messenger.add('', color=RED, message_time=10, font_size=red_font_size, sticky=True)

    yellow_font_size = 25
    if settings['first_run']:
        engine.messenger.add('WELCOME!', 15, YELLOW, font_size=yellow_font_size, sticky=True)
        engine.messenger.add('Press F1 for help', 15, YELLOW, font_size=yellow_font_size, sticky=True)
        engine.messenger.add('Press F2 for credits (WiP)', 15, YELLOW, font_size=yellow_font_size, sticky=True)
        settings['first_run'] = 0
        save_settings(settings)
    elif settings['autoload_on_start']:
        load_universe('autosave.uni', sim, engine)

    # EVENTS
    pygame.time.set_timer(pygame.USEREVENT, 200)  # updates octrees every 200 milliseconds
    while game.running:
        events = pygame.event.get()
        mouse_position = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        event_handler.handle(events, mouse_position, keys, mouse_buttons, joysticks, game, sim, engine)

        if game.state == SPLASH_SCREEN:
            engine.tick(sim)
            engine.render_splash_screen()

        elif game.state == SIMULATION:
            engine.tick(sim)

            if not sim.paused:
                engine.calculate_physics(sim)

            engine.render_simulation(events, sim, mouse_buttons, mouse_position, game.help, game.credits)

        elif game.state == REPLAY:
            engine.tick(sim)

            if sim.is_recording:
                engine.calculate_physics(sim)
                engine.record_frame(sim)
            elif not sim.paused:
                engine.read_recording(sim)
                engine.render_simulation(events, sim, mouse_buttons, mouse_position, game.help, game.credits)

                if engine.recording_index == 1:
                    engine.messenger.add('Playing recording', 3)
                elif engine.recording_index == len(engine.recording):
                    game.state = SIMULATION
                    engine.messenger.add('Recording has ended, simulation mode is now active', 3)

        pygame.display.update()


if __name__ == '__main__':
    main()

import sys

import pygame.display
from pygame import constants as constant

from constants import MIN_SCREEN_WIDTH, MIN_SCREEN_HEIGHT, SIMULATION, SPLASH_SCREEN, MAIN_MENU, RECORDING, MAIN_MENU_OPTIONS, OPTIONS, CREDITS
from file_handler import *
from functions import mouse_hover


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————


def handle(events,
           mouse_position,
           keys,
           mouse_buttons,
           joysticks,
           game,
           sim,
           engine
           ):

    key_value = 1
    if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT] or (pygame.key.get_mods() & constant.KMOD_LSHIFT) or (
            pygame.key.get_mods() & constant.KMOD_RSHIFT):
        key_value = 100

    elif game.state == SIMULATION or game.state == RECORDING:
        keyboard_panning(keys, key_value, sim.camera.zoom_multiplier, sim)
        keyboard_rotation(keys, sim)
        keyboard_zoom(keys, key_value, sim)

        if keys[constant.K_KP_PLUS]:
            sim.timescale += key_value
        if keys[constant.K_KP_MINUS]:
            sim.timescale -= key_value

        # MOUSE
        if mouse_buttons[0]:
            mouse_panning(mouse_position, engine, sim, game)
        else:
            game.holding_lmb = False
            game.first_click_on_widget[0] = False

        if mouse_buttons[2]:
            mouse_rotation(mouse_position, engine, sim, game)
        else:
            game.holding_rmb = False
            game.first_click_on_widget[2] = False

    for event in events:
        if event.type == constant.USEREVENT:
            engine.root.update(sim.bodies)

        if event.type == constant.KEYDOWN:  # TODO clean up menu selection
            if event.key == constant.K_ESCAPE:
                if sim.save_on_exit:
                    save_universe('autosave.uni', sim, engine)
                    print('Autosaved')
                sys.exit('Quitting')
            if event.key == constant.K_f or (
                    (pygame.key.get_mods() & constant.KMOD_LALT) and event.key == constant.K_RETURN):
                if engine.screen_mode_flag == pygame.RESIZABLE:
                    pygame.display.set_mode((engine.native_screen_width, engine.native_screen_height),
                                            pygame.FULLSCREEN)
                    engine.screen_mode_flag = pygame.FULLSCREEN
                else:
                    pygame.display.set_mode((engine.window_screen_width, engine.window_screen_height), pygame.RESIZABLE)
                    engine.screen_mode_flag = pygame.RESIZABLE

        if game.state == SPLASH_SCREEN:
            if event.type == constant.KEYDOWN or event.type == constant.MOUSEBUTTONDOWN:  # TODO ends up pressing key to skip splash screen also in main menu, so pressing enter will immediately press 'Start simulation'
                game.state = MAIN_MENU
                engine.timer = 0

        if game.state == MAIN_MENU:
            if event.type == constant.KEYDOWN:

                if event.key == constant.K_w or event.key == constant.K_UP:
                    engine.option_index += 1
                    if engine.option_index > len(MAIN_MENU_OPTIONS) - 1:
                        engine.option_index = 0
                if event.key == constant.K_s or event.key == constant.K_DOWN:
                    engine.option_index -= 1
                    if engine.option_index < 0:
                        engine.option_index = len(MAIN_MENU_OPTIONS) - 1

                if event.key == constant.K_d or event.key == constant.K_RIGHT:
                    if MAIN_MENU_OPTIONS[engine.option_index] == f'Start simulation' or MAIN_MENU_OPTIONS[engine.option_index] == f'Start recording':
                        sim.template_index += 1
                        if sim.template_index > len(sim.templates) - 1:
                            sim.template_index = 0

                    elif MAIN_MENU_OPTIONS[engine.option_index] == f'Load simulation' or MAIN_MENU_OPTIONS[engine.option_index] == f'Load recording':
                        engine.save_index += 1
                        if engine.save_index > len(sim.templates) - 1:  # TODO get number of saves in folder and use that as max value
                            engine.save_index = 0

                if event.key == constant.K_a or event.key == constant.K_LEFT:
                    if MAIN_MENU_OPTIONS[engine.option_index] == f'Start simulation' or MAIN_MENU_OPTIONS[engine.option_index] == f'Start recording':
                        sim.template_index -= 1
                        if sim.template_index < 0:
                            sim.template_index = len(sim.templates) - 1

                    elif MAIN_MENU_OPTIONS[engine.option_index] == f'Load simulation' or MAIN_MENU_OPTIONS[engine.option_index] == f'Load recording':
                        engine.save_index -= 1
                        if engine.save_index < 0:
                            engine.save_index = len(sim.templates) - 1  # TODO get number of saves in folder and use that as max value

                if event.key == constant.K_RETURN:

                    if MAIN_MENU_OPTIONS[engine.option_index] == f'Start simulation':
                        game.state = SIMULATION
                        sim.read_template()
                        engine.reset_values()

                    if MAIN_MENU_OPTIONS[engine.option_index] == 'Load simulation':  # TODO make this load selected save slot instead of autosave
                        load_universe('autosave.uni', sim, engine)
                        game.state = SIMULATION

                    if MAIN_MENU_OPTIONS[engine.option_index] == 'Start recording':
                        game.state = RECORDING
                        sim.is_recording = True
                        sim.read_template()
                        engine.reset_values()

                    if MAIN_MENU_OPTIONS[engine.option_index] == 'Options':
                        game.state = OPTIONS

                    if MAIN_MENU_OPTIONS[engine.option_index] == 'Credits':
                        game.state = CREDITS

                    if MAIN_MENU_OPTIONS[engine.option_index] == 'Quit':
                        game.running = False

                    engine.timer = 0  # check if this line will cause unforeseen consequences
                    engine.option_index = 0

        elif game.state == SIMULATION:
            if event.type == constant.KEYDOWN:
                if event.key == constant.K_F1:
                    game.help = not game.help
                    game.credits = False

                if event.key == constant.K_F2:
                    game.credits = not game.credits
                    game.help = False

                if event.key == constant.K_PERIOD:
                    sim.focused_body_index += 1
                    if sim.focused_body_index > len(sim.bodies) - 1:
                        sim.focused_body_index = 0
                if event.key == constant.K_COMMA:
                    sim.focused_body_index -= 1
                    if sim.focused_body_index < 0:
                        sim.focused_body_index = len(sim.bodies) - 1

                if event.key == constant.K_SPACE:
                    sim.paused = not sim.paused

                if event.key == constant.K_f:
                    sim.follow_focused_body = not sim.follow_focused_body

                if event.key == constant.K_r:
                    sim.read_template()
                    engine.reset_values()

                if event.key == constant.K_y:
                    if sim.template_index < len(sim.templates) - 1:
                        sim.template_index += 1
                    else:
                        sim.template_index = 0
                    sim.read_template()
                    engine.reset_values()
                if event.key == constant.K_t:
                    if sim.template_index > 0:
                        sim.template_index -= 1
                    else:
                        sim.template_index = len(sim.templates) - 1
                    sim.read_template()
                    engine.reset_values()

                # load autosave
                if (pygame.key.get_mods() & constant.KMOD_LCTRL) and event.key == constant.K_l:
                    pickled_dict = load_universe('autosave.uni', sim, engine)

                # save slots
                slot_keys = (constant.K_1, constant.K_2, constant.K_3, constant.K_4, constant.K_5, constant.K_6,
                             constant.K_7, constant.K_8, constant.K_9)

                for i, slot_key in enumerate(slot_keys, start=1):
                    if (pygame.key.get_mods() & constant.KMOD_LCTRL) and event.key == slot_key:
                        save_universe(f'my_universe_{i}.uni', sim, engine)
                        engine.messenger.add(f'Universe has been saved in slot {i}', 3)

                    if not (pygame.key.get_mods() & constant.KMOD_LCTRL) and event.key == slot_key:
                        pickled_dict = load_universe(f'my_universe_{i}.uni', sim, engine, i)

            if event.type == constant.MOUSEBUTTONDOWN:
                select_planet(mouse_buttons, mouse_position, engine, sim)

            if event.type == constant.MOUSEMOTION:
                pass

            if event.type == constant.MOUSEWHEEL:
                sim.camera.change_zoom(event.y * key_value)

        elif game.state == RECORDING and not sim.is_recording:
            if event.type == constant.KEYDOWN:

                if event.key == constant.K_PERIOD:
                    sim.focused_body_index += 1
                    if sim.focused_body_index > len(sim.bodies) - 1:
                        sim.focused_body_index = 0
                if event.key == constant.K_COMMA:
                    sim.focused_body_index -= 1
                    if sim.focused_body_index < 0:
                        sim.focused_body_index = len(sim.bodies) - 1

                if event.key == constant.K_SPACE:
                    sim.paused = not sim.paused

                if event.key == constant.K_f:
                    sim.follow_focused_body = not sim.follow_focused_body

            if event.type == constant.MOUSEBUTTONDOWN:
                select_planet(mouse_buttons, mouse_position, engine, sim)

            if event.type == constant.MOUSEMOTION:
                pass

            if event.type == constant.MOUSEWHEEL:
                sim.camera.change_zoom(event.y * key_value)

        if event.type == constant.JOYAXISMOTION:
            print(
                f'X{joysticks[0].get_axis(0)}  Y{joysticks[0].get_axis(1)}   LT{joysticks[0].get_axis(4)}   RT{joysticks[0].get_axis(5)}')

        # SCREEN
        if event.type == constant.VIDEORESIZE:
            display_info = pygame.display.Info()
            width, height = display_info.current_w, display_info.current_h
            if width < MIN_SCREEN_WIDTH:
                width = MIN_SCREEN_WIDTH
            if height < MIN_SCREEN_HEIGHT:
                height = MIN_SCREEN_HEIGHT
            engine.screen = pygame.display.set_mode((width, height), engine.screen_mode_flag)

        # QUIT
        if event.type == constant.QUIT:
            quit()


def select_planet(mouse_buttons,
                  mouse_position,
                  engine,
                  sim
                  ):
    mouse_x, mouse_y = mouse_position
    clicked_on_body = False
    if (mouse_x > engine.left_tab.border_position) and (mouse_x < engine.right_tab.border_position) and not \
            engine.timescale_slider.hover(mouse_x, mouse_y) and not engine.buttons[0].hover(mouse_x, mouse_y):
        if mouse_buttons[0] or mouse_buttons[2]:
            for body in sim.bodies:
                if mouse_hover(engine.screen_width,
                               engine.screen_height,
                               body,
                               mouse_position,
                               sim.camera):
                    sim.focused_body_index = sim.bodies.index(body)
                    clicked_on_body = True
            if not clicked_on_body:
                sim.focused_body_index = -1


def mouse_on_widget(mouse_x,
                    mouse_y,
                    engine,
                    ):
    if (engine.left_tab.side == 'Left' and mouse_x > engine.left_tab.border_position) and \
            (engine.left_tab.side == 'Left' and mouse_x < engine.right_tab.border_position) and not \
            engine.timescale_slider.hover(mouse_x, mouse_y) and not engine.buttons[0].contains(mouse_x, mouse_y):
        return False
    else:
        return True


def mouse_panning(mouse_position,
                  engine,
                  sim,
                  game
                  ):
    mouse_x, mouse_y = mouse_position[0], mouse_position[1]
    if not mouse_on_widget(mouse_x, mouse_y, engine):
        if not game.first_click_on_widget[0]:  # do not pan if started to hold MB on top of a widget
            if not game.holding_lmb:
                game.holding_lmb = True
                game.mousedown_position = mouse_position
            else:
                x = (game.mousedown_position[0] - mouse_x) / sim.camera.zoom_multiplier
                y = (mouse_y - game.mousedown_position[1]) / sim.camera.zoom_multiplier
                sim.camera.pan(x, y)
                game.mousedown_position = mouse_position
    else:
        game.first_click_on_widget[0] = True


def mouse_rotation(mouse_position,
                   engine,
                   sim,
                   game
                   ):
    mouse_x, mouse_y = mouse_position[0], mouse_position[1]
    if not mouse_on_widget(mouse_x, mouse_y, engine):
        if not game.first_click_on_widget[2]:
            if not game.holding_rmb:
                game.holding_rmb = True
                game.mousedown_position = mouse_position
            else:
                x = (game.mousedown_position[0] - mouse_x) / sim.camera.zoom_multiplier
                y = (mouse_y - game.mousedown_position[1]) / sim.camera.zoom_multiplier
                sim.camera.rotate(y / 1000, x / 1000, 0)
                game.mousedown_position = mouse_position
    else:
        game.first_click_on_widget[2] = True


def keyboard_panning(keys, key_value, zoom_multiplier, sim):
    if keys[constant.K_w] and not (pygame.key.get_mods() & constant.KMOD_LCTRL):
        sim.camera.pan(0, 4 * key_value / zoom_multiplier)
    if keys[constant.K_s] and not (pygame.key.get_mods() & constant.KMOD_LCTRL):
        sim.camera.pan(0, -4 * key_value / zoom_multiplier)
    if keys[constant.K_d] and not (pygame.key.get_mods() & constant.KMOD_LCTRL):
        sim.camera.pan(4 * key_value / zoom_multiplier, 0)
    if keys[constant.K_a] and not (pygame.key.get_mods() & constant.KMOD_LCTRL):
        sim.camera.pan(-4 * key_value / zoom_multiplier, 0)


def keyboard_rotation(keys, sim):
    if keys[constant.K_KP0]:
        sim.camera.rotation_x = 0
        sim.camera.rotation_y = 0
        sim.camera.rotation_z = 0
        sim.camera.rotate(0, 0, 0)  # just to recalculate rotation matrices
    if keys[constant.K_KP_PERIOD]:
        sim.camera.x = 0
        sim.camera.y = 0
    if keys[constant.K_KP8] or keys[constant.K_UP]:
        sim.camera.rotate(3.14159 / 40, 0, 0)
    if keys[constant.K_KP2] or keys[constant.K_DOWN]:
        sim.camera.rotate(-3.14159 / 40, 0, 0)
    if keys[constant.K_KP6] or keys[constant.K_RIGHT]:
        sim.camera.rotate(0, 3.14159 / 40, 0)
    if keys[constant.K_KP4] or keys[constant.K_LEFT]:
        sim.camera.rotate(0, -3.14159 / 40, 0)
    if keys[constant.K_KP9]:
        sim.camera.rotate(0, 0, 3.14159 / 40)
    if keys[constant.K_KP7]:
        sim.camera.rotate(0, 0, -3.14159 / 40)


def keyboard_zoom(keys, key_value, sim):
    if keys[constant.K_e]:
        sim.camera.change_zoom(0.1 * key_value)
    if keys[constant.K_q]:
        sim.camera.change_zoom(-0.1 * key_value)

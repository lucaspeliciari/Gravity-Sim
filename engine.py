from copy import deepcopy
from math import copysign

import pygame.display
import pygame.draw
import pygame.font
import pygame.image
import pygame_widgets

from classes.barnes_hut.node import Cube
from classes.barnes_hut.node import Node
from classes.button import Button
from classes.messenger import Messenger
from classes.slider import Slider
from classes.tab import Tab
from classes.toggle import Toggle
from physics import *
from render.splash_screen import *
from render.trees import *
from render.universe import *


RECORDING_TIME = 5  # TODO put this variable somewhere else

class Engine:
    def __init__(self,
                 sim,
                 window_size: tuple,
                 fullscreen: int,
                 body_trail_settings: tuple,
                 max_messages_in_log: int
                 ):
        self.window_screen_width, self.window_screen_height = window_size[0], window_size[1]
        self.screen_width, self.screen_height = window_size[0], window_size[1]
        desktop_info = pygame.display.Info()
        self.native_screen_width, self.native_screen_height = desktop_info.current_w, desktop_info.current_h

        self.screen_mode_flag = pygame.RESIZABLE
        # if screen_mode = borderless:
        #     self.screen_mode_flag = pygame.NOFRAME
        if fullscreen:
            self.screen_mode_flag = pygame.FULLSCREEN
            # desktop_info = pygame.display.Info()
            self.screen_width, self.screen_height = self.native_screen_width, self.native_screen_height

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), self.screen_mode_flag)

        self.clock = pygame.time.Clock()
        self.timescale = sim.timescale
        self.physics_interval = PHYSICS_INTERVAL
        self.current_frame = 1
        self.radius_scale = sim.radius_scale  # RADIUS_SCALE
        self.timer = 0
        self.octree_update_interval = 0.5
        self.octree_update_timer = 0
        self.simulation_timer = 0

        self.scale = sim.scale  # SCALE

        self.font = pygame.font.SysFont("monospace", 15)
        self.large_font = pygame.font.SysFont("monospace", 50)

        self.left_tab = Tab(self.screen_width, side='Left')
        self.right_tab = Tab(self.screen_width, side='Right')
        self.tabs = [self.left_tab, self.right_tab]

        self.buttons = []
        self.toggles = []
        self.sliders = []

        self.__initialize_buttons(sim.focused_body_index, sim.self_functions)
        y = self.__initialize_toggles(sim.booleans)
        self.__initialize_sliders(y)

        # self.trail_length = max_trail_length
        self.trail_interval = body_trail_settings[0]
        self.trail_length = body_trail_settings[1]
        self.min_distance_to_trail = body_trail_settings[2]

        self.vector_scale = 1

        self.template_title_timer = TEMPLATE_TITLE_TIME_ON_SCREEN

        self.messenger = Messenger(max_messages_in_log)

        self.recording = []
        self.recording_index = 0

    def reset_values(self):
        self.timescale = 0
        self.timer = 0
        self.simulation_timer = 0
        self.current_frame = 0
        self.template_title_timer = TEMPLATE_TITLE_TIME_ON_SCREEN

    def __initialize_buttons(self, focused_body_index, sim_functions):
        # UI BUTTONS
        play_pause_width = play_pause_height = 50

        play_pause = Button(self.screen,
                            self.screen_width // 2,
                            self.screen_height - 25,  # 25 is timescale slider height (use a var, not just the number)
                            play_pause_width,
                            play_pause_height,
                            sim_functions[0]['toggle_pause'],
                            border_thickness=50,
                            )
        play_pause.lines = pause_bars
        play_pause.polygon = play_triangle

        # TAB BUTTONS
        button_x = 20
        button_y = TAB_BUTTON_Y_START
        add_body_button = Button(self.screen,
                                 button_x,
                                 button_y,
                                 100,
                                 25,
                                 sim_functions[0]['add_random_body'],
                                 text='Add random planet')
        add_body_button.tab = self.left_tab
        button_y += TAB_BUTTON_SPACING  # use a for loop

        remove_body_button = Button(self.screen,
                                    button_x,
                                    button_y,
                                    100,
                                    25,
                                    lambda: sim_functions[0]['remove_body']([focused_body_index]),
                                    text='Remove planet')
        remove_body_button.tab = self.left_tab
        button_y += TAB_BUTTON_SPACING  # use a for loop

        self.buttons.append(play_pause)
        self.buttons.append(add_body_button)
        self.buttons.append(remove_body_button)

    def __initialize_toggles(self, booleans):
        # TAB TOGGLES
        y = TAB_BUTTON_Y_START + TAB_BUTTON_SPACING * 2 + TAB_BUTTON_TOGGLE_SPACING  # REALLY NEED A FOR LOOP
        # for text in toggle_booleans:
        for text in [x for x in booleans]:
            text_width, text_height = self.font.size(text)
            boolean = booleans[text]
            toggle = Toggle(self.screen, text_width + 15, y, 20, 15, tab=self.left_tab, start_on=boolean)
            self.toggles.append(toggle)
            y += TAB_TOGGLE_SPACING
        return y

    def __initialize_sliders(self, y):
        timescale_width, timescale_height = 120, 15
        timescale_slider_x = self.screen_width // 2
        timescale_slider_y = self.screen_height - 5
        self.timescale_slider = Slider(self.screen, timescale_slider_x, timescale_slider_y, timescale_width,
                                       timescale_height,
                                       min=-100, max=100, start_on=0, step=1,
                                       )  # no handle radius?
        self.timescale_slider.handleRadius = 10

        # TAB SLIDERS
        scale_slider = Slider(self.screen, 15, y, 120, 15, min=1000, max=10000000, start_on=1000000, tab=self.left_tab)
        self.sliders.append(scale_slider)
        y += TAB_TOGGLE_SPACING

        radius_scale_slider = Slider(self.screen, 15, y, 120, 15, min=80000, max=1000000, start_on=100000,
                                     tab=self.left_tab)
        self.sliders.append(radius_scale_slider)
        y += TAB_TOGGLE_SPACING

        trail_length_slider = Slider(self.screen, 15, y, 120, 15, min=10, max=5000, start_on=100, step=100,
                                     tab=self.left_tab)
        self.sliders.append(trail_length_slider)
        y += TAB_TOGGLE_SPACING

        vectors_scale_slider = Slider(self.screen, 15, y, 120, 15, min=1, max=100, start_on=100, step=1,
                                      tab=self.left_tab)
        self.sliders.append(vectors_scale_slider)
        y += TAB_TOGGLE_SPACING

    def get_current_tick(self):
        return pygame.time.get_ticks()

    def tick(self, sim):
        self.timescale = sim.timescale  # terrible but it works
        self.clock.tick(FRAMERATE)

        if not sim.paused:
            self.simulation_timer += (self.clock.get_time() / 1000) * self.timescale

        self.timer += self.clock.get_time() / 1000  # in seconds

        # self.octree_update_timer = (pygame.time.get_ticks() - self.start_timer)  # old timer, remove when below is working 100%
        self.octree_update_timer = self.timer  # new timer, test some more since it might break something

        self.current_frame += 1


        if sim.is_recording and self.timer > RECORDING_TIME:
            sim.is_recording = False
            print(RECORDING_TIME, 'seconds and', len(self.recording), 'frames recorded')

        self.resize_screen()  # should run only if resized window

    def render_splash_screen(self):  # maybe not the best name bc there's a splash_screen.py
        render_splash_screen(self.screen, self.screen_width, self.screen_height)

    def render_main_menu(self):
        render_main_menu(self.screen, self.screen_width)

    def __camera_follow(self, sim):
        # works if no rotation
        x, y = sim.bodies[sim.focused_body_index].x - (self.screen_width / 2), \
               sim.bodies[sim.focused_body_index].y - (self.screen_height / 2)

        # takes rotation into account, does not work, fix and delete above
        # x, y = sim.bodies[sim.focused_body_index].projected_data[0] - (self.screen_width / 2), \
        #        sim.bodies[sim.focused_body_index].projected_data[1] - (self.screen_height / 2)
        # print(f'X{sim.bodies[sim.focused_body_index].x}  PX{sim.bodies[sim.focused_body_index].projected_data[0]}')
        # print(f'Y{sim.bodies[sim.focused_body_index].y}  PY{sim.bodies[sim.focused_body_index].projected_data[1]}')

        sim.camera.x, sim.camera.y = x, -y

    def render_simulation(self, events, sim, mouse_buttons, mouse_position, help_menu, credits):  # render_universe?
        self.screen.fill(BLACK)

        if sim.follow_focused_body and sim.focused_body_index != -1:
            self.__camera_follow(sim)

        if sim.background_stars:
            draw_background_stars(self.screen, self.screen_width, self.screen_height, sim.bg_stars, sim.camera,
                                  self.timer)

        if sim.draw_grid:
            draw_grid(self.screen, self.screen_width, self.screen_height, sim.universe_boundary_size, sim.camera)

        # debug
        # draw_center_lines(self.screen, self.screen_width, self.screen_height)

        if sim.universe_boundary:
            draw_universe_boundaries(self.screen, self.screen_width, self.screen_height, sim.universe_boundary_size,
                                     sim.camera)
        if len(sim.bodies) > 0:
            # if sim.draw_trails:
            #     draw_trails(self.screen, self.screen_width, self.screen_height, sim.bodies, sim.camera)
            draw_bodies(self.screen, self.screen_width, self.screen_height, sim.bodies, sim.camera, self.radius_scale,
                        sim.draw_trails, sim.bodies_emit_light)
            if sim.draw_body_vectors:
                draw_body_vectors(self.screen, self.screen_width, self.screen_height, sim.bodies, sim.camera,
                                  self.vector_scale)
            if sim.draw_lines_between_bodies:
                draw_lines_between_bodies(self.screen, sim.bodies, sim.focused_body_index)
            if sim.show_data != 0:
                draw_body_data(self.screen, self.screen_width, self.screen_height, sim.bodies, sim.camera,
                               sim.show_data, mouse_position, self.font)

        if sim.draw_system_center_of_mass:
            draw_system_center_of_mass(self.screen, self.screen_width, self.screen_height, sim.system_center_of_mass,
                                       sim.camera)

        # draw_center_of_universe(self.screen, self.screen_width, self.screen_height, sim.camera)

        # experimental
        if sim.draw_octrees:
            draw_octrees(self.screen, self.screen_width, self.screen_height, self.root, sim.camera)
            draw_octo_center_of_mass(self.screen, self.screen_width, self.screen_height, self.root, sim.camera)

        draw_rosetta(self.screen, self.screen_width, self.screen_height, sim.camera)

        draw_ui(self.screen, mouse_position, sim, self)
        # self.messenger.update(self.screen, self.font, self.screen.get_size(), self.clock.get_time())
        self.messenger.update(self.screen, self.screen.get_size(), self.clock.get_time())

        if self.template_title_timer > 0:
            draw_template_title(self.screen, sim, self)
            self.template_title_timer -= self.clock.get_time() / 1000

        for tab in self.tabs:
            tab.update(self.screen, mouse_buttons, mouse_position, sim, self, help_menu)

        self.update_buttons(sim.paused)
        y = self.update_toggles(sim, help_menu)
        self.update_sliders(sim, help_menu, y)
        pygame_widgets.update(events)

        # DRAW BUTTON LINES / POLYGONS
        for button in self.buttons:  # shouldn't repeat
            button.draw_figures(self.screen, self.screen_width)

        if help_menu and not credits:
            draw_help_menu(self.screen, self.screen_width, self.screen_height)
        elif credits and not help_menu:
            draw_credits(self.screen, self.screen_width, self.screen_height)

    def read_recording(self, sim):
        sim.bodies = self.recording[self.recording_index]

        self.recording_index += 1

    def update_buttons(self, paused):
        for button in self.buttons:
            button.update(self.screen, self.screen_width, self.screen_height)

            # SWITCH BETWEEN PLAY / PAUSE ICONS
            if not paused:
                self.buttons[0].state = 1
            else:
                self.buttons[0].state = 2

    def update_toggles(self, sim, help_menu):
        y = TAB_BUTTON_Y_START + TAB_BUTTON_SPACING * 2 + TAB_BUTTON_TOGGLE_SPACING  # gotta clean this up
        for toggle, text in zip(self.toggles, sim.booleans):
            toggle.update(self.screen_width)
            if not help_menu and toggle.enabled:
                text_width, text_height = self.font.size(text)
                self.screen.blit(self.font.render(text, True, WHITE), (toggle.get('x') - text_width - 10, y))
                y += TAB_TOGGLE_SPACING
            # sim.booleans[text] = toggle.value  # does not work, fix

        # remove after making above work
        sim.collisions = self.toggles[0].value
        sim.draw_grid = self.toggles[1].value
        sim.draw_trails = self.toggles[2].value
        sim.draw_lines_between_bodies = self.toggles[3].value
        sim.universe_boundary = self.toggles[4].value
        sim.draw_system_center_of_mass = self.toggles[5].value
        sim.background_stars = self.toggles[6].value
        sim.bodies_emit_light = self.toggles[7].value
        sim.draw_octrees = self.toggles[8].value
        sim.calculate_system_energy = self.toggles[9].value
        sim.draw_body_vectors = self.toggles[10].value

        return y

    def update_sliders(self, sim, help_menu, y):
        # TIMESCALE
        if self.timescale_slider.selected:
            timescale_percentage = (self.timescale_slider.value + 100) / 200
            timescale_modifier = lerp(-10, 10, timescale_percentage)
            sim.timescale += timescale_modifier
        else:  # reset if not selected
            self.timescale_slider.value = 0

        # reposition slider when resizing screen, not efficient
        self.timescale_slider.update(self.screen_width, self.screen_height)

        # TABS
        for slider in self.sliders:
            slider.update(self.screen_width, self.screen_height)
            if not help_menu and slider.enabled:
                text = str(slider.value)
                text_width, text_height = self.font.size(text)
                self.screen.blit(self.font.render(text, True, WHITE),
                                 (slider.get('x') + slider.get('width') + 15, y - 1))
                y += TAB_TOGGLE_SPACING
        self.scale = self.sliders[0].value
        self.radius_scale = self.sliders[1].value
        self.trail_length = self.sliders[2].value
        self.vector_scale = self.sliders[3].value / PERCENT

    def calculate_physics(self, sim):
        for i in range(int(abs(self.timescale) / self.physics_interval)):
            update_acceleration(sim.bodies)
            update_velocity(sim.bodies, copysign(1, self.timescale) * self.physics_interval)
            update_position(sim.bodies,
                            copysign(1, self.timescale) * self.physics_interval,
                            self.trail_interval,
                            self.trail_length,
                            self.min_distance_to_trail)
            if sim.collisions:  # fix
                check_body_collision(sim, self.radius_scale)

            # causing major issues
            # if sim.boundary_collisions:
            #     check_boundaries(sim.bodies, self.radius_scale)

            if sim.calculate_system_energy:
                sim.kinetic_energy, sim.potential_energy, sim.system_energy = get_system_energy(sim.bodies)

        sim.get_system_center_of_mass()

    def record_frame(self, sim):
        self.recording.append(deepcopy(sim.bodies))
        draw_recording_message(self.screen, self, RECORDING_TIME)

    def set_octrees(self, sim):
        # try to center on universe boundary (it is currently a fourth the volume)
        origin, side = universe_boundary_side // 2, universe_boundary_side + 1  # +1 because it is not inclusive
        self.root = Node(Cube(-origin, -origin, -origin, side, side, side))
        for body in sim.bodies:
            self.root.insert(body)

    def resize_screen(self):  # should run only if resized window
        self.screen_width, self.screen_height = self.screen.get_size()
        for tab in self.tabs:
            tab.width = self.screen_width / 6

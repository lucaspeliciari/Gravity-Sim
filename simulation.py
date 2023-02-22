import pygame.mouse

from classes.body import Body
from classes.camera import Camera
from functions import random_body_data, body_data, random_background_stars, get_orbital_velocities
from vars import number_random_bodies, universe_boundary, bg_stars_per_layer, layers_bg_stars


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

class Simulation:
    def __init__(self,
                 templates,
                 templates_index,
                 bg_stars_radius: tuple,
                 save_on_exit: bool = True
                 ):
        self.running = True
        self.paused = False

        # PREFERENCES
        self.collisions = True
        self.orbit_first_body = False  # set velocity vectors in order to orbit self.bodies[0]
        self.follow_focused_body = True
        self.show_data = 1  # 0: never, 1: mouse hover, 2: always
        self.draw_trails = True
        self.draw_lines_between_bodies = False
        self.draw_grid = False
        self.universe_boundary = False
        self.boundary_collisions = False
        self.background_stars = True
        self.bodies_emit_light = True
        self.draw_system_center_of_mass = False
        self.draw_octrees = False
        self.calculate_system_energy = False  # far from ok but it works
        self.draw_body_vectors = False
        self.three_d_test = False

        self.universe_boundary_size = universe_boundary
        self.focused_body_index = -1  # -1: no body selected

        self.camera = Camera()

        self.bodies = []
        self.templates = templates
        self.template_index = templates_index

        self.system_center_of_mass = (0, 0)

        # bad way of doing this, engine reading sim reading template but had to centralize due to interface widgets
        # but find a way of fixing this anyway!
        self.timescale = 0.0
        self.scale = 0
        self.radius_scale = 0

        self.number_random_bodies = number_random_bodies
        self.read_template()

        self.booleans = {'Collisions': self.collisions,
                         'Grid': self.draw_grid,
                         'Trails': self.draw_trails,
                         'Lines': self.draw_lines_between_bodies,
                         'Boundary': self.universe_boundary,
                         'System\'s center of mass': self.draw_system_center_of_mass,
                         'Background stars': self.background_stars,
                         'Bodies emit light': self.bodies_emit_light,
                         'Draw octrees': self.draw_octrees,
                         'System energy': self.calculate_system_energy,
                         'Body vectors': self.draw_body_vectors
                         }

        self.self_functions = {0: {'toggle_pause': self.toggle_pause,  # on press
                                   'reverse_timescale': self.reverse_timescale,
                                   'add_random_body': self.add_random_body,
                                   'remove_body': self.remove_body,
                                   'toggle_collisions': self.toggle_collisions,
                                   'toggle_show_data': self.toggle_show_data,
                                   'toggle_trails': self.toggle_trails,
                                   'toggle_lines_between_bodies': self.toggle_lines_between_bodies,
                                   'toggle_grid': self.toggle_grid,
                                   'toggle_universe_boundary': self.toggle_universe_boundary,

                                   },
                               1: {'change_timescale': self.change_timescale},  # on hold
                               # 2: {'debug_print': self.debug_print}  # on release
                               }

        self.system_energy = 0.0
        self.kinetic_energy = 0.0
        self.potential_energy = 0.0

        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        self.bg_stars = random_background_stars(bg_stars_per_layer, layers_bg_stars, bg_stars_radius[0],
                                                bg_stars_radius[1])

        self.save_on_exit = save_on_exit

    def read_template(self):
        self.camera.reset()
        self.bodies.clear()
        self.templates[self.template_index].set_up_universe()

        self.timescale = self.templates[self.template_index].timescale
        self.scale = self.templates[self.template_index].scale
        self.radius_scale = self.templates[self.template_index].radius_scale
        self.bodies = self.templates[self.template_index].bodies.copy()

        self.collisions = self.templates[self.template_index].collisions
        for body in self.bodies:  # don't put overall disabled collisions per body like this
            body.can_collide = self.collisions
        self.can_move = self.templates[self.template_index].can_move  # pointless line, innit?
        for body in self.bodies:
            body.can_move = self.can_move
            body.influenced_by_gravity = self.templates[self.template_index].influenced_by_gravity
        self.orbit_first_body = self.templates[self.template_index].orbit_first_body  # remove this, use collision lists instead

        self.boundary_collisions = self.templates[self.template_index].boundary_collisions

        self.camera.x = self.templates[self.template_index].starting_camera_position[0]
        self.camera.y = self.templates[self.template_index].starting_camera_position[1]
        self.camera.zoom = self.templates[self.template_index].starting_camera_zoom
        self.camera.get_zoom_multiplier()

        for i in range(self.number_random_bodies):
            self.add_random_body()

        # quick fix: prevents creating a weird trail when changing / resetting template
        self.bodies[0].trail.clear()

        self.__set_orbits()

        self.focused_body_index = self.templates[self.template_index].focused_body_index

    def __set_orbits(self):
        if self.orbit_first_body:
            self.bodies[0].can_move = False
            self.bodies[0].x, self.bodies[0].y = 0, 0

            # finish this
            for i, body in enumerate(self.bodies):
                if len(body.circle_of_influence) > 0:
                    body.velocity_x, body.velocity_y, body.velocity_z = get_orbital_velocities(body)

    def get_system_center_of_mass(self):  # should this should return xyz instead of setting it?
        if len(self.bodies) <= 0:
            self.system_center_of_mass = (0, 0, 0)
            return False
        x = 0
        y = 0
        z = 0
        total_mass = 0
        for body in self.bodies:
            x += body.x * body.mass
            y += body.y * body.mass
            z += body.z * body.mass
            total_mass += body.mass
        x /= total_mass
        y /= total_mass
        z /= total_mass
        self.system_center_of_mass = (x, y, z)

    def add_random_body(self):
        # count number of already-added random bodies
        random_index = 1
        for body in self.bodies:
            if 'Unidentified' in body.name:
                random_index += 1

        random_body = Body(random_body_data(random_index))
        random_body.collisions_with_bodies = [0 for x in self.bodies]
        if self.orbit_first_body:
            random_body.circle_of_influence = [self.bodies[0]]
        else:
            random_body.circle_of_influence = [x for x in self.bodies]

        # add a new collision index for this new random body in pre-existing bodies
        for body in self.bodies:
            body.collisions_with_bodies.append(0)

        if self.orbit_first_body:
            random_body.velocity_x, random_body.velocity_y, random_body.velocity_z = get_orbital_velocities(random_body)

        self.bodies.append(random_body)

    def remove_body(self,  # don't forget to change circles_of_influence!
                    body_indices: list
                    ):
        for i in reversed(body_indices):
            if i != -1:
                print(f'{self.bodies[i].name} was destroyed!')
                del (self.bodies[i])

    # RETURN TEXT FOR TABS, messy, don't use this, not here at least
    def return_texts(self, side):
        to_return = []
        if self.focused_body_index != -1:
            if side == 'Right':
                to_return.append(body_data(self.bodies[self.focused_body_index]))
        else:
            if side == 'Right':
                to_return.append('      SYSTEM INFO')  # should center in tab
                for body in self.bodies:
                    to_return.append(body.name)
                if self.calculate_system_energy:
                    to_return.append('')  # no \n in text blit
                    to_return.append('Energy in zettajoules')
                    to_return.append(f' Kinetic: {self.kinetic_energy / pow(10, 21):.2E} ZJ')
                    to_return.append(f' Potential: {self.potential_energy / pow(10, 21):.2E} ZJ')
                    to_return.append(f' Total: {self.system_energy / pow(10, 21):.2E} ZJ')
                    to_return.append('DEBUG REMINDER: total should be close to 0')
        return to_return

    # find a way to reduce these fucntions
    def toggle_collisions(self):
        self.collisions = not self.collisions

    def toggle_universe_boundary(self):
        self.universe_boundary = not self.universe_boundary

    def toggle_show_data(self):
        self.show_data += 1
        if self.show_data > 2:
            self.show_data = 0

    def toggle_trails(self):
        self.draw_trails = not self.draw_trails

    def toggle_lines_between_bodies(self):
        self.draw_lines_between_bodies = not self.draw_lines_between_bodies

    def toggle_grid(self):
        self.draw_grid = not self.draw_grid

    def change_timescale(self, mouse_buttons):
        if mouse_buttons[0]:
            self.timescale -= 10
        if mouse_buttons[2]:
            self.timescale += 10

    def toggle_pause(self):
        self.paused = not self.paused

    def set_timescale(self, increment):  # use these set functions with sliders
        self.timescale += increment

    def set_scale(self, increment):
        self.scale += increment

    def set_radius_scale(self, increment):
        self.radius_scale += increment

    def reverse_timescale(self):
        self.timescale = -self.timescale
        for body in self.bodies:
            body.trail.clear()

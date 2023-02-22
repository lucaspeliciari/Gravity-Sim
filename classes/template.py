from classes.body import Body
from constants import SCALE, RADIUS_SCALE
from functions import random_body_data
from vars import screen_width, screen_height


class Template:
    def __init__(self,
                 body_data: list,
                 circles_of_influence: list = None,
                 timescale: int = 3600,
                 scale: int = SCALE,
                 radius_scale: int = RADIUS_SCALE,
                 starting_camera_position: tuple = (-int(screen_width / 2), int(screen_height / 2)),
                 starting_camera_zoom: int = 0,
                 collisions: bool = True,
                 influenced_by_gravity: bool = True,
                 boundary_collisions: bool = True,
                 orbit_first_body: bool = False,
                 can_move: bool = True,
                 number_random_bodies: int = 0,
                 focused_body_index: int = -1,
                 name: str = ''
                 ):
        self.name = name

        self.timescale = timescale
        self.scale = scale
        self.radius_scale = radius_scale

        self.body_data = body_data
        self.circles_of_influence = circles_of_influence

        self.collisions = collisions
        self.influenced_by_gravity = influenced_by_gravity
        self.boundary_collisions = boundary_collisions
        self.orbit_first_body = orbit_first_body
        self.can_move = can_move

        self.starting_camera_position = starting_camera_position
        self.starting_camera_zoom = starting_camera_zoom

        self.number_random_bodies = number_random_bodies

        self.focused_body_index = focused_body_index

        self.set_up_universe()

    def set_up_universe(self):
        body_objects = self.generate_bodies()
        self.generate_random_bodies(body_objects)
        self.generate_collision_lists(body_objects)
        self.generate_circles_of_influence()

    def generate_bodies(self):
        body_objects = []
        for data in self.body_data:
            # SET INITIAL VELOCITY
            vx = vy = vz = 0.0
            if len(data) > 7:
                vx = data[7]
                vy = data[8]
                vz = data[9]

            # SET LIGHT EMISSION
            light = False
            if len(data) > 10:
                light = data[10]

            body = Body(data, velocity_x=vx, velocity_y=vy, velocity_z=vz, emits_light=light)

            body.has_gravity = True

            body_objects.append(body)
        return body_objects

    def generate_random_bodies(self, body_objects):
        for i in range(self.number_random_bodies):
            data = random_body_data(i + 1)
            body = Body(data)
            body_objects.append(body)
        # return body_objects

    # these lists are used to only destroy body if there are x collisions in a row
    # avoids always destroying bodies when they touch
    # always destroying is more realistic, but elastic collisions are more fun
    # I will probably remove this (it's more trouble than it's worth)
    def generate_collision_lists(self, body_objects):
        self.bodies = body_objects
        for body in self.bodies:
            body.collisions_with_bodies = [0 for x in range(len(self.bodies))]

    # each body is only affected by the gravity of other bodies in its circle of influence
    def generate_circles_of_influence(self):
        if self.circles_of_influence is None:
            for body in self.bodies:
                body.circle_of_influence = [x for x in self.bodies if x != body]
        else:
            for body, circle in zip(self.bodies, self.circles_of_influence):
                if len(circle) == 0:
                    body.circle_of_influence = [x for x in self.bodies if x != body]
                elif circle[0] == -1:  # empty circle i.e. not affected by gravity at all
                    pass
                else:
                    for body_index in circle:
                        body.circle_of_influence.append(self.bodies[body_index])

    def __len__(self):
        return f'There are {len(self.bodies)} in this template'

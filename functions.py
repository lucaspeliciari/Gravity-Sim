from math import sqrt, atan2, sin, cos, radians
from random import randint, triangular, gauss

import numpy as np

from classes.bg_star import BgStar
from classes.body import Body
from classes.camera import Camera
from constants import *
from vars import universe_boundary_side


def components_to_vector(x, y, z):
    mod = sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2))
    angXY = atan2(x, y)
    angXZ = atan2(x, z)
    ang = angXY
    return mod, ang


def get_distances(body1: Body,
                  body2: Body,
                  scale_type: int = PIXELS,
                  scale: int = SCALE
                  ):
    if scale_type != PROJECTED:
        dx = body2.x - body1.x
        dy = body2.y - body1.y
        dz = body2.z - body1.z
        if scale_type == METERS:
            dx *= scale
            dy *= scale
            dz *= scale
    else:
        dx = body2.projected_position[0] - body1.projected_position[0]
        dy = body2.projected_position[1] - body1.projected_position[1]
        dz = body2.projected_position[2] - body1.projected_position[2]

    return dx, dy, dz


# does not work if planet is not on an axis (x, y, and z all different from 0)
# does not work very well with keplerian orbits
def get_orbital_velocities(body: Body
                           ):
    # see https://github.com/sczesla/PyAstronomy/blob/master/src/pyasl/asl/gal_uvw.py
    # could rotation_relative work here? Or something of the sort
    # consider ZY i.e. the XY plane with inclination around X
    orbital_velocities = []
    for other_body in body.circle_of_influence:
        dx, dy, dz = get_distances(body, other_body, METERS)
        o_v_x = 0.0
        o_v_y = 0.0
        o_v_z = 0.0
        if dx != 0:
            o_v_x = sqrt(G * other_body.mass / abs(dx)) * np.sign(dx)
        if dy != 0:
            o_v_y = sqrt(G * other_body.mass / abs(dy)) * np.sign(dy)
        if dz != 0:
            o_v_z = sqrt(G * other_body.mass / abs(dz)) * np.sign(dz)

        orbital_velocities.append((o_v_z, o_v_x, o_v_y))  # how to set this to any angle?

    starting_orbital_velocity = orbital_velocities[0]

    # for keplerian orbits, far from perfect
    # 1.05 is very arbitrary
    for orbital_velocity in orbital_velocities[1:]:
        x = 1.05 * orbital_velocity[0] * cos(radians(45))
        y = starting_orbital_velocity[1] + 1.05 * orbital_velocity[1] * sin(radians(45))
        starting_orbital_velocity = (x, y, starting_orbital_velocity[2])

    return starting_orbital_velocity


def get_g_forces(body: Body,
                 other_body: Body,
                 scale_type: str = PIXELS,
                 scale: int = SCALE
                 ):
    force_x = force_y = force_z = 0

    dx = other_body.x - body.x
    dy = other_body.y - body.y
    dz = other_body.z - body.z
    softening = 1  # to avoid issues when particles are too close together
    d = sqrt(pow(dx, 2) + pow(dy, 2) + pow(dz, 2) + pow(softening, 2))

    if scale_type == METERS:
        dx *= scale
        dy *= scale
        dz *= scale
        d *= scale

    # dividing G * other.mass by d³ and then multiplying that by distance
    if dx != 0:
        force_x = (G * other_body.mass / pow(d, 3)) * dx
    if dy != 0:
        force_y = (G * other_body.mass / pow(d, 3)) * dy
    if dz != 0:
        force_z = (G * other_body.mass / pow(d, 3)) * dz

    return force_x, force_y, force_z


def body_data(body: Body,
              data_level: int = 0,
              scale: int = SCALE
              ):
    body_name_text = f'{body.name.upper()}'  # use this to center name in tab

    # have to display μm/s², otherwise it will always round to 0
    to_return = [body_name_text,
                 f'X{body.x:.2f}  Y{body.y:.2f}  Z{body.z:.2f}',
                 f'{body.mass:.0E} kg  {(body.radius / 1000):.0E} km',
                 f'VX{body.velocity_x:.2f}  VY{body.velocity_y:.2f}  VZ{body.velocity_z:.2f} (m/s)',
                 f'AX{body.acceleration_x * pow(10, 6):.2f}  AY{body.acceleration_y * pow(10, 6):.2f}  AZ{body.acceleration_z * pow(10, 6):.2f} (μm/s²)',
                 ''  # '\n' does not work with pygame text
                ]

    if data_level == 0:
        to_return.append('Orbits:')
        if len(body.circle_of_influence) > 0:
            for other_body in body.circle_of_influence:
                to_return.append(f' {other_body.name}')
        else:
            to_return.append('  None')
        to_return.append('')

        if not body.can_move:
            to_return.append('Can\'t move  ')
        if not body.has_gravity:
            to_return.append('Gravity disabled ')
        if not body.influenced_by_gravity:
            to_return.append('Not influenced by gravity ')
        if not body.can_collide:
            to_return.append('No collisions ')

    return to_return


def mouse_hover(engine_screen_width,  # not working properly with perspective or rotation
                engine_screen_height,
                body,
                mouse_position: tuple,
                camera: Camera(),
                radius_scale: int = RADIUS_SCALE
                ):
    output = False
    mouse_x, mouse_y = mouse_position[0], mouse_position[1]
    body_relative_coords, _ = rotation_relative_to_camera(engine_screen_width, engine_screen_height, body, camera)
    body_x, body_y = body_relative_coords[0][0], body_relative_coords[0][1]

    # make hit box bigger if body too small (under radius of 1000 km)
    if body.radius / 1000 < 1000:
        r = 1000000 / radius_scale
    else:
        r = (body.radius / radius_scale) * camera.zoom_multiplier

    d = pow(pow(body_x - mouse_x, 2) + pow(body_y - mouse_y, 2), 0.5)
    if d <= r:
        output = True

    return output


def random_body_data(index: int):
    name = f'Unidentified {index}'
    x = randint(-universe_boundary_side // 2, universe_boundary_side // 2)
    y = randint(-universe_boundary_side // 2, universe_boundary_side // 2)
    z = randint(-universe_boundary_side // 2, universe_boundary_side // 2)
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    if color == BLACK:
        color = WHITE
    radius = randint(100, 8000)
    mass = triangular(0.01, 6)

    to_return = (name, x, y, z, color, radius, mass)
    return to_return


def random_background_stars(n,
                            layers: int = 1,
                            avg_radius: int = 15,
                            radius_deviation: int = 5
                            ):
    bg_stars = []
    radius = universe_boundary_side * 2
    for layer in range(layers):
        stars_in_layer = []
        for i in range(n):
            x = gauss(1, 10)
            y = gauss(1, 10)
            z = gauss(1, 10)
            normalizer = 1 / sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2))
            x *= normalizer * radius
            y *= normalizer * radius
            z *= normalizer * radius
            r = randint(avg_radius - radius_deviation, avg_radius + radius_deviation)
            stars_in_layer.append(BgStar(x, y, z, r))
        bg_stars.append(tuple(stars_in_layer))
        radius *= 1.1
    return bg_stars


def position_relative_to_camera(screen_width: int,
                                screen_height: int,
                                obj,
                                camera
                                ):
    z = camera.zoom_multiplier
    if type(obj) == Body:  # body class
        x, y = obj.x, obj.y
    else:  # tuple = (x, y), for grid, universe boundary, trails, lines between bodies
        x, y = obj[0], obj[1]
    x_to_camera = (x - camera.x) * z - (screen_width / 2) * (z - 1)
    y_to_camera = (y + camera.y) * z - (screen_height / 2) * (z - 1)
    # z_to_camera = z * z - (screen_height / 2) * (z - 1)

    return x_to_camera, y_to_camera


def rotation_relative_to_camera(screen_width: int,
                                screen_height: int,
                                obj,
                                camera,
                                is_position_relative_to_camera: bool = True
                                ):
    vertices = []
    if type(obj) == Body or type(obj) == BgStar:
        vertices = [np.array((obj.x, obj.y, obj.z))]
    else:
        for vertex in obj:
            vertices.append(np.array(vertex))

    projected_vertices = []
    for i, vertex in enumerate(vertices):  # order of dots matters (a little)
        # rotation = np.dot(camera.rotation_matrix_x, vertex.reshape((3, 1)))
        rotation = np.dot(camera.rotation_matrix_z, vertex.reshape((3, 1)))
        rotation = np.dot(camera.rotation_matrix_y, rotation)
        rotation = np.dot(camera.rotation_matrix_x, rotation)

        if type(obj) == Body:  # delete
            obj.debug = [x for x in rotation.tolist()]
            t = ''
            for d in obj.debug:
                for e in d:
                    t += f'{e:.0f}, '
            obj.debug = t

        projection = np.dot(camera.projection_matrix, rotation)  # reshape with 3 rows and 1 column
        x = int(projection[0][0])
        y = int(projection[1][0])
        z = int(projection[2][0])

        if is_position_relative_to_camera:
            x, y = position_relative_to_camera(screen_width, screen_height, (x, y), camera)
        else:  # for the rosetta
            x += screen_width / 2
            y += screen_height / 2
        projected_vertices.append((x, y))

    return projected_vertices, z


def get_system_energy(bodies):
    # should use numpy otherwise it is too slow (and imprecise and prone to error)
    # see https://github.com/pmocz/nbody-python/blob/master/nbody.py
    kinetic_energy = 0
    potential_energy = 0
    for body in bodies:
        # Kinetic
        vmod, _ = components_to_vector(body.velocity_x, body.velocity_y, body.velocity_z)
        ke = 0.5 * body.mass * pow(vmod, 2)
        kinetic_energy += ke

        # Potential, G * M * m / d, way too small, fix
        for other_body in body.circle_of_influence:
            dx, dy, dz = get_distances(body, other_body, METERS)
            d, _ = components_to_vector(dx, dy, dz)
            if d > 1 or d < -1:
                pex = (G * body.mass * other_body.mass / pow(d, 3)) * dx
                pey = (G * body.mass * other_body.mass / pow(d, 3)) * dy
                pez = (G * body.mass * other_body.mass / pow(d, 3)) * dz
                potential_energy += components_to_vector(pex, pey, pez)[0]

    total_energy = kinetic_energy - potential_energy
    return kinetic_energy, potential_energy, total_energy

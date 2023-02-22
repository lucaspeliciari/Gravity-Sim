import pygame.draw
import pygame.image

from math import degrees
from functions import *
from common_functions import lerp
from vars import grid_width


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————


# UI
def draw_template_title(screen, sim, engine):
    text = sim.templates[sim.template_index].name
    text_width, text_height = engine.large_font.size(text)
    screen.blit(engine.large_font.render(text, True, WHITE), (engine.screen_width // 2 - text_width // 2, 20))  # 20 is vertical offset, arbitrary


def draw_message(screen, font, screen_size, current_vertical_offset, message, color: tuple = WHITE):
    text_width, text_height = font.size(message)
    vertical_offset = current_vertical_offset + text_height
    screen.blit(font.render(message, True, color), (screen_size[0] // 2 - text_width // 2, 80 + vertical_offset))  # 80 is vertical offset, arbitrary
    return vertical_offset


def draw_ui(screen, mouse_position, sim, engine):
    texts_left = [f'{engine.clock.get_fps():.2f} fps',
                  f'Template: {sim.template_index + 1}/{len(sim.templates)}',
                  f'Simulation time: {engine.simulation_timer / 3600:.2f} hours',
                  f'Real time: {engine.timer:.2f} seconds',
                  f'Current frame: {engine.current_frame}',
                  f'Timescale: {engine.timescale:.0f}',
                  ]
    for i, text in enumerate(texts_left):
        text_width, text_height = engine.font.size(text)
        screen.blit(engine.font.render(text, True, WHITE), (10, engine.screen_height - (i + 1) * text_height))

    texts_right = [f'Zoom: {sim.camera.zoom}  -->  x{sim.camera.zoom_multiplier:.2f}',
                   f'Cam RX: {degrees(sim.camera.rotation_x):.0f}°  Cam RY: {degrees(sim.camera.rotation_y):.0f}°  '
                   f'Cam RZ: {degrees(sim.camera.rotation_z):.0f}°',
                   f'Cam X: {sim.camera.x:.2f}  Cam Y: {sim.camera.y:.2f}  Cam Z: {sim.camera.z}',
                   f'Bodies: {len(sim.bodies)}',
                   f'Mouse X: {mouse_position[0]:.2f} Mouse Y: {mouse_position[1]}']
    if not sim.collisions:
        texts_right.append('Collisions disabled!')
    for i, text in enumerate(texts_right):
        text_width, text_height = engine.font.size(text)
        screen.blit(engine.font.render(text, True, WHITE),
                    (engine.screen_width - text_width - 5, engine.screen_height - (i + 1) * text_height))


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————


# SIMULATION
def draw_grid(screen, engine_screen_width, engine_screen_height, sim_universe_boundary, camera):  # only 2D
    # VERTICAL
    step = grid_width * camera.zoom_multiplier
    grid_start_x, grid_start_y = position_relative_to_camera(engine_screen_width, engine_screen_height,
                                                             (sim_universe_boundary[0], sim_universe_boundary[2]),
                                                             camera)
    grid_end_x, grid_end_y = position_relative_to_camera(engine_screen_width, engine_screen_height,
                                                         (sim_universe_boundary[0], sim_universe_boundary[3]), camera)
    number_lines = (sim_universe_boundary[1] - sim_universe_boundary[0]) / grid_width
    for i in range(int(number_lines)):
        if i % 2 == 0:
            pygame.draw.line(screen, LIGHT_GRAY, (grid_start_x, grid_start_y), ((grid_end_x, grid_end_y)))
        grid_start_x += step
        grid_end_x = grid_start_x

    # HORIZONTAL
    step_y = grid_width * camera.zoom_multiplier
    grid_start_x, grid_start_y = position_relative_to_camera(engine_screen_width, engine_screen_height,
                                                             (sim_universe_boundary[0], sim_universe_boundary[2]),
                                                             camera)
    grid_end_x, grid_end_y = position_relative_to_camera(engine_screen_width, engine_screen_height,
                                                         (sim_universe_boundary[1], sim_universe_boundary[2]), camera)

    number_lines = (sim_universe_boundary[3] - sim_universe_boundary[2]) / grid_width
    for j in range(int(number_lines)):
        if j % 2 == 0:
            pygame.draw.line(screen, LIGHT_GRAY, (grid_start_x, grid_start_y),
                             (grid_end_x, grid_end_y))
        grid_start_y += step_y
        grid_end_y = grid_start_y


def draw_center_lines(screen, screen_width, screen_height):
    pygame.draw.line(screen, WHITE, (screen_width / 2, 0), (screen_width / 2, screen_height))
    pygame.draw.line(screen, WHITE, (0, screen_height / 2), (screen_width, screen_height / 2))


def draw_trail(screen, engine_screen_width, engine_screen_height, body, camera):
    if len(body.trail) > 1:
        corrected_trail, _ = rotation_relative_to_camera(engine_screen_width, engine_screen_height, body.trail, camera)
        pygame.draw.lines(screen,
                          WHITE,
                          False,
                          corrected_trail)


def draw_bodies(screen,
                engine_screen_width,
                engine_screen_height,
                bodies,
                camera,
                radius_scale: int = RADIUS_SCALE,
                draw_trails: bool = True,
                light: bool = True
                ):
    for i, body in enumerate(bodies):
        xy, z = rotation_relative_to_camera(engine_screen_width, engine_screen_height, body, camera)
        x, y = xy[0][0], xy[0][1]

        r = (body.radius / radius_scale) * camera.zoom_multiplier
        perspective_scaling = lerp(0.5, 2, (z + (Z_SCALING / 2)) / Z_SCALING)  # increases or decreases radius based on distance do camera
        r *= perspective_scaling

        body.projected_z = z  # merge with projected_data into projected_position
        body.projected_data = (x, y, r)  # r depends on zoom, standardize and improve name

        body.projected_position = (x, y, z)
        body.projected_radius = r

    sorted_bodies = sorted(bodies, key=lambda a: a.projected_position[2])
    for body in sorted_bodies:  # sort object by projected z coordinate
        x, y, r = body.projected_position[0], body.projected_position[1], body.projected_radius

        if light and body.emits_light:  # "or body.name == 'Earth'" is just for debug
            base_color = triangular(50, 150)
            glow_color = (base_color, base_color, 0)

            # prevents "out of memory" crashes
            surface_size_width = min(r * 4, engine_screen_width)
            surface_size_height = min(r * 4, engine_screen_height)

            transparent_surface = pygame.Surface((surface_size_width, surface_size_height), pygame.SRCALPHA)
            transparent_surface.set_alpha(128)
            size = 1.3
            pygame.draw.circle(transparent_surface, glow_color, (r * size, r * size), r * size)
            screen.blit(transparent_surface, (x - r * size, y - r * size))

        if draw_trails:
            draw_trail(screen, engine_screen_width, engine_screen_height, body, camera)

        pygame.draw.circle(screen, body.color, (x, y), r)


def draw_body_vectors(screen,  # bugged: does not show vectors correctly
                      engine_screen_width,
                      engine_screen_height,
                      bodies,
                      camera,
                      vector_scale
                      ):
    for body in bodies:
        # VELOCITY, not 90° to accel when orbiting even if the orbit is perfectly round
        # Bugged, pointing to a specific point and never changing instead of tangential orbit
        velocity = (body.velocity_x, body.velocity_y, body.velocity_z)
        xy, _ = rotation_relative_to_camera(engine_screen_width, engine_screen_height, [velocity], camera)
        x, y = body.projected_position[0] + 10, body.projected_position[1] + 10

        x *= vector_scale
        y *= vector_scale

        pygame.draw.line(screen, RED, (body.projected_position[0], body.projected_position[1]), (x, y), 3)

        # ACCELERATION
        acceleration = (body.acceleration_x, body.acceleration_y, body.acceleration_z)
        xy, _ = rotation_relative_to_camera(engine_screen_width, engine_screen_height, [acceleration], camera)
        x, y = xy[0][0], xy[0][1]
        pygame.draw.line(screen, BLUE, (body.projected_position[0], body.projected_position[1]), (x, y), 3)


def draw_lines_between_bodies(screen, bodies, selected_body_index):
    if selected_body_index != -1:
        body = bodies[selected_body_index]
        if body.has_gravity:
            for other_body in [x for x in bodies if x != body]:
                if other_body.influenced_by_gravity:
                    start_x, start_y = body.projected_position[0], body.projected_position[1]
                    end_x, end_y = other_body.projected_position[0], other_body.projected_position[1]

                    dx, dy, dz = get_distances(body, other_body, PIXELS)
                    d = components_to_vector(dx, dy, dz)[0]

                    if d > 1000:
                        color = LIGHT_GRAY
                    elif 700 < d <= 1000:
                        color = RED
                    elif 500 < d >= 700:
                        color = YELLOW
                    else:
                        color = GREEN

                    pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 3)


def draw_body_data(screen,
                   engine_screen_width,
                   engine_screen_height,
                   bodies,
                   camera,
                   show_data,
                   mouse_position,
                   font,
                   ):
    if show_data == 1:  # ON MOUSE HOVER
        for body in bodies:
            if mouse_hover(engine_screen_width,
                           engine_screen_height,
                           body,
                           mouse_position,
                           camera):
                texts = body_data(body, 1)

                x, y, r = body.projected_position[0], body.projected_position[1], body.projected_radius

                text_width, text_height = font.size('M')  # get width of 'M' because it is a pretty wide character
                y_offset = len(texts) * text_height / 2

                for i, text in enumerate(reversed(texts)):
                    screen.blit(font.render(text, True, WHITE),
                                (x + r + 8, y + y_offset - (i + 1) * text_height))  # wrong

    elif show_data == 2:  # ALWAYS SHOW
        for body in bodies:
            texts = body_data(body, 1)

            x, y, r = body.projected_position[0], body.projected_position[1], body.projected_radius

            for i, text in enumerate(reversed(texts)):
                text_width, text_height = font.size(text)
                screen.blit(font.render(text, True, WHITE), (x + r, y - (i + 1) * text_height))


def draw_universe_boundaries(screen, engine_screen_width, engine_screen_height, sim_universe_boundary, camera):
    minus_x, minus_y, minus_z = sim_universe_boundary[0], sim_universe_boundary[2], sim_universe_boundary[4]
    plus_x, plus_y, plus_z = sim_universe_boundary[1], sim_universe_boundary[3], sim_universe_boundary[5]

    universe_vertices = [(minus_x, minus_y, minus_z),  # -1 -1 -1
                         (plus_x, plus_y, plus_z),  # 1 1 1
                         (minus_x, minus_y, plus_z),  # -1 -1 1
                         (plus_x, minus_y, plus_z),  # 1 -1 1
                         (minus_x, plus_y, plus_z),  # -1 1 1
                         (plus_x, minus_y, minus_z),  # 1 -1 -1
                         (plus_x, plus_y, minus_z),  # 1 1 -1
                         (minus_x, plus_y, minus_z)]  # -1 1 -1

    projected_universe_vertices, z = rotation_relative_to_camera(engine_screen_width, engine_screen_height,
                                                                 universe_vertices, camera)
    text_points = projected_universe_vertices.copy()

    faces = [
        (0, 2, 3, 5, 0),
        (1, 6, 7, 4, 1),
        (0, 7, 6, 5, 0),
        (5, 6, 1, 3, 5),
        (0, 7, 4, 2, 0),
        (2, 3, 1, 4, 2),
    ]
    face_coords = []
    for face in faces:
        face_s = []
        for vertex in face:
            face_s.append((projected_universe_vertices[vertex][0], projected_universe_vertices[vertex][1]))
        face_coords.append(face_s)
    draw_faces(screen, face_coords, (100, 0, 0))

    # EDGES
    lines = [
        [(0, 2),
         (2, 3),
         (3, 5),
         (5, 0)],
        [(1, 6),
         (6, 7),
         (7, 4),
         (4, 1)],
        [(0, 7),
         (2, 4),
         (3, 1),
         (5, 6)],
    ]
    for line in lines:
        for vertices in line:
            draw_line(screen, vertices[0], vertices[1], projected_universe_vertices, (255, 0, 0), 5)


def draw_cube_vertex_indices(screen, text_points, points, camera):
    # change sizes based on "distance to camera"
    for i in range(len(text_points)):
        depth_multiplier_y = lerp(0.1, 2, (
                1000 + points[i][0] * sin(camera.rotation_y)) / 2000)
        depth_multiplier = 1  # this var should take all axes and angles into account

        font = pygame.font.SysFont("monospace", int(25 * depth_multiplier), bold=True)
        text = f'{i}'
        text_width, text_height = font.size(text)
        pygame.draw.circle(screen, WHITE, (text_points[i][0], text_points[i][1]), 12 * depth_multiplier)
        screen.blit(font.render(text, True, (0, 0, 0)),
                    (text_points[i][0] - text_width / 2, text_points[i][1] - 13 * depth_multiplier))


def draw_line(screen, i, j, points, color: tuple = (0, 0, 0), line_width: int = 3):
    pygame.draw.line(screen, color, (points[i][0], points[i][1]), (points[j][0], points[j][1]), line_width)


def draw_faces(screen, faces, color):
    for face in faces:
        pygame.draw.polygon(screen, color, face)


def draw_background_stars(screen, engine_screen_width, engine_screen_height, bg_stars, camera, timer):
    big_list_of_stars = []  # bad fix, remove later
    for bg_star_layer in bg_stars:
        for bg_star in bg_star_layer:
            xy, z = rotation_relative_to_camera(engine_screen_width, engine_screen_height, bg_star, camera)
            x = xy[0][0]
            y = xy[0][1]
            bg_star.projected_position = (x, y, z)
            big_list_of_stars.append(bg_star)

    for bg_star in sorted(big_list_of_stars, key=lambda a: a.projected_position[2]):
        if bg_star.projected_position[2] < -1000:  # if in the far background, adjust
            zoom_multiplier = max(1, min(camera.zoom_multiplier, 5))
            r = bg_star.radius * zoom_multiplier * lerp(0.1, 1,
                                                        (bg_star.projected_position[2] + (Z_SCALING / 2)) / Z_SCALING)
            base_color = abs(cos(timer) * sin(degrees(randint(10, 90))) * 255)  # messy
            base_color = min(100, int(base_color))
            random_color = (base_color, base_color, base_color)
            pygame.draw.circle(screen, random_color, (bg_star.projected_position[0], bg_star.projected_position[1]), r)


def draw_center_of_universe(screen, engine_screen_width, engine_screen_height, camera):  # simple but it works
    line_length = 20
    x, y = position_relative_to_camera(engine_screen_width, engine_screen_height, (0, 0), camera)
    pygame.draw.line(screen, WHITE, (x - line_length, y - line_length), (x + line_length, y + line_length), 5)
    pygame.draw.line(screen, WHITE, (x - line_length, y + line_length), (x + line_length, y - line_length), 5)


def draw_system_center_of_mass(screen, engine_screen_width, engine_screen_height, center_xy, camera):  # not very good
    line_length = 65
    xy, z = rotation_relative_to_camera(engine_screen_width, engine_screen_height, [center_xy], camera)
    x = xy[0][0]
    y = xy[0][1]
    line_length = line_length * lerp(0.5, 2, (z - 25) / 50) * camera.zoom_multiplier
    pygame.draw.line(screen, WHITE, (x - line_length, y - line_length), (x + line_length, y + line_length), 5)
    pygame.draw.line(screen, WHITE, (x - line_length, y + line_length), (x + line_length, y - line_length), 5)


def draw_rosetta(screen,  # probably not called rosetta
                 engine_screen_width,
                 engine_screen_height,
                 camera):
    rosetta_vertices = [(100, 0, 0),
                        (0, -100, 0),
                        (0, 0, 100)]
    projected_rosetta_vertices, _ = rotation_relative_to_camera(engine_screen_width, engine_screen_height,
                                                                rosetta_vertices, camera,
                                                                is_position_relative_to_camera=False)

    for i, projected_rosetta_vertex in enumerate(projected_rosetta_vertices):
        color = (255, 255, 255)
        if i == 0:
            color = (255, 0, 0)
        elif i == 1:
            color = (0, 255, 0)
        elif i == 2:
            color = (0, 0, 255)
        offset = 100
        pygame.draw.line(screen, color, (engine_screen_width - offset, engine_screen_height - offset),
                         (projected_rosetta_vertex[0] + engine_screen_width / 2 - offset,
                          projected_rosetta_vertex[1] + engine_screen_height / 2 - offset), 10)


# does not work well with resolutions other than 1440x900, especially smaller ones
def draw_help_menu(screen, engine_screen_width, engine_screen_height):
    pygame.draw.rect(screen, WHITE, (20, 15, engine_screen_width - 40, engine_screen_height - 30), 5)
    pygame.draw.rect(screen, BLACK, (22.5, 17.5, engine_screen_width - 42.5, engine_screen_height - 32.5))

    title = 'HELP'
    font = pygame.font.SysFont("monospace", 40)
    title_width, title_height = font.size(title)
    screen.blit(font.render(title, True, WHITE),
                ((engine_screen_width - title_width) / 2, 20))

    # needs a proper text wrap
    texts = ['• Click on any body or use , and . to focus on it and see its info on the right tab',
             '• Use WASD or LMB to pan camera',
             '• Use arrows, numkeys (2, 4, 6, 8, 7, 9) or RMB to rotate camera',
             '• Use numpad 0 to reset camera rotation',
             '• Mouse wheel or Q and E to zoom in and out',
             '• Use bottom slider, keypad + or keypad - to change timescale',
             '• Hold shift to increase zoom and panning speed',
             '• Left tab contains buttons, toggles and sliders that affect the entire simulation',
             '• Right tab contains info about universe if nothing is selected and specific info about ',
             '  selected object if body is selected',
             '• Click on a tab\'s triangle to keep it extended',
             '• Press r to reset simulation',
             '• Press t or y to switch simulation template',
             '• Press 1 through 9 to save universe in that slot and ctrl + 1 through 9 to load previously',
             '  saved universe in that slot',
             '• Universe is saved automatically on exit',
             '• Latest autosave is automatically loaded when starting program. This can be changed in the ',
             '  settings file',
             '• You can also press ctrl + L to restore most recent autosave',
             '• Settings can be changed in the settings.json file',
             '',
             '',
             'NOTES: • Performance is still pretty terrible',
             '       • Collision and keplerian orbits are still very WiP',
             '       • Octrees have been implemented, but are still not used in the back-end',
             '       • Trails are not fully 3D, and that might sometimes give the impression that a body\'s ',
             '       "depth" is wrong e.g. Earth seems to be behind Sun when it\'s actually in front of it',
             '       • Camera won\'t center on bodies if camera rotation isn\'t 0',
             ]
    font = pygame.font.SysFont("monospace", 25)
    for i, text in enumerate(texts):
        text_width, text_height = font.size(text)
        screen.blit(font.render(text, True, WHITE),
                    (40, title_height + (i + 2) * text_height))


# does not work well with resolutions other than 1440x900, especially smaller ones
def draw_credits(screen, engine_screen_width, engine_screen_height):
    pygame.draw.rect(screen, WHITE, (20, 15, engine_screen_width - 40, engine_screen_height - 30), 5)
    pygame.draw.rect(screen, BLACK, (22.5, 17.5, engine_screen_width - 42.5, engine_screen_height - 32.5))

    title = 'CREDITS'
    font = pygame.font.SysFont("monospace", 40)
    title_width, title_height = font.size(title)
    screen.blit(font.render(title, True, WHITE),
                ((engine_screen_width - title_width) / 2, 20))

    texts = ['• By Lucas Peliciari',
             '• Made with:',
             '      ○ Python 3.10.2',
             '      ○ Pygame 2.1.2',
             '      ○ and more (WiP credits)',
             ]
    font = pygame.font.SysFont("monospace", 25)
    for i, text in enumerate(texts):
        text_width, text_height = font.size(text)
        screen.blit(font.render(text, True, WHITE),
                    (40, title_height + (i + 2) * text_height))

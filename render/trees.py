import pygame.draw

from constants import *
from functions import rotation_relative_to_camera


def draw_octrees(screen,  # very slow
                 engine_screen_width,
                 engine_screen_height,
                 root,
                 camera,
                 ):
    colors = [WHITE, RED, GREEN, BLUE, PURPLE, YELLOW, CYAN]
    for cube in root.get_cubes():  # cube[0] is (x,y,z,w,h,d) and cube[1] is level
        x, y, z = cube[0].x, cube[0].y, cube[0].z
        width, height, depth = cube[0].width, cube[0].height, cube[0].depth
        cube_vertices = [
            (x, y, z),  # 0
            (x + width, y, z),  # 1
            (x + width, y, z + depth),  # 2
            (x, y, z + depth),  # 3
            (x, y + height, z),  # 4
            (x + width, y + height, z),  # 5
            (x + width, y + height, z + depth),  # 6
            (x, y + height, z + depth), ]  # 7

        projected_cube_vertices, z = rotation_relative_to_camera(engine_screen_width, engine_screen_height,
                                                                 cube_vertices,
                                                                 camera)

        lines = [
            [(0, 1),
             (1, 2),
             (2, 3),
             (3, 0)],
            [(4, 5),
             (5, 6),
             (6, 7),
             (7, 4)],
            [(0, 4),
             (1, 5),
             (2, 6),
             (3, 7)],
        ]

        color_index = cube[1]
        if color_index > len(colors) - 1:
            color_index = 0
        for line in lines:
            for vertices in line:
                i, j = vertices[0], vertices[1]
                pygame.draw.line(screen,
                                 colors[color_index],
                                 (projected_cube_vertices[i][0], projected_cube_vertices[i][1]),
                                 (projected_cube_vertices[j][0], projected_cube_vertices[j][1]),
                                 5)


def draw_octo_center_of_mass(screen,  # very slow
                             engine_screen_width,
                             engine_screen_height,
                             root,
                             camera,
                             ):
    root.get_center_of_mass(0, 0)

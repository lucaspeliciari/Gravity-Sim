from numpy import matrix

from math import sin, cos

from vars import screen_width, screen_height, max_zoom, camera_pan_sensitivity


# 0 for no zoom, positive for zoom in, negative for zoom out
class Camera:
    def __init__(self,
                 starting_zoom: int = 0
                 ):
        self.x = -screen_width / 2  # negative left, positive right
        self.y = screen_height / 2  # negative down, positive up
        self.z = 0  # kind of completely useless
        self.zoom = starting_zoom
        self.zoom_multiplier = 1

        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0

        self.projection_matrix = matrix(
            [[1, 0, 0],
             [0, 1, 0],
             [0, 0, 1]])

        self.rotation_matrix_x = matrix([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        self.rotation_matrix_y = matrix([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        self.rotation_matrix_z = matrix([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])

    def pan(self, x, y):
        self.x += x * camera_pan_sensitivity
        self.y += y * camera_pan_sensitivity

        # CLAMP TO BOUNDARIES, bugged
        # self.x = max(universe_boundary[0] - screen_width, min(self.x, universe_boundary[1]))
        # self.y = max(universe_boundary[2] - screen_height, min(self.y, universe_boundary[3]))

    def change_zoom(self, zoom_change):
        self.zoom += zoom_change  # should always be int
        self.zoom = max(-max_zoom, min(self.zoom, max_zoom))
        self.get_zoom_multiplier()

    def get_zoom_multiplier(self):
        zoom_multiplier = 1
        if self.zoom > 0:
            zoom_multiplier = self.zoom + 1
        elif self.zoom < 0:
            zoom_multiplier = self.zoom - 1
            zoom_multiplier = 1 / zoom_multiplier
        self.zoom_multiplier = abs(zoom_multiplier)

    def rotate(self,
               x: float,
               y: float,
               z: float
               ):
        self.rotation_y += y
        self.rotation_z += z
        self.rotation_x += x

        self.rotation_matrix_x = matrix([
            [1, 0, 0],
            [0, cos(self.rotation_x), -sin(self.rotation_x)],
            [0, sin(self.rotation_x), cos(self.rotation_x)]
        ])
        self.rotation_matrix_y = matrix([
            [cos(self.rotation_y), 0, sin(self.rotation_y)],
            [0, 1, 0],
            [-sin(self.rotation_y), 0, cos(self.rotation_y)]
        ])
        self.rotation_matrix_z = matrix([
            [cos(self.rotation_z), -sin(self.rotation_z), 0],
            [sin(self.rotation_z), cos(self.rotation_z), 0],
            [0, 0, 1]
        ])

    def reset(self):
        self.x = 0
        self.y = 0
        
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0
        self.rotate(0, 0, 0)  # just to reset rotation matrices

        self.zoom = 0
        self.zoom_multiplier = 1
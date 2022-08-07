from constants import FULLSCREEN

# DISPLAY
screen_width = 800
screen_height = 600

screen_mode = FULLSCREEN
ui_tab_width = screen_width / 6

# ENGINE
universe_boundary_side = 5000  # universe doesn't have to be a perfect square, but it looks better this way
universe_boundary = (-universe_boundary_side, universe_boundary_side, -universe_boundary_side, universe_boundary_side,
                     -universe_boundary_side, universe_boundary_side)

# SIMULATION
number_random_bodies = 0

# VISUALS
trail_interval = 1000  # append body.trail every x physics calculations (physics_interval), should be as high as it possibly can by without making trails look ugly for performance reasons, lower is better but more expensive
max_trail_length = 100  # higher is better but more expensive
min_distance_to_trail = 3  # has to move x pixels from last trail point in order to append new position, lower is better but more expensive

grid_width = 50

layers_bg_stars = 6
bg_stars_per_layer = 150

# CAMERA
max_zoom = 5000
camera_pan_sensitivity = 1

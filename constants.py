import pygame.constants

# DISPLAY
WINDOWED = 0
BORDERLESS = 1
FULLSCREEN = 2
SCREEN_MODE = [pygame.RESIZABLE, pygame.NOFRAME, pygame.FULLSCREEN]
COMMON_RESOLUTIONS = [(1920, 1080),
                      (1440, 900),
                      (1366, 768),
                      (1280, 720),
                      (800, 600)]
MIN_SCREEN_WIDTH = 640
MIN_SCREEN_HEIGHT = 480

# GAMES STATES
SPLASH_SCREEN = 0
MAIN_MENU = 1
OPTIONS = 2
CREDITS = 3
SIMULATION = 4
RECORDING = 5

# ENGINE
FRAMERATE = 60
PHYSICS_INTERVAL = 10  # One calculation every x ms(?), test different values

PIXELS = 0
METERS = 1
PROJECTED = 2  # use rotation-dependant coordinates

# SIMULATION
SCALE = 1000000  # 1 PIXEL IS X METERS
RADIUS_SCALE = 100000  # SCALE FOR RADII ONLY, test different values
Z_SCALING = 500  # Z = -Z_SCALING is the smallest visual radius for 3D and Z = +Z_SCALING the largest
MAX_ZOOM = 5000  # not being used, didn't remove this from vars yet

RECORDING_TIME = 10

# UI
TAB_BUTTON_Y_START = 50
TAB_BUTTON_SPACING = 30
TAB_TOGGLE_SPACING = 30
TAB_BUTTON_TOGGLE_SPACING = 30
TEMPLATE_TITLE_TIME_ON_SCREEN = 1.75

MAIN_MENU_OPTIONS = [
        f'Quit',
        f'Credits',
        f'Options',
        f'Start recording',
        f'Load simulation',
        f'Start simulation',
    ]

DEFAULT_SETTINGS = {"first_run": 1, "state": 0, "windowed_res_x": 800, "windowed_res_Y": 600, "fullscreen": 1,
                    "number_random_bodies": 0, "trail_interval": 1000, "max_trail_length": 100,
                    "min_distance_to_trail": 3, "layers_bg_stars": 6, "bg_stars_per_layer": 150,
                    "bg_star_avg_radius": 20, "bg_star_radius_deviation": 10, "start_template_index": 1,
                    "autosave_on_exit": 1, "autoload_on_start": 1, "max_messages_in_log": 16}

# PLAY / PAUSE BUTTON ICONS
play_triangle = ((12, 8),
                 (12, 40),
                 (38, 24))
pause_bars = ((15, 10,
               15, 40),
              (35, 10,
               35, 40))

# PHYSICS
G = 6.67408 * pow(10, -11)  # GRAVITATIONAL CONSTANT
GRAVITATIONAL_FORCE_LIMIT = 1 * pow(10, 23)  # GRAVITATIONAL FORCE LIMIT
ELASTICITY = 1  # BODY "ELASTICITY" FOR COLLISIONS

# COLORS
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (121, 121, 121)
LIGHT_GRAY = (175, 175, 175)
WHITE = (255, 255, 255)
PURPLE = (255, 0, 255)
LIGHT_PURPLE = (175, 0, 175)
CYAN = (0, 255, 255)

# OTHERS
PERCENT = 100
MONTHS_IN_YEAR = 12

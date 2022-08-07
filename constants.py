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
SIMULATION = 1

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

# UI
TAB_BUTTON_Y_START = 50
TAB_BUTTON_SPACING = 30
TAB_TOGGLE_SPACING = 30
TAB_BUTTON_TOGGLE_SPACING = 30
TEMPLATE_TITLE_TIME_ON_SCREEN = 1.75

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

# DEBUG
TEST_MODE = True

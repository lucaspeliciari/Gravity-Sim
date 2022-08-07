from constants import *

# radius in km, Body() converts it to meters and calculations use pixels
# mass in (10 ** 24) kg
# correct distances from the Sun
# increased diameters for more visibility
sun = ('Sun', 0, 0, 0, YELLOW, 1988500, 347850, 0, 0, 0, True)
mercury = ('Mercury', 57000, 0, 0, GRAY, 2439.5, 0.330)
venus = ('Venus', 108000, 0, 0, GRAY, 6052, 4.87)
earth = ('Earth', 150000, 0, 0, BLUE, 6378, 5.97)
moon = ('Moon', 150000 + 384, 0, 0, GRAY, 1737.5, 0.073)
mars = ('Mars', 228000, 0, 0, RED, 900, 0.642)  # radius = 3396
phobos = ('Phobos', 228100, 0, 0, LIGHT_GRAY, 500, 0.000000010659)  # real radius: 11.67, distance from Mars: 10000 km...?
deimos = ('Deimos', 228240, 0, 0, LIGHT_GRAY, 500, 0.0000000014762)  # real radius: 6.38, distance from Mars: 24000 km...?
jupiter = ('Jupiter', 779000, 0, 0, GREEN, 71492, 1898)
saturn = ('Saturn', 1430000, 0, 0, YELLOW, 60268, 568)
uranus = ('Uranus', 2880000, 0, 0, LIGHT_GRAY, 25559, 86.8)
neptune = ('Neptune', 4500000, 0, 0, BLUE, 24764, 102)
pluto = ('Pluto', 5910000, 0, 0, BLUE, 1188, 0.013)

# orbital moons, 90º of each other
moon_orbital_1 = ('Moon 1', 0, 384, 0, GRAY, 1737.5, 0.073)
moon_orbital_2 = ('Moon 2', 0, -384, 0, GRAY, 1737.5, 0.073)
moon_orbital_3 = ('Moon 3', 384, 0, 0, GRAY, 1737.5, 0.073)
moon_orbital_4 = ('Moon 4', -384, 0, 0, GRAY, 1737.5, 0.073)
moon_orbital_5 = ('Moon 5', 0, 0, 384, GRAY, 1737.5, 0.073)
moon_orbital_6 = ('Moon 6', 0, 0, -384, GRAY, 1737.5, 0.073)

# orbital moons, aligned
moon5 = ('Moon 5', 800, 0, 0, GRAY, 2500, 0.073)
moon6 = ('Moon 6', 900, 0, 0, RED, 2500, 0.073)
moon7 = ('Moon 7', 1000, 0, 0, YELLOW, 2500, 0.073)
moon8 = ('Moon 8', 1100, 0, 0, LIGHT_GRAY, 2500, 0.073)
moon9 = ('Moon 9', 1200, 0, 0, LIGHT_PURPLE, 2500, 0.073)

jupiter_pattern = ('Jupiter', 0, 0, 0, GREEN, 25000, 400)
earth_pattern_1 = ('Earth 1', -1000, 0, 0, BLUE, 6378, 5.97, 0, 4800, 0)
earth_pattern_2 = ('Earth 2', 1000, 0, 0, BLUE, 6378, 5.97, 0, -4800, 0)
moon_pattern_1 = ('Moon 1', -1300, 0, 0, WHITE, 1737.5, 0.073, 0, -3000, 0)
moon_pattern_2 = ('Moon 2', 1300, 0, 0, WHITE, 1737.5, 0.073, 0, 3000, 0)

sun_kepler = ('Sun', 0, 0, 0, YELLOW, 10000, 10, 0, 0, 0, True)
earth_kepler_1 = ('Earth 1', -1000, 0, 0, BLUE, 6378, 5.97, 0, 4800, 0)
moon_kepler_1 = ('Moon 1', -1350, 0, 0, GRAY, 1550, 0.1)
earth_kepler_2 = ('Earth 2', 1000, 0, 0, BLUE, 6378, 5.97, 0, -4800, 0)
moon_kepler_2 = ('Moon 2', 1350, 0, 0, GRAY, 1550, 0.1)
earth_kepler_3 = ('Earth 3', 0, 1000, 0, BLUE, 6378, 5.97, 0, -4800, 0)
moon_kepler_3 = ('Moon 3', 0, 1350, 0, GRAY, 1550, 0.1)
earth_kepler_4 = ('Earth 4', 0, -1000, 0, BLUE, 6378, 5.97, 0, -4800, 0)
moon_kepler_4 = ('Moon 4', 0, -1350, 0, GRAY, 1550, 0.1)

# DEBUG
earth_debug = ('DEBUG Earth', 0, 0, 0, BLUE, 15000, 15.97)
moon_debug = ('DEBUG Moon', 384, 0, 0, GRAY, 1737.5, 0.073)
perspective_right = ('Perspective Right', 500, 0, 0, RED, 9000, 0.073, 0, 0, 0)
perspective_left = ('Perspective Left', -1500, 0, 0, YELLOW, 9000, 0.073, 0, 0, 0)
perspective_front = ('Perspective Front', 0, 0, -1500, PURPLE, 9000, 0.073, 0, 0, 0)
perspective_back = ('Perspective Back', 0, 0, 1500, WHITE, 9000, 0.073, 0, 0, 0)
perspective_up = ('Perspective Up', 0, -1500, 0, PURPLE, 9000, 0.073, 0, 0, 0)
perspective_down = ('Perspective Down', 0, 1500, 0, WHITE, 9000, 0.073, 0, 0, 0)
perspective_upleft = ('Perspective Up Left', -400, 400, 0, WHITE, 9000, 0.073, 0, 0, 0)
perspective_backdown = ('Perspective Back Down', 0, -400, 400, WHITE, 9000, 0.073, 0, 0, 0)

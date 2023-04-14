from constants import *
from classes.template import Template
from vars import screen_width, screen_height
from prefabs.bodies import *



template_data = ([],
                 [sun, mercury, venus, earth, moon, mars, phobos, deimos, jupiter, saturn, uranus, neptune, pluto],
                 [earth, moon, mars, venus],
                 [sun, mercury, venus, earth, moon, mars, phobos, deimos],
                 [earth, moon_orbital_1],
                 [earth, moon_orbital_1, moon_orbital_2, moon_orbital_3, moon_orbital_4, moon_orbital_5, moon_orbital_6],
                 [earth_debug, moon5, moon6, moon7, moon8, moon9],
                 [earth_debug, moon_debug],
                 [earth_debug,  perspective_upleft, perspective_left, perspective_front, perspective_back, perspective_up, perspective_down, perspective_upleft, perspective_backdown],
                 [jupiter_pattern, earth_pattern_1, earth_pattern_2, moon_pattern_1, moon_pattern_2]
                 )

orbital_moons_circles_of_influence = [[-1],
                                      [0],
                                      [0],
                                      [0],
                                      [0],
                                      [0],
                                      [0],
                                      ]
orbital_moons_around = Template(template_data[5],
                                name='Moons Around Earth',
                                circles_of_influence=orbital_moons_circles_of_influence,
                                orbit_first_body=True,
                                focused_body_index=0)

orbital_moons_aligned = Template(template_data[6],
                                 name='Moons Beside Earth',
                                 circles_of_influence=orbital_moons_circles_of_influence,
                                 orbit_first_body=True,
                                 focused_body_index=0,
                                 starting_camera_zoom=-1)

solar_system_circles_of_influence = [[-1],
                                     [0],
                                     [0],
                                     [0],
                                     [0, 3],  # Moon orbiting Earth
                                     [0],
                                     [0, 5],  # Phobos orbiting Mars
                                     [0, 5],  # Deimos orbiting Mars
                                     [0],
                                     [0],
                                     [0],
                                     [0],
                                     [0]]
solar_system = Template(template_data[1],
                        name='Solar System',
                        circles_of_influence=solar_system_circles_of_influence,
                        starting_camera_zoom=-1,
                        starting_camera_position=(3000000, screen_height / 2),
                        orbit_first_body=True,
                        collisions=False,
                        focused_body_index=3)

test_system_test_circles_of_influence = [[-1]]  # empty circle of influence
for i in range(len(template_data[8])):
    test_system_test_circles_of_influence.append([0])
test_system = Template(template_data[8], name='Collision Test System', circles_of_influence=test_system_test_circles_of_influence,
                                   starting_camera_zoom=-4, orbit_first_body=False, influenced_by_gravity=True,
                                   can_move=True, number_random_bodies=0, focused_body_index=0, collisions=True)


perspective_test_circles_of_influence = [[-1]]  # empty circle of influence
for i in range(len(template_data[8])):
    perspective_test_circles_of_influence.append([0])
perspective_test_system = Template(template_data[8], circles_of_influence=perspective_test_circles_of_influence,
                                   starting_camera_zoom=-4, orbit_first_body=False, influenced_by_gravity=True, collisions=True,
                                   can_move=True, number_random_bodies=0)

cool_pattern_circles_of_influence = [[-1],
                                     [0],
                                     [0],
                                     [0],
                                     [0],
                                     ]
cool_pattern = Template(template_data[-1], name='Cool Pattern', 
                        circles_of_influence=cool_pattern_circles_of_influence,
                        focused_body_index=0, 
                        starting_camera_zoom=-3, 
                        timescale=500)

keplerian_list = [sun_kepler,
                  earth_kepler_1,
                  moon_kepler_1,
                  earth_kepler_2,
                  moon_kepler_2,
                #   earth_kepler_3,  # keplerian orbit function does not work with more than 2 moons/earths
                #   moon_kepler_3,
                #   earth_kepler_4,
                #   moon_kepler_4,
                 ]
keplerian_circles_of_influences = [[-1],
                                    [0],
                                    [0, 1],
                                    [0],
                                    [0, 3]]
keplerian_orbits = Template(keplerian_list, name='Keplerian Orbits', 
                            orbit_first_body=True, 
                            circles_of_influence=keplerian_circles_of_influences,
                            focused_body_index=0,
                            starting_camera_zoom=-2)

free_for_all = Template(template_data[-3], name='Free For All')

stress_test = Template([earth_debug, moon_orbital_1, moon_orbital_2, moon_orbital_3, moon_orbital_4, moon_orbital_5, moon_orbital_6, moon5, moon6, moon7, moon8, moon9], name='Stress Test')


randoms_only = Template(template_data[0], name='Random Planets', number_random_bodies=5,
                        starting_camera_zoom=-4, orbit_first_body=False, collisions=False)


templates = [solar_system,
             orbital_moons_around,
             orbital_moons_aligned,
             cool_pattern,
             keplerian_orbits,
             free_for_all,
             stress_test,
             test_system,
             randoms_only]

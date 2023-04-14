import json
import os
import pickle

from constants import RED, DEFAULT_SETTINGS


# default_settings = {"first_run": 1, "state": 0, "windowed_res_x": 800, "windowed_res_Y": 600, "fullscreen": 1,
#                     "number_random_bodies": 0, "trail_interval": 1000, "max_trail_length": 100,
#                     "min_distance_to_trail": 3, "layers_bg_stars": 6, "bg_stars_per_layer": 150,
#                     "bg_star_avg_radius": 20, "bg_star_radius_deviation": 10, "start_template_index": 1,
#                     "autosave_on_exit": 1, "autoload_on_start": 1, "max_messages_in_log": 16}


# restore default settings if something went wrong with settings.json, probably overkill
def check_settings():
    settings = read_settings()
    if settings == 1:
        restore_default_settings()
        print('Can\'t find settings.json\nDefault settings restored')
        return 1
    else:
        for setting, default_setting in zip(settings, DEFAULT_SETTINGS):
            if setting != default_setting:  # order shouldn't matter, fix
                restore_default_settings()
                print('Something is wrong with settings.json\nDefault settings restored')
                return 2
        return 0


def read_settings():
    try:
        with open(f'{os.getcwd()}\\settings.json', 'r') as file:
            data = json.load(file)
            settings = {}
            for setting in data:
                settings[setting] = data[setting]
            return settings
    except FileNotFoundError:
        return 1


def restore_default_settings():
    with open(f'{os.getcwd()}\\settings.json', 'w') as file:
        json.dump(default_settings, file, indent=4)


def save_settings(settings):
    with open(f'{os.getcwd()}\\settings.json', 'w') as file:
        json.dump(settings, file, indent=4)


def check_saves():
    path = os.getcwd() + '\\saves\\'
    if os.path.isdir(path):
        print('Save folder already exists')
        return 0
    else:
        print('Save folder does not exist')
        os.mkdir(path)
        print('Created save folder')
        return 1


def check_recordings():
    path = os.getcwd() + '\\recordings\\'
    if os.path.isdir(path):
        print('Recordings folder already exists')
        return 0
    else:
        print('Recordings folder does not exist')
        os.mkdir(path)
        print('Created recordings folder')
        return 1


def save_universe(file_name, sim, engine):
    with open(f'{os.getcwd()}\\saves\\{file_name}', 'wb') as file:
        pickled_dict = {'bodies': sim.bodies, 'timescale': sim.timescale, 'real_time': engine.timer,
                        'simulation_timer': engine.simulation_timer, 'current_frame': engine.current_frame,
                        'paused': sim.paused, 'template_index': sim.template_index,
                        'focused_body_index': sim.focused_body_index, 'camera': sim.camera,
                        'collisions': sim.collisions, 'background_stars': sim.background_stars,
                        'bodies_emit_light': sim.bodies_emit_light,
                        'draw_system_center_of_mass': sim.draw_system_center_of_mass, 'draw_octrees': sim.draw_octrees,
                        'calculate_system_energy': sim.calculate_system_energy,
                        'draw_body_vectors': sim.draw_body_vectors, 'draw_trails': sim.draw_trails,
                        'draw_lines_between_bodies': sim.draw_lines_between_bodies, 'draw_grid': sim.draw_grid,
                        'universe_boundary': sim.universe_boundary}
        pickle.dump(pickled_dict, file)


def load_universe(file_name, sim, engine, slot: int = 0):
    try:
        file = open(f'{os.getcwd()}\\saves\\{file_name}', 'rb')
        pickled_dict = pickle.load(file)
    except FileNotFoundError:
        if slot == 0:
            engine.messenger.add('Autosave not found')
        else:
            engine.messenger.add(f'Save in slot {slot} not found')
        return 1

    try:
        sim.bodies = pickled_dict['bodies']
        sim.paused = pickled_dict['paused']
        sim.timescale = pickled_dict['timescale']
        engine.timer = pickled_dict['real_time']
        engine.simulation_timer = pickled_dict['simulation_timer']
        engine.current_frame = pickled_dict['current_frame']
        sim.camera = pickled_dict['camera']
        sim.template_index = pickled_dict['template_index']
        sim.focused_body_index = pickled_dict['focused_body_index']

        sim.collisions = pickled_dict['collisions']
        sim.background_stars = pickled_dict['background_stars']
        sim.bodies_emit_light = pickled_dict['bodies_emit_light']
        sim.draw_system_center_of_mass = pickled_dict['draw_system_center_of_mass']
        sim.draw_octrees = pickled_dict['draw_octrees']
        sim.calculate_system_energy = pickled_dict['calculate_system_energy']
        sim.draw_body_vectors = pickled_dict['draw_body_vectors']
        sim.draw_trails = pickled_dict['draw_trails']
        sim.draw_lines_between_bodies = pickled_dict['draw_lines_between_bodies']
        sim.draw_grid = pickled_dict['draw_grid']
        sim.universe_boundary = pickled_dict['universe_boundary']
    except KeyError:
        engine.messenger.add('Error loading saved universe', 3, color=RED)
        engine.messenger.add('Key error', 3, color=RED)
        engine.messenger.add('', 3)

    engine.reset_values()

    if slot == 0:
        engine.messenger.add('Autosaved universe has been loaded', 3)
    else:
        engine.messenger.add(f'Saved universe in slot {slot} has been loaded', 3)
    return 0


def save_recording(file_name, bodies):
    with open(f'{os.getcwd()}\\recordings\\{file_name}.rec', 'wb') as file:
        pickle.dump(bodies, file)


def load_recording(file_name, engine, sim):  # only pass messenger instead of engine?
    try:
        file = open(f'{os.getcwd()}\\saves\\{file_name}', 'rb')
        pickled_bodies = pickle.load(file)
        sim.bodies = pickled_bodies  # check if this needs the deepcopy as well

    except FileNotFoundError:
        engine.messenger.add('Recording not found')


def get_file_names(folder):
    names = []

    allowed_file_extensions = ['.uni', '.rec']
    for filename in os.listdir(f'{os.getcwd()}\\{folder}'):
        file_extension = filename[-4:]
        if file_extension in allowed_file_extensions and not 'auto' in filename:
            names.append(filename[:-4])

    return names

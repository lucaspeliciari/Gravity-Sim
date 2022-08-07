from util.vectors import Vector3  # use this!

# use getters and setters?
class Body:
    def __init__(self,
                 data,
                 velocity_x: float = 0.0,
                 velocity_y: float = 0.0,
                 velocity_z: float = 0.0,
                 acceleration_x: float = 0.0,
                 acceleration_y: float = 0.0,
                 acceleration_z: float = 0.0,
                 emits_light: bool = False,
                 orbit_direction: int = 0,
                 can_move: bool = True,
                 has_gravity: bool = True,
                 influenced_by_gravity: bool = True,
                 can_collide: bool = True,
                 ):
        self.name = data[0]
        self.x = data[1]
        self.y = data[2]
        self.z = data[3]
        self.color = data[4]
        self.radius = data[5] * 1000  # in meters
        self.mass = data[6] * pow(10, 24)
        self.emits_light = emits_light

        self.projected_position = (self.x, self.y, self.z)
        self.projected_radius = self.radius

        self.velocity_x = velocity_x  # call it vx?
        self.velocity_y = velocity_y
        self.velocity_z = velocity_z
        self.acceleration_x = acceleration_x  # call it ax?
        self.acceleration_y = acceleration_y
        self.acceleration_z = acceleration_z

        self.circle_of_influence = []

        self.orbit_direction = orbit_direction  # 0: no particular direction, 1: counter-clockwise, 2: clockwise remove?

        self.can_move = can_move
        self.has_gravity = has_gravity
        self.influenced_by_gravity = influenced_by_gravity
        self.can_collide = can_collide

        self.physics_interval_counter = 0
        self.trail = [(self.x, self.y, self.z)]

    def __del__(self):
        return f'{self.name} was deleted'

    def __mul__(self, other):
        if type(other) == Body:
            pass  # return distance between bodies?

    def __call__(self, *args, **kwargs):
        print(f'{self.name} was created')

    def __str__(self):
        string_to_return = f'{self.name} \n' \
                           f'X{self.x:.2f}  Y{self.y:.2f}  Y{self.z:.2f} \n' \
                           f'VX{self.velocity_x:.2f}  VY{self.velocity_y:.2f}  VZ{self.velocity_z:.2f}\n' \
                           f'AX{self.acceleration_x:.2f}  AY{self.acceleration_y:.2f}  AZ{self.acceleration_z:.2f}'
        return string_to_return

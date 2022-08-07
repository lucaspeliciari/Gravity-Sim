class BgStar:
    def __init__(self, x, y, z, radius):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius

        self.projected_position = (x, y, z)

    def __str__(self):
        return f'X{self.x}  Y{self.y}  Z{self.z}\nPX{self.projected_position[0]}  PY{self.projected_position[1]}  PZ{self.projected_position[2]}'

class Cube:
    def __init__(self,
                 x: int,
                 y: int,
                 z: int,
                 width: int,
                 height: int,
                 depth: int,
                 ):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth

    def __str__(self):
        return f'X{self.x} Y{self.y} Z{self.z}\nW{self.width} H{self.height} D{self.depth}'

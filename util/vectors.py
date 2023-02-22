from math import atan2


class Vector3:
    def __init__(self, values: tuple = (0, 0)):
        self.x = values[0]
        self.y = values[1]
        self.z = values[2]

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def angle(self):
        return atan2(self.x, self.y)

    def __add__(self, other):
        if type(other) == Vector3:
            self.x += other.x
            self.y += other.y
            self.z += other.z
        elif type(other) == int or type(other) == float:
            self.x += other
            self.y += other
            self.z += other
        else:
            raise Exception(f'Cannot add Vector2 to {type(other)}')
        return self

    def __sub__(self, other):
        if type(other) == Vector3:
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        elif type(other) == int or type(other) == float:
            self.x -= other
            self.y -= other
            self.z -= other
        else:
            raise Exception(f'Cannot subtract Vector2 by {type(other)}')
        return self

    def __mul__(self, other):
        if type(other) == Vector3:
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        elif type(other) == int or type(other) == float:
            self.x *= other
            self.y *= other
            self.z *= other
        else:
            raise Exception(f'Cannot multiply Vector2 by {type(other)}')
        return self

    def __truediv__(self, other):
        if type(other) == Vector3:
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
        elif type(other) == int or type(other) == float:
            self.x /= other
            self.y /= other
            self.z /= other
        else:
            raise Exception(f'Cannot divide Vector2 by {type(other)}')
        return self

    def __floordiv__(self, other):
        if type(other) == Vector3:
            self.x //= other.x
            self.y //= other.y
            self.z //= other.z
        elif type(other) == int or type(other) == float:
            self.x //= other
            self.y //= other
            self.z //= other
        else:
            raise Exception(f'Cannot floor divide Vector2 by {type(other)}')
        return self

    def __str__(self):
        return f'x{self.x:.2f}  y{self.y:.2f}'
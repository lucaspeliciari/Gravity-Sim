class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __str__(self):
        return f'x: {self.x}  y: {self.y}  width: {self.w}  height: {self.h}'

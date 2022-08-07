import pygame.display
import pygame.draw
import pygame.font
from pygame_widgets.button import Button as WidgetsButton

from classes.tab import Tab
from constants import *


class Button(WidgetsButton):
    def __init__(self,
                 screen,

                 x: int,
                 y: int,
                 width: int,
                 height: int,

                 on_click,

                 text: str = '',

                 tab: Tab = None,

                 lines: tuple = (),  # 2D tuple
                 polygon: tuple = (),  # 2D tuple

                 state: int = 0,

                 border_thickness: int = 0,
                 ):
        super().__init__(screen,
                         x,
                         y,
                         width,
                         height,
                         onClick=on_click,
                         text=text,
                         borderThickness=border_thickness)
        screen_width, screen_height = screen.get_size()

        self.x = x  # x value that never changes (not relative to tab)
        self.x_percent = x / screen_width
        self.y = y
        self.y_percent = y / screen_height  # to reposition properly
        
        self.enabled = True

        self.tab = tab

        self.state = state  # 0: draw lines and polygon, 1: only draw lines, 2: only draw polygon
        self.lines = lines
        self.polygon = polygon

    def return_rect(self, engine_screen_width):
        x, y, width, height = map(self.get, ['x', 'y', 'width', 'height'])
        if self.tab is not None:
            if self.tab.side == 'Left':
                x += self.tab.current_width - self.tab.width
            else:
                x += engine_screen_width - self.tab.current_width
        output = (x, y, width, height)
        return output

    def update(self,
               screen,
               engine_screen_width,
               engine_screen_height
               ):
        x = 0
        if self.tab is not None:
            if self.tab.current_width == 0:
                self.enabled = False
            else:
                self.enabled = True
                if self.tab.side == 'Left':
                    x = self.x + self.tab.current_width - self.tab.width
                else:
                    x = self.x + engine_screen_width - self.tab.current_width
        else:
            x = self.x_percent * engine_screen_width - self.get('width') // 2
        self.set('x', x)
        y = self.y_percent * engine_screen_height - self.get('height')
        if y + self._height > engine_screen_height:
            y = engine_screen_height - self._height
        self.set('y', y)

        if self.lines is not None:
            self.draw_figures(screen, engine_screen_width)

        if self.enabled:
            self.show()
            self.enable()
        else:
            self.hide()
            self.disable()

    def draw_figures(self,
                     screen,
                     engine_screen_width: int
                     ):
        x, y, width, height = self.return_rect(engine_screen_width)
        if self.state == 0 or self.state == 1:
            if len(self.lines) > 0:  # adapt to tab
                for line in self.lines:
                    pygame.draw.line(screen,
                                     WHITE,
                                     (x + line[0], y + line[1]),
                                     (x + line[2], y + line[3]),
                                     5)

        if self.state == 0 or self.state == 2:
            if len(self.polygon) > 0:  # adapt polygons to tab
                relative_polygon = []
                for point in self.polygon:
                    relative_polygon.append((x + point[0], y + point[1]))

                pygame.draw.polygon(screen,
                                    WHITE,
                                    relative_polygon,
                                    0)

    # remove this later, use self.contains instead (from pygame-widgets)
    def hover(self, mouse_x, mouse_y): 
        if self._x <= mouse_x <= self._x + self._width and self._y <= mouse_y <= self._y + self._height:
            return True
        return False

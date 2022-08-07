from pygame_widgets.slider import Slider as WidgetsSlider

from classes.tab import Tab

from constants import SCALE, WHITE, LIGHT_GRAY


class Slider(WidgetsSlider):
    def __init__(self,
                 screen,
                 x,
                 y,
                 width,
                 height,
                 min: int = 1000,
                 max: int = 1000000000,
                 step: int = 1000,
                 handle_color=WHITE,
                 color=LIGHT_GRAY,
                 start_on: int = SCALE,
                 tab: Tab = None,
                 ):
        super().__init__(screen, x, y, width, height, min=min, max=max, step=step, colour=color,
                         handleColour=handle_color, initial=start_on)
        screen_width, screen_height = screen.get_size()

        self.x = x
        self.x_percent = x / screen_width
        self.y = y
        self.y_percent = y / screen_height

        self.tab = tab

        self.enabled = True

    def update(self,
               engine_screen_width,
               engine_screen_height):
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
            y = self.y_percent * engine_screen_height - self.get('height')
            if y + self._height > engine_screen_height:
                y = engine_screen_height - self._height
            self.set('y', int(y))
        self.set('x', int(x))

        if self.enabled:
            self.show()
            self.enable()
        else:
            self.hide()
            self.disable()

    def hover(self, mouse_x, mouse_y):  # I think widgets has a contains() that is better than this
        if self.curved:
            curve_radius = 10
        else:
            curve_radius = 0
        if self._x - curve_radius <= mouse_x <= self._x + self._width + curve_radius and self._y <= mouse_y <= self._y + self._height:
            return True
        return False

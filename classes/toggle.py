from pygame_widgets.toggle import Toggle as WidgetToggle

from classes.tab import Tab




class Toggle(WidgetToggle):
    def __init__(self,
                 screen,
                 x,
                 y,
                 width,
                 height,
                 tab: Tab = None,
                 start_on: bool = True
                 ):
        super().__init__(screen, x, y, width, height, startOn=start_on)
        # screen_width, screen_height = screen.get_size()  # not necessary, yet anyway

        self.x = x
        self.tab = tab

        self.enabled = True

    def update(self,
               screen_width):
        if self.tab is not None:
            if self.tab.current_width == 0:
                self.enabled = False
            else:
                self.enabled = True
                if self.tab.side == 'Left':
                    x = int(self.x + self.tab.current_width - self.tab.width)
                else:
                    x = int(self.x + screen_width - self.tab.current_width)
                self.set('x', x)


        if self.enabled:
            self.show()
            self.enable()
        else:
            self.hide()
            self.disable()

            # hide() does not work for some reason
            # disables, but always visible
            # added quick fix
            x = -50
            self.set('x', x)



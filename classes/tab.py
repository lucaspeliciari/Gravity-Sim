import pygame.display
import pygame.draw
import pygame.font

from common_functions import lerp
from constants import *


class Tab:
    def __init__(self,
                 engine_screen_width: int,
                 side: str = 'Left',
                 buttons: list = None,
                 color: tuple = BLACK,
                 border_color: tuple = WHITE,
                 border_pin_color: tuple = LIGHT_GRAY
                 ):
        if buttons is None:
            buttons = []
        self.hidden = False
        self.side = side
        self.width = engine_screen_width / 6
        self.current_width = 0  # absolute value of width
        self.border_position = 0  # relative position to screen
        self.border_thickness = 10
        self.triangle_points = []  # tab triangle, should only be calculated when necessary instead of every frame
        self.pin = []  # same as above

        self.color = color
        self.border_color = border_color
        self.border_pin_color = border_pin_color

        self.extended = True  # if fully extended
        self.collapsed = not self.extended
        self.timer = 0
        self.start_timer = 0
        self.time_to_extend = 0.2
        self.delay_to_collapse = 0.5
        self.time_to_collapse = 0.3
        self.movement = 0  # -1 to collapse, 0 to stand still, 1 to extend
        self.timer_multiplier = 0

        self.buttons = buttons
        for button in self.buttons:
            button.tab = self

        self.texts = []

        self.pinned = False
        self.triangle = ()
        self.pin_triangle = ()

        self.mouse_button_pressed = False

    def update(self,
               screen,
               mouse_buttons,
               mouse_position,
               sim,
               engine,
               help_menu
               ):
        self.calculate_timer_multiplier()

        self.current_width = self.width * self.timer_multiplier

        if self.side == 'Left':  # still messy
            self.border_position = self.current_width
            border_end = self.border_position + self.border_thickness / 2
            triangle_side_multiplier = 1
        else:
            self.border_position = engine.screen_width - self.current_width
            border_end = self.border_position - self.border_thickness / 2
            triangle_side_multiplier = -1

        self.triangle_points = [(self.border_position, engine.screen_height / 2 - 50),
                                (self.border_position, engine.screen_height / 2 + 50),
                                (self.border_position + triangle_side_multiplier * 25, engine.screen_height / 2)]

        if not self.pinned:  # not very good or identical triangles
            self.pin = [(border_end, engine.screen_height / 2 - 18),
                        (border_end, engine.screen_height / 2 + 18),
                        (border_end + triangle_side_multiplier * 16, engine.screen_height / 2)]
        else:
            self.pin = [(border_end + triangle_side_multiplier * 12, engine.screen_height / 2 - 13),
                        (border_end + triangle_side_multiplier * 12, engine.screen_height / 2 + 13),
                        (border_end - triangle_side_multiplier * 5, engine.screen_height / 2)]
        self.pin_tab(mouse_buttons, mouse_position, help_menu)
        self.move(engine.timer, mouse_position, engine.screen_width, help_menu)

        self.texts = []
        self.texts = sim.return_texts(self.side)
        self.draw(screen, mouse_buttons, mouse_position, sim, engine)

    def tab_hover(self,
                  mouse: tuple,
                  triangle_only: bool = False
                  ):

        mouse_x, mouse_y = mouse[0], mouse[1]

        # TRIANGLE HOVER
        triangle_hover = False
        try:
            m_upper_x = self.triangle_points[0][0] - self.triangle_points[2][0]
            m_upper_y = self.triangle_points[0][1] - self.triangle_points[2][1]
            m_lower_x = self.triangle_points[1][0] - self.triangle_points[2][0]
            m_lower_y = self.triangle_points[1][1] - self.triangle_points[2][1]
            m_upper = m_upper_y / m_upper_x
            c = self.triangle_points[2][1] - m_upper * self.triangle_points[2][0]
            y_upper = m_upper * mouse_x + c
            m_lower = m_lower_y / m_lower_x
            c = self.triangle_points[2][1] - m_lower * self.triangle_points[2][0]
            y_lower = m_lower * mouse_x + c
            if y_upper <= mouse_y <= y_lower:
                if not triangle_only:
                    triangle_hover = True
                else:
                    if self.side == 'Left':
                        x1 = self.border_position - self.border_thickness / 2
                        x2 = self.border_position + self.triangle_points[2][0]
                    else:
                        x1 = self.border_position + self.border_thickness / 2
                        x2 = self.triangle_points[2][0]
                    min_x = min(x1, x2)
                    max_x = max(x1, x2)
                    if min_x <= mouse_x <= max_x:
                        triangle_hover = True
        except IndexError:
            print('self.triangle_points should be run only once and before anything else!')

        if not triangle_only:
            # BORDER HOVER
            border_hover = False

            if self.side == 'Left':
                if mouse_x <= self.border_position + self.border_thickness / 2:
                    border_hover = True
            else:
                if mouse_x >= self.border_position - self.border_thickness / 2:
                    border_hover = True

            tab_hover = False
            if triangle_hover or border_hover:
                tab_hover = True

        else:
            tab_hover = triangle_hover
        return tab_hover

    def pin_tab(self,
                mouse_buttons: tuple,
                mouse_position: tuple,
                help_menu: bool
                ):

        if not help_menu and len(mouse_buttons) > 1:  # len(mouse_buttons) > 1 really shouldn't be needed, but it is
            if self.extended and mouse_buttons[0]:
                if self.tab_hover(mouse_position, triangle_only=True):
                    if not self.mouse_button_pressed:
                        self.pinned = not self.pinned
                        self.mouse_button_pressed = True
                else:
                    self.mouse_button_pressed = False
            else:
                self.mouse_button_pressed = False

    def move(self,
             current_timer: float,
             mouse_position: tuple,
             engine_screen_width: int,
             help_menu
             ):

        if not help_menu:
            if not self.pinned:
                mouse_on_tab = self.tab_hover(mouse_position)
                if mouse_on_tab:
                    if self.movement == 1:
                        pass

                    elif self.movement == 0:
                        if self.extended:
                            self.start_timer = current_timer
                        else:
                            self.movement = 1
                            self.collapsed = False

                    elif self.movement == -1:
                        self.extended = True
                        self.movement = 0
                        self.start_timer = current_timer

                if self.movement == 1 and self.timer >= self.time_to_extend:
                    self.extended = True
                    self.movement = 0
                    self.start_timer = current_timer

                elif self.movement == 0:
                    if self.extended and self.timer >= self.delay_to_collapse:
                        self.extended = False
                        self.movement = -1
                        self.start_timer = current_timer
                    elif not self.extended:
                        self.start_timer = current_timer

                elif self.movement == -1:
                    if self.timer >= self.time_to_collapse:
                        self.movement = 0
                        self.collapsed = True

            else:
                self.extended = True

            self.timer = current_timer - self.start_timer
        else:
            self.extended = False
            self.movement = 0
            self.border_position = 0
            self.current_width = 0

    def draw(self,
             screen,
             mouse_buttons,
             mouse_position,
             sim,
             engine
             ):

        if self.side == 'Left':
            x = self.border_position - self.current_width
        else:
            x = engine.screen_width - self.current_width + 1  # +1 to hide gap to the right of the tab
        pygame.draw.rect(screen,
                         self.color,
                         (x, 0, self.current_width, engine.screen_height),
                         0)

        pygame.draw.line(screen,
                         self.border_color,
                         (self.border_position, 0),
                         (self.border_position, engine.screen_height),
                         self.border_thickness)

        pygame.draw.polygon(screen,
                            self.border_color,
                            self.triangle_points,
                            0)

        pygame.draw.polygon(screen,
                            self.border_pin_color,
                            self.pin,
                            0)

        self.draw_buttons(screen, mouse_buttons, mouse_position, sim, engine)
        self.draw_texts(screen, sim, engine)

    def draw_buttons(self,
                     screen,
                     mouse_buttons,
                     mouse_position,
                     sim,
                     engine
                     ):

        if not self.collapsed:
            if sim.focused_body_index == -1:
                button_condition = -1  # if nothing selected
            else:
                button_condition = 0  # if body selected
            for button in self.buttons:
                button.update(screen, mouse_buttons, mouse_position, sim.self_functions, engine.screen_width,
                              button_condition)

    def draw_texts(self,
                   screen,
                   sim,
                   engine
                   ):
        tab_current_width = self.width * self.timer_multiplier

        x = tab_current_width - self.width

        if self.side == 'Right':
            x = engine.screen_width - tab_current_width

        if sim.focused_body_index != -1:
            for text_tuple in self.texts:
                for i, text in enumerate(text_tuple):
                    text_width, text_height = engine.font.size(str(text))
                    screen.blit(engine.font.render(str(text),
                                                   True,
                                                   WHITE),
                                (x + self.border_thickness, 10 + i * text_height))
        else:
            for i, text in enumerate(self.texts):
                text_width, text_height = engine.font.size(str(text))
                screen.blit(engine.font.render(str(text),
                                               True,
                                               WHITE),
                            (x + self.border_thickness, 10 + i * text_height))

    def calculate_timer_multiplier(self):
        timer_multiplier_width = 0
        timer_multiplier_height = 0

        if self.movement == 1:
            timer_multiplier_width = lerp(0, 1, self.timer / self.time_to_extend)
        elif self.movement == -1:
            timer_multiplier_width = lerp(1, 0, self.timer / self.time_to_collapse)
        elif self.extended:
            timer_multiplier_width = 1

        if self.side == 'Left' or self.side == 'Right':
            timer_multiplier = timer_multiplier_width
        else:
            timer_multiplier = timer_multiplier_height

        self.timer_multiplier = timer_multiplier

    def __str__(self):
        return self.side

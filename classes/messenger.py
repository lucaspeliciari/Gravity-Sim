import pygame.font

from constants import WHITE
from render.universe import draw_message


class Message():
    def __init__(self, text, timer, color, font_size, sticky):
        self.text = text
        self.timer = timer
        self.color = color
        self.font_size = font_size
        self.sticky = sticky  # these are never popped when adding new messages to already full log i.e. only popped when timer <= 0


class Messenger:
    def __init__(self, max_messages_in_log):
        self.log = []
        self.max_messages_in_log = max_messages_in_log

    def update(self,
               screen,
               screen_size,
               delta_time
               ):
        current_vertical_offset = 0
        for message in self.log:
            font = pygame.font.SysFont("monospace", message.font_size)
            current_vertical_offset = draw_message(screen, font, screen_size, current_vertical_offset, message.text,
                                                   color=message.color)
            message.timer -= delta_time / 1000

        to_pop_list = []
        for i, message in enumerate(self.log):
            if message.timer <= 0:
                to_pop_list.append(i)
        for pop_index in reversed(to_pop_list):
            try:
                self.log.pop(pop_index)
            except IndexError:
                print("EXCEPTION IN MESSENGER: INDEX OUT OF RANGE WHEN POPPING LISTS")

    def add(self,
            text: str,
            message_time: float = 3,
            color: tuple = WHITE,
            font_size: int = 15,
            sticky: bool = False
            ):

        self.log.append(Message(text, message_time, color, font_size, sticky))
        if len(self.log) > self.max_messages_in_log:
            for i, message in enumerate(self.log):
                if not message.sticky:
                    self.log.pop(i)
                    break

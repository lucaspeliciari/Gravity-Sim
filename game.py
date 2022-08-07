from constants import SPLASH_SCREEN


class Game:
    def __init__(self,
                 state: int = SPLASH_SCREEN
                 ):
        self.state = state
        self.running = True  # maybe not necessary

        self.splash_screen_time = 3

        self.mousedown_position = [1000, 1000]
        self.holding_lmb = False
        self.holding_rmb = False

        self.holding_mb = [False, False, False]

        # to avoid panning when first holding RMB on widget (when "dragging" widget
        self.first_click_on_widget = [False, False, False]

        self.help = False  # pops up a little help window
        self.credits = False  # pops up a little credits window

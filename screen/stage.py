from kivy.uix.widget import Widget


APPEAR_COMMAND = 'appear'

COMMANDS = (APPEAR_COMMAND, )


class Stage(Widget):
    def update(self, dt):
        pass

    def set_next(self, data):
        for c in COMMANDS:
            if c in data:
                pass

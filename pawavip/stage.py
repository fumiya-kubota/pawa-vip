from kivy.uix.anchorlayout import AnchorLayout
from kivy.animation import Animation, AnimationTransition
from kivy.uix.image import Image
import yaml
from kivy.uix.button import Button
from kivy.uix.widget import Widget


APPEAR_COMMAND = 'appear'
EXPRESSION_COMMAND = 'expression'
COMMANDS = (APPEAR_COMMAND, )


class Actor(Widget):
    pass


class Stage(AnchorLayout):
    # : :type: dict
    _data = None

    # : :type: dict
    _actors = None

    # : :type: dict
    _stage_looking = None

    def __init__(self, **kwargs):
        super(Stage, self).__init__(**kwargs)

    def update(self, dt):
        pass

    def set_next(self, val):
        for command in COMMANDS:
            if command in val:
                self.data = val
                return
        else:
            self.data = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, val):
        self._data = val
        if val:
            if APPEAR_COMMAND in val:
                pass

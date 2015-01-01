from kivy.animation import Animation, AnimationTransition
from kivy.graphics.context_instructions import Color
from kivy.uix.image import Image
from kivy.graphics.vertex_instructions import Rectangle
import yaml
from kivy.uix.button import Button
from kivy.uix.widget import Widget


APPEAR_COMMAND = 'appear'
EXPRESSION_COMMAND = 'expression'
COMMANDS = (APPEAR_COMMAND, )


class Actor(Widget):
    pass


class Stage(Widget):
    # : :type: dict
    _data = None

    # : :type: dict
    _actors = None

    # : :type: dict
    _stage_looking = None

    def __init__(self, **kwargs):
        super(Stage, self).__init__(**kwargs)
        with open('scenario/actors.yaml') as fp:
            self._actors = yaml.load(fp)

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
                actor_name = val[APPEAR_COMMAND]
                expression_name = val[EXPRESSION_COMMAND]
                expressions = self._actors[actor_name]
                file_name = expressions[expression_name]
                path = '{}/{}/{}'.format('scenario',
                                         actor_name,
                                         file_name)
                actor = Image(source=path)
                actor.size = actor.texture_size
                actor.pos = (-actor.width / 2, 225)

                self.add_widget(actor)

                animation = Animation(x=100, duration=0.15, t=AnimationTransition.in_out_cubic)
                animation.start(actor)


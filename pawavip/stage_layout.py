from kivy.animation import Animation, AnimationTransition
from kivy.uix.image import Image
from kivy.uix.layout import Layout
from pawavip.manager import sample_scenario


ACTOR_CENTER = 125


class Actor(Image):
    # :type: str
    _direction = 'left'

    def __init__(self, **kwargs):
        super(Actor, self).__init__(**kwargs)
        self.size = self.texture_size

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, val):
        self._direction = val


class StageLayout(Layout):
    # :type: Actor
    _left_actor = None

    @property
    def left_actor(self):
        return self._left_actor

    @left_actor.setter
    def left_actor(self, val):
        if self._left_actor:
            self.remove_widget(self._left_actor)
        self._left_actor = val
        self.add_widget(self._left_actor)

    # :type: Actor
    _right_actor = None

    @property
    def right_actor(self):
        return self._right_actor

    @right_actor.setter
    def right_actor(self, val):
        if self._right_actor:
            self.remove_widget(self._right_actor)
        self._right_actor = val
        self.add_widget(self._right_actor)

    def __init__(self, **kwargs):
        super(StageLayout, self).__init__(**kwargs)
        self.bind(
            children=self._trigger_layout,
            parent=self._trigger_layout,
            size=self._trigger_layout,
            pos=self._trigger_layout)

    def do_layout(self, *largs):
        if self.left_actor:
            self.left_actor.y = self.y
            self.left_actor.center_x = self.x + ACTOR_CENTER

        if self.right_actor:
            self.right_actor.y = self.y
            self.right_actor.center_x = self.width - ACTOR_CENTER

    def appear(self, data):
        info = {
            'expression': 'normal',
            'position': 'left',
            'direction': 'right',
            'animation': {
                'from': 'left',
                'to': 'left'
            }
        }
        info.update(data)
        actor = Actor(source=sample_scenario.actor_path(info['actor'], info['expression']))
        actor.direction = info['direction']

        animation = None
        position = info['position']
        if info['animation']:
            a = info['animation']
            if a['from'] == 'left':
                actor.center_x = self.x
            else:
                actor.center_x = self.width

            position = a['to']
            animation = Animation(center_x=self.x + ACTOR_CENTER if position == 'left' else self.width - ACTOR_CENTER,
                                  duration=0.1, transition=AnimationTransition.in_out_circ)

        self.add_widget(actor)

        def set_actor(a, b):
            if position == 'left':
                self._left_actor = actor
            else:
                self._right_actor = actor

        if animation:
            animation.bind(on_complete=set_actor)
        else:
            set_actor(None, None)


def background_transition(self, animate=False):
    pass

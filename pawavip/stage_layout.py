from kivy.graphics.context_instructions import Rotate, PushMatrix, PopMatrix
from kivy.properties import StringProperty
from kivy.animation import Animation, AnimationTransition
from kivy.uix.image import Image
from kivy.uix.layout import Layout
from pawavip.manager import sample_scenario


ACTOR_CENTER = 125

EXPRESSION_COMMAND = 'exp'
ACTOR_COMMAND = 'actor'
ID_COMMAND = 'id'
DIRECTION_COMMAND = 'dir'
ANIMATION_COMMAND = 'animation'
POSITION_COMMAND = 'position'


class Actor(Image):
    # :type: str
    direction = StringProperty(None)

    # :type: str
    name = None

    def __init__(self, **kwargs):
        super(Actor, self).__init__(**kwargs)
        self.size = self.texture_size


class StageLayout(Layout):
    # :type: dict
    _actors = {}

    def add_actor(self, identifier, actor):
        if identifier in self._actors:
            old_actor = actor[identifier]
            self.remove_widget(old_actor)
        self._actors[identifier] = actor
        self.add_widget(actor)

    def get_actor(self, identifier):
        return self._actors.get(identifier)

    def remove_actor(self, identifier):
        actor = self._actors.pop(identifier)
        if actor:
            self.remove_widget(actor)
            del self._actors[identifier]

    def __init__(self, **kwargs):
        super(StageLayout, self).__init__(**kwargs)
        self.bind(
            children=self._trigger_layout,
            parent=self._trigger_layout,
            size=self._trigger_layout,
            pos=self._trigger_layout)

    def do_layout(self, *largs):
        for actor in self._actors.itervalues():
            actor.y = self.y

    def appear(self, data):
        actor_name = data[ACTOR_COMMAND]
        actor = Actor(source=sample_scenario.actor_path(actor_name, data[EXPRESSION_COMMAND]))
        actor.direction = data[DIRECTION_COMMAND]
        actor.name = actor_name
        self.add_actor(data.get(ID_COMMAND, actor_name), actor)
        if ANIMATION_COMMAND in data:
            animate = data[ANIMATION_COMMAND]
            from_pos = self._get_pos(animate['from'])
            to_pos = self._get_pos(animate['to'])
            actor.center_x = from_pos
            animation = Animation(center_x=to_pos, duration=0.2, t=AnimationTransition.in_out_cubic)
            animation.start(actor)
        elif POSITION_COMMAND in data:
            pos = self._get_pos(data[POSITION_COMMAND])
            actor.center_x = pos

    def _get_pos(self, pos):
        if pos == 'l':
            return self.x + ACTOR_CENTER
        elif pos == 'r':
            return self.x + 800 - ACTOR_CENTER
        elif pos == 'le':
            return self.x
        elif pos == 're':
            return self.x + 800
        else:
            return pos

    def change_expression(self, expression):
        actor = self.get_actor(expression[ID_COMMAND])
        if actor:
            actor_name = actor.name
            actor.source = sample_scenario.actor_path(actor_name, expression[EXPRESSION_COMMAND])
            actor.size = actor.texture_size

    def background_transition(self, animate=False):
        pass

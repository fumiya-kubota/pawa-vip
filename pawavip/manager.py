
# -*- coding: utf-8 -*-
from collections import defaultdict
from kivy.event import EventDispatcher
import yaml
import os

PATH_ROOT = 'story'
SCENARIO_FILE = 'scenario.yaml'
ACTORS_FILE = 'actors/actors.yaml'

SAY_COMMAND = 'say'
CLEAR_COMMAND = 'clear'
SLOW_COMMAND = 'slow'
COLOR_COMMAND = 'color'
SPEAKER_COMMAND = 'speaker'

APPEAR_COMMAND = 'appear'
EXPRESSION_COMMAND = 'exp'
DIRECTION_COMMAND = 'dir'
MOVE_COMMAND = 'move'
CONTINUE_COMMAND = 'continue'
REMOVE_COMMAND = 'remove'

ACTOR_COMMAND = 'actor'
ID_COMMAND = 'id'
ANIMATION_COMMAND = 'animation'
POSITION_COMMAND = 'position'
CHAIN_COMMAND = 'chain'


class MessageManager(EventDispatcher):
    #: :type: tuple
    scenario = None

    #: :type: int
    index = 0

    __events__ = ('on_start', 'on_end', )

    def __init__(self, scenario):
        self.scenario = scenario

    def next_commands(self):
        if self.index == len(self.scenario):
            self.dispatch('on_end')
            return

        commands = []
        while True:
            data = self.scenario[self.index]
            commands.append(data)
            self.index += 1
            if SAY_COMMAND in data or CHAIN_COMMAND in data:
                break
        return commands

    def on_end(self, *args):
        pass

    def on_start(self, *args):
        pass


class SuccessManager(object):
    # : :type: int
    time = 0

    #: :type:defaultdict
    _flags = defaultdict(int)

    # : :type: str
    file_root = None

    # : :type: str
    name = None

    # : :type: dict
    _actors = None

    # : :type: dict
    _event_calendar = None

    # : :type: str
    _scenario_name = None

    @property
    def scenario_name(self):
        return self._scenario_name

    @scenario_name.setter
    def scenario_name(self, val):
        self._scenario_name = val
        self.file_root = os.path.join(PATH_ROOT, self._scenario_name)
        scenario_file_name = os.path.join(self.file_root, SCENARIO_FILE)
        if not os.path.exists(scenario_file_name):
            raise

        with open(scenario_file_name) as fp:
            data = yaml.load(fp)

        self.name = data.get('name', '')
        self._event_calendar = data.get('event_calendar', {})
        with open(os.path.join(self.file_root, ACTORS_FILE)) as fp:
            data = yaml.load(fp)
        self._actors = data

    def actor_path(self, actor_name, expression):
        expression_file = self._actors[actor_name][expression]
        return os.path.join(self.file_root, 'actors', actor_name, expression_file)

    def pop_fixed_event_before(self):
        event = self._event_calendar.get(self.time)
        if 'before' in event:
            return self._event_pop(event['before'])

    def pop_fixed_event_after(self):
        event = self._event_calendar.get(self.time)
        if 'after' in event:
            return self._event_pop(event['after'])

    def _event_pop(self, event):
        with open(os.path.join(self.file_root, 'events', '{}.yaml'.format(event))) as fp:
            data = yaml.load(fp)
        return MessageManager(data)

    def load_save_data(self, fp):
        pass

sample_scenario = SuccessManager()

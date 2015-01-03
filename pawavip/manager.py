
# -*- coding: utf-8 -*-
from collections import defaultdict
import yaml
import os

PATH_ROOT = 'story'
SCENARIO_FILE = 'scenario.yaml'
ACTORS_FILE = 'actors/actors.yaml'


class GeneralEvent(object):
    #: :type: tuple
    scenario = None

    #: :type: int
    index = 0

    def __init__(self, scenario):
        self.scenario = scenario

    def __iter__(self):
        return self

    def next(self):
        if self.index == len(self.scenario):
            raise StopIteration
        data = self.scenario[self.index]
        self.index += 1
        return data


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
        return GeneralEvent(data)

    def load_save_data(self, fp):
        pass

sample_scenario = SuccessManager()

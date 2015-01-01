# cording:utf-8
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import yaml
from screen.general_event import GeneralEvent
from screen.message_board import MessageBoard
from screen.stage import Stage

Builder.load_file('screen/screen.kv')


class AdventureScreen(Screen):
    #: :type: MessageBoard
    board = ObjectProperty(None)

    #: :type:Stage
    stage = ObjectProperty(None)

    def __init__(self, **kw):
        super(AdventureScreen, self).__init__(**kw)
        with open('scenario/start.yaml') as fp:
            scenario = yaml.load(fp)
        self.event = GeneralEvent(scenario)

    def update(self, dt):
        self.board.update(dt)
        self.stage.update(dt)

    def on_enter(self, *args):
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.proceed_scenario()

    def on_leave(self, *args):
        Clock.unschedule(self.update, True)

    def click(self):
        if self.board.processing:
            self.board.display_all()
            return
        self.proceed_scenario()

    def proceed_scenario(self):
        self.board.waiting = False
        while not self.board.waiting:
            if self.event:
                try:
                    command = self.event.next()
                except StopIteration:
                    self.event = None
                    return
                self.board.set_next(command)
                self.stage.set_next(command)
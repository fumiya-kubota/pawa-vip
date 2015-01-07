# cording:utf-8
import weakref
from kivy.properties import ObjectProperty

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from pawavip.stage import Stage
from pawavip.message_board import MessageBoard
from pawavip.manager import sample_scenario

Builder.load_file('pawavip/adventure.kv')


class AdventureScreen(Screen):
    # : :type: MessageBoard
    board = ObjectProperty(None)

    #: :type:Stage
    stage = ObjectProperty(None)

    #: :type:GeneralEvent
    event = None

    def __init__(self, **kw):
        super(AdventureScreen, self).__init__(**kw)

    def update(self, dt):
        self.board.update(dt)

    def on_enter(self, *args):
        weakref_proxy = weakref.proxy(self)
        self.board.adventure_screen = weakref_proxy
        self.stage.adventure_screen = weakref_proxy
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        sample_scenario.scenario_name = 'sample'
        self.event = sample_scenario.pop_fixed_event_before()
        self.proceed_scenario()

    def on_leave(self, *args):
        Clock.unschedule(self.update, True)

    def click(self):
        if self.stage.next and not self.board.processing:
            self.proceed_scenario()

    def proceed_scenario(self):
        self.board.next = self.stage.next = True
        while self.board.next and self.stage.next:
            if self.event:
                try:
                    command = self.event.next()
                except StopIteration:
                    self.event = None
                    return
                self.stage.set_next(command)
                self.board.set_next(command)

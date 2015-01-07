from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from pawavip.stage_layout import StageLayout

APPEAR_COMMAND = 'appear'
EXPRESSION_COMMAND = 'exp'
DIRECTION_COMMAND = 'dir'
MOVE_COMMAND = 'move'
CONTINUE_COMMAND = 'continue'
REMOVE_COMMAND = 'remove'

COMMANDS = (APPEAR_COMMAND, EXPRESSION_COMMAND, DIRECTION_COMMAND, MOVE_COMMAND, REMOVE_COMMAND)


class Stage(AnchorLayout):
    # : :type: StageLayout
    stage_layout = ObjectProperty(None)

    # : :type: bool
    next = True

    # : :type: AdventureScreen
    adventure_screen = None

    # : :type: dict
    _data = None

    # : :type: dict
    _actors = None

    # : :type: dict
    _stage_looking = None

    def __init__(self, **kwargs):
        super(Stage, self).__init__(**kwargs)

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
            self.next = True
            if APPEAR_COMMAND in val:
                self.next = self.stage_layout.appear(val[APPEAR_COMMAND], self.adventure_screen.proceed_scenario)
            if EXPRESSION_COMMAND in val:
                self.stage_layout.change_expression(val[EXPRESSION_COMMAND])
            if DIRECTION_COMMAND in val:
                self.stage_layout.change_direction(val[DIRECTION_COMMAND])
            if MOVE_COMMAND in val:
                self.next = self.stage_layout.move(val[MOVE_COMMAND], self.adventure_screen.proceed_scenario)
            if REMOVE_COMMAND in val:
                self.stage_layout.remove_actor(val[REMOVE_COMMAND])
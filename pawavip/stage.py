from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from pawavip.stage_layout import StageLayout

APPEAR_COMMAND = 'appear'
EXPRESSION_COMMAND = 'exp'

COMMANDS = (APPEAR_COMMAND, EXPRESSION_COMMAND)

class Stage(AnchorLayout):
    # : :type: StageLayout
    stage_layout = ObjectProperty(None)

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
                self.stage_layout.appear(val[APPEAR_COMMAND])
            if EXPRESSION_COMMAND in val:
                self.stage_layout.change_expression(val[EXPRESSION_COMMAND])
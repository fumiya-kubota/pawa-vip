from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from pawavip.stage_layout import StageLayout
from pawavip import manager

COMMANDS = (manager.APPEAR_COMMAND,
            manager.EXPRESSION_COMMAND,
            manager.DIRECTION_COMMAND,
            manager.MOVE_COMMAND,
            manager.REMOVE_COMMAND)


class Stage(AnchorLayout):
    __events__ = ('on_continue', )

    def on_continue(self, *args):
        pass

    # : :type: StageLayout
    stage_layout = ObjectProperty(None)

    # : :type: dict
    _actors = None

    # : :type: dict
    _stage_looking = None

    # : :type: bool
    next = False

    def __init__(self, **kwargs):
        super(Stage, self).__init__(**kwargs)

    def set_commands(self, commands):
        for command in commands:
            for c in COMMANDS:
                if c in command:
                    break
            else:
                continue

            completion = self.dispatch_continue if manager.CHAIN_COMMAND in command else None

            if manager.APPEAR_COMMAND in command:
                self.stage_layout.appear(command[manager.APPEAR_COMMAND], completion)
                completion = None

            if manager.EXPRESSION_COMMAND in command:
                self.stage_layout.change_expression(command[manager.EXPRESSION_COMMAND])

            if manager.DIRECTION_COMMAND in command:
                self.stage_layout.change_direction(command[manager.DIRECTION_COMMAND])

            if manager.MOVE_COMMAND in command:
                self.stage_layout.move(command[manager.MOVE_COMMAND], completion)
                completion = None

            if manager.REMOVE_COMMAND in command:
                self.stage_layout.remove_actor(command[manager.REMOVE_COMMAND])

            if completion:
                completion()

    def dispatch_continue(self):
        self.dispatch('on_continue')
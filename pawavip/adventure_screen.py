# cording:utf-8
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from pawavip.stage import Stage
from pawavip.message_board import MessageBoard
from pawavip.manager import sample_scenario

Builder.load_string('''
<Actor>
    canvas.before:
        PushMatrix
        Rotate:
            angle: 0 if self.direction == 'r' else 180
            axis: 0, 1, 0
            origin: self.center
    canvas.after:
        PopMatrix

<AdventureScreen>
    board: message_board
    stage: stage
    Widget:
        size_hint: 1., None
        pos_hint: {'top': 1}
        height: 125
        canvas.before:
            Color:
                rgb: 1, 0, 0
            Rectangle:
                pos: self.pos
                size: self.size

    Stage:
        id: stage
        size_hint: 1., None
        pos_hint: {'top': 1 - 125. / 600}
        anchor_y: 'bottom'
        anchor_x: 'left'
        height: 250
        stage_layout: stage_layout
        StageLayout:
            id: stage_layout
            canvas.before:
                Color:
                    rgba: 1, 0, 1, 0.5
                Rectangle:
                    pos: self.pos
                    size: self.size

    MessageBoard:
        id: message_board
        size_hint: 1., None
        pos_hint: {'bottom': 1}
        height: 225
        on_touch_down: root.click()
        canvas.before:
            Color:
                rgb: 1, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size
''')


class AdventureScreen(Screen):
    # : :type: MessageBoard
    board = ObjectProperty(None)

    # : :type:Stage
    stage = ObjectProperty(None)

    #: :type:MessageManager
    message_manager = None

    #: :type:bool
    is_idling = None

    def __init__(self, **kw):
        super(AdventureScreen, self).__init__(**kw)
    
    def on_enter(self, *args):
        self.do_layout()
        sample_scenario.scenario_name = 'sample'
        self.message_manager = sample_scenario.pop_fixed_event_before()
        self.proceed_scenario()
        self.board.bind(on_idling=self.on_idling)
        self.board.bind(on_continue=self.proceed_scenario)
        self.stage.bind(on_continue=self.proceed_scenario)

    def on_idling(self, *args):
        self.is_idling = True

    def click(self):
        if self.is_idling:
            self.is_idling = False
            commands = self.message_manager.next_commands()
            if commands:
                self.stage.set_commands(commands)
                self.board.set_commands(commands)

    def proceed_scenario(self, *args):
        self.is_idling = True
        self.click()

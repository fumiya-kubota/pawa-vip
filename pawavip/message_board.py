# coding=utf-8

from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from pawavip import manager

COMMANDS = (manager.SAY_COMMAND,
            manager.CLEAR_COMMAND,
            manager.SLOW_COMMAND,
            manager.SPEAKER_COMMAND)

SPEED_DEFAULT = 0.04
SLOW_SPEED_DEFAULT = 0.1


class Letter(Label):
    # : :type: int
    col_number = 0

    # : :type: int
    row_number = 0


Builder.load_string('''
<MessageBoard>:
    message_area: area
    Widget:
        id: area
        size: self.parent.width - 20, self.parent.height - 50.
        x: self.parent.x + 10
        top: self.parent.height - 30
        canvas.before:
            Color:
                rgb: 0, 0, 0
            Rectangle:
                pos: self.pos
                size: self.size

    Widget:
        size: self.parent.width - 20, 30
        pos: self.parent.x + 10, self.parent.height - self.height
        canvas:
            Color:
                rgb: 1, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size

    Widget:
        size: self.parent.width - 20, 20
        pos: self.parent.x + 10, self.parent.height - 30 - self.height
        canvas:
            Color:
                rgb: 0, 0, 0
            Rectangle:
                pos: self.pos
                size: self.size
''')


class MessageBoard(Widget):
    __events__ = ('on_idling', 'on_continue')

    def on_idling(self, *args):
        pass

    def on_continue(self, *args):
        pass

    FONT_SIZE = 30
    LINE_SPAN = 10

    # : :type: int
    position = 0

    # : :type: str
    speaker = None

    # : :type: Widget
    message_area = ObjectProperty(None)

    # : :type: int
    _index = 0

    # : :type: float
    _speed = SPEED_DEFAULT

    # : :type: list
    _letters = []

    # : :type: int
    _col_number = 0

    # : :type: int
    _row_number = 0

    # : :type: list
    _message_queue = [[]]

    # : :type: list
    _display_letters = []

    # : :type: bool
    _continue = False

    def interpretation(self, command):
        if command:
            self._continue = command.get(manager.CONTINUE_COMMAND, False)

            if manager.SPEAKER_COMMAND in command and not self.speaker == command[manager.SPEAKER_COMMAND]:
                self._clear_board()
                self.speaker = command[manager.SPEAKER_COMMAND]

            if manager.CLEAR_COMMAND in command:
                self._clear_board()

            # slow
            if manager.SLOW_COMMAND in command:
                speed = SLOW_SPEED_DEFAULT if command[manager.SLOW_COMMAND] == 0 else command[manager.SLOW_COMMAND]
                self._speed = speed
            else:
                self._speed = SPEED_DEFAULT

            text_color = command.get(manager.COLOR_COMMAND, (1, 1, 1, 1))
            if manager.SAY_COMMAND in command:
                for c in command[manager.SAY_COMMAND]:
                    if c == '/':
                        self._next_row()
                    else:
                        l = Letter(text=c, font_size=self.FONT_SIZE,
                                   font_name='resource/fonts/rounded-mgenplus-1c-regular.ttf',
                                   size=(self.FONT_SIZE, self.FONT_SIZE), size_hint=(None, None), color=text_color)
                        self._letters.append(l)
                        l.pos = self._calc_pos()
                        l.col_number = self._col_number
                        l.row_number = self._row_number
                        self._message_queue[-1].append(l)
                        self._next_col()
                else:
                    if not self._continue and self._letters and not self._col_number == 0:
                        self._next_row()

    def max_row(self):
        return int(self.message_area.height / (self.FONT_SIZE + self.LINE_SPAN)) - 1

    @staticmethod
    def max_col():
        return 24  # int(self.message_area.width / self.FONT_SIZE) - 1

    def _update(self, dt):
        if self._index < len(self._letters):
            l = self._letters[self._index]
            self._show_letter(l)
            self._index += 1
        else:
            Clock.unschedule(self._update, True)
            if self._continue:
                self.dispatch('on_continue')
            else:
                self.dispatch('on_idling')

    def _show_letter(self, letter):
        def show_letter(a, b):
            self.message_area.add_widget(letter)
            self._display_letters.append(letter)

        if letter.col_number == 0 and letter.row_number > self.max_row():
            self._scroll_message(show_letter)
        else:
            show_letter(None, None)

    def set_commands(self, commands):
        for command in commands:
            self.interpretation(command)
        else:
            Clock.schedule_interval(self._update, self._speed)

    def _calc_pos(self):
        origin_x = self.message_area.x
        origin_y = self.message_area.height + self.message_area.y - self.FONT_SIZE - 20
        return origin_x + self.FONT_SIZE * self._col_number, origin_y - (self.FONT_SIZE + self.LINE_SPAN) * min(
            self._row_number,
            self.max_row())

    def _next_col(self):
        if self._col_number == self.max_col():
            self._next_row()
        else:
            self._col_number += 1

    def _next_row(self):
        self._col_number = 0
        self._row_number += 1
        self._message_queue.append([])

    def _scroll_message(self, completion):
        Clock.unschedule(self._update, True)

        old_row = self._message_queue.pop(0)

        def remove_old_row(a, b):
            Clock.schedule_interval(self._update, self._speed)
            completion(a, b)
            for label in old_row:
                self.message_area.remove_widget(label)
                self._display_letters.remove(label)

        animation = None
        for l in self._display_letters:
            animation = Animation(y=l.y + (self.FONT_SIZE + self.LINE_SPAN), duration=0.1)
            animation.start(l)
        else:
            animation.bind(on_complete=remove_old_row)

    def _clear_board(self):
        self._index = 0
        self._letters = []
        self._message_queue = [[]]
        self._col_number = self._row_number = 0
        self.message_area.clear_widgets()

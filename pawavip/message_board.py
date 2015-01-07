# coding=utf-8

from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.uix.widget import Widget

SAY_COMMAND = 'say'
CLEAR_COMMAND = 'clear'
SLOW_COMMAND = 'slow'
CONTINUE_COMMAND = 'continue'
COLOR_COMMAND = 'color'
SPEAKER_COMMAND = 'speaker'
COMMANDS = (SAY_COMMAND, CLEAR_COMMAND, SLOW_COMMAND, SPEAKER_COMMAND)

FONT_SIZE = 30
MAX_ROW = 3
MAX_COL = 23
SPEED_DEFAULT = 0.04
SLOW_SPEED_DEFAULT = 0.1
LINE_SPAN = 10


class Letter(Label):
    # : :type: int
    col_number = 0

    # : :type: int
    row_number = 0


class MessageBoard(Widget):
    # : :type: AdventureScreen
    adventure_screen = None

    # : :type: bool
    next = False

    # : :type: str
    speaker = None

    # : :type: Widget
    message_area = ObjectProperty(None)

    # : :type: bool
    processing = False

    # : :type: dict
    _data = None

    # : :type: float
    _total_time = 0

    # : :type: float
    _span_time = 0

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

    def update(self, dt):
        self._total_time += dt
        index_ = min(int((self._total_time - self._span_time) / self._speed + self._index),
                     len(self._letters))
        if self._index < index_:
            self._span_time = self._total_time
            l = self._letters[self._index]
            self._show_letter(l)
            self._index += 1
            if self._index == len(self._letters):
                self.processing = False
                if self._continue:
                    self.adventure_screen.proceed_scenario()

    # def display_all(self):
    #     for l in self._letters[self._index:]:
    #         self._show_letter(l, animate=False)
    #     self.processing = False
    #     self._index = len(self._letters)
    #     while self._continue:
    #         self.adventure_screen.proceed_scenario()
    #         self.display_all()

    def _show_letter(self, letter, animate=True):
        def show_letter(a, b):
            self.message_area.add_widget(letter)
            self._display_letters.append(letter)

        if letter.col_number == 0 and letter.row_number > MAX_ROW:
            self._scroll_message(show_letter, animate=animate)
        else:
            show_letter(None, None)

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
            self.processing = True
            # clean
            if SPEAKER_COMMAND in val and not self.speaker == val[SPEAKER_COMMAND]:
                self._clear_board()
                self.speaker = val[SPEAKER_COMMAND]

            if CLEAR_COMMAND in val:
                self._clear_board()

            # slow
            if SLOW_COMMAND in val:
                self._speed = SLOW_SPEED_DEFAULT if val[SLOW_COMMAND] == 0 else val[SLOW_COMMAND]
            else:
                self._speed = SPEED_DEFAULT

            if not self._continue and self._letters and not self._col_number == 0:
                self._next_row()

            text_color = val.get(COLOR_COMMAND, (1, 1, 1, 1))
            for c in val[SAY_COMMAND]:
                if c == '/':
                    self._next_row()
                else:
                    l = Letter(text=c, font_size=FONT_SIZE, font_name='resource/fonts/rounded-mgenplus-1c-regular.ttf',
                               size=(FONT_SIZE, FONT_SIZE), size_hint=(None, None), color=text_color)
                    self._letters.append(l)
                    l.pos = self._calc_pos()
                    l.col_number = self._col_number
                    l.row_number = self._row_number
                    self._message_queue[-1].append(l)
                    self._next_col()

            # continue命令が入っている場合は改行されない、入力待ちにもならない。
            self._continue = CONTINUE_COMMAND in val
            self.next = False
        else:
            self.next = True

    def _calc_pos(self):
        origin_x = self.message_area.x
        origin_y = self.message_area.height + self.message_area.y - FONT_SIZE - 20
        return origin_x + FONT_SIZE * self._col_number, origin_y - (FONT_SIZE + LINE_SPAN) * min(self._row_number,
                                                                                                 MAX_ROW)

    def _next_col(self):
        if self._col_number == MAX_COL:
            self._next_row()
        else:
            self._col_number += 1

    def _next_row(self):
        self._col_number = 0
        self._row_number += 1
        self._message_queue.append([])

    def _scroll_message(self, completion, animate=True):
        old_row = self._message_queue.pop(0)
        for l in old_row:
            self.message_area.remove_widget(l)
            self._display_letters.remove(l)

        animation = None
        for l in self._display_letters:
            animation = Animation(y=l.y + (FONT_SIZE + LINE_SPAN), duration=0.02 if animate else 0.0)
            animation.start(l)
        else:
            animation.bind(on_complete=completion)

    def _clear_board(self):
        self._index = 0
        self._letters = []
        self._message_queue = [[]]
        self._total_time = self._span_time = 0
        self._col_number = self._row_number = 0
        self.message_area.clear_widgets()
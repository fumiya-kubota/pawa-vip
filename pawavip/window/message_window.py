__author__ = 'sasau'

import pygame
from utils import image

LEFT_MARGIN = 20
RIGHT_MARGIN = 3
VERTICAL_MARGIN = 20
MAX_LINE = 3
MARKS = {
    '。',
    '、'
}


class Character(pygame.sprite.Sprite):
    def __init__(self, character, font, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(character, True, color)
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = pygame.Rect(0, 0, width, height)
        self.c = character
        self.move_y = 0

    def update(self):
        if not self.move_y <= 0:
            y = self.rect.height / 3
            self.rect.move_ip(0, -y)
            self.move_y -= y

    def scroll(self):
        self.move_y = self.rect.height


class MessageWindow(object):
    def __init__(self, rect):
        self.background = pygame.Surface((rect.width, rect.height))
        self.background.fill(pygame.Color('yellow'))
        # bg_image = image.load_image('message.png')
        # self.background.blit(bg_image, (0, 0))
        self.character_group = pygame.sprite.RenderUpdates()

        self._rect = rect
        self.skip = False
        self._waiting = False

        self.font = pygame.font.Font('resource/fonts/rounded-mgenplus-1c-regular.ttf', 24)
        self.color = pygame.Color('black')

        self._line_number = 0
        self._character_cursor = 0
        self._lines = []
        self._next_show_line = 0
        self.request_next_text = False
        self._origin_x = 0

        self._paragraph_number = 0
        self._paragraph = ()

        self._current_line = []
        self._real_line = []

    def next(self):
        if self._waiting:
            self._waiting = False
            self._character_cursor = 0
            self._line_number += 1
            self._new_line()
            if self._line_number >= len(self._lines):
                self.request_next_text = True
                self.clean()
                self._paragraph_number += 1
                self.next_text()

    def update(self):
        if not self.request_next_text:
            if self._character_cursor < len(self._lines[self._line_number]):
                character = self._lines[self._line_number][self._character_cursor]
                if character is None:
                    self._character_cursor += 1
                    character = self._lines[self._line_number][self._character_cursor]
                    self._new_line()
                elif character.c not in MARKS and self._rect.width < LEFT_MARGIN + RIGHT_MARGIN + self._origin_x + character.rect.width:
                    self._new_line()

                self._current_line.append(character)
                character.rect.left = LEFT_MARGIN + self._origin_x
                character.rect.top = self._rect.top + VERTICAL_MARGIN + character.rect.height * self._next_show_line
                self.character_group.add(character)
                self._character_cursor += 1
                self._origin_x += character.rect.width
            else:
                self._waiting = True

        self.character_group.update()

    def _new_line(self):
        self._next_show_line += 1
        self._real_line.append(self._current_line)
        self._current_line = []
        if self._next_show_line > MAX_LINE:
            self._next_show_line = MAX_LINE
            self.character_group.remove(self._real_line.pop(0))
            for character in self.character_group:
                character.scroll()
        self._origin_x = 0

    def draw(self, screen):
        return self.character_group.draw(screen)

    def next_text(self):
        self.clean()
        text = self._paragraph[self._paragraph_number]
        self.request_next_text = False
        for row in text:
            line = []
            for c in row:
                if c == '/':
                    character = None
                else:
                    character = Character(c, self.font, self.color)
                line.append(character)
            self._lines.append(line)

    def set_paragraph(self, paragraph):
        self._paragraph = paragraph
        self.next_text()

    def clean(self):
        self._line_number = 0
        self._character_cursor = 0
        self._next_show_line = 0
        self._origin_x = 0
        self._lines.clear()
        self.character_group.empty()

        self._real_line.clear()
        self._current_line.clear()
__author__ = 'sasau'

import pygame
from Scene.Scene import Scene
from pawavip.window.message_window import MessageWindow


class SuccessMainScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.background.fill(pygame.Color("purple"))

        # message area
        message_area_height = self.director.screen_rect.height * 0.38
        message_area_rect = pygame.Rect(0, self.director.screen_rect.height - message_area_height,
                                        self.director.screen_rect.width, message_area_height)
        self.message_window = MessageWindow(message_area_rect)
        self.background.blit(self.message_window.background,
                             (message_area_rect.x, message_area_rect.y))

        paragraph = (
            (
                'さて、ここが図書館か。',
                'あの手紙について、何か手がかりがあるかもしれないな。',
                '一応探してみるか。',
            ),
            (
                'ガラッ',
            ),
            (
                '・・・・・・・・・・・。',
            ),
            (
                'ダメだ。人が少ない上に、/有力な情報は入ってきそうにない。',
                'もうここで手がかりを探すのはあきらめよう・・・。',
                '・・・おや？さっきは気づかなかったが、/奥に部屋があるな。',
                'どうしようか？'
            ),
        )
        self.message_window.set_paragraph(paragraph)
        # information area
        information_area_height = self.director.screen_rect.height * 0.183
        self.information_area = pygame.Surface((self.director.screen_rect.width, information_area_height))
        self.information_area.fill(pygame.Color('yellow'))
        self.background.blit(self.information_area, (0, 0))

    def on_update(self):
        self.message_window.update()

    def on_draw(self, screen):
        self.message_window.character_group.clear(screen, self.background)
        areas = self.message_window.draw(screen)
        pygame.display.update(areas)

    def on_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.message_window.next()

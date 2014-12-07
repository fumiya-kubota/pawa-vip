import pygame

__author__ = 'sasau'


class Scene(object):
    def __init__(self, director):
        super().__init__()
        self.director = director
        self.background = pygame.Surface(self.director.screen_rect.size)

    def on_event(self, events):
        pass

    def on_update(self):
        pass

    def on_draw(self, screen):
        pass
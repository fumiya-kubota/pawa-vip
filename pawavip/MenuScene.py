from Scene.Scene import Scene
import pygame

__author__ = 'sasau'


class MenuScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.background.fill(pygame.Color('red'), director.screen.get_rect())

    def on_update(self):
        pass

    def on_draw(self, screen):
        pass

    def on_event(self, events):
        pass
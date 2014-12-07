from Scene.Scene import Scene
import pygame
from pawavip.MenuScene import MenuScene

__author__ = 'sasau'


class TitleScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.background.fill(pygame.Color('blue'), director.screen.get_rect())
        self.add_alpha = 5

    def on_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                menu_scene = MenuScene(self.director)
                self.director.change_scene(menu_scene)

    def on_update(self):
        pass

    def on_draw(self, screen):
        pass
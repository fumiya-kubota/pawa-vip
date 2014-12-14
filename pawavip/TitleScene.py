from Scene.Scene import Scene
import pygame
from pawavip.MenuScene import MenuScene

__author__ = 'sasau'


class TitleScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.background.fill(pygame.Color('red'), director.screen.get_rect())
        self.add_alpha = 5
        self.font = pygame.font.Font('resource/fonts/rounded-mgenplus-1c-regular.ttf', 40)
        title_text = self.font.render('パワプロクンポケット', True, (0, 0, 0))
        self.background.blit(title_text, (self.director.screen_rect.width / 2 - title_text.get_rect().width / 2, 150))

    def on_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                menu_scene = MenuScene(self.director)
                self.director.change_scene(menu_scene)

    def on_update(self):
        pass

    def on_draw(self, screen):
        pass

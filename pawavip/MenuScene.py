from Scene.Scene import Scene
import pygame

__author__ = 'sasau'


class MenuCursor(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        color = pygame.Color('black')
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, self.rect.width - 1, self.rect.height - 1), 2)


class MenuScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.background.fill(pygame.Color('white'), director.screen.get_rect())
        self.font = pygame.font.Font('resource/fonts/rounded-mgenplus-1c-regular.ttf', 26)
        success_button = self.font.render('サクセス', True, pygame.Color('black'))
        self.background.blit(success_button, (50, 50))
        rect = success_button.get_rect()
        rect.x = 50
        rect.y = 50
        cursor = MenuCursor(rect)
        self.sprites = pygame.sprite.Group(cursor)

    def on_update(self):
        self.sprites.update()

    def on_draw(self, screen):
        self.sprites.clear(screen, self.background)
        rects = self.sprites.draw(screen)
        pygame.display.update(rects)
        pygame.display.flip()

    def on_event(self, events):
        pass

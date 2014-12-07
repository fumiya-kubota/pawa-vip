__author__ = 'sasau'

import pygame
from Scene.transition.Transition import CrossFade


class Director:
    def __init__(self, title, screen_rect):
        """
        :param title: String
        :param screen_rect: pygame.Rect()
        """
        self.screen_rect = screen_rect
        self.screen = pygame.display.set_mode(screen_rect.size)
        pygame.display.set_caption(title)
        self.scene = None
        self.quit_flag = False
        self.clock = pygame.time.Clock()

    def loop(self):

        while not self.quit_flag:
            self.clock.tick(60)

            # Exit events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit()

            # Detect events
            self.scene.on_event(events)

            # Update scene
            self.scene.on_update()

            # Draw the screen
            self.scene.on_draw(self.screen)

    def fade_out(self):
        fade = CrossFade(self.scene.background, fade_in=False)
        self.transition(fade)

    def fade_in(self):
        fade = CrossFade(self.scene.background)
        self.transition(fade)

    def transition(self, fade):
        all_sprites = pygame.sprite.Group(fade)
        keep_playing = True
        while keep_playing and not fade.complete:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_playing = False

            all_sprites.clear(self.screen, self.scene.background)
            all_sprites.update()
            all_sprites.draw(self.screen)

            pygame.display.flip()

    def change_scene(self, scene):
        """
        :param scene:Scene
        """
        self.fade_out()
        self.scene = scene

        self.screen.blit(scene.background, (0, 0))
        self.fade_in()

    def set_scene(self, scene):
        self.scene = scene
        self.screen.blit(scene.background, (0, 0))
        pygame.display.flip()

    def quit(self):
        self.quit_flag = True

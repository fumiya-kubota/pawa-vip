__author__ = 'sasau'

from Scene.Scene import Scene
from pawavip.Player import Player
import pygame


class MakingScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.background.fill(pygame.Color('white'))
        self.player = Player()


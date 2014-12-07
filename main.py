import sys
from Scene import Director, Scene
import pygame
import pygame.locals
from pawavip.TitleScene import TitleScene
from utils import image

image.MAIN_DIR = ''
SCREEN_RECT = pygame.Rect((0, 0, 640, 480))


def main():
    pygame.init()
    director = Director.Director('PawaPoke VIP!', SCREEN_RECT)
    scene = TitleScene(director)
    director.set_scene(scene)
    director.loop()
    sys.exit()


if __name__ == '__main__':
    main()

import sys
from Scene import Director
import pygame
import pygame.locals
from pawavip.TitleScene import TitleScene
from utils import image

image.MAIN_DIR = ''
SCREEN_RECT = pygame.Rect((0, 0, 800, 600))


def main(mode):
    pygame.init()
    if mode is None:
        director = Director.Director('PawaPoke VIP!', SCREEN_RECT)
        scene = TitleScene(director)
        director.set_scene(scene)
        director.loop()
    else:
        if mode == 'making':
            from pawavip.MakingScene import MakingScene
            director = Director.Director('キャラメイクテスト', SCREEN_RECT)
            scene = MakingScene(director)
        elif mode == 'message':
            from pawavip.SuccessMainScene import SuccessMainScene
            director = Director.Director('キャラメイクテスト', SCREEN_RECT)
            scene = SuccessMainScene(director)

        director.set_scene(scene)
        director.loop()

    sys.exit()


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
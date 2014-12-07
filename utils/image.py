from utils import MAIN_DIR
import os
import pygame

__author__ = 'sasau'


def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join(MAIN_DIR, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))
    return surface.convert()


def load_images(*files):
    images = []
    for file in files:
        images.append(load_image(file))
    return images
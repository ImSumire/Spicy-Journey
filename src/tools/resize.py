from src.tools.memoize import memoize
import pygame


@memoize
def resize(img, factor):
    return pygame.transform.scale(
        img, (int(img.get_width() * factor), int(img.get_height() * factor))
    )
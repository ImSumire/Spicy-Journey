from src.tools.memoize import memoize
import pygame
import os


@memoize
def get_images(path):
    surface_list = []
    for _, __, img_files in os.walk(path):
        for image in img_files:
            surface_list.append(
                pygame.image.load(os.path.join(path, image)).convert_alpha()
            )
    return surface_list

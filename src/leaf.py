from random import randint, choice, uniform
from src.memoize import memoize
import pygame
import os


@memoize
def import_folder(path):
    surface_list = []
    for _, __, img_files in os.walk(path):
        for image in img_files:
            surface_list.append(
                pygame.image.load(os.path.join(path, image)).convert_alpha()
            )
    return surface_list


class Leaf:
    def __init__(self, x_speed, y_speed, height_limit):
        self.x = randint(0, 1280)
        self.y = randint(0, 700)

        self.height_limit = height_limit

        self.vector = (
            -uniform(0.4, 2.4),
            uniform(1, 3),
        )

        self.image = self.resize(
            choice(import_folder("res/sprites/Atmosphere/")),
            uniform(1.5, 2.5),
        )

        self.rotation_factor = choice([-4, -3, -2, -1, 1, 2, 3, 4])
        self.display = self.image
        self.rotation = 1

    @staticmethod
    @memoize
    def resize(img, factor):
        return pygame.transform.scale(
            img, (int(img.get_width() * factor), int(img.get_height() * factor))
        )

    def update(self):
        self.x += self.vector[0]
        self.y += self.vector[1]

        self.rotation += self.rotation_factor
        self.image = pygame.transform.rotate(self.display, self.rotation)

        if self.y > self.height_limit or self.x < -10:
            self.x = randint(100, 1280)
            self.y = randint(-200, 0)

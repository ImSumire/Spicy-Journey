from random import randint, choice, uniform
import pygame
import os
from src.memoize import memoize


@memoize
def resize(img, factor):
    return pygame.transform.scale(
        img, (int(img.get_width() * factor), int(img.get_height() * factor))
    )


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
        self.x = randint(100, 2000)
        self.y = randint(-600, 600)

        self.height_limit = height_limit

        self.vector = (
            -uniform(2 * x_speed, 2 * x_speed + 2),
            uniform(2 * y_speed, 2 * y_speed + 2),
        )

        self.image = resize(
            choice(import_folder("res/sprites/Atmosphere/orange_leaves/")),
            uniform(1.5, 2.5),
        )

        self.rotation_factor = choice([-4, -3, -2, -1, 1, 2, 3, 4])
        self.display = self.image
        self.rotation = 1

    def update(self):
        self.x += self.vector[0]
        self.y += self.vector[1]

        self.rotation += self.rotation_factor
        self.image = pygame.transform.rotate(self.display, self.rotation)

        if self.y > self.height_limit or self.x < -10:
            self.y = randint(-200, 0)
            self.x = randint(100, 1250)

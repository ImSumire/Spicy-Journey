from random import randint, choice, uniform
from src.tools.files import get_images
from src.tools.memoize import memoize
from src.tools.resize import resize
import pygame


class Leaf:
    __slots__ = (
        # Position
        "x",
        "y",
        # Display
        "image",
        "display",
        # Constant
        "height_limit",
        # Movement
        "vector",
        "rotation",
        "rotation_factor",
    )

    def __init__(self, height_limit):
        self.x = randint(0, 1280)
        self.y = randint(0, 700)

        self.height_limit = height_limit

        self.vector = (
            -uniform(0.4, 2.4),
            uniform(1, 3),
        )

        self.image = resize(
            choice(get_images("res/sprites/Atmosphere/")),
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
            self.x = randint(100, 1280)
            self.y = randint(-200, 0)

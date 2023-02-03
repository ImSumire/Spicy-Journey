import pygame
from random import randint

class Image:
    """
    The `Image` class is used to load and display an image file as
    a Pygame surface. The `display` method of the `Image` class takes
    a surface and a position tuple as arguments and blits the image
    onto the surface at the given position.
    """

    def __init__(self, file):
        self.file = file
        self.image = pygame.image.load(file)
        self.size = self.image.get_size()
        self.x_mod = randint(0, 6)
        self.y_mod = randint(0, 4)
        # print(self.size)

    def display(self, surf, position):
        # self.x_mod = randint(0,6)
        # self.y_mod = randint(0,4)
        surf.blit(self.image, (position[0] + self.x_mod, position[1] + self.y_mod))
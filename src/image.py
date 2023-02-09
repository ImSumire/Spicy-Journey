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
        self.image = pygame.image.load(file).convert_alpha()
        self.size = self.image.get_size()

    def display(self, surf, position):
        surf.blit(self.image, (position[0], position[1]))
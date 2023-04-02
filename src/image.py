#  __  __    __  ______  ______  ______
# /\ \/\ "-./  \/\  __ \/\  ___\/\  ___\
# \ \ \ \ \-./\ \ \  __ \ \ \__ \ \  __\
#  \ \_\ \_\ \ \_\ \_\ \_\ \_____\ \_____\
#   \/_/\/_/  \/_/\/_/\/_/\/_____/\/_____/
#

from src.tools.resize import resize
import pygame


class Image:
    __slots__ = ("image", "surf", "pos")

    def __init__(self, path, surf, pos):
        self.image = resize(pygame.image.load(path).convert_alpha(), 2)
        self.pos = pos

    def draw(self, surf):
        surf.blit(self.image, self.pos)

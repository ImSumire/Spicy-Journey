#  ______  ______  _____   ______
# /\  ___\/\  __ \/\  __-./\  ___\
# \ \  __\\ \  __ \ \ \/\ \ \  __\
#  \ \_\   \ \_\ \_\ \____-\ \_____\
#   \/_/    \/_/\/_/\/____/ \/_____/
#

import pygame


def nothing():
    pass


class Fade:
    __slots__ = (
        # Support
        "surf",
        "display",
        # Variables
        "alpha",
        "active",
        "direction",
        "speed",
        "func",
    )

    def __init__(self, width, height, surf):
        self.surf = surf
        self.display = pygame.Surface((width, height))
        self.display.fill((255, 255, 255))
        self.alpha = 0
        self.active = False
        self.direction = 1
        self.speed = 2
        self.func = nothing

    def draw(self, surf):
        self.active = True
        self.alpha += self.speed * self.direction
        if self.alpha >= 255:
            self.direction = -1
            self.func()

        elif self.alpha < 0:
            self.active = False
            self.alpha = 0
            self.direction = 1

        self.display.set_alpha(self.alpha)
        surf.blit(self.display, (0, 0))

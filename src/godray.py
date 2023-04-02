#  ______  ______  _____   ______  ______  __  __
# /\  ___\/\  __ \/\  __-./\  __ \/\  __ \/\ \_\ \
# \ \ \__ \ \ \/\ \ \ \/\ \ \  __<\ \  __ \ \____ \
#  \ \_____\ \_____\ \____-\ \_\ \_\ \_\ \_\/\_____\
#   \/_____/\/_____/\/____/ \/_/ /_/\/_/\/_/\/_____/
#

from src.tools.resize import resize
import pygame


class Godray:
    def __init__(self, width, height, surf):
        self.surf = surf
        self.image = resize(
            pygame.image.load("res/sprites/godray2.png").convert_alpha(), 4
        )
        self.active = False

    def draw(self):
        self.surf.blit(self.image, (0, 0))

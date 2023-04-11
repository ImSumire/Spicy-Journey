#  ______  ______  _____   ______  ______  __  __
# /\  ___\/\  __ \/\  __-./\  __ \/\  __ \/\ \_\ \
# \ \ \__ \ \ \/\ \ \ \/\ \ \  __<\ \  __ \ \____ \
#  \ \_____\ \_____\ \____-\ \_\ \_\ \_\ \_\/\_____\
#   \/_____/\/_____/\/____/ \/_/ /_/\/_/\/_/\/_____/
#

from src.tools.resize import resize
import pygame


class Godray:
    # Pourquoi utiliser  `__slots__` ? La réponse  courte est que les slots sont
    # plus efficaces en termes d'espace mémoire et de vitesse d'accès, et un peu
    # plus sûrs que la méthode d'accès aux   données  par défaut de  Python. Par
    # défaut, lorsque Python crée une nouvelle instance d'une classe, il crée un
    # attribut __dict__ pour la classe.

    __slots__ = (
        # Surface
        "surf",
        # Affichage
        "image",
        "active",
    )

    def __init__(self, width, height, surf):
        # Surface
        self.surf = surf

        # Affichage
        self.image = resize(
            pygame.image.load("res/sprites/godray.png").convert_alpha(), 4
        )
        self.active = True

    def draw(self):
        self.surf.blit(self.image, (0, 0))

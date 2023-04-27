"""
Ce module  contient l'implémentation de la classe Godray, qui est responsable de
l'affichage de l'effet des godrays sur la surface fournie.
"""

#  ______  ______  _____   ______  ______  __  __
# /\  ___\/\  __ \/\  __-./\  __ \/\  __ \/\ \_\ \
# \ \ \__ \ \ \/\ \ \ \/\ \ \  __<\ \  __ \ \____ \
#  \ \_____\ \_____\ \____-\ \_\ \_\ \_\ \_\/\_____\
#   \/_____/\/_____/\/____/ \/_/ /_/\/_/\/_/\/_____/
#

# pylint: disable=duplicate-code
# Pour pouvoir lancer le programme avec n'importe quel fichier
if __name__ == "__main__":
    from os.path import dirname, realpath, join
    from subprocess import call
    import sys

    DIR_PATH = dirname(realpath(__file__))
    call(["python3", join(DIR_PATH, "../main.py")])

    sys.exit()

# pylint: disable=wrong-import-position
# pylint: disable=too-few-public-methods

import pygame
from src.tools.resize import resize


class Godray:
    """
    La classe  Godray peut être initialisée en passant un objet pygame.Surface à
    son constructeur. Une fois initialisé, l'objet  ne changera plus, il ne sera
    qu'affiché sur la surface du jeu.
    """

    __slots__ = (
        # Surface
        "surf",
        # Affichage
        "image",
        "active",
    )

    def __init__(self, surf):
        # Surface
        self.surf = surf

        # Affichage
        self.image = resize(
            pygame.image.load("res/sprites/godray.png").convert_alpha(), 4
        )
        self.active = True

    def draw(self):
        """
        Affichage simple des rayons de soleil.
        """
        self.surf.blit(self.image, (0, 0))

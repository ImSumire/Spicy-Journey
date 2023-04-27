"""
Ce module  contient une classe Fade pour créer des effets de fondu, utilisé pour
l'animation au lancement du jeu  (rentré  dans le monde), pour l'assombrissement
dans les menus et pour l'appareil photo. Ça rajoute un bel effet qui rend le jeu
bien plus complet.
"""

#  ______  ______  _____   ______
# /\  ___\/\  __ \/\  __-./\  ___\
# \ \  __\\ \  __ \ \ \/\ \ \  __\
#  \ \_\   \ \_\ \_\ \____-\ \_____\
#   \/_/    \/_/\/_/\/____/ \/_____/
#

# Pour pouvoir lancer le programme avec n'importe quel fichier
if __name__ == "__main__":
    from os.path import dirname, realpath, join
    from subprocess import call
    import sys

    DIR_PATH = dirname(realpath(__file__))
    call(["python3", join(DIR_PATH, "../main.py")])

    sys.exit()

# pylint: disable=duplicate-code
# pylint: disable=too-many-arguments
# pylint: disable=wrong-import-position
# pylint: disable=too-few-public-methods

import pygame


def nothing():
    """
    Création d'une fonction qui ne fait rien.
    """
    return


class Fade:
    """
    La classe Fade a sa propre surface d'affichage qui n'est changé qu'une seule
    fois,  ensuite  dans la méthode draw  c'est   là  où l'on l'applique  sur la
    surface du jeu avec une certaine transparence.
    """

    __slots__ = (
        # Surfaces
        "surf",
        "display",
        # Variables
        "alpha",
        "active",
        "direction",
        "speed",
        "func",
    )

    def __init__(self, width, height, speed, surf, color=(255, 255, 255)):
        # Surfaces
        self.surf = surf
        self.display = pygame.Surface((width, height))
        self.display.fill(color)

        # Variables
        self.active = False

        self.alpha = 0
        self.direction = 1  # 1 ou -1
        self.speed = speed

        self.func = nothing

    def draw(self, surf):
        """
        Affichage  du  fondu en  soustrayant  puis   en  ajoutant  après   de la
        transparence, la fonction de  l'argument self.func est lancée lorsque la
        transparence est à son périgée (0%).
        """
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

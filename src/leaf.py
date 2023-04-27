"""
Ce module comprend la classe Leaf qui correspond a une feuille, cet effet en jeu
rend très bien car il donne une impression de vie et de mouvement avec le vent. 
"""

#  __      ______  ______  ______
# /\ \    /\  ___\/\  __ \/\  ___\
# \ \ \___\ \  __\\ \  __ \ \  __\
#  \ \_____\ \_____\ \_\ \_\ \_\
#   \/_____/\/_____/\/_/\/_/\/_/
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

# pylint: disable=invalid-name
# pylint: disable=wrong-import-position
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes

from random import randint, choice, uniform
import pygame
from src.tools.files import get_images
from src.tools.resize import resize


class Leaf:
    """
    La classe   Leaf représente un objet de  type  feuille tombante dans un jeu.
    Elle comprend des attributs de position,   d'affichage    et   de mouvement,
    ainsi qu'une méthode de mise à jour de sa position et de sa rotation.
    """

    __slots__ = (
        # Position
        "x",
        "y",
        # Affichage
        "image",
        "display",
        # Constante
        "height_limit",
        # Mouvement
        "vector",
        "rotation",
        "rotation_factor",
    )

    def __init__(self, height_limit):
        # Position
        self.x = randint(0, 1280)
        self.y = randint(0, 700)

        # Constante
        self.height_limit = height_limit

        # Affichage (choisie une image aléatoire)
        self.image = resize(
            choice(get_images("res/sprites/Atmosphere/")),
            uniform(1.5, 2.5),
        )
        self.display = self.image

        # Mouvements
        self.vector = (
            -uniform(0.4, 2.4),
            uniform(1, 3),
        )
        self.rotation_factor = choice([-4, -3, -2, -1, 1, 2, 3, 4])
        self.rotation = 1

    def update(self):
        """
        La méthode  "update" met à jour la position et la rotation de l'image de
        la feuille en fonction de son vecteur de déplacement et de sa vitesse de
        rotation.  Si la feuille sort  de   l'écran,  elle  est  replacée  à une
        nouvelle position aléatoire.
        """
        # Incrémentation du vecteur à la position de la feuille
        self.x += self.vector[0]
        self.y += self.vector[1]

        # Rotation de l'image
        self.rotation += self.rotation_factor
        self.image = pygame.transform.rotate(self.display, self.rotation)

        # Résoud la sortie de l'écran
        if self.y > self.height_limit or self.x < -10:
            self.x = randint(100, 1280)
            self.y = randint(-200, 0)

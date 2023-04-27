"""
Ce  module  est là pour  simplifier   l'affichage  des  images  pour  avoir une
compatibilité avec la commande  draw  qui est lancée pour tous  les éléments du
contenue du GUI.
"""

#  __  __    __  ______  ______  ______
# /\ \/\ "-./  \/\  __ \/\  ___\/\  ___\
# \ \ \ \ \-./\ \ \  __ \ \ \__ \ \  __\
#  \ \_\ \_\ \ \_\ \_\ \_\ \_____\ \_____\
#   \/_/\/_/  \/_/\/_/\/_/\/_____/\/_____/
#

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


class Image:
    """
    Simple classe qui enregistre la position et le contenue de l'image.
    """

    __slots__ = ("image", "pos")

    def __init__(self, path, pos):
        self.image = resize(pygame.image.load(path).convert_alpha(), 2)
        self.pos = pos

    def draw(self, surf):
        """
        Affiche l'image sur la surface de jeu.
        """
        surf.blit(self.image, self.pos)

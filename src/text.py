"""
Le module sert à définir la classe Text, qui permet de dessiner du texte sur une
surface donnée tout  en prenant en compte  les  sauts de ligne et les limites de
largeur.

Le module contient les éléments suivants:
- La  fonction principale qui permet de  lancer le programme avec n'importe quel
fichier.
- La classe  Text qui  permet  de  dessiner   du  texte sur une  surface donnée.
- La variable "FONT" qui contient la police utilisée pour dessiner du texte.
"""

#  ______  ______  __  __  ______
# /\__  _\/\  ___\/\_\_\_\/\__  _\
# \/_/\ \/\ \  __\\/_/\_\/\/_/\ \/
#    \ \_\ \ \_____\/\_\/\_\ \ \_\
#     \/_/  \/_____/\/_/\/_/  \/_/
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

# pylint: disable=no-member
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable= wrong-import-position

import pygame

# Initialisation de la police
pygame.init()
font = pygame.font.Font("res/font/8-bit.ttf", 12)


class Text:
    """
    Cette classe  permet de dessiner du texte sur une surface donnée, en prenant
    en compte les sauts de ligne et les limites de largeur.
    """
    def __init__(self, text, pos, color, max_width):
        self.text = text
        self.pos = pos
        self.color = color
        self.space_width = font.size(" ")[0]  # La largeur d'un espace.
        self.max_width = max_width + self.pos[0]

    def draw(self, surf):
        """
        La méthode  commence par créer un  tableau  2D appelé words, dont chaque
        ligne est une liste de mots. Pour  cela, elle divise le  texte en lignes
        et   chaque  ligne en  mots   à l'aide de  la méthode   split de Python.

        La méthode parcourt ensuite chaque  ligne de words à l'aide d'une boucle
        for. Pour chaque ligne,  elle  parcourt chaque mot de la  ligne à l'aide
        d'une   autre  boucle for. Pour  chaque   mot,  elle utilise  la méthode
        font.render pour créer une   surface  de texte représentant  le  mot, en
        utilisant la police et la couleur spécifiées lors de l'initialisation de
        la  classe.  Elle récupère ensuite  les  dimensions de cette  surface de
        texte à l'aide de la méthode get_size()  pour  vérifier si le texte peut
        tenir, si oui alors il l'affiche, sinon il saute de ligne.
        """
        # Tableau 2D dont chaque ligne est une liste de mots.
        words = [word.split(" ") for word in self.text.splitlines()]
        x, y = self.pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, self.color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= self.max_width:
                    # Réinitialiser le x.
                    x = self.pos[0]
                    # Commencer une nouvelle rangée.
                    y += word_height
                surf.blit(word_surface, (x, y))
                x += word_width + self.space_width
            # Réinitialiser le x.
            x = self.pos[0]
            # Commencer une nouvelle rangée.
            y += word_height

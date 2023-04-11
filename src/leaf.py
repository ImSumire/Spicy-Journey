#  __      ______  ______  ______
# /\ \    /\  ___\/\  __ \/\  ___\
# \ \ \___\ \  __\\ \  __ \ \  __\
#  \ \_____\ \_____\ \_\ \_\ \_\
#   \/_____/\/_____/\/_/\/_/\/_/
#

from random import randint, choice, uniform
from src.tools.files import get_images
from src.tools.memoize import memoize
from src.tools.resize import resize
import pygame


class Leaf:
    # Pourquoi utiliser  `__slots__` ? La réponse  courte est que les slots sont
    # plus efficaces en termes d'espace mémoire et de vitesse d'accès, et un peu
    # plus sûrs que la méthode d'accès aux   données  par défaut de  Python. Par
    # défaut, lorsque Python crée une nouvelle instance d'une classe, il crée un
    # attribut __dict__ pour la classe.
    
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

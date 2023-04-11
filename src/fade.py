#  ______  ______  _____   ______
# /\  ___\/\  __ \/\  __-./\  ___\
# \ \  __\\ \  __ \ \ \/\ \ \  __\
#  \ \_\   \ \_\ \_\ \____-\ \_____\
#   \/_/    \/_/\/_/\/____/ \/_____/
#

import pygame


# Création d'une fonction qui ne fait rien
def nothing():
    pass


class Fade:
    # Pourquoi utiliser  `__slots__` ? La réponse  courte est que les slots sont
    # plus efficaces en termes d'espace mémoire et de vitesse d'accès, et un peu
    # plus sûrs que la méthode d'accès aux   données  par défaut de  Python. Par
    # défaut, lorsque Python crée une nouvelle instance d'une classe, il crée un
    # attribut __dict__ pour la classe.
    
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
        self.alpha = 0
        self.active = False
        self.direction = 1
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

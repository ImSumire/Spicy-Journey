#  __  __    __  ______  ______  ______
# /\ \/\ "-./  \/\  __ \/\  ___\/\  ___\
# \ \ \ \ \-./\ \ \  __ \ \ \__ \ \  __\
#  \ \_\ \_\ \ \_\ \_\ \_\ \_____\ \_____\
#   \/_/\/_/  \/_/\/_/\/_/\/_____/\/_____/
#

from src.tools.resize import resize
import pygame


class Image:
    # Pourquoi utiliser  `__slots__` ? La réponse  courte est que les slots sont
    # plus efficaces en termes d'espace mémoire et de vitesse d'accès, et un peu
    # plus sûrs que la méthode d'accès aux   données  par défaut de  Python. Par
    # défaut, lorsque Python crée une nouvelle instance d'une classe, il crée un
    # attribut __dict__ pour la classe.
    
    __slots__ = (
        "image",
        "pos"
    )

    def __init__(self, path, pos):
        self.image = resize(pygame.image.load(path).convert_alpha(), 2)
        self.pos = pos

    def draw(self, surf):
        surf.blit(self.image, self.pos)

#  ______  __  __  ______  ______  ______  __   __
# /\  __ \/\ \/\ \/\__  _\/\__  _\/\  __ \/\ "-.\ \
# \ \  __<\ \ \_\ \/_/\ \/\/_/\ \/\ \ \/\ \ \ \-.  \
#  \ \_____\ \_____\ \ \_\   \ \_\ \ \_____\ \_\\"\_\
#   \/_____/\/_____/  \/_/    \/_/  \/_____/\/_/ \/_/
#

from math import cos
import pygame


# Création d'une fonction qui ne fait rien
def nothing():
    pass


# Initialisation de la police
pygame.init()
font = pygame.font.Font("res/font/8-bit.ttf", 12)


class Button:
    # Pourquoi utiliser  `__slots__` ? La réponse  courte est que les slots sont
    # plus efficaces en termes d'espace mémoire et de vitesse d'accès, et un peu
    # plus sûrs que la méthode d'accès aux   données  par défaut de  Python. Par
    # défaut, lorsque Python crée une nouvelle instance d'une classe, il crée un
    # attribut __dict__ pour la classe.

    __slots__ = (
        "pressed",
        # Couleurs
        "color",
        "outside",
        "over",
        # Affichage
        "rect",
        "text_surf",
        "text_rect",
        # Au clic
        "function",
        "temp_function",
        # Animation
        "animation",
        "start",
        "end",
        "step",
        "steps",
        "final",
        "speed",
        "delta",
    )

    def __init__(self, text, pos, function, end=None, destroy=False):
        size = font.size(text)
        width = size[0] + 30
        height = size[1] + 3

        x, y = pos

        self.pressed = False

        # Couleurs
        self.color = (179, 127, 69)
        self.outside = (179, 127, 69)
        self.over = (186, 138, 84)

        # Affichage
        self.rect = pygame.Rect(
            (x - width // 2, y - height // 2),  # Centré
            (width, height),
        )
        self.text_surf = font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        # Au clic
        self.temp_function = function

        # Animation
        if end is None:
            self.animation = False
            self.function = function
        else:
            self.animation = True
            self.function = nothing

            self.start = (x, y)
            self.end = end

            self.step = 0
            self.steps = 1 / (0.0016)
            self.final = self.steps // 7

            self.speed = 1 / self.steps
            self.delta = 0

    def draw(self, surf):
        """
        Affichage  du  bouton avec  détéction    de   passage avec   la  méthode
        self.check() et calculs de l'animation si cette dernière est activée
        """
        self.check()
        if self.animation:
            self.animate()
        pygame.draw.rect(surf, self.color, self.rect)
        surf.blit(self.text_surf, self.text_rect)

    def check(self):
        """
        Détéction de passage de souris sur le bouton et lancement de la fonction
        du bouton lorsque le clic et laché.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.color = self.over
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.function()
                    self.pressed = False
        else:
            self.color = self.outside

    def animate(self):
        """
        Une courbe de Bézier est une courbe paramétrique utilisée en infographie
        et dans  des domaines connexes.  Un   ensemble  de "points  de contrôle"
        discrets définit une courbe lisse et continue au moyen d'une formule.

        Voici la formule simplifiée :
        f(x) = cos(x * 3) + 0,989

        J'utilise 3  à la place de pi  puisque  la fin de l'animation était trop
        lente. L'utilisation de 0.95 ne fonctionne pas alors que  l'intégrale de
        f  de 0 à 1 est égale à  1. Après  quelques essais, le meilleur résultat
        est 0.989, pourquoi pas ?

        https://fr.wikipedia.org/wiki/Courbe_de_B%C3%A9zier
        """
        if int(self.step) != self.final:
            self.delta += self.speed * self.step * (cos(3 * self.delta) + 0.989)
            self.step += 1
            x = self.start[0] + self.delta * (self.end[0] - self.start[0])
            y = self.start[1] + self.delta * (self.end[1] - self.start[1])
            self.rect.centerx = x
            self.rect.centery = y
            self.text_rect.centerx = x
            self.text_rect.centery = y
        else:
            self.rect.centerx, self.rect.centery = self.end
            self.function = self.temp_function
            self.animation = False

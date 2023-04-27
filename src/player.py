"""
Ce module  est  une implémentation du  joueur   dans  le jeu. La  classe  Player
représente  le  joueur et est   utilisée  pour animer le   personnage, gérer son
inventaire, le  mouvement du  joueur et   la  génération  de bruits  de pas.

Ce  module dépend de pygame  pour les  animations et  les  contrôles du clavier,
ainsi que du module 'src.tools.files' pour la récupération d'images.
"""

#  ______  __      ______  __  __  ______  ______
# /\  __ \/\ \    /\  __ \/\ \_\ \/\  ___\/\  __ \
# \ \  _-/\ \ \___\ \  __ \ \____ \ \  __\\ \  __<
#  \ \_\   \ \_____\ \_\ \_\/\_____\ \_____\ \_\ \_\
#   \/_/    \/_____/\/_/\/_/\/_____/\/_____/\/_/ /_/
#

# Pour pouvoir lancer le programme avec n'importe quel fichier
if __name__ == "__main__":
    from os.path import dirname, realpath, join
    from subprocess import call
    import sys

    DIR_PATH = dirname(realpath(__file__))
    call(["python3", join(DIR_PATH, "../main.py")])

    sys.exit()

# pylint: disable=invalid-name
# pylint: disable=duplicate-code
# pylint: disable=no-name-in-module
# pylint: disable=wrong-import-position
# pylint: disable= c-extension-no-member
# pylint: disable=too-many-instance-attributes

import pygame
from pygame.locals import K_z, K_s, K_q, K_a, K_w, K_d
from src.tools.files import get_images


class Player:
    """
    Cette classe représente le joueur, elle comprend les données d'animation, de
    position, de statue (bouge ou non, cours ou non) et toutes les méthodes pour
    mettre à jour en fonction des actions faites par le joueur.
    """

    def __init__(self, world):
        # Animation
        self.idle_animation_speed = 0.08
        self.animation_speed = 0.18
        self.frame_index = 0

        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "right_idle": [],
            "left_idle": [],
            "up_idle": [],
            "down_idle": [],
        }
        # Chargement des images pour les animations
        for self.animation in self.animations:
            full_path = "res/sprites/Characters/" + self.animation
            self.animations[self.animation] = get_images(full_path)
        self.idle = "_idle"

        # Chargement de l'image du début
        self.image = pygame.image.load(
            "res/sprites/Characters/down/0.png"
        ).convert_alpha()

        # Mouvements
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(world.spawn)
        self.status = "down"
        self.speed = 0.05  # Vitesse de base : 0.05
        self.exist = False
        self.move = False

        # Sons de pas
        self.running = False
        self.step = pygame.mixer.Sound("res/sound/running.ogg")
        self.step.set_volume(0.8)

        # Instances
        self.world = world

        # Touches de déplacement
        self.up = K_z
        self.down = K_s
        self.left = K_q
        self.right = K_d
        self.harvest = K_a

        # Inventaire
        self.inventory = {}

    def switch(self):
        """
        Inverse les touches de déplacements de AZERTY à QWERTY. Voici la version
        simplifiée, l'officielle est tout simplement une version optimisée :

        if self.up == K_z:
            self.up, self.left, self.harvest= K_w, K_a, K_q
        else:
            self.up, self.left, self.harvest= K_z, K_q, K_a
        """
        self.up, self.left, self.harvest = ((K_z, K_q, K_a), (K_w, K_a, K_q))[
            self.up == K_z
        ]

    def input(self):
        """
        Récupère les touches du clavier pressées par l'utilisateur pour déplacer
        le personnage  met à jour sa  position  en conséquence. La direction est
        calculée à partir des touches direction (zqsd ou wasd) et un  vecteur de
        déplacement est généré. Le vecteur est  ensuite pour assurer une vitesse
        de déplacement constante, puis la position du personnage mise à jour. Si
        la prochaine position est dans l'eau, la méthode  arrête le bruit de pas
        arrête  l'animation de déplacement. Sinon, la méthode lance  le bruit de
        pas si nécessaire et met à jour le statut de déplacement en conséquence.
        """
        keys = pygame.key.get_pressed()

        self.direction = pygame.math.Vector2(0, 0)

        # Haut (z)(w)
        if keys[self.up] and not keys[self.down]:
            self.direction.y -= 1
            self.direction.x -= 1
            self.status = "up"

        # Bas (s)(s)
        elif keys[self.down] and not keys[self.up]:
            self.direction.x += 1
            self.direction.y += 1
            self.status = "down"

        # Gauche (q)(a)
        if keys[self.left] and not keys[self.right]:
            self.direction.x -= 1
            self.direction.y += 1
            self.status = "left"

        # Droite (d)(d)
        elif keys[self.right] and not keys[self.left]:
            self.direction.x += 1
            self.direction.y -= 1
            self.status = "right"

        # Sans mouvements (idle)
        if self.direction == (0, 0):
            self.idle = "_idle"
            self.running = False
            self.step.stop()

        else:
            # Normalisation  du vecteur de direction  pour garder une vitesse de
            # déplacement de 0.05 même en diagonal.
            self.direction.normalize()
            x_pos_mod = self.pos.x - int(self.pos.x)
            y_pos_mod = self.pos.y - int(self.pos.y)
            x = self.direction.x * self.speed
            y = self.direction.y * self.speed

            # Vérification que la prochaine position soit dans l'eau.
            height = self.world.coords[round(self.world.center + y + y_pos_mod)][
                round(self.world.center + x + x_pos_mod)
            ][3]
            if height > self.world.water_level:
                self.idle = "_idle"
                self.running = False
                self.step.stop()

            # Si la prochaine position est correcte alors modifier la position.
            else:
                self.pos.x = round(self.pos.x + x, 2)
                self.pos.y = round(self.pos.y + y, 2)
                self.idle = ""

                # Bruit de pas
                if not self.running:
                    self.step.play(loops=-1)

                self.running = True

    def animate(self):
        """
        Cette méthode  sélectionne la séquence  d'animation en cours en fonction
        de l'état du sprite et de son  état d'inactivité. L'animation est mise à
        jour  en fonction des attributs de  vitesse  d'animation  et  de vitesse
        d'animation au repos. L'index de l'image courante est incrémenté jusqu'à
        l'image suivante de la séquence d'animation, et si la fin de la séquence
        est atteinte, l'index est  remis  à 0 pour répéter  l'animation. L'image
        actuelle  du  sprite est  définie sur  l'image  à l'indice d'image mis à
        jour.
        """
        animation = self.animations[self.status + self.idle]

        # Incrémentation de l'index
        if self.idle:
            self.frame_index += self.idle_animation_speed
        else:
            self.frame_index += self.animation_speed

        # Évite le out of range
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Définir l'image
        self.image = animation[int(self.frame_index)]

    def update(self):
        """
        Cette  méthode utilise  la gestion  des inputs  et des  animations  pour
        mettre à jour le joueur.
        """
        if self.move:
            self.input()
        self.animate()

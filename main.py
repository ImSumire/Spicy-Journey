"""
Ce module  est le script principal du  jeu, il comporte le chargement des autres
modules, il créé les instances de base et lance le jeu dans une boucle while.
"""

#              ______  ______  __  ______  __  __
#             /\  ___\/\  __ \/\ \/\  ___\/\ \_\ \
#             \ \___  \ \  _-/\ \ \ \ \___\ \____ \
#              \/\_____\ \_\   \ \_\ \_____\/\_____\
#               \/_____/\/_/    \/_/\/_____/\/_____/
#        __  ______  __  __  ______  __   __  ______  __  __
#       /\ \/\  __ \/\ \/\ \/\  __ \/\ "-.\ \/\  ___\/\ \_\ \
#      _\_\ \ \ \/\ \ \ \_\ \ \  __<\ \ \-.  \ \  __\  \____ \
#     /\_____\ \_____\ \_____\ \_\ \_\ \_\ "\_\ \_____\/\_____\
#     \/_____/\/_____/\/_____/\/_/ /_/\/_/ \/_/\/_____/\/_____/
#


# GitHub : https://github.com/ImSumire/Spicy-Journey
# Wiki : https://github.com/ImSumire/Spicy-Journey/wiki

# Benchmark : `python3 -m cProfile -s tottime main.py > exit.txt`

#pylint: disable=duplicate-code
__inspiration__ = (
    "Ghibli",  # Pour le style graphique
    "Minecraft",  # Pour la génération du monde
    "Animal Crossing",  # Pour la vue en top-down
    "Zelda Breath of the Wild",  # Pour le système de cuisine
)

# pylint: disable=no-member
# pylint: disable=invalid-name
# pylint: disable=duplicate-code
# pylint: disable=no-name-in-module
# pylint: disable=consider-using-f-string

### Importation des modules

# exit() quitte  simplement le script   Python, mais pas  l'environnement Python
# complet, tandis que sys.exit() quitte à  la fois  le script et l'environnement
# Python complet.
import sys

from json import load

# json est  meilleur que yaml car c'est  facile  de l'utiliser, il y a une
# meilleure compatibilité et de meilleures performances.
from time import perf_counter

import pygame
from pygame.locals import K_F3, KEYDOWN, QUIT

# Chargement des classes de source
from src.player import Player
from src.world import World
from src.gui import Gui

### Création des constantes à partir du fichier config.json

# Charge les données du fichier config grâce à la librairie json
with open("config.json", encoding="utf-8") as f:
    CONFIG = load(f)

# Définition des constantes à partir du fichier config
WIDTH = CONFIG["dimensions"]["width"]
HEIGHT = CONFIG["dimensions"]["height"]
FPS = CONFIG["fps"]
TITLE = CONFIG["title"]
X_CENTER, Y_CENTER = CENTER = (WIDTH // 2, HEIGHT // 2)


def handle_events():
    """
    Cette fonction  traîte toutes les données en relation avec les interactions,
    comme le fait de fermer la fenêtre de  jeu, l'activation du menu de débogage
    et d'autres.
    """
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # Activer l'écran de débogage, échange la valeur booléenne
            if event.key == K_F3:
                gui.debug = not gui.debug

            elif event.key == player.harvest:
                # Position actuelle du joueur
                player_x, player_y = player.pos

                # Position fixée du joueur
                x_pos_fixed = world.center + round(player_x - int(player_x))
                y_pos_fixed = world.center + round(player_y - int(player_y))

                # Data aux coordonnées fixées
                pos = world.coords[y_pos_fixed][x_pos_fixed]

                is_ingredient = int(str(pos[2])[-2:]) in world.ingredients_range
                is_available = world.vegetation_data[
                    int(player_x + x_pos_fixed),
                    int(player_y + y_pos_fixed),
                ]

                # Si aux coordonnées fixées il y a un ingrédient
                if is_ingredient and is_available:
                    # Récupérer l'ingrédient
                    gui.mixer.pok.play()
                    world.vegetation_data[
                        int(player_x + x_pos_fixed),
                        int(player_y + y_pos_fixed),
                    ] = False
                    ingredient = world.ingredients_list[
                        int(str(pos[2])[-2:]) - world.ingredients_range[0]
                    ]
                    if ingredient in player.inventory:
                        player.inventory[ingredient] += 1
                    else:
                        player.inventory[ingredient] = 1

        # Fermeture du jeu
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()


def render(_seconds: float, _tick: int, _display: pygame.Surface):
    """
    Cette fonction met à jour les données en jeu puis les affiches, ici c'est le
    monde et l'interface.
    """
    world.update(int(player.pos.x), int(player.pos.y))

    # Récupérer et afficher les sprites
    for sprite in world.get_sprites(player, tick * 0.04):  # 0.04 ralentie l'animation
        _display.blit(sprite[0], (sprite[1], sprite[2]))

    # Dessiner l'interface graphique
    gui.draw()

    # Dessiner l'écran de débogage
    if gui.debug:
        gui.draw_debug(_tick, _seconds, clock.get_fps())

    # Dessiner le fondu
    if gui.fade.active:
        gui.fade.draw(screen)

    if gui.photo_fade.active:
        gui.photo_fade.draw(screen)

    pygame.display.flip()


if __name__ == "__main__":
    # Initialisation
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    display = pygame.Surface(CENTER)
    clock = pygame.time.Clock()

    # Nombre de secondes passées
    seconds = 0
    # Nombre de fois qu'il y a eu une update
    tick = 0
    # Récupération du temps au démarage
    start = perf_counter()

    # Création du monde
    world = World(WIDTH, HEIGHT)
    print("Seed : %s" % world.seed)
    print("Spawn : %s" % str(world.spawn))

    # Création du personnage
    player = Player(world)

    # Création du GUI (Graphical User Interface)
    gui = Gui(WIDTH, HEIGHT, screen, display, player, world)

    ### Démarrage du jeu
    while True:
        handle_events()
        player.update()
        render(seconds, tick, display)

        clock.tick(FPS)
        tick += 1  # Tick est la valeur représentative du temps en jeu
        seconds = perf_counter() - start  # Seconds est le temps passé en jeu

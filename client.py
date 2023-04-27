"""
Ce module  est le script principal du  jeu, il comporte le chargement des autres
modules, il créé les instances de base et lance le jeu dans une boucle while.

Cette version du jeu est en ligne, cela veut dire qu'il faut démarrer le serveur
pour pouvoir jouer, s'il n'est pas démarré demandez à : Zecter#2847 sur Discord.
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

__inspiration__ = (
    "Ghibli",  # Pour le style graphique
    "Minecraft",  # Pour la génération du monde
    "Animal Crossing",  # Pour la vue en top-down
    "Zelda Breath of the Wild",  # Pour le système de cuisine
)

# pylint: disable=no-member
# pylint: disable=invalid-name
# pylint: disable=no-name-in-module

### Importation des modules

# Gestion des packets
import socket
import pickle
from traceback import print_exc

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
with open("config.json") as f:
    CONFIG = load(f)

# Définition des constantes à partir du fichier config
WIDTH = CONFIG["dimensions"]["width"]
HEIGHT = CONFIG["dimensions"]["height"]
FPS = CONFIG["fps"]
TITLE = CONFIG["title"]
X_CENTER, Y_CENTER = CENTER = (WIDTH // 2, HEIGHT // 2)

SERVER_ADDR = "ulysses.ddns.net"
SERVER_PORT = 9595

players = {}
current_id = -1


def handle_events():
    """
    Cette fonction  traîte toutes les données en relation avec les interactions,
    comme le fait de fermer la fenêtre de  jeu, l'activation du menu de débogage
    et d'autres.
    """
    _send_quit = "False "

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
            _send_quit = "True "

    return _send_quit


def render(_seconds, _tick, _display):
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

    # Connexion au server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.connect((SERVER_ADDR, SERVER_PORT))

    # Récupération de l'id
    current_id = int(server.recv(4).decode())

    # Création du pseudo
    response = "False"
    while response == "False":
        name = input("Entrez votre pseudo : ")
        server.send(name.encode())
        response = server.recv(5).decode()

    # Création du monde
    # pylint: disable=too-many-function-args
    world = World(WIDTH, HEIGHT, int(server.recv(10).decode()))
    print("Seed : %s" % world.seed)
    print("Spawn : %s" % str(world.spawn))

    # Création du personnage
    player = Player(world)

    server.send((str(world.spawn[0]) + " " + str(world.spawn[1])).encode())
    server.send(
        (
            "get False " + str(player.frame_index) + " " + player.status + player.idle
        ).encode()
    )
    players = pickle.loads(server.recv(1024))

    # Création du GUI (Graphical User Interface)
    gui = Gui(WIDTH, HEIGHT, screen, display, player, world)

    ### Démarrage du jeu
    while True:
        try:
            send_quit = handle_events()
            player.update()
            player.frame_index = player.frame_index % len(
                world.player_sprites[player.status + player.idle]
            )

            data = "get "

            # Vérifie si les positions ont changées
            if [player.pos.x, player.pos.y] != players[current_id][1]:
                data = "move " + str(player.pos.x) + " " + str(player.pos.y) + " "

            # Envoie des positions
            server.send(
                (
                    data
                    + send_quit
                    + str(player.frame_index)
                    + " "
                    + player.status
                    + player.idle
                ).encode()
            )

            data = data.split(" ")

            # Fermeture du jeu
            if send_quit == "True ":
                response = server.recv(10).decode()
                if response == "ok":
                    pygame.quit()
                    sys.exit()

            elif data[0] == "get" or data[0] == "move":
                players = pickle.loads(server.recv(1024))

            render(seconds, tick, display)

            clock.tick(FPS)
            tick += 1  # Tick est la valeur représentative du temps en jeu
            seconds = perf_counter() - start  # Seconds est le temps passé en jeu

        except Exception:  # pylint: disable=broad-except
            print_exc()
            pygame.quit()
            sys.exit()

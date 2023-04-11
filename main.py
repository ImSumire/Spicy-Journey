"""
                   ______  ______  __  ______  __  __    
                  /\  ___\/\  __ \/\ \/\  ___\/\ \_\ \   
                  \ \___  \ \  _-/\ \ \ \ \___\ \____ \  
                   \/\_____\ \_\   \ \_\ \_____\/\_____\ 
                    \/_____/\/_/    \/_/\/_____/\/_____/ 
             __  ______  __  __  ______  __   __  ______  __  __    
            /\ \/\  __ \/\ \/\ \/\  __ \/\ "-.\ \/\  ___\/\ \_\ \   
           _\_\ \ \ \/\ \ \ \_\ \ \  __<\ \ \-.  \ \  __\  \____ \  
          /\_____\ \_____\ \_____\ \_\ \_\ \_\ "\_\ \_____\/\_____\ 
          \/_____/\/_____/\/_____/\/_/ /_/\/_/ \/_/\/_____/\/_____/ 

"""
#
# L'histoire se déroule dans un monde fantastique rempli de magie et de mystère.
# Le personnage  que vous contrôlez est  une  jeune femme japonaise nommée Hana,
# née dans un petit village isolé niché dans une forêt luxuriante.  Hana est une
# cuisinière  passionnée et a hérité  de  sa grand-mère  un   livre  de recettes
# traditionnelles japonaises. Les  ingrédients  dont elle a besoin pour cuisiner
# ces plats sont éparpillés aux quatre coins du monde. Elle a décidé de partir à
# l'aventure pour les collecter et les cuisiner afin de perpétuer les traditions
# familiales   et  de rendre hommage à  sa   grand-mère.  Elle se lance  dans un
# incroyable  voyage  à  travers   la   nature sauvage, découvrant   des secrets
# mystiques   sur le monde  qui   l'entoure.   En  chemin,   Hana  rencontre des
# personnages fascinants qui l'aident dans sa quête, comme des marchands qui lui
# vendent des ingrédients utiles pour ses recettes.
#
# Spicy Journey est un jeu qui vous aidera à vous détendre et à  vous relaxer en
# explorant   un  monde généré   de  manière  procédurale  et  rempli  de forêts
# luxuriantes. Avec son point de vue  isométrique  et son style pixel art, Spicy
# Journey est un jeu rétro-visuel qui ne manquera pas de vous captiver.    Spicy
# Journey offre des possibilités infinies d'exploration et de découverte. Il n'y
# a pas deux jeux identiques, vous pouvez donc revenir à Spicy Journey encore et
# encore pour une nouvelle expérience. Si vous cherchez un jeu qui vous aidera à
# vous détendre et à vous relaxer, ne  cherchez pas plus loin que Spicy Journey.
# Avec ses magnifiques forêts, son charmant style pixel  art et ses possibilités
# d'exploration  infinies, c'est le jeu   idéal pour tous ceux   qui cherchent à
# s'évader dans un monde paisible et immersif.
#
# Auteurs : @Zecyl and @ImSumire
#
# Requis: python==3.*, pygame, noise, numba
#
# Spicy Journey - littéralement "voyage épicé" ou "voyage pimenté"
# 香り旅 (kaori tabi) - littéralement "voyage d'odeurs agréables"
#


#  __  __    __  ______  ______  ______  ______  ______
# /\ \/\ "-./  \/\  __ \/\  __ \/\  __ \/\__  _\/\  ___\
# \ \ \ \ \-./\ \ \  _-/\ \ \/\ \ \  __<\/_/\ \/\ \___  \
#  \ \_\ \_\ \ \_\ \_\   \ \_____\ \_\ \_\ \ \_\ \/\_____\
#   \/_/\/_/  \/_/\/_/    \/_____/\/_/ /_/  \/_/  \/_____/
#

import sys

# exit() quitte  simplement le script   Python, mais pas  l'environnement Python
# complet, tandis que sys.exit() quitte à  la fois  le script et l'environnement
# Python complet.
import json

# json est  meilleur que yaml car c'est  facile  de l'utiliser, il y a une
# meilleure compatibilité et de meilleures performances.
from time import perf_counter

import pygame
from pygame.locals import *

# Chargement des classes de source
from src.player import Player
from src.world import World
from src.gui import Gui


global seconds, tick, display, temp

#    ______  ______  __   __  ______  __  ______
#   /\  ___\/\  __ \/\ "-.\ \/\  ___\/\ \/\  ___\
#   \ \ \___\ \ \/\ \ \ \-.  \ \  __\\ \ \ \ \__ \
#    \ \_____\ \_____\ \_\\"\_\ \_\   \ \_\ \_____\
#     \/_____/\/_____/\/_/ \/_/\/_/    \/_/\/_____/
#

# Charge les données du fichier config grâce à la librairie json
with open("config.json") as f:
    config = json.load(f)

# Accéder aux valeurs de configuration en tant qu'éléments du dictionnaire
WIDTH = config["dimensions"]["width"]
HEIGHT = config["dimensions"]["height"]
FPS = config["fps"]
TITLE = config["title"]
X_CENTER, Y_CENTER = CENTER = (WIDTH // 2, HEIGHT // 2)


def handle_events():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # Activer l'écran de débogage, échange la valeur booléenne
            if event.key == K_F3:
                gui.debug = not gui.debug

            elif event.key == K_a:
                # Position actuelle du joueur
                x, y = player.pos

                # Position fixée du joueur
                x_pos_fixed = world.center + round(x - int(x))
                y_pos_fixed = world.center + round(y - int(y))

                # Data aux coordonnées fixées
                pos = world.coords[y_pos_fixed][x_pos_fixed]

                # Si aux coordonnées fixées il y a un ingrédient
                if (
                    bool(round(pos[2]))  # S'il y a une végétation
                    and not pos[3] > world.water_level
                    and int(str(pos[2])[-2:]) in world.ingredients_range
                    and world.vegetation_data[
                        int(x + x_pos_fixed),
                        int(y + y_pos_fixed),
                    ]
                ):
                    # Récupérer l'ingrédient
                    gui.mixer.pok.play()
                    world.vegetation_data[
                        int(x + x_pos_fixed),
                        int(y + y_pos_fixed),
                    ] = False

            # elif event.key == K_p:
            #     gui.mixer.page_sound()

        # Fermeture du jeu
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()


def render():
    # Mise à jour des coordonnées du terrain
    world.update(int(player.pos.x), int(player.pos.y))

    # Récupérer et afficher les sprites
    for sprite in world.get_sprites(player, tick):
        display.blit(sprite[0], (sprite[1], sprite[2]))

    # Dessiner l'interface graphique
    gui.draw()

    # Dessiner l'écran de débogage
    if gui.debug:
        gui.draw_debug(tick, seconds, clock.get_fps())

    # Dessiner le fondu
    if gui.fade.active:
        gui.fade.draw(screen)

    if gui.photo_fade.active:
        gui.photo_fade.draw(screen)

    # Mise à jour de l'affichage
    pygame.display.flip()


if __name__ == "__main__":
    #    __  __   __  __  ______
    #   /\ \/\ "-.\ \/\ \/\__  _\
    #   \ \ \ \ \-.  \ \ \/_/\ \/
    #    \ \_\ \_\\"\_\ \_\ \ \_\
    #     \/_/\/_/ \/_/\/_/  \/_/
    #

    # Initialisation, définition du titre et des dimensions de la fenêtre
    pygame.init()
    pygame.display.set_caption(TITLE)  # "Spicy Journey"
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # (1280, 700)
    display = pygame.Surface(CENTER)  # (640, 350)
    clock = pygame.time.Clock()
    seconds = 0
    tick = 0

    # Création du monde
    world = World(WIDTH, HEIGHT)
    print("Seed : %s" % world.seed)

    # Création du personnage
    player = Player(world)

    # Création du GUI (Graphical User Interface)
    gui = Gui(WIDTH, HEIGHT, screen, display, player, world)

    #  ______  ______  ______  ______  ______
    # /\  ___\/\__  _\/\  __ \/\  __ \/\__  _\
    # \ \___  \/_/\ \/\ \  __ \ \  __<\/_/\ \/
    #  \/\_____\ \ \_\ \ \_\ \_\ \_\ \_\ \ \_\
    #   \/_____/  \/_/  \/_/\/_/\/_/ /_/  \/_/
    #

    while True:
        start = perf_counter()
        handle_events()  # Gestion des pressions sur les boutons
        player.update()  # Gère l'animation et les mouvements du joueur
        render()  # Effectue les calculs et dessine l'écran
        clock.tick(FPS)  # Limite les fps à la valeur inscrite dans les configs

        tick += 1  # Tick est la valeur représentative du temps en jeu
        seconds += perf_counter() - start  # Seconds est le temps passé en jeu

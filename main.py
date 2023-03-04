"""
         ______  ______  __      ______  ______
        /\  __ \/\__  _\/\ \    /\  __ \/\  ___\ 
        \ \  __ \/_/\ \/\ \ \___\ \  __ \ \___  \ 
         \ \_\ \_\ \ \_\ \ \_____\ \_\ \_\/\_____\ 
          \/_/\/_/  \/_/  \/_____/\/_/\/_/\/_____/
"""
#
# Introducing Atlas,  the game that   will help you unwind and
# relax as you explore a  procedurally generated  world filled
# with  lush forests. With its isometric  viewpoint  and pixel
# art style, Atlas is  a  retro-visually game that is  sure to
# captivate you.
#
# With its  procedurally generated world, Atlas offers endless
# opportunities for exploration and   discovery. No  two games
# will be the same, so you can keep coming back to Atlas again
# and again for a new and exciting experience.
#
# So if you're looking for a game that will help you relax and
# unwind,  look no further than   Atlas.  With   its beautiful
# forests, charming pixel art style, and endless possibilities
# for exploration, it's the perfect game for anyone looking to
# escape into a peaceful and immersive world.
#
# Why Pygame?
# Because it is a beautifully optimized and much more complete
# library, and  quite low-level compared to Raylib and  Arcade
# Pyglet.  Moreover, it is in  the computer science speciality
# program in high school.
#
# Authors : @Zecyl and @ImGalaad
#
# Requirements: Python 3, pygame, noise, pyyaml
#

from time import perf_counter

import sys
from math import fmod
import json


import pygame
from pygame.locals import *
import pygame.gfxdraw

from src.player import Player
from src.terrain import Terrain
from src.leaf import Leaf

# Load the configuration file using the json lib
with open("config.json") as f:
    config = json.load(f)

# Access configuration values as dictionary items
WIDTH = config["game"]["dimensions"]["width"]
HEIGHT = config["game"]["dimensions"]["height"]
FPS = config["game"]["fps"]
TITLE = config["title"]

#  __  __   __  __  ______
# /\ \/\ "-.\ \/\ \/\__  _\
# \ \ \ \ \-.  \ \ \/_/\ \/
#  \ \_\ \_\\"\_\ \_\ \ \_\
#   \/_/\/_/ \/_/\/_/  \/_/
#

# Initialization, setting of the window title and dimensions
pygame.init()
pygame.display.set_caption(TITLE)  # 'Atlas'
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)  # (1280, 700)
display = pygame.Surface((WIDTH // 2, HEIGHT // 2))  # (640, 350)
clock = pygame.time.Clock()
tick = 0

# Basics instances
terrain = Terrain(0.08, WIDTH, HEIGHT)  # 0.08
player = Player((0, 0))

# Debug
font = pygame.font.Font(None, 25)
debug = False

# Aesthetic
leaves = [Leaf(0.2, 0.5, HEIGHT) for i in range(100)]
bloom = True

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                global debug
                debug = not debug

            elif event.key == pygame.K_m:
                terrain.temp -= 1
                print(terrain.temp)

            elif event.key == pygame.K_p:
                terrain.temp += 1
                print(terrain.temp)

            elif event.key == pygame.K_k:
                if player.up == pygame.K_z:
                    player.up = pygame.K_w
                    player.left = pygame.K_a
                else:
                    player.up = pygame.K_z
                    player.left = pygame.K_q


def debug_screen(text):
    for index, line in enumerate(text.split("\n")):
        screen.blit(
            font.render(
                line,
                True,
                (255, 255, 255),
            ),
            (10, 10 + 25 * index),
        )


def render():
    global display
    display.fill((0, 0, 0))

    #start = perf_counter()
    terrain.get_coords(player.pos.x, player.pos.y)
    terrain_sprites, props_sprites = terrain.get_sprites(player)
    #print('Calculation : ', round(perf_counter() - start, 3), end=" | ")

    #start = perf_counter()
    for sprite in terrain_sprites + props_sprites:
        display.blit(sprite[0], (sprite[1], sprite[2]))
    #print('Sprites : ', round(perf_counter() - start, 3), end=" | ")

    #start = perf_counter()
    for leaf in leaves:
        display.blit(leaf.image, (leaf.x, leaf.y))
        leaf.update()
    #print('Leaves : ', round(perf_counter() - start, 3), end=" | ")

    if bloom:
        pass

    #start = perf_counter()
    screen.blit(pygame.transform.scale(display, (WIDTH, HEIGHT)), (0, 0))
    #print('Display : ', round(perf_counter() - start, 3))

    if debug:
        debug_screen(
            "x : "
            + str(player.pos[0])
            + "\ny : "
            + str(player.pos[1])
            + "\nz : "
            + str(round(170 - terrain.coords[terrain.center][terrain.center][1], 2))
        )

    pygame.display.flip()


if __name__ == "__main__":
    while True:
        handle_events()
        player.update()
        render()

        pygame.display.set_caption(str(int(clock.get_fps())))
        clock.tick(FPS)

        tick += 1
        if tick == FPS:
            tick = 0

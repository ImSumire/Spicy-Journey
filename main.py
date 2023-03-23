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
import json


import pygame
from pygame.locals import *

from src.player import Player
from src.terrain import Terrain
from src.leaf import Leaf
from src.button import Button
from src.fade import Fade

# Load the configuration file using the json lib
with open("config.json") as f:
    config = json.load(f)

# Access configuration values as dictionary items
WIDTH = config["game"]["dimensions"]["width"]
HEIGHT = config["game"]["dimensions"]["height"]
FPS = config["game"]["fps"]
TITLE = config["title"]
CENTER = (WIDTH // 2, HEIGHT // 2)

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
display = pygame.Surface(CENTER)  # (640, 350)
clock = pygame.time.Clock()
tick = 0

# Basics instances
terrain = Terrain(WIDTH, HEIGHT)
print("Seed :", terrain.seed)
player = Player((0, 0))

# Debug
font = pygame.font.Font("res/font/8-bit.ttf", 12)
debug = False

# Aesthetic
leaves = [Leaf(0.2, 0.5, HEIGHT) for i in range(100)]
fade = Fade(WIDTH, HEIGHT)
bloom = True


def test():
    print("Start Game")


# GUI
buttons = [Button("Play", font, 80, 20, CENTER, test)]

temp = 0


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global temp, tick
            print("Second per frame (average) :", temp / tick)
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                global debug
                debug = not debug

            elif event.key == pygame.K_m:
                terrain.temp -= 0.25
                print(terrain.temp)

            elif event.key == pygame.K_p:
                terrain.temp += 0.25
                print(terrain.temp)

            elif event.key == pygame.K_f:
                fade.active = True

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
    global display, temp
    display.fill((0, 0, 0))

    start = perf_counter()
    terrain.update(int(player.pos.x), int(player.pos.y))
    # print('Calculation : ', round(perf_counter() - start, 6), end=" | ")

    # start = perf_counter()
    terrain_sprites, props_sprites = terrain.get_sprites(player, tick)
    # print('Get sprites : ', round(perf_counter() - start, 6), end=" | ")

    # start = perf_counter()
    for sprite in terrain_sprites + props_sprites:
        display.blit(sprite[0], (sprite[1], sprite[2]))
    # print('Sprites : ', round(perf_counter() - start, 6), end=" | ")

    # start = perf_counter()
    for leaf in leaves:
        leaf.update()
        display.blit(leaf.image, (leaf.x, leaf.y))
    # print('Leaves : ', round(perf_counter() - start, 6), end=" | ")

    if bloom:
        pass

    # start = perf_counter()
    #for button in buttons:
    #    button.draw(display)
    # print('GUI : ', round(perf_counter() - start, 6), end=" | ")

    # start = perf_counter()
    screen.blit(pygame.transform.scale(display, (WIDTH, HEIGHT)), (0, 0))
    # print('Display : ', round(perf_counter() - start, 6))

    if fade.active:
        fade.draw(screen)

    if debug:
        debug_screen(
            "x : "
            + str(player.pos[0])
            + "\ny : "
            + str(player.pos[1])
            + "\nz : "
            + str(round(170 - terrain.coords[terrain.center][terrain.center][1], 2))
        )

    pygame.display.update()
    temp += perf_counter() - start


if __name__ == "__main__":
    while True:
        handle_events()  # Manages button presses
        player.update()  # Manages the animation and the movements of the player
        render()

        pygame.display.set_caption(str(int(clock.get_fps())))
        clock.tick(FPS)

        tick += 1

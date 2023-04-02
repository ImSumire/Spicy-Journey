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
# Authors : @Zecyl and @ImSumire
#
# Requirements: python==3.*, pygame, noise, json, numba
#

import sys
import json

import pygame
from pygame.locals import *

from src.player import Player
from src.world import World
from src.leaf import Leaf
from src.gui import Gui


global seconds, tick, display, temp

#    ______  ______  __   __  ______  __  ______
#   /\  ___\/\  __ \/\ "-.\ \/\  ___\/\ \/\  ___\
#   \ \ \___\ \ \/\ \ \ \-.  \ \  __\\ \ \ \ \__ \
#    \ \_____\ \_____\ \_\\"\_\ \_\   \ \_\ \_____\
#     \/_____/\/_____/\/_/ \/_/\/_/    \/_/\/_____/
#

# Load the configuration file using the json lib
with open("config.json") as f:
    config = json.load(f)

# Access configuration values as dictionary items
WIDTH = config["dimensions"]["width"]
HEIGHT = config["dimensions"]["height"]
FPS = config["fps"]
TITLE = config["title"]
X_CENTER, Y_CENTER = CENTER = (WIDTH // 2, HEIGHT // 2)

g = 2
w = ""


def handle_events():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_F3:  # Active the debug screen
                gui.debug = not gui.debug

            elif event.key in [K_KP_MINUS, K_KP_PLUS]:  # Debugging
                world.temp += 1 if event.key == K_KP_PLUS else -1
                print("- Temp : %s" % world.temp)

            elif event.key in [K_m, K_p]:  # Debugging
                # world.offseted_x_center += 1 if event.key == K_p else -1
                # print("- Offset x cent : %s" % world.offseted_x_center)
                pass

            elif event.key == K_k:  # Change the keys
                if player.up == K_z:
                    player.up, player.left = K_w, K_a
                else:
                    player.up, player.left = K_z, K_q

        elif event.type == QUIT:
            print("Second per frame (average) :", round(seconds / tick, 5))
            sys.exit()


def render():
    display.fill((0, 0, 0))

    # Update the terrain coordinates
    world.update(int(player.pos.x), int(player.pos.y))

    # Get and display the sprites
    for sprite in world.get_sprites(player, tick):
        display.blit(sprite[0], (sprite[1], sprite[2]))

    # Draw the GUI
    gui.draw()

    # Draw the debug screen
    if gui.debug:
        gui.draw_debug(tick, seconds, clock.get_fps())

    # Draw the fade
    if gui.fade.active:
        gui.fade.draw(screen)

    # Update the display
    pygame.display.flip()


if __name__ == "__main__":
    from time import perf_counter

    #    __  __   __  __  ______
    #   /\ \/\ "-.\ \/\ \/\__  _\
    #   \ \ \ \ \-.  \ \ \/_/\ \/
    #    \ \_\ \_\\"\_\ \_\ \ \_\
    #     \/_/\/_/ \/_/\/_/  \/_/
    #

    # Initialization, setting of the window title and dimensions
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # (1280, 700)
    display = pygame.Surface(CENTER)  # (640, 350)
    clock = pygame.time.Clock()
    seconds = 0
    tick = 0

    # World creation
    world = World(WIDTH, HEIGHT)
    print("Seed :", world.seed)
    print("Valide spawn:", world.spawn)

    # Player
    player = Player(world.spawn)

    # GUI
    gui = Gui(WIDTH, HEIGHT, screen, display, player, world)

    #  ______  ______  ______  ______  ______
    # /\  ___\/\__  _\/\  __ \/\  __ \/\__  _\
    # \ \___  \/_/\ \/\ \  __ \ \  __<\/_/\ \/
    #  \/\_____\ \ \_\ \ \_\ \_\ \_\ \_\ \ \_\
    #   \/_____/  \/_/  \/_/\/_/\/_/ /_/  \/_/
    #

    while True:
        start = perf_counter()
        handle_events()  # Manages button presses
        player.update()  # Manages animation and movements of the player
        render()  # Make the calculations and draws the screen
        clock.tick(FPS)

        tick += 1
        seconds += perf_counter() - start

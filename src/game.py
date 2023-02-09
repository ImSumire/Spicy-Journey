import yaml
import noise
import sys

import pygame
from pygame.locals import *

from src.image import Image
from src.player import Player
from src.godray import Godray
from src.terrain import Terrain
from src.particule import Particule, create_particules


# Load the configuration file using yaml.safe_load
with open("_config.yml", "r") as f:
    config = yaml.safe_load(f)

# Access configuration values as dictionary items
width = config["game"]["dimensions"]["width"]
height = config["game"]["dimensions"]["height"]
fps = config["game"]["fps"]
title = config["title"]

# Initialization, setting of the window title and dimensions
pygame.init()
pygame.display.set_caption(title)
screen = pygame.display.set_mode((width, height), 0, 32)
display = pygame.Surface((width // 2, height // 2))
pygame.display.set_caption(title)

screen_size = screen.get_size()

# Allow only certains events
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

# Creation of the clock to recover the fps and block them
clock = pygame.time.Clock()

x_center = width // 4
y_center = height // 4

vegetation = []
for image in (
    ["little-tree1"]
    + ["little-tree2"]
    + ["tree1"]
    + ["tree2"]
    + ["tree3"]
    + ["little-tree2"]
    + ["rock" + str(n) for n in range(1, 5)]
    # bigrock0 | bigrock1 | bigrock2 | brush
):
    vegetation.append(Image(f"res/sprites/Props/{image}.png"))

godray = Godray(width, height)
player = Player()
block = Image("res/sprites/Terrain/sprite_00.png")
tree = Image("res/sprites/Props/little-tree1.png")
terrain = Terrain(block, vegetation, 0.14, width, height)

changed = True

# particules = create_particules(50, 'res/sprites/Atmosphere/leaves/', 2, 2, 2, rotation = True)

while True:
    # Inputs
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            # Movements
            if event.key == K_z:
                if not round(terrain.coords[terrain.center - 1][terrain.center - 1][2]):
                    player.y -= player.speed
                    player.x -= player.speed
                    changed = True

            elif event.key == K_s:
                if not round(terrain.coords[terrain.center + 1][terrain.center + 1][2]):
                    player.y += player.speed
                    player.x += player.speed
                    changed = True

            if event.key == K_q:
                if not round(terrain.coords[terrain.center + 1][terrain.center - 1][2]):
                    player.y += player.speed
                    player.x -= player.speed
                    changed = True

            elif event.key == K_d:
                if not round(terrain.coords[terrain.center - 1][terrain.center + 1][2]):
                    player.y -= player.speed
                    player.x += player.speed
                    changed = True

            # Render distance modifications
            if event.key == K_KP_MINUS:
                terrain.render_distance -= 1
                changed = True

            elif event.key == K_KP_PLUS:
                terrain.render_distance += 1
                changed = True

    # Particules
    # for particule in particules:
    #     particule.display_particules(display)

    # Update
    if changed:
        display.fill((0, 0, 0))

        # Terrain display
        terrain.draw_terrain(display, (player.x, player.y))

        player_pos = terrain.coords[terrain.center][terrain.center]
        pygame.draw.circle(display, "white", (player_pos[0], player_pos[1] + 16), 8)

        # Props display
        terrain.draw_props(display, (player.x, player.y))

        # Show `display` on `screen`
        screen.blit(pygame.transform.scale(display, screen_size), (0, 0))

        # Godray
        # godray.godray_display(screen)

        pygame.display.flip()
        changed = False

        # Set FPS to 60
        # clock.tick(fps)

    # Display FPS in the window title
    # pygame.display.set_caption(str(round(clock.get_fps(), 1)))

    # Set FPS to 60
    clock.tick(fps)

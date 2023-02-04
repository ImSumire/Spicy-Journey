import yaml

import pygame, sys, time
from pygame.locals import *
from random import randint, choice

from src.image import Image
from src.camera import Camera
from src.godray import Godray
from src.terrain import Terrain


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
camera = Camera()
block = Image("res/sprites/Terrain/sprite_00.png")
tree = Image("res/sprites/Props/little-tree1.png")
terrain = Terrain(block, vegetation, 0.14, width, height)

changed = True


while 1: # Works like `True` but more efficient (speed of execution) (This only has a notable effect on Python versions 2.x, not 3.x and above)
    display.fill((0, 0, 0))

    # Terrain display/draw
    terrain.draw(display, (camera.x, camera.y))

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
    keys = pygame.key.get_pressed()
    if keys[pygame.K_z] or keys[pygame.K_UP]:
        camera.y -= camera.speed
        camera.x -= camera.speed
        changed = True

    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        camera.y += camera.speed
        camera.x += camera.speed
        changed = True

    if keys[pygame.K_q] or keys[pygame.K_LEFT]:
        camera.x -= camera.speed
        camera.y += camera.speed
        changed = True

    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        camera.x += camera.speed
        camera.y -= camera.speed
        changed = True

    # Show `display` on `screen`
    screen.blit(pygame.transform.scale(display, screen_size), (0, 0))

    # Godray
    # godray.godray_display(screen)

    # Update
    if changed :
        pygame.display.flip()
        changed = False
        # Set FPS to 60
        #clock.tick(fps)

    # Display FPS in the window title
    pygame.display.set_caption(str(round(clock.get_fps(), 1)))

    # Set FPS to 60
    clock.tick(fps)

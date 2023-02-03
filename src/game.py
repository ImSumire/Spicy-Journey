import pygame, sys, time
from random import randint, choice
from pygame.locals import *
from src.terrain import Terrain
from src.image import Image
import yaml

# Load the configuration file using yaml.safe_load
with open("_config.yml", "r") as f:
    config = yaml.safe_load(f)

# Access configuration values as dictionary items
width = config["game"]["dimensions"]["width"]
height = config["game"]["dimensions"]["height"]
fps = config["game"]["fps"]
title = config["title"]


# Creation of the Camera class for traveling
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 1  # .5  # 0.17


# Creation of the Godray class for aesthetic
class Godray:
    def __init__(self, width, height):
        self.image = pygame.image.load("res/sprites/godray.png")
        self.display = pygame.Surface((width, height))
        self.display.blit(self.image, (0, 0))
        self.display.set_alpha(35)

    def godray_display(self, surf):
        surf.blit(self.display, (0, 0))


# Initialization, setting of the window title and dimensions
pygame.init()
pygame.display.set_caption(title)
screen = pygame.display.set_mode((width, height), 0, 32)
display = pygame.Surface((width // 2, height // 2))

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


while True:
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

    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        camera.y += camera.speed
        camera.x += camera.speed

    if keys[pygame.K_q] or keys[pygame.K_LEFT]:
        camera.x -= camera.speed
        camera.y += camera.speed

    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        camera.x += camera.speed
        camera.y -= camera.speed

    # Change of the render_distance
    if keys[pygame.K_KP_PLUS] or keys[pygame.K_PLUS]:
        terrain.render_distance += 1
    if keys[pygame.K_KP_MINUS] or keys[pygame.K_MINUS]:
        terrain.render_distance -= 1

    # Show `display` on `screen`
    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))

    # Godray
    godray.godray_display(screen)

    # Update
    pygame.display.flip()

    # Display FPS in the window title
    pygame.display.set_caption(str(round(clock.get_fps(), 1)))

    # Set FPS to 60
    clock.tick(fps)

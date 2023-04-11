import pygame
import sys
from src.noise import *
import noise as ns

# import matplotlib.pyplot as plt
# import numpy as np


#      ____     _ __
#     /  _/__  (_) /_
#    _/ // _ \/ / __/
#   /___/_//_/_/\__/
#

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Define the dimensions of the window
window_width = 1280
window_height = 720

# Create the window
screen = pygame.display.set_mode((window_width, window_height))

# Define the size of the squares
square_size = 8

# Define the distance at which the squares should be displayed
distance = 40 * square_size

# Get the center of the window
center_x, center_y = window_width // 2, window_height // 2


### Function to apply colors to the different regions of the map
def height(h):  # Sand [156, 145, 93]
    return brighten(
        [
            [19, 20, 87],  # Sea
            [19, 20, 87],  # Sea
            [19, 20, 87],  # Sea
            [17, 54, 5],  # Grass
            [17, 54, 5],  # Grass
            [42, 42, 42],  # Mountain
            [181, 181, 181],  # Snow on the moutains
            [181, 181, 181],  # Snow on the moutains
        ][h // 13],
        h // 2,
    )


### Function to adjust color shades    r                g                b
def brighten(color, rate):
    #return "#%02x%02x%02x" % (color[0] + rate, color[1] + rate, color[2] + rate)
    return [color[0] + rate, color[1] + rate, color[2] + rate]


#    _____
#   / ___/__ ___ _  ___ _______ _
#  / /__/ _ `/  ' \/ -_) __/ _ `/
#  \___/\_,_/_/_/_/\__/_/  \_,_/
#

# Creation of the Camera class to move on the map
class Camera:
    def __init__(self):
        self.x = 30000
        self.y = 30000
        self.scale = 1
        self.speed = 0.04


# Instance of the Camera
camera = Camera()

# Placement of the seed
new_seed()

# Function that darkens the white
def get_color(n: float):
    gray_value = int((1 - abs(n)) * 128)
    return (gray_value, gray_value, gray_value)


#     ___             ___          __  _
#    / _ | ___  ___  / (_)______ _/ /_(_)__  ___
#   / __ |/ _ \/ _ \/ / / __/ _ `/ __/ / _ \/ _ \
#  /_/ |_/ .__/ .__/_/_/\__/\_,_/\__/_/\___/_//_/
#       /_/  /_/

# Run the main loop
while True:
    # Check all events
    if [event for event in pygame.event.get() if event.type == pygame.QUIT]:
        pygame.quit()
        sys.exit()

    """
    for event in pygame.event.get():
        # If the user has clicked on the cross to close the window, exit the program
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Scroll Zoom
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_WHEELUP:
                camera.scale *= 0.98
            elif event.button == pygame.BUTTON_WHEELDOWN:
                camera.scale *= 1.02
    """

    # ZQSD camera movement
    keys = pygame.key.get_pressed()

    # KeyPad +/- Zooom
    """
    if keys[pygame.K_KP_PLUS] or keys[pygame.K_PLUS]:
        camera.scale *= 0.99
    if keys[pygame.K_KP_MINUS] or keys[pygame.K_MINUS]:
        camera.scale *= 1.01
    """

    if keys[pygame.K_z] or keys[pygame.K_UP]:
        camera.y -= camera.speed * 200
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        camera.y += camera.speed * 200

    if keys[pygame.K_q] or keys[pygame.K_LEFT]:
        camera.x -= camera.speed * 200
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        camera.x += camera.speed * 200

    """
    # Mouse camera movement
    left_click = pygame.mouse.get_pressed()[0]
    # If the left mouse click is pressed, move the camera according to the mouse position
    if left_click:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        camera.x += (mouse_x - window_width // 2) * camera.speed
        camera.y += (mouse_y - window_height // 2) * camera.speed
    """

    # Clear the screen in black
    screen.fill((0, 0, 0))

    # Go through all the squares at a distance smaller than the distance from the center of the window
    for x in range(center_x - distance, center_x + distance + 1, square_size):
        for y in range(center_y - distance, center_y + distance + 1, square_size):
            # Use simplex noise to determine color
            x_temp = (x + camera.x) * 0.5  # * camera.scale
            y_temp = (y + camera.y) * 0.5  # * camera.scale

            pygame.draw.rect(
                screen,
                height(
                    int(
                        (
                            ns.snoise2(
                                x_temp / 100,
                                y_temp / 100,
                            )
                            + ns.snoise2(
                                x_temp / 33,
                                y_temp / 33,
                            )
                            / 3
                            + 1
                        )
                        * 40
                    )
                ),
                (x, y, square_size, square_size),
            )
            """
            pygame.draw.rect(
                screen,
                height(
                    int(
                        (
                            noise(
                                x_temp / 100,
                                y_temp / 100,
                            )
                            + noise(
                                x_temp / 33,
                                y_temp / 33,
                            )
                            / 3
                            + 1
                        )
                        * 50
                    )
                ),
                (x, y, square_size, square_size),
            )
            """
            """
            REALISTIC
            pygame.draw.rect(
                screen,
                height(
                    int(
                        (
                            noise(
                                x_temp / 800,
                                y_temp / 800,
                            )
                            + noise(
                                x_temp / 100,
                                y_temp / 100,
                            )
                            / 20
                            + noise(
                                x_temp / 33,
                                y_temp / 33,
                            )
                            / 25
                            + 1
                        )
                        * 50
                    )
                ),
                (x, y, square_size, square_size),
            )
            """

    # Updating the screen
    pygame.display.flip()

    # Display the fps in the window title
    pygame.display.set_caption(str(round(clock.get_fps(), 1)))

    # 60 FPS
    clock.tick(60)

import pygame
import sys
from noise import snoise2

"""
Use for debugging, to visualize noise
"""

#      ____     _ __
#     /  _/__  (_) /_
#    _/ // _ \/ / __/
#   /___/_//_/_/\__/
#

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Define the dimensions of the window
window_width = 640
window_height = 480

# Create the window
screen = pygame.display.set_mode((window_width, window_height))

# Define the size of the squares
square_size = 8

# Define the distance at which the squares should be displayed
distance = 25 * square_size


#    _____
#   / ___/__ ___ _  ___ _______ _
#  / /__/ _ `/  ' \/ -_) __/ _ `/
#  \___/\_,_/_/_/_/\__/_/  \_,_/
#

# Creation of the Camera class to move on the map
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.scale = 1
        self.speed = 0.04


# Instance of the Camera
camera = Camera()

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
    for event in pygame.event.get():
        # If the user has clicked on the cross to close the window, exit the program
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Scroll Zoom
        #elif event.type == pygame.MOUSEBUTTONDOWN:
        #    if event.button == pygame.BUTTON_WHEELUP:
        #        camera.scale *= 1.02
        #    elif event.button == pygame.BUTTON_WHEELDOWN:
        #        camera.scale *= 0.98

    # KeyPad +/- Zooom
    keys = pygame.key.get_pressed()
    if keys[pygame.K_KP_PLUS] or keys[pygame.K_PLUS]:
        camera.scale *= 1.01
    if keys[pygame.K_KP_MINUS] or keys[pygame.K_MINUS]:
        camera.scale *= 0.99

    # ZQSD camera movement
    if keys[pygame.K_UP]:
        camera.y -= camera.speed * 200
    if keys[pygame.K_DOWN]:
        camera.y += camera.speed * 200
    if keys[pygame.K_LEFT]:
        camera.x -= camera.speed * 200
    if keys[pygame.K_RIGHT]:
        camera.x += camera.speed * 200


    # Mouse camera movement
    left_click = pygame.mouse.get_pressed()[0]
    # If the left mouse click is pressed, move the camera according to the mouse position
    if left_click:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        camera.x += (mouse_x - window_width // 2) * camera.speed
        camera.y += (mouse_y - window_height // 2) * camera.speed

    # Clear the screen in black
    screen.fill((0, 0, 0))

    # Get the center of the window
    center_x, center_y = window_width // 2, window_height // 2

    # Go through all the squares at a distance smaller than the distance from the center of the window
    for x in range(center_x - distance, center_x + distance + 1, square_size):
        for y in range(center_y - distance, center_y + distance + 1, square_size):
            pygame.draw.rect(
                screen,
                get_color(
                    snoise2(
                        (x + camera.x) / (300 * camera.scale),
                        (y + camera.y) / (300 * camera.scale),
                    )
                ),
                (x, y, square_size, square_size),
            )

    # Updating the screen
    pygame.display.flip()

    # Display the fps in the window title
    pygame.display.set_caption("%s | %s" % (str(round(clock.get_fps(), 1)), camera.scale))

    # 60 FPS
    clock.tick(60)
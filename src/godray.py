import pygame

# Creation of the Godray class for aesthetic
class Godray:
    def __init__(self, width, height):
        self.image = pygame.image.load("res/sprites/godray.png")
        self.display = pygame.Surface((width, height))
        self.display.blit(self.image, (0, 0))
        self.display.set_alpha(35)

    def godray_display(self, surf):
        surf.blit(self.display, (0, 0))
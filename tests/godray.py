import pygame

# Creation of the Godray class for aesthetic
class Godray:
    def __init__(self, width, height):
        self.image = pygame.image.load("res/sprites/godray.png").convert_alpha()
        self.display = pygame.Surface((width, height), pygame.SRCALPHA)
        self.display.set_alpha(60)  # 60
        self.display.blit(self.image, (0, 0))

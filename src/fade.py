import pygame


class Fade:
    def __init__(self, width, height):
        self.display = pygame.Surface((width, height))
        self.display.fill((0, 0, 0))
        self.alpha = 0
        self.active = False
        self.direction = 1
        self.speed = 3

    def draw(self, surf):
        self.active = True
        self.alpha += self.speed * self.direction
        if self.alpha >= 255:
            self.direction = -1

        elif self.alpha < 0:
            self.active = False
            self.alpha = 0
            self.direction = 1

        self.display.set_alpha(self.alpha)
        surf.blit(self.display, (0, 0))

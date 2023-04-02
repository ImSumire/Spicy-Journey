import pygame
import sys
from math import cos, pi
from random import randint, uniform

pygame.init()
pygame.display.set_caption("Animation")
screen = pygame.display.set_mode((1280, 700))
clock = pygame.time.Clock()


class Point:
    def __init__(self, end, start, speed=1):
        self.end = end
        self.start = start

        self.pos = start

        self.step = 0
        self.steps = 1 / (speed * 0.002)
        self.final = self.steps // 3

        self.speed = 1 / self.steps
        self.delta = 0

    def animate(self):
        """
        f(x) = cos(x * 3) + 0.95
        But 0.95 does not work even though the integral of f from 0 to 1 is equal to 1...
        After some tests, the best result is 0.9898, why not ?
        """
        if int(self.step) != self.final:
            self.delta += self.speed * self.step * (cos(3 * self.delta) + 0.9898)
            self.step += 1
            self.pos = (
                int(self.start[0] + self.delta * (self.end[0] - self.start[0])),
                int(self.start[1] + self.delta * (self.end[1] - self.start[1])),
            )
        else:
            self.pos = self.end


points = [
    Point((randint(0, 1280), randint(0, 700)), (randint(0, 1280), randint(0, 700)), speed=uniform(0.5, 5)) for i in range(1000)
]
point_size = 2


if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        for point in points:
            point.animate()
            pygame.draw.circle(screen, (0, 255, 0), point.start, point_size)
            pygame.draw.circle(screen, (255, 0, 0), point.pos, point_size)
            pygame.draw.circle(screen, (0, 0, 255), point.end, point_size)

        pygame.display.update()
        clock.tick(60)

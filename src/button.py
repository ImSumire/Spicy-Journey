#  ______  __  __  ______  ______  ______  __   __
# /\  __ \/\ \/\ \/\__  _\/\__  _\/\  __ \/\ "-.\ \
# \ \  __<\ \ \_\ \/_/\ \/\/_/\ \/\ \ \/\ \ \ \-.  \
#  \ \_____\ \_____\ \ \_\   \ \_\ \ \_____\ \_\\"\_\
#   \/_____/\/_____/  \/_/    \/_/  \/_____/\/_/ \/_/
#

from math import cos
import pygame


def nothing():
    pass


# Init the font
pygame.init()
font = pygame.font.Font("res/font/8-bit.ttf", 12)


class Button:
    # Why Use  `__slots__`? The short answer is  slots  are more efficient in terms of
    # memory space and speed of access, and a bit safer than the default Python method
    # of data access. By default, when Python creates  a new  instance of  a class, it
    # creates a __dict__ attribute for the class.

    __slots__ = (
        "pressed",
        # Colors
        "color",
        "outside",
        "over",
        # Display
        "rect",
        "text_surf",
        "text_rect",
        # On click
        "function",
        # Animation
        "animation",
        "start",
        "end",
        "step",
        "steps",
        "final",
        "speed",
        "delta",
    )

    def __init__(self, text, pos, function, end=None, destroy=False):
        size = font.size(text)
        width = size[0] + 30
        height = size[1] + 3

        x, y = pos

        self.pressed = False

        self.color = (179, 127, 69)
        self.outside = (179, 127, 69)
        self.over = (186, 138, 84)

        self.rect = pygame.Rect((x - width // 2, y - height // 2), (width, height))
        self.text_surf = font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        self.function = function

        if end is None:
            self.animation = False
        else:
            self.animation = True

            self.start = (x, y)
            self.end = end

            self.step = 0
            self.steps = 1 / (0.0016)
            self.final = self.steps // 7

            self.speed = 1 / self.steps
            self.delta = 0

    def draw(self, surf):
        self.check()
        if self.animation:
            self.animate()
        pygame.draw.rect(surf, self.color, self.rect)
        surf.blit(self.text_surf, self.text_rect)

    def check(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.color = self.over
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.function()
                    self.pressed = False
        else:
            self.color = self.outside

    def animate(self):
        """
        f(x) = cos(x * 3) + 0.95
        But 0.95 does not work even though the integral of f from 0 to 1 is equal to 1...
        After some tests, the best result is 0.9898, why not ?
        """
        if int(self.step) != self.final:
            self.delta += self.speed * self.step * (cos(3 * self.delta) + 0.9898)
            self.step += 1
            x = self.start[0] + self.delta * (self.end[0] - self.start[0])
            y = self.start[1] + self.delta * (self.end[1] - self.start[1])
            self.rect.centerx = x
            self.rect.centery = y
            self.text_rect.centerx = x
            self.text_rect.centery = y
        else:
            self.rect.centerx, self.rect.centery = self.end

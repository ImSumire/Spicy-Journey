import pygame

light = (218, 205, 169)
inventory = (179, 127, 69)
second = (202, 160, 103)


class Button:
    def __init__(self, text, font, width, height, pos, function):
        self.pressed = False

        self.color = (179, 127, 69)
        self.outside = (179, 127, 69)
        self.over = (202, 160, 103)

        self.top_rect = pygame.Rect(pos, (width, height))
        self.text_surf = font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        self.function = function

    def draw(self, surf):
        self.check()
        pygame.draw.rect(surf, self.color, self.top_rect)  # , border_radius=8)
        surf.blit(self.text_surf, self.text_rect)

    def check(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.color = self.over
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.function()
                    self.pressed = False
        else:
            self.color = self.outside

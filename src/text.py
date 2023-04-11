#  ______  ______  __  __  ______
# /\__  _\/\  ___\/\_\_\_\/\__  _\
# \/_/\ \/\ \  __\\/_/\_\/\/_/\ \/
#    \ \_\ \ \_____\/\_\/\_\ \ \_\
#     \/_/  \/_____/\/_/\/_/  \/_/
#

import pygame

# Initialisation de la police
pygame.init()
font = pygame.font.Font("res/font/8-bit.ttf", 12)


class Text:
    def __init__(self, text, pos, color, max_width):
        self.text = text
        self.pos = pos
        self.color = color
        self.space_width = font.size(" ")[0]  # La largeur d'un espace.
        self.max_width = max_width + self.pos[0]

    def draw(self, surf):
        # Tableau 2D dont chaque ligne est une liste de mots.
        words = [word.split(" ") for word in self.text.splitlines()]
        x, y = self.pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, self.color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= self.max_width:
                    # Réinitialiser le x.
                    x = self.pos[0]
                    # Commencer une nouvelle rangée.
                    y += word_height
                surf.blit(word_surface, (x, y))
                x += word_width + self.space_width
            # Réinitialiser le x.
            x = self.pos[0]
            # Commencer une nouvelle rangée.
            y += word_height

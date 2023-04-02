from src.tools.resize import resize
from src.godray import Godray
from src.button import Button
from src.image import Image
from src.fade import Fade
from src.leaf import Leaf
import pygame

light = (218, 205, 169)
inventory = (179, 127, 69)
second = (202, 160, 103)


def nothing():
    pass


# Init the font
pygame.init()
font = pygame.font.Font("res/font/8-bit.ttf", 12)

#  ______  __  __  __
# /\  ___\/\ \/\ \/\ \
# \ \ \__ \ \ \_\ \ \ \
#  \ \_____\ \_____\ \_\
#   \/_____/\/_____/\/_/
#


class Gui:
    def __init__(self, width, height, surf, display, player, world):
        # Dimensions
        self.width = width
        self.height = height

        # Instances
        self.surf = surf
        self.world = world
        self.display = display
        self.player = player
        self.fade = Fade(width, height, surf)
        self.leaves = [Leaf(height) for _ in range(100)]
        self.godray = Godray(width, height, surf)

        # Positions constants
        self.center = (width // 2, height // 2)

        self.title_img = (width // 2 - 149, 80)
        self.title_play = (width // 2, height // 2 + 150)
        self.title_sett = (width // 2, height // 2 + 190)

        self.back = (width // 2, height - 80)

        self.menu = (width - 80, height - 25)
        self.settings = (width - 400, height - 25)
        self.cook = (width - 280, height - 25)
        self.photo = (width - 180, height - 25)

        # Content
        self.title()

        # Debug screen
        self.debug = False

    def draw(self):
        # Draw leaves
        for leaf in self.leaves:
            leaf.update()
            self.display.blit(leaf.image, (leaf.x, leaf.y))

        # Draw the display in the main screen
        self.surf.blit(
            pygame.transform.scale(self.display, (self.width, self.height)), (0, 0)
        )

        if self.godray.active:
            self.godray.draw()

        # Draw elements
        for element in self.content:
            element.draw(self.surf)

    # Lauch game after title screen
    def start(self):
        self.fade.active = True
        self.fade.func = self.main

    # Title screen
    def title(self):
        self.content = [
            Button("Enter into the world", self.title_play, self.start),
            Button("Settings", self.title_sett, lambda: self.settings_menu(True)),
            Image("res/sprites/Logo/deep-blue.png", self.surf, self.title_img),
        ]

    # Settings with title screen back button
    def settings_menu(self, title=False):
        self.content = [
            Button("Back", self.back, lambda: (self.title() if title else self.main())),
            Button(
                "Leaves : %s" % ("On" if self.leaves else "Off"),
                (self.width // 2, self.height // 2),
                lambda: (
                    setattr(
                        self,
                        "leaves",
                        (
                            []
                            if self.leaves
                            else [Leaf(self.height) for _ in range(100)]
                        ),
                    ),
                    self.settings_menu(title),
                ),
            ),
            Button(
                "Godray : %s" % ("On" if self.godray.active else "Off"),
                (self.width // 2, self.height // 2 - 40),
                lambda: (
                    setattr(self.godray, "active", not self.godray.active),
                    self.settings_menu(title),
                ),
            ),
        ]

    # Main menu without animation
    def main(self):
        self.player.play = True
        self.content = [
            Button("Open menu", self.menu, self.menu_opened),
        ]

    # Main menu closed
    def menu_closed(self):
        self.content = [
            Button("Settings", self.settings, nothing, end=self.menu),
            Button("Cook", self.cook, nothing, end=self.menu),
            Button("Photo", self.photo, nothing, end=self.menu),
            Button("Open menu", self.menu, self.menu_opened),
        ]

    # Main menu opened
    def menu_opened(self):
        self.content = [
            Button("Settings", self.menu, self.settings_menu, end=self.settings),
            Button("Cook", self.menu, nothing, end=self.cook),
            Button("Photo", self.menu, nothing, end=self.photo),
            Button("X", self.menu, self.menu_closed),
        ]

    # Draw each lines of the debug screen
    def draw_debug(self, tick, seconds, fps):
        x, y = self.player.pos
        z = round(self.world.coords[self.world.center][self.world.center][3], 2)

        debug_lines = (
            "fps : %s (%s)" % (int(fps), int(tick // seconds))
            + "\nx : %s" % x
            + "\ny : %s" % y
            + "\nz : %s" % z
            # + "\ningredient : %s" % ingredient_around
        )

        for index, line in enumerate(debug_lines.split("\n")):
            self.surf.blit(
                font.render(
                    line,  # Text
                    True,  # Anti-aliasing
                    "white",  # Color
                ),
                (10, 10 + 25 * index),
            )

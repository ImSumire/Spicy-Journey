#  ______  __  __  __
# /\  ___\/\ \/\ \/\ \
# \ \ \__ \ \ \_\ \ \ \
#  \ \_____\ \_____\ \_\
#   \/_____/\/_____/\/_/
#

from src.tools.lang import load_lang, get_langs
from res.recipes import recipes
from src.godray import Godray
from src.button import Button
from src.image import Image
from src.mixer import Mixer
from src.fade import Fade
from src.leaf import Leaf
from src.text import Text

from datetime import datetime
import subprocess
import pygame
import os


# Création d'une fonction qui ne fait rien
def nothing():
    pass


# Initialisation de la police
pygame.init()
font = pygame.font.Font("res/font/8-bit.ttf", 12)


class Gui:
    def __init__(self, width, height, surf, display, player, world):
        # Dimensions
        self.width = width
        self.height = height

        # Instances
        self.surf = surf
        self.world = world
        self.mixer = Mixer()
        self.player = player
        self.display = display
        self.godray = Godray(width, height, surf)
        self.leaves = [Leaf(height) for _ in range(200)]

        # Langue
        self.lang_id = "fr"
        self.lang_ids = get_langs()
        self.lang_index = self.lang_ids.index(self.lang_id)
        self.lang = load_lang(self.lang_id)

        # Fondues
        self.fade = Fade(width, height, 2, surf)
        self.photo_fade = Fade(width, height, 20, surf)
        self.ui_fade = Fade(width, height, 0, surf, (0, 0, 0))
        self.ui_fade.display.set_alpha(35)

        # Constantes de position
        self.center = (width // 2, height // 2)

        self.title_play = (width // 2, height // 2 + 150)
        self.title_sett = (width // 2, height // 2 + 190)

        self.back = (width // 2, height - 80)

        self.menu = (width - 80, height - 25)
        self.photo = (width - 175, height - 25)
        self.cook = (width - 300, height - 25)
        self.settings = (width - 440, height - 25)
        self.album = (width - 565, height - 25)

        # Constantes d'éléments
        self.logo = Image("res/sprites/logo.png", (width // 2 - 149, 80))
        self.book = Image("res/sprites/book.png", (width // 2 - 187, 80))

        # Contenues
        self.title()

        # Écran de débogage
        self.debug = False

        # Recettes
        self.recipes = [
            "\n\n".join(
                (
                    key,
                    "\n".join(
                        [
                            "- " + ingredient.replace("#", "any ")
                            for ingredient in ingredients
                        ]
                    ),
                )
            )
            for key, ingredients in recipes.items()
        ]

    @staticmethod
    def open_dir():
        """
        La méthode  statique "open_dir"  ouvre  le répertoire  "screenshots/" en
        utilisant   l'explorateur  de    fichiers   approprié  pour   le système
        d'exploitation actuel. Si le système   d'exploitation n'est pas  pris en
        charge, une exception est levée.
        """
        path = "screenshots/"

        if os.name == "nt":  # Pour Windows
            subprocess.Popen('explorer "' + path + '"')
        elif os.name == "posix":  # Pour Linux ou macOS
            subprocess.Popen(["xdg-open", path])
        else:
            raise Exception("OS not supported")

    def draw(self):
        # Affichage des feuilles
        for leaf in self.leaves:
            leaf.update()
            self.display.blit(leaf.image, (leaf.x, leaf.y))

        # Dessiner l'affichage dans l'écran principal
        self.surf.blit(
            pygame.transform.scale(self.display, (self.width, self.height)),
            (0, 0),
        )

        # Affichage des rayons de soleil
        if self.godray.active:
            self.godray.draw()

        # Affichage du fade des UI
        if self.ui_fade.active:
            self.surf.blit(self.ui_fade.display, (0, 0))

        # Affichage des éléments du GUI
        for element in self.content:
            element.draw(self.surf)

    # Lancer le jeu après l'écran titre
    def start(self):
        self.fade.active = True
        self.fade.func = self.main

    def take_photo(self):
        self.mixer.photo_sound.play()
        pygame.image.save(
            self.surf,
            "screenshots/%s.png"
            % str(datetime.now()).replace(" ", "_").replace(":", "."),
            # 2023-04-07_10.53.20.638260
            # année-mois-jour_heure.minute.seconde.microseconde
        )
        self.photo_fade.active = True

    #  __  __  __
    # /\ \/\ \/\ \
    # \ \ \_\ \ \ \
    #  \ \_____\ \_\
    #   \/_____/\/_/
    #

    # Le code ci-dessous est assez en bazarre, il ne fait qu'appliquer une liste
    # de boutons et images dans le contenue de l'interface.

    # Écran titre
    def title(self):
        self.ui_fade.active = False
        self.content = [
            Button(self.lang["world.enter"], self.title_play, self.start),
            Button(
                self.lang["settings"],
                self.title_sett,
                lambda: self.settings_ui(True),
            ),
            self.logo,
        ]

    def book_ui(self, page=0):
        self.mixer.page_sound()
        self.ui_fade.active = True
        self.player.move = False
        self.content = [
            Button(
                self.lang["book.prev"],
                (self.width // 2 - 300, self.height // 2 + 120),
                lambda: self.book_ui(page - 1) if page > 0 else nothing,
            ),
            Button(
                self.lang["book.next"],
                (self.width // 2 + 300, self.height // 2 + 120),
                lambda: self.book_ui(page + 1)
                if page < len(self.recipes) - 1
                else nothing,
            ),
            self.book,
            Text(
                self.recipes[page],
                (500, 120),
                (0, 0, 0),
                300,
            ),
            Button(self.lang["close"], self.back, self.main),
        ]

    # Paramètres avec ou sans retour à l'écran titre
    def settings_ui(self, title: bool = False):
        self.ui_fade.active = True
        self.player.move = False
        self.content = [
            Button(
                self.lang["back"],
                self.back,
                lambda: (self.title() if title else self.main()),
            ),
            Button(
                "%s : %s"
                % (
                    self.lang["settings.leaves"],
                    (self.lang["on"] if self.leaves else self.lang["off"]),
                ),
                (self.width // 2, self.height // 2 + 40),
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
                    self.settings_ui(title),
                ),
            ),
            Button(
                "%s : %s"
                % (
                    self.lang["settings.godray"],
                    (self.lang["on"] if self.godray.active else self.lang["off"]),
                ),
                (self.width // 2, self.height // 2),
                lambda: (
                    setattr(self.godray, "active", not self.godray.active),
                    self.settings_ui(title),
                ),
            ),
            Button(
                "%s : %s"
                % (
                    self.lang["settings.switch"],
                    (
                        self.lang["on"]
                        if not self.player.up == pygame.K_z
                        else self.lang["off"]
                    ),
                ),
                (self.width // 2, self.height // 2 - 40),
                lambda: (
                    self.player.switch(),
                    self.settings_ui(title),
                ),
            ),
            Button(
                "%s : %s"
                % (
                    self.lang["settings.language"],
                    self.lang[self.lang_ids[self.lang_index]],
                ),
                (self.width // 2, self.height // 2 - 80),
                lambda: (
                    setattr(
                        self, "lang_index", (self.lang_index + 1) % len(self.lang_ids)
                    ),
                    setattr(self, "lang", load_lang(self.lang_ids[self.lang_index])),
                    self.settings_ui(title),
                ),
            ),
        ]

    # Menu principal sans animation
    def main(self):
        self.ui_fade.active = False
        self.player.exist = self.player.move = True
        self.content = [
            Button(self.lang["menu.open"], self.menu, self.menu_opened),
        ]

    # Menu principal fermé
    def menu_closed(self):
        self.ui_fade.active = False
        self.content = [
            Button(self.lang["menu.album"], self.album, nothing, end=self.menu),
            Button(self.lang["settings"], self.settings, nothing, end=self.menu),
            Button(self.lang["menu.book"], self.cook, nothing, end=self.menu),
            Button(self.lang["menu.photo"], self.photo, nothing, end=self.menu),
            Button(self.lang["menu.open"], self.menu, self.menu_opened),
        ]

    # Menu principal ouvert
    def menu_opened(self):
        self.ui_fade.active = False
        self.content = [
            Button(self.lang["menu.album"], self.menu, self.open_dir, end=self.album),
            Button(
                self.lang["settings"], self.menu, self.settings_ui, end=self.settings
            ),
            Button(self.lang["menu.book"], self.menu, self.book_ui, end=self.cook),
            Button(self.lang["menu.photo"], self.menu, self.take_photo, end=self.photo),
            Button(self.lang["menu.close"], self.menu, self.menu_closed),
        ]

    # Dessinez chaque ligne de l'écran de débogage
    def draw_debug(self, tick, seconds, fps):
        x, y = self.player.pos
        pos = self.world.coords[self.world.center + round(y - int(y))][
            self.world.center + round(x - int(x))
        ]
        z = round(pos[3], 2)

        debug_lines = (
            "fps : %s (%s)" % (int(fps), int(tick // seconds))
            + "\nx : %s" % x
            + "\ny : %s" % y
            + "\nz : %s" % z
            + "\n%s : %s" % (self.lang["debug.seed"], self.world.seed)
        )

        for index, line in enumerate(debug_lines.split("\n")):
            self.surf.blit(
                font.render(
                    line,  # Texte
                    True,  # Anti-aliasing
                    (255, 255, 255),  # Couleur
                ),
                (10, 10 + 25 * index),
            )
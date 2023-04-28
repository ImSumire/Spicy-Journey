"""
Ce  module  comporte  la  classe  GUI (Graphical  User Interface)  qui  comprend
l'ensemble de la gestion de l'interface.
"""

#  ______  __  __  __
# /\  ___\/\ \/\ \/\ \
# \ \ \__ \ \ \_\ \ \ \
#  \ \_____\ \_____\ \_\
#   \/_____/\/_____/\/_/
#

# pylint: disable=duplicate-code
# Pour pouvoir lancer le programme avec n'importe quel fichier
if __name__ == "__main__":
    from os.path import dirname, realpath, join
    from subprocess import call
    import sys

    DIR_PATH = dirname(realpath(__file__))
    call(["python3", join(DIR_PATH, "../main.py")])

    sys.exit()

# pylint: disable=no-member
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=consider-using-with
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-f-string
# pylint: disable=too-many-instance-attributes

import os
import subprocess
from datetime import datetime
import pygame

from src.text import Text
from src.leaf import Leaf
from src.fade import Fade
from src.mixer import Mixer
from src.image import Image
from src.button import Button
from src.godray import Godray
from src.tools.resize import resize
from src.tools.lang import load_lang, get_langs

from res.recipes import recipes


def nothing():
    """
    Création d'une fonction qui ne fait rien.
    """
    return


# Initialisation de la police
pygame.init()
FONT = pygame.font.Font("res/font/8-bit.ttf", 12)


class Gui:
    """
    Cette classe  comporte la gestion de l'interface. Elle gère les boutons, le
    logo, le livre de recette, les feuilles tombantes et les rayons de soleil.
    """

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
        self.godray = Godray(surf)
        self.leaves = [Leaf(height) for _ in range(200)]

        # Langue
        self.lang_id = "fr"
        self.lang_ids = get_langs()
        self.lang_index = self.lang_ids.index(self.lang_id)
        self.lang = load_lang(self.lang_id)

        # Fondues
        self.fade = Fade(width, height, 3, surf)
        self.photo_fade = Fade(width, height, 20, surf)
        self.ui_fade = Fade(width, height, 0, surf, (0, 0, 0))
        self.ui_fade.display.set_alpha(35)

        # Constantes de position
        self.center = (width // 2, height // 2)

        self.title_play = (width // 2, height // 2 + 150)
        self.title_sett = (width // 2, height // 2 + 190)

        self.back = (width // 2, height - 80)

        self.cook_place = (width // 2, height - 125)

        self.menu = (width - 80, height - 25)
        self.photo = (width - 175, height - 25)
        self.cook = (width - 300, height - 25)
        self.settings = (width - 440, height - 25)
        self.album = (width - 565, height - 25)

        # Constantes d'éléments
        self.logo = Image("res/sprites/logo.png", (width // 2 - 149, 80))
        self.book = Image("res/sprites/book.png", (width // 2 - 187, 80))
        self.check = Image("res/sprites/check.png", (width // 2 + 20, 380))

        # Contenues
        self.content = []
        self.title()

        # Screenshot
        self.take_picture = False

        # Écran de débogage
        self.debug = False

        # Recettes
        self.load_recipes()
        self.load_ingredients()

    ### Gestion des recettes

    def load_recipes(self):
        """
        Cette méthode  a pour but de charger des recettes depuis le dictionnaire
        de recettes et de les formater  et  traduire pour les rendre utilisables
        dans le livre des recettes.
        """
        # Création de la liste de recettes (en format texte)
        self.recipes_text = []
        # et en format liste
        self.recipes = []

        # Parcours du dictionnaire de recettes
        for key, ingredients in recipes.items():
            self.recipes.append(ingredients)

            # Formatage de chaque recette
            # recipe = self.lang[key] + "\n\n"
            recipe = key + "\n\n"

            for ingredient in ingredients:
                if ingredient.startswith("#"):
                    recipe += "- "
                    recipe += self.lang["any"] + " "
                    recipe += self.lang[ingredient.replace("#", "")]
                    recipe += "\n"
                else:
                    recipe += "- " + self.lang[ingredient] + "\n"

            # Ajout de la recette formatée à la liste
            self.recipes_text.append(recipe)

    def load_ingredients(self):
        """
        Cette méthode enregistre dans dictionnaire les images des ingrédients.
        """
        self.ingredient_images = {}
        for ingredient in self.world.ingredients_list:
            self.ingredient_images[ingredient] = resize(
                pygame.image.load(
                    "res/sprites/Ingredients/%s.png" % ingredient
                ).convert_alpha(),
                1.4,
            )

    @staticmethod
    def can_cook(inv, _recipe):
        """
        Vérifie si le plat peut être cuisiné.
        """
        for ingredient in set(_recipe):
            if ingredient not in inv or _recipe.count(ingredient) > inv[ingredient]:
                return False
        return True

    def cooking(self, _page):
        """
        Supprime les ingrédients de l'inventaire et ajoute le plat.
        """
        # Récupération de la liste des ingrédients
        _recipe = self.recipes[_page]

        # Parcours les ingrédients de la recette
        for ingredient in set(_recipe):
            if ingredient in self.player.inventory:
                # Enlever les ingrédients
                self.player.inventory[ingredient] -= _recipe.count(ingredient)
                # Éviter de laisser des valeurs vides dans l'inventaire
                if self.player.inventory[ingredient] == 0:
                    del self.player.inventory[ingredient]
                # Ajout du plat
                self.player.dishes.add(_page)
        self.book_ui(page=_page)


    ### Gestion des screenshoots et album

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
            print("Your os is unsupported, go to ./screenshots/")

    def take_photo(self):
        """
        Prend une photo.
        """
        self.mixer.photo_sound.play()
        self.take_picture = True

    ### Affichage

    def draw(self):
        """
        Ce méthode affiche l'interface graphique du jeu:
        - Les feuilles (et mise à jour au passage)
        - L'écran de jeu
        - Les rayons de soleil
        - ...
        """
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

        for index, (ingredient, number) in enumerate(self.player.inventory.items()):
            self.surf.blit(
                self.ingredient_images[ingredient], (self.width - 52, 20 + 52 * index)
            )
            self.surf.blit(
                FONT.render(
                    "x " + str(number),  # Texte
                    True,  # Anti-aliasing
                    (255, 255, 255),  # Couleur
                ),
                (self.width - 100, 30 + 52 * index),
            )

        if self.take_picture:
            pygame.image.save(
                self.surf,
                "screenshots/%s.png"
                % str(datetime.now()).replace(" ", "_").replace(":", "."),
                # 2023-04-07_10.53.20.638260
                # année-mois-jour_heure.minute.seconde.microseconde
            )
            self.photo_fade.active = True
            self.take_picture = False

    # Lancer le jeu après l'écran titre
    def start(self):
        """
        Lance le  jeu en faisant commencer  le  fondu et en mettant en paramètre
        d'animation la fonction qui démarre le jeu à l'entrée dans le monde.
        """
        self.fade.active = True
        self.fade.func = self.main

    #  __  __  __
    # /\ \/\ \/\ \
    # \ \ \_\ \ \ \
    #  \ \_____\ \_\
    #   \/_____/\/_/
    #

    # Le code ci-dessous est assez en bazarre, il ne fait qu'appliquer une liste
    # de boutons et images dans le contenue de l'interface. Veuillez ne pas vous
    # casser la tête avec...

    # Écran titre
    def title(self):
        """
        ┌─────────────────────────────────────────┐
        │                                         │
        │                 ┌────┐                  │
        │                 │ Lo │                  │
        │                 │ go │                  │
        │                 └────┘                  │
        │           Enter in the world            │
        │                Settings                 │
        │                                         │
        │                                         │
        └─────────────────────────────────────────┘
        """
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
        """
        ┌─────────────────────────────────────────┐
        │                                         │
        │               ┌─────────┐               │
        │               │         │               │
        │               │         │               │
        │         Prev  │         │  Next         │
        │               │         │               │
        │               └─────────┘               │
        │                  Close                  │
        │                                         │
        └─────────────────────────────────────────┘
        """
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
                if page < len(self.recipes_text) - 1
                else nothing,
            ),
            self.book,
            Text(
                self.recipes_text[page],
                (500, 120),
                (0, 0, 0),
                300,
            ),
            Button(self.lang["close"], self.back, self.main),
        ]
        if self.can_cook(self.player.inventory, self.recipes[page]):
            self.content.append(
                Button(
                    self.lang["book.cook"],
                    self.cook_place,
                    lambda: self.cooking(page),
                )
            )
        if page in self.player.dishes:
            self.content.append(self.check)

    # Paramètres avec ou sans retour à l'écran titre
    def settings_ui(self, title: bool = False):
        """
        ┌─────────────────────────────────────────┐
        │                                         │
        │                                         │
        │            Musique : Active             │
        │            Langue: Français             │ (il y a les autre
        │            Rayons de soleil             │ paramètres aussi)
        │                Feuilles                 │
        │                                         │
        │                  Back                   │
        │                                         │
        └─────────────────────────────────────────┘
        """
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
            Button(
                "%s : %s"
                % (
                    self.lang["settings.music"],
                    (self.lang["on"] if self.mixer.playing_music else self.lang["off"]),
                ),
                (self.width // 2, self.height // 2 - 120),
                lambda: (
                    self.mixer.stop_music()
                    if self.mixer.playing_music
                    else self.mixer.play(),
                    setattr(self.mixer, "playing_music", not self.mixer.playing_music),
                    self.settings_ui(title),
                ),
            ),
            Button(
                "%s : %s"
                % (
                    self.lang["settings.ambience"],
                    (
                        self.lang["on"]
                        if self.mixer.playing_ambient
                        else self.lang["off"]
                    ),
                ),
                (self.width // 2, self.height // 2 - 160),
                lambda: (
                    self.mixer.stop_ambience()
                    if self.mixer.playing_ambient
                    else self.mixer.play_ambience(),
                    setattr(
                        self.mixer, "playing_ambient", not self.mixer.playing_ambient
                    ),
                    self.settings_ui(title),
                ),
            ),
        ]

    # Menu principal sans animation de bouton
    def main(self):
        """
        ┌─────────────────────────────────────────┐
        │                                         │
        │                                         │
        │                                         │
        │                                         │
        │                                         │ (sans animation)
        │                                         │
        │                                         │
        │                                         │
        │                                    Open │
        └─────────────────────────────────────────┘
        """
        self.ui_fade.active = False
        self.player.exist = self.player.move = True
        self.content = [
            Button(self.lang["menu.open"], self.menu, self.menu_opened),
        ]

    # Menu principal fermé
    def menu_closed(self):
        """
        ┌─────────────────────────────────────────┐
        │                                         │
        │                                         │
        │                                         │
        │                                         │
        │                                         │ (avec animation)
        │                                         │
        │                                         │
        │                                         │
        │                                    Open │
        └─────────────────────────────────────────┘
        """
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
        """
        ┌─────────────────────────────────────────┐
        │                                         │
        │                                         │
        │                                         │
        │                                         │
        │                                         │
        │                                         │
        │                                         │
        │                                         │
        │                   ... ... ... ... Close │
        └─────────────────────────────────────────┘
        """
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
        """
        ┌─────────────────────────────────────────┐
        │x: 124                                   │
        │y: 807                                   │
        │z: 2.3                                   │
        │seed: -2543                              │
        │                                         │
        │                                         │
        │                                         │
        │                                         │
        │                                         │
        └─────────────────────────────────────────┘
        """
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
                FONT.render(
                    line,  # Texte
                    True,  # Anti-aliasing
                    (255, 255, 255),  # Couleur
                ),
                (10, 10 + 25 * index),
            )

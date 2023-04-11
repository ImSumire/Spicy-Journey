#  __     __  ______  ______  __      _____
# /\ \  _ \ \/\  __ \/\  __ \/\ \    /\  __-.
# \ \ \/ ".\ \ \ \/\ \ \  __<\ \ \___\ \ \/\ \
#  \ \__/".~\_\ \_____\ \_\ \_\ \_____\ \____-
#   \/_/   \/_/\/_____/\/_/ /_/\/_____/\/____/
#

from src.tools.memoize import memoize

from random import randint
from noise import snoise2
from math import sin, cos
import pygame

# Il se peut que votre python ne soit pas compatible avec numba, je créé donc un
# décorateur pour éviter une erreur et donc faire tourner le jeu sans numba.
try:
    from numba import njit

except ImportError:
    print("Numba lib wasn't installed, please install it : pip install numba")

    def njit(**kw):
        def wrap(func):
            def inner(*args, **kwargs):
                return func(*args, **kwargs)

            return inner

        return wrap


@memoize
@njit(fastmath=True)
def iso(x, y, x_offset, y_offset):
    """Calculates isometric perspective coordinates."""
    # iso_x = x_offset + x * 16 - y * 16
    # iso_y = y_offset + x * 8 + y * 8
    # return iso_x, iso_y
    return (x_offset + x * 16 - y * 16, y_offset + x * 8 + y * 8)


class World:
    # Pourquoi utiliser  `__slots__` ? La réponse  courte est que les slots sont
    # plus efficaces en termes d'espace mémoire et de vitesse d'accès, et un peu
    # plus sûrs que la méthode d'accès aux   données  par défaut de  Python. Par
    # défaut, lorsque Python crée une nouvelle instance d'une classe, il crée un
    # attribut __dict__ pour la classe.

    __slots__ = (
        # Sprites
        "block",
        "water",
        "vegetation",
        "vegetation_size",
        "vegetation_shadows",
        "ingredients_range",
        # Paramètres de génération du terrain
        "frequence",
        "amplitude",
        "water_level",
        "v_amplitude",
        "v_frequence",
        "render_distance",
        # Constantes d'affichage
        "center",
        "x_center",
        "y_center",
        # Offsets
        "height_offset",
        "offseted_x_center",
        "offseted_y_center",
        # Variables de base
        "seed",
        "coords",
        "spawn",
        "vegetation_data",
    )

    def __init__(self, width: int, height: int):
        # Chargement des sprites de terrain, d'eau et de végétation
        self.block = pygame.image.load("res/sprites/Terrain/grass.png").convert_alpha()
        self.water = pygame.image.load("res/sprites/Terrain/water.png").convert_alpha()
        self.vegetation = []
        self.vegetation_size = []
        self.vegetation_shadows = []
        for path in [
            # Arbres (0-79)
            *["tree1"] * 17,
            *["tree2"] * 17,
            *["tree3"] * 17,
            *["tree4"] * 10,
            *["tree5"] * 10,
            *["tree6"] * 3,
            *["tree7"] * 2,
            *["tree8"] * 4,
            # Ingrédients (80-84)
            *["apple"] * 1,
            *["carrot"] * 1,
            *["radish"] * 1,
            *["rice"] * 1,
            *["wheat"] * 1,
            # Pierres (85-99)
            *["rock1"] * 2,
            *["rock2"] * 2,
            *["rock3"] * 2,
            *["rock4"] * 2,
            *["rock5"] * 2,
            *["rock6"] * 2,
            *["rock7"] * 1,
            *["rock8"] * 1,
            *["rock9"] * 1,
        ]:  # Total de 100
            prop = pygame.image.load("res/sprites/Props/%s.png" % path).convert_alpha()
            self.vegetation.append(prop)
            self.vegetation_size.append(
                prop.get_height() - 8
            )  # 8 : offset d'un demi block

            # self.vegetation_shadows.append(
            #     pygame.image.load(
            #         "res/sprites/Props/shadow/%s.png" % path
            #     ).convert_alpha()
            # )
            
        self.ingredients_range = range(80, 85)

        # Définir les paramètres de génération du terrain
        self.amplitude = 50
        self.frequence = 0.01
        self.water_level = 0.5
        self.v_amplitude = 0.8  # Pour la végétation
        self.v_frequence = 0.08  # Pour la végétation
        self.render_distance = 50

        # Constantes d'affichage
        self.center = (self.render_distance - 3) // 2
        self.x_center = width // 4
        self.y_center = height // 4

        # Offsets
        self.height_offset = self.block.get_height() // 2
        self.offseted_x_center = self.x_center - (self.block.get_width() // 2) + 4
        self.offseted_y_center = (
            self.y_center
            - self.height_offset
            - ((self.render_distance) // 2) * self.height_offset
        ) - 90

        # Variables de base
        self.seed = randint(-10e4, 10e4)  # Ne pas aller au dessus (farlands)
        self.coords = []

        self.found_spawn()

        self.vegetation_data = {}

    def found_spawn(self):
        """
        À chaque  itération de la  boucle,  deux nombres aléatoires sont générés
        pour les coordonnées x et y d'un  point.  Ces nombres sont  choisis dans
        l'intervalle  entre -500 et  500. Ensuite, la méthode  process_coord est
        appelée avec les coordonnées du  centre et les coordonnées  aléatoires x
        et  y.  Cette  méthode renvoie  une quadruplet contenant les coordonnées
        x_pos et y_pos, ainsi que deux  valeurs  de noise :  vegetation_noise et
        terrain_noise;  et finalement vérifie  si les  coordonnées  sont valides
        (pas dans l'eau).
        """
        while True:
            x, y = randint(-500, 500), randint(-500, 500)
            h = self.process_coord(self.center, self.center, x, y)[3]
            if not h > self.water_level:
                self.spawn = (x, y)
                return

    def vegetation_check(self, x, y, vegetation_noise):
        """
        La méthode  "vegetation_check" est appelée  à chaque fois qu'on souhaite
        savoir si la végétation est présente ou  non, ça simplifie la gestion de
        la récolte.
        """
        try:
            return self.vegetation_data[x, y]
        except:
            result = bool(round(vegetation_noise))
            self.vegetation_data[x, y] = result
            return result

    @memoize
    def process_coord(self, x, y, player_x, player_y):
        """
        La méthode  "process_coord" prend en   entrée quatre coordonnées  (x, y)
        pour la position de la case et  (player_x, player_y) pour la position du
        joueur.   Elle effectue  des   calculs pour  convertir   les coordonnées
        cartésiennes en  coordonnées isométriques.    Elle utilise  également la
        fonction  "snoise2" de la bibliothèque "noise"  pour générer des valeurs
        de bruit pour le terrain et la végétation en fonction des coordonnées et
        de la position du joueur.

        La  méthode utilise  également  un décorateur de  mémoïsation "@memoize"
        pour éviter de recalculer les mêmes valeurs plusieurs fois.
        """
        x_pos, y_pos = iso(x, y, self.offseted_x_center, self.offseted_y_center)
        terrain_noise = snoise2(
            (x + player_x) * self.frequence,
            (y + player_y) * self.frequence,
            base=self.seed,
        )
        vegetation_noise = (
            snoise2(
                (x + player_x) * self.v_frequence,
                (y + player_y) * self.v_frequence,
                base=self.seed,
            )
            * self.v_amplitude
        )
        return (
            x_pos,
            y_pos + terrain_noise * self.amplitude,
            vegetation_noise,
            terrain_noise,
        )

    def update(self, player_x, player_y):
        """
        La méthode  "update" met à jour  les coordonnées d'un ensemble de points
        en fonction de la position du joueur. Les coordonnées sont stockées dans
        une liste à deux dimensions. La méthode parcourt cette liste et applique
        la méthode "process_coord" à chaque coordonnée pour la mettre à jour.
        """
        self.coords = [
            [
                self.process_coord(x, y, player_x, player_y)
                for x in range(self.render_distance)
            ]
            for y in range(self.render_distance)
        ]

    def get_sprites(self, player, tick):
        """
        La méthode  "get_sprites" calcule la   position de chaque  sprite (objet
        affichable)  sur l'écran en  fonction de  la  position  du  joueur. Elle
        parcourt  une tableau de  coordonnées   qui   décrit  le terrain  et  la
        végétation.  Pour chaque case de la matrice, elle crée un sprite pour le
        terrain (de l'eau ou de l'herbe) et, éventuellement, pour la végétation.
        Les sprites sont stockés dans deux listes séparées, "terrain_sprites" et
        "props_sprites".

        La méthode calcule également la position du joueur sur l'écran et ajoute
        son sprite à la liste "props_sprites", qui est la liste de la végétation
        (c'est pour simplifier puisque le  joueur peut se déplacer à travers les
        végétations).

        Enfin, la méthode renvoie la liste complète des sprites, triée par ordre
        d'affichage (en utilisant la position y puis x pour trier les sprites).
        """
        # Calcule les chiffres après la virgule
        x_pos_mod = player.pos.x - int(player.pos.x)
        y_pos_mod = player.pos.y - int(player.pos.y)

        # Calcule les offsets du terrain pour un déplacement smooth
        x_offset = int((x_pos_mod - y_pos_mod) * 16)
        y_offset = int((x_pos_mod + y_pos_mod) * 8)

        terrain_sprites = []
        props_sprites = []

        water_factor = -(tick * 0.06)

        for y, row in enumerate(self.coords):
            for x, column in enumerate(row):
                x_pos, y_pos, vegetation_noise, terrain_noise = column
                x_temp = x_pos - x_offset
                y_temp = y_pos - y_offset

                # Eau
                if terrain_noise > self.water_level:
                    terrain_sprites.append(
                        (
                            self.water,
                            x_temp,
                            y_temp
                            - terrain_noise * self.amplitude
                            + 29
                            + 1.2
                            * cos(
                                water_factor
                                + (int(player.pos.x) + x)
                                - (int(player.pos.y) + y)
                            ),
                        )
                    )

                # Herbe
                else:
                    terrain_sprites.append((self.block, x_temp, y_temp))

                    # Vegetation
                    if self.vegetation_check(
                        int(player.pos.x) + x, int(player.pos.y) + y, vegetation_noise
                    ):
                        index = int(
                            # Éviter le slicing pour soucis de performance.
                            str(vegetation_noise)[-2]
                            + str(vegetation_noise)[-1]
                        )
                        vegetation_sprite = self.vegetation[index]
                        props_sprites.append(
                            (
                                vegetation_sprite,
                                x_temp,
                                y_temp - self.vegetation_size[index],
                                x,
                                y,
                            )
                        )

        # Si le joueur se trouve dans le monde (en jeu)
        if player.exist:
            player_pos = self.coords[self.center][self.center]

            props_sprites.append(
                (
                    player.image,
                    player_pos[0] + 4,
                    player_pos[1] - 16,
                    self.center + x_pos_mod,
                    self.center + y_pos_mod,
                )
            )

        return terrain_sprites + sorted(
            props_sprites, key=lambda s: (s[4], s[3])
        )  # (sprite, display_x, display_y, x, y)

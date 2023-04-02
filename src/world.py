# Imports
from src.tools.memoize import memoize
from random import randint
from noise import snoise2
from math import sin, cos
import pygame

try:
    from numba import njit

except ImportError:
    print("Numba lib wasn't installed, please install it with : pip install numba")

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


#  __     __  ______  ______  __      _____
# /\ \  _ \ \/\  __ \/\  __ \/\ \    /\  __-.
# \ \ \/ ".\ \ \ \/\ \ \  __<\ \ \___\ \ \/\ \
#  \ \__/".~\_\ \_____\ \_\ \_\ \_____\ \____-
#   \/_/   \/_/\/_____/\/_/ /_/\/_____/\/____/
#


class World:
    # Why Use  `__slots__`? The short answer is  slots  are more efficient in terms of
    # memory space and speed of access, and a bit safer than the default Python method
    # of data access. By default, when Python creates  a new  instance of  a class, it
    # creates a __dict__ attribute for the class.

    __slots__ = (
        # Sprites
        "block",
        "water",
        "vegetation",
        "vegetation_size",
        "vegetation_shadows",
        # Terrain generation parameters
        "frequence",
        "amplitude",
        "water_level",
        "v_amplitude",
        "v_frequence",
        "render_distance",
        # Display constants
        "center",
        "x_center",
        "y_center",
        # Offsets
        "height_offset",
        "offseted_x_center",
        "offseted_y_center",
        # Base variables
        "seed",
        "coords",
        "spawn",
        # For debugging
        "temp",
    )

    def __init__(self, width: int, height: int):
        # Load terrain, water and vegetation sprites
        self.block = pygame.image.load("res/sprites/Terrain/grass.png").convert_alpha()
        self.water = pygame.image.load("res/sprites/Terrain/water.png").convert_alpha()
        self.vegetation = []
        self.vegetation_size = []
        self.vegetation_shadows = []
        for path in [
            "tree4",
            "tree5",
            "tree1",
            "tree1",
            "tree2",
            "tree2",
            "tree3",
            "tree3",
            "radish",
            "rock1",
        ]:
            prop = pygame.image.load("res/sprites/Props/%s.png" % path).convert_alpha()
            self.vegetation.append(prop)
            self.vegetation_size.append(prop.get_height() - 8)  # 8 : half block offset

            # self.vegetation_shadows.append(
            #     pygame.image.load(
            #         "res/sprites/Props/shadow/%s.png" % path
            #     ).convert_alpha()
            # )

        # Set terrain generation parameters
        self.frequence = 0.01
        self.amplitude = 50
        self.water_level = 0.5
        self.v_amplitude = 0.8
        self.v_frequence = 0.08

        # Will be configurable in futur settings menu
        self.render_distance = 50

        # Display constants
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

        # Base variables
        self.seed = randint(-10e4, 10e4)
        self.spawn = (0, 0)
        self.coords = []

        # For debugging
        self.temp = 0

        self.found_spawn()

    def found_spawn(self):
        self.spawn = (0, 0)
        return
        while True:
            x, y = randint(-500, 500), randint(-500, 500)
            h = self.process_coord(x, y, 0, 0)[3]
            print(x, y, h)
            if h < self.water_level:
                self.spawn = (x, y)
                return

    @memoize
    def process_coord(self, x, y, player_x, player_y):
        x_pos, y_pos = iso(
            x,
            y,
            self.offseted_x_center,
            self.offseted_y_center,
        )

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
        self.coords = [
            [
                self.process_coord(x, y, player_x, player_y)
                for x in range(self.render_distance)
            ]
            for y in range(self.render_distance)
        ]

    def get_sprites(self, player, tick):
        x_pos_mod = player.pos.x - int(player.pos.x)
        y_pos_mod = player.pos.y - int(player.pos.y)
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

                # Water
                if terrain_noise > self.water_level:
                    terrain_sprites.append(
                        (
                            self.water,
                            x_temp,
                            y_temp
                            - terrain_noise * self.amplitude
                            + 30
                            + 1.2
                            * cos(
                                water_factor + (int(player.pos.x) + x) - (int(player.pos.y) + y)
                            ),
                        )
                    )

                # Grass
                else:
                    terrain_sprites.append((self.block, x_temp, y_temp))

                    # Vegetation
                    if round(vegetation_noise):
                        index = int(str(vegetation_noise)[-1])
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

        # If the player is in the world
        if player.play:
            player_pos = self.coords[self.center][self.center]

            props_sprites.append(
                (
                    player.image,
                    player_pos[0] - 4,
                    player_pos[1] - 8,
                    self.center + x_pos_mod,
                    self.center + y_pos_mod + 1,
                )
            )

        return terrain_sprites + sorted(
            props_sprites, key=lambda s: (s[4], s[3])
        )  # (sprite, display_x, display_y, x, y)

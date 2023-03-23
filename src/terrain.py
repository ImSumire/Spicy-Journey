# Imports
from math import fmod, sin, cos
from src.memoize import memoize
from time import perf_counter
from random import randint
from noise import snoise2
from numba import njit
import pygame


@memoize
@njit(fastmath=True)  # To put after the memoize
def isometric_perspective(x, y, x_offset, y_offset):
    """Calculates isometric perspective coordinates."""
    # iso_x = x_offset + x * 16 - y * 16
    # iso_y = y_offset + x * 8 + y * 8
    # return iso_x, iso_y
    return (x_offset + x * 16 - y * 16, y_offset + x * 8 + y * 8)


class Terrain:
    def __init__(
        self,
        width: int,
        height: int,
    ):
        # Load terrain and water sprites
        self.block = pygame.image.load("res/sprites/Terrain/grass.png").convert_alpha()
        self.water = pygame.image.load("res/sprites/Terrain/water.png").convert_alpha()

        # Set terrain generation parameters
        self.frequence = 0.06
        self.amplitude = 10
        self.water_level = 0.5

        # Will be configurable in futur settings menu
        self.render_distance = 45

        # Display constants and offsets
        self.center = self.render_distance >> 1
        self.x_center = width >> 2
        self.y_center = height >> 2
        self.x_offset = self.x_center - self.render_distance
        self.y_offset = self.y_center - self.render_distance
        self.width_offset = self.block.get_width() >> 1
        self.height_offset = self.block.get_height() >> 1
        self.offseted_x_center = self.x_center - self.width_offset
        self.offseted_y_center = (
            self.y_center
            - self.height_offset
            - ((self.render_distance - 0.5) // 2) * self.height_offset
        )

        # Base variables
        self.seed = randint(-10e4, 10e4)
        self.coords = []
        self.spawn = (0, 0)

        # For debugging
        self.temp = 0

        # Load vegetation sprites
        self.vegetation = []
        self.vegetation_size = []
        # self.vegetation_shadows = []
        for image in [
            "little-tree1",
            "little-tree2",
            "tree1",
            "tree1",
            "tree2",
            "tree2",
            "tree3",
            "tree3",
        ] + ["rock" + str(n) for n in range(1, 6)]:
            self.vegetation.append(
                pygame.image.load(
                    "res/sprites/Props/{}.png".format(image)
                ).convert_alpha()
            )

            # self.vegetation_shadows.append(
            #     pygame.image.load(
            #         "res/sprites/Props/shadow/{}.png".format(image)
            #     ).convert_alpha()
            # )

        for v in self.vegetation:
            self.vegetation_size.append(v.get_height() - 15)

    @memoize
    def process_coord(self, x, y, player_x, player_y):
        x_pos, y_pos = isometric_perspective(
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
            snoise2((x + player_x) * 0.08, (y + player_y) * 0.08, base=self.seed) * 0.8
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
        # x_pos_mod = fmod(player.pos.x, 1)
        # y_pos_mod = fmod(player.pos.y, 1)
        x_pos_mod = player.pos.x - int(player.pos.x)
        y_pos_mod = player.pos.y - int(player.pos.y)
        x_offset = int((x_pos_mod - y_pos_mod) * 16)
        y_offset = int((x_pos_mod + y_pos_mod) * 8)

        player_pos = self.coords[self.center][self.center]

        terrain_sprites = []
        props_sprites = []

        cos_factor = -(tick * 0.06)

        for y, row in enumerate(self.coords):
            for x, column in enumerate(row):
                x_pos, y_pos, vegetation_noise, terrain_noise = column
                x_temp = x_pos - x_offset
                y_temp = y_pos - y_offset

                if terrain_noise > self.water_level:
                    terrain_sprites.append(
                        (
                            self.water,
                            x_temp,
                            y_temp
                            - terrain_noise * self.amplitude
                            + 8
                            + 1.2
                            * cos(cos_factor - (player.pos.x - x) + (player.pos.y - y)),
                        )
                    )

                else:
                    terrain_sprites.append((self.block, x_temp, y_temp))

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

        props_sprites.append(
            (
                player.image,
                player_pos[0],
                player_pos[1] + 16,
                self.center,
                self.center + (2.5 if player.pos.y > 0 else 1.5),
            )
        )

        return terrain_sprites, sorted(
            props_sprites, key=lambda s: (s[4], s[3])
        )  # (sprite, display_x, display_y, x, y)

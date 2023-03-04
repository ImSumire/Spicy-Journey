# Imports
import pygame
from noise import snoise2
from math import fmod
from random import randint

from src.player import Player

from src.memoize import memoize


@memoize
def isometric_perspective(x, y, x_offset, y_offset):
    return (x_offset + x * 16 - y * 16, y_offset + x * 8 + y * 8)


class Terrain:
    def __init__(
        self,
        frequence_height: float,
        width: int,
        height: int,
    ):

        self.block = pygame.image.load("res/sprites/Terrain/grass.png").convert_alpha()

        self.frequence_height = frequence_height

        self.x_center = width // 4
        self.y_center = height // 4

        self.render_distance = 45
        self.center = self.render_distance // 2

        self.x_offset = self.x_center - self.render_distance
        self.y_offset = self.y_center - self.render_distance

        self.width_offset = self.block.get_width() // 2
        self.height_offset = self.block.get_height() // 2

        self.vegetation = []
        for image in (
            ["little-tree1"]
            + ["little-tree2"]
            + ["tree1"]
            + ["tree2"]
            + ["tree3"]
            + ["rock" + str(n) for n in range(1, 6)]
            # bigrock0 | bigrock1 | bigrock2 | brush
        ):
            self.vegetation.append(
                pygame.image.load(
                    "res/sprites/Props/{}.png".format(image)
                ).convert_alpha()
            )

        self.vegetation_shadows = []
        for image in (
            ["little-tree1"]
            + ["little-tree2"]
            + ["tree1"]
            + ["tree2"]
            + ["tree3"]
            + ["rock" + str(n) for n in range(1, 6)]
            # bigrock0 | bigrock1 | bigrock2 | brush
        ):
            self.vegetation_shadows.append(
                pygame.image.load(
                    "res/sprites/Props/shadow/{}.png".format(image)
                ).convert_alpha()
            )

        self.coords = []
        self.sprites_list = []

        self.seed = randint(-10e4, 10e4)

        self.spawn = (0, 0)

        self.temp = 93

    @memoize
    def _process_coord(self, x, y, player_x, player_y):
        x_pos, y_pos = isometric_perspective(
            x,
            y,
            self.x_center - self.width_offset,
            self.y_center
            - self.height_offset
            - ((self.render_distance - 0.5) // 2) * self.height_offset,
        )

        y_pos = y_pos + 10 * snoise2(
            (x + player_x) * self.frequence_height,
            (y + player_y) * self.frequence_height,
            base=self.seed,
        )

        props_noise = snoise2(
            (x + player_x) * 0.03, (y + player_y) * 0.03, base=self.seed
        )
        return x_pos, y_pos, props_noise

    def get_coords(self, player_x, player_y):
        self.coords = []

        for y in range(self.render_distance):
            coords_cache_sub = []
            for x in range(self.render_distance):
                coords_cache_sub.append(
                    self._process_coord(x, y, int(player_x), int(player_y))
                )
            self.coords.append(coords_cache_sub)

    def get_sprites(self, player):
        x_offset = int((fmod(player.pos.x, 1) - fmod(player.pos.y, 1)) * 16)
        y_offset = int((fmod(player.pos.x, 1) + fmod(player.pos.y, 1)) * 8)

        player_pos = self.coords[self.center][self.center]

        self.terrain_sprites = []
        # self.props_shadows = []
        self.props_sprites = []

        player_blited = False

        for y, row in enumerate(self.coords):
            for x, column in enumerate(row):

                x_pos, y_pos, props_noise = column

                self.terrain_sprites.append(
                    (self.block, x_pos - x_offset, y_pos - y_offset)
                )

                if round(props_noise):
                    prop = self.vegetation[int(str(props_noise)[-1])]
                    prop_shadow = self.vegetation_shadows[int(str(props_noise)[-1])]
                    #prop = self.vegetation[2]
                    self.props_sprites.append(
                        (
                            prop,
                            x_pos - x_offset,
                            y_pos - y_offset - prop.get_height() + 15,
                        )
                    )
                    # self.props_shadows.append(
                    #     (
                    #         prop_shadow,
                    #         x_pos - x_offset,
                    #         y_pos - y_offset - prop.get_height() + 15,
                    #     )
                    # )

                if not player_blited:
                    if (
                        x - 1 > self.render_distance // 2
                        and y - 1 > self.render_distance // 2
                    ):
                        self.props_sprites.append(
                            (player.image, player_pos[0], player_pos[1] + 16)
                        )
                        player_blited = True

        #print(len(self.coords))

        # self.props_sprites = sorted(self.props_sprites, key=lambda sprite: (sprite[2], sprite[1]))
        # print(self.terrain_sprites)
        # print(type(player))
        # for sprite in self.props_sprites:
        #     print('P' if isinstance(sprite[0], Player) else 'G', round(sprite[1]), round(sprite[2]), end=' | ')
        # exit()
        # self.terrain_sprites += self.props_shadows
        return self.terrain_sprites, self.props_sprites

    def get_sprites2(self, player):
        x_offset = int((fmod(player.pos.x, 1) - fmod(player.pos.y, 1)) * 16)
        y_offset = int((fmod(player.pos.x, 1) + fmod(player.pos.y, 1)) * 8)

        player_pos = self.coords[self.center][self.center]

        self.terrain_sprites = []
        self.props_sprites = []

        for y, row in enumerate(self.coords):
            for x, column in enumerate(row):

                x_pos, y_pos, props_noise = column

                self.terrain_sprites.append(
                    (self.block, x_pos - x_offset, y_pos - y_offset)
                )

                if round(props_noise):
                    prop = self.vegetation[int(str(props_noise)[-1])]
                    prop_shadow = self.vegetation_shadows[int(str(props_noise)[-1])]
                    self.props_sprites.append(
                        (
                            prop,
                            x_pos - x_offset,
                            y_pos - y_offset - prop.get_height() + 15,
                        )
                    )
                else:
                    self.props_sprites.append(())

        self.props_sprites.insert(
                                  len(self.props_sprites) // 2 + self.temp,
                                  (player.image, player_pos[0], player_pos[1] + 16)
                                 )
        return self.terrain_sprites, [_ for _ in self.props_sprites if _]

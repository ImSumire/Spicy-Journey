# Imports
import pygame
import noise as ns
from src.memoize import memoize
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import repeat


@memoize
def isometric_perspective(x, y, x_offset, y_offset):
    return (x_offset + x * 16 - y * 16, y_offset + x * 8 + y * 8)


class Terrain:
    def __init__(self, block, vegetation, frequence_height, width, height):
        self.block = block
        self.vegetation = vegetation

        self.frequence_height = frequence_height
        self.frequence_props = 0.03

        self.x_center = width // 4
        self.y_center = height // 4 - 5

        self.render_distance = 43

        self.x_offset = self.x_center - self.render_distance
        self.y_offset = self.y_center - self.render_distance

        self.width_offset = self.block.size[0] // 2
        self.height_offset = self.block.size[1] // 2

    @memoize
    def get_coords(self, camera_pos):
        coords_cache = []
        with ThreadPoolExecutor() as executor:
            results = executor.map(self._process_y_coord, range(0, self.render_distance), repeat(camera_pos))
            for result in results:
                coords_cache.append(result)
        return coords_cache

    @memoize
    def _process_y_coord(self, y, camera_pos):
        coords_cache_sub = []
        for x in range(0, self.render_distance):
            x_pos, y_pos = isometric_perspective(
                x,
                y,
                self.x_center - self.width_offset,
                self.y_center
                - self.height_offset
                - ((self.render_distance - 0.5) // 2) * self.height_offset,
            )

            y_noise = y_pos + 8 * ns.snoise2(
                (x + int(camera_pos[0])) * self.frequence_height,
                (y + int(camera_pos[1])) * self.frequence_height,
            )

            props_noise = ns.snoise2(
                (x + int(camera_pos[0])) * 0.03,
                (y + int(camera_pos[1])) * 0.03,
            )

            coords_cache_sub.append([x_pos, y_pos, y_noise, props_noise])
        return coords_cache_sub

    def draw(self, surf, camera_pos):
        coords = self.get_coords(camera_pos)
        for row in coords:
            for column in row:
                x_pos, y_pos, y_noise, props_noise = column
                surf.blit(
                    self.block.image,
                    (
                        x_pos,
                        y_noise,
                    ),
                )

                if round(props_noise):
                    prop = self.vegetation[int(str(props_noise)[-1])]

                    surf.blit(
                        prop.image,
                        (
                            x_pos,
                            y_noise - prop.size[1] + 15,
                        ),
                    )

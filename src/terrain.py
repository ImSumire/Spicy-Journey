# Imports
import pygame
import noise as ns
from src.memoize import memoize


@memoize
def isometric_perspective(x, y, x_offset, y_offset):
    return (x_offset + x * 16 - y * 16, y_offset + x * 8 + y * 8)


class Terrain:
    def __init__(
        self,
        block: pygame.image,
        vegetation: pygame.image,
        frequence_height: float,
        width: int,
        height: int,
    ):
        self.block = block
        self.vegetation = vegetation

        self.frequence_height = frequence_height

        self.x_center = width // 4
        self.y_center = height // 4 - 5

        self.render_distance = 45
        self.center = self.render_distance // 2

        self.x_offset = self.x_center - self.render_distance
        self.y_offset = self.y_center - self.render_distance

        self.width_offset = self.block.size[0] // 2
        self.height_offset = self.block.size[1] // 2

    @memoize
    def _process_coord(self, x, y, camera_pos):
        x_pos, y_pos = isometric_perspective(
            x,
            y,
            self.x_center - self.width_offset,
            self.y_center
            - self.height_offset
            - ((self.render_distance - 0.5) // 2) * self.height_offset,
        )

        y_pos = y_pos + 10 * ns.snoise2(
            (x + int(camera_pos[0])) * self.frequence_height,
            (y + int(camera_pos[1])) * self.frequence_height,
        )

        props_noise = ns.snoise2(
            (x + int(camera_pos[0])) * 0.03,
            (y + int(camera_pos[1])) * 0.03,
        )
        return x_pos, y_pos, props_noise

    @memoize
    def get_coords(self, camera_pos):
        coords_cache = []

        for y in range(0, self.render_distance):
            coords_cache_sub = []
            for x in range(0, self.render_distance):
                coords_cache_sub.append(self._process_coord(x, y, camera_pos))
            coords_cache.append(coords_cache_sub)

        return coords_cache

    def draw_terrain(self, surf, camera_pos):
        self.coords = self.get_coords(camera_pos)
        for row in self.coords:
            for column in row:
                x_pos, y_pos, props_noise = column
                surf.blit(
                    self.block.image,
                    (
                        x_pos,
                        y_pos,
                    ),
                )

    def draw_props(self, surf, camera_pos):
        self.coords = self.get_coords(camera_pos)
        for row in self.coords:
            for column in row:
                x_pos, y_pos, props_noise = column
                if round(props_noise):
                    prop = self.vegetation[int(str(props_noise)[-1])]

                    surf.blit(
                        prop.image,
                        (
                            x_pos,
                            y_pos - prop.size[1] + 15,
                        ),
                    )

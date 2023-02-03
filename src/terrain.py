# Imports
import pygame
import noise as ns


def isometric_perspective(x, y, x_offset, y_offset):
    return (x_offset + x * 16 - y * 16, y_offset + x * 8 + y * 8)


class Terrain:
    def __init__(self, block, vegetation, frequence_height, width, height):
        self.block = block
        self.vegetation = vegetation

        self.frequence_height = frequence_height

        self.x_center = width // 4
        self.y_center = height // 4 - 5

        self.render_distance = 40

        self.x_offset = self.x_center - self.render_distance
        self.y_offset = self.y_center - self.render_distance

        self.width_offset = self.block.size[0] // 2
        self.height_offset = self.block.size[1] // 2

    def draw(self, surf, camera_pos):
        for y in range(0, self.render_distance):
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

                surf.blit(
                    self.block.image,
                    (
                        x_pos,
                        y_noise,
                        # * noise(
                        #     (x + int(camera_pos[0])) * self.frequence_height,
                        #     (y + int(camera_pos[1])) * self.frequence_height,
                        # ),
                    ),
                )

                if round(props_noise):
                    propos = self.vegetation[int(str(props_noise)[-1])]
                    surf.blit(
                        propos.image,
                        (
                            x_pos,
                            y_noise - propos.size[1] + 15,
                        ),
                    )

                    # ( - 1 + 300 + x * 16 - y + (int(camera_pos[1])) * self.frequence_height * 16,  15 + 50 + x * 8 + y + (int(camera_pos[1])) * self.frequence_height * 8 - 8))

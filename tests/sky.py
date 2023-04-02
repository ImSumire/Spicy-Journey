import pygame, sys
from noise import snoise2
import numpy as np

__inspiration__ = "https://codepen.io/xgundam05/pen/zLQjva"

if __name__ == '__main__':
    WIDTH, HEIGHT = 1280, 700
    D_WIDTH, D_HEIGHT = CENTER = (WIDTH // 2, HEIGHT // 2)
    width_range = range(D_WIDTH)
    height_range = range(D_HEIGHT)

    width_freq = 0.0122
    height_freq = 0.0046
    depth_freq = 0.006

    octaves = [(0.57, 0.282, 38), (0.81, 0.9, 19), (1.5, 1.14, 22), (2.25, 2.1, 19)]

    pygame.init()
    pygame.display.set_caption("Noise")
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)  # (1280, 700)
    display = pygame.Surface(CENTER)  # (640, 350)
    clock = pygame.time.Clock()

    display_data = np.zeros((D_WIDTH, D_HEIGHT, 3), dtype=np.uint8)

    colors = [(255, 255, 255), (0, 164, 201)]


    def base_display():
        for x in height_range:
            for y in width_range:
                value = (
                    snoise2(x * width_freq * 0.57, y * height_freq * 0.81) * 38
                    + snoise2(x * width_freq * 0.81, y * height_freq * 0.9) * 19
                    + snoise2(x * width_freq * 1.5, y * height_freq * 1.14) * 22
                    + snoise2(x * width_freq * 2.25, y * height_freq * 2.1) * 19
                )
                display_data[y, x] = colors[value > -10]

        screen.blit(
            pygame.transform.scale(
                pygame.surfarray.make_surface(display_data), (WIDTH, HEIGHT)
            ),
            (0, 0),
        )
        pygame.display.flip()


    def update_display(tick):
        global display_data
        new_line = [(0, 0, 0) for _ in height_range]
        for y in height_range:
            value = (
                snoise2(tick * height_freq * 0.57, y * width_freq * 0.81) * 38
                + snoise2(tick * height_freq * 0.81, y * width_freq * 0.9) * 19
                + snoise2(tick * height_freq * 1.5, y * width_freq * 1.14) * 22
                + snoise2(tick * height_freq * 2.25, y * width_freq * 2.1) * 19
            )
            new_line[y] = colors[value > -10]

        display_data = np.concatenate((np.array(display_data)[1:], [np.array(new_line)]))

        screen.blit(
            pygame.transform.scale(
                pygame.surfarray.make_surface(np.array(display_data)), (WIDTH, HEIGHT)
            ),
            (0, 0),
        )
        pygame.display.flip()


    tick = WIDTH
    base_display()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        update_display(tick)
        clock.tick(20)
        pygame.display.set_caption(str(int(clock.get_fps())))
        tick += 1



class Sky:
    def __init__(self, width, height, surf):
        self.width = width
        self.height = height

        self.d_width, self.d_height = (width // 2, height // 2)

        self.width_range = range(self.d_width)
        self.height_range = range(self.d_height)

        self.surf = surf

        self.data = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        self.width_freq = 0.0122
        self.height_freq = 0.0046
        self.depth_freq = 0.006

        self.octaves = [
            (0.57, 0.282, 38),
            (0.81, 0.9, 19),
            (1.5, 1.14, 22),
            (2.25, 2.1, 19),
        ]

        self.colors = [(255, 255, 255), (0, 164, 201)]

        self.base_display()

    def base_display(self):
        for x in self.height_range:
            for y in self.width_range:
                value = (
                    snoise2(x * self.width_freq * 0.57, y * self.height_freq * 0.81)
                    * 38
                    + snoise2(x * self.width_freq * 0.81, y * self.height_freq * 0.9)
                    * 19
                    + snoise2(x * self.width_freq * 1.5, y * self.height_freq * 1.14)
                    * 22
                    + snoise2(x * self.width_freq * 2.25, y * self.height_freq * 2.1)
                    * 19
                )
                self.data[y, x] = self.colors[value > -10]

        self.surf.blit(
            pygame.transform.scale(
                pygame.surfarray.make_surface(self.data), (self.width, self.height)
            ),
            (0, 0),
        )

    def update_display(self, tick):
        new_line = [(0, 0, 0) for _ in range(self.height_range)]
        for y in self.height_range:
            value = (
                snoise2(tick * self.height_freq * 0.571, y * self.width_freq * 0.81)
                * 38
                + snoise2(tick * self.height_freq * 0.81, y * self.width_freq * 0.9)
                * 19
                + snoise2(tick * self.height_freq * 1.5, y * self.width_freq * 1.14)
                * 22
                + snoise2(tick * self.height_freq * 2.25, y * self.width_freq * 2.1)
                * 19
            )
            new_line[y] = self.colors[value > -10]

        data = np.concatenate((np.array(self.data)[1:], [np.array(new_line)]))

        self.surf.blit(
            pygame.transform.scale(
                pygame.surfarray.make_surface(np.array(data)),
                (self.width, self.height),
            ),
            (0, 0),
        )

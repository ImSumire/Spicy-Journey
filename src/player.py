import pygame
from os import walk


def import_folder(path):
    surface_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            surface_list.append(pygame.image.load(path + "/" + image).convert_alpha())
    return surface_list


class Player:
    def __init__(self, pos):
        # Display
        self.idle_animation_speed = 0.08
        self.animation_speed = 0.18
        self.frame_index = 0
        self.image = pygame.image.load(
            "res/sprites/Characters/down/0.png"
        ).convert_alpha()
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "right_idle": [],
            "left_idle": [],
            "up_idle": [],
            "down_idle": [],
        }
        for self.animation in self.animations.keys():
            full_path = "res/sprites/Characters/" + self.animation
            self.animations[self.animation] = import_folder(full_path)
        self.idle = "_idle"

        # Movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(pos)
        self.status = "down"
        self.speed = 0.05  # 0.05

        # Keys
        self.up = pygame.K_z
        self.down = pygame.K_s
        self.left = pygame.K_q
        self.right = pygame.K_d

    def input(self):
        keys = pygame.key.get_pressed()

        self.direction = pygame.math.Vector2(0, 0)

        if keys[self.up] and not keys[self.down]:  # Up (z)(w)
            self.direction.y -= 1
            self.direction.x -= 1
            self.status = "up"
            self.idle = ""
        elif keys[self.down] and not keys[self.up]:  # Down (s)(s)
            self.direction.x += 1
            self.direction.y += 1
            self.status = "down"
            self.idle = ""

        if keys[self.left] and not keys[self.right]:  # Left (q)(a)
            self.direction.x -= 1
            self.direction.y += 1
            self.status = "left"
            self.idle = ""
        elif keys[self.right] and not keys[self.left]:  # Right (d)(d)
            self.direction.x += 1
            self.direction.y -= 1
            self.status = "right"
            self.idle = ""

        if self.direction == (0, 0):
            self.idle = "_idle"
        else:
            self.direction.normalize()
            self.pos.x = round(self.pos.x + self.direction.x * self.speed, 2)
            self.pos.y = round(self.pos.y + self.direction.y * self.speed, 2)

    def animate(self):
        animation = self.animations[self.status + self.idle]
        # Add to frame_index
        if self.idle:
            self.frame_index += self.idle_animation_speed
        else:
            self.frame_index += self.animation_speed
        # Avoid out of range
        if self.frame_index >= len(animation):
            self.frame_index = 0
        # Set the image
        self.image = animation[int(self.frame_index)]

    def update(self):
        self.input()
        self.animate()

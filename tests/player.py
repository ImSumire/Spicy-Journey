import pygame
from src.tools.import_folder import *


def import_folder(path):
    surface_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            surface_list.append(pygame.image.load(path + "/" + image).convert_alpha())

    return surface_list


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # Display
        self.idle_animation_speed = 0.1
        self.animation_speed = 0.15
        self.frame_index = 0
        self.image = pygame.image.load(
            "res/sprites/Characters/down/0.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
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
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.idle = "_idle"

        # Movement
        self.direction = pygame.math.Vector2()
        self.status = "down"
        self.speed = 1

        self.posx, self.posy = pos

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:  # Up
            self.direction.y = -1
            self.posy -= self.speed
            self.status = "up"
            self.idle = ""
        elif keys[pygame.K_DOWN]:  # Down
            self.direction.y = 1
            self.posy += self.speed
            self.status = "down"
            self.idle = ""
        else:
            self.direction.y = 0  # Nothing

        if keys[pygame.K_RIGHT]:  # Right
            self.direction.x = 1
            self.posx += self.speed
            self.status = "right"
            self.idle = ""
        elif keys[pygame.K_LEFT]:  # Left
            self.direction.x = -1
            self.posx -= self.speed
            self.status = "left"
            self.idle = ""
        else:
            self.direction.x = 0  # Nothing

        if self.direction.x == 0 and self.direction.y == 0:
            self.idle = "_idle"

        self.hitbox = self.rect.inflate(0 + self.posx, -26 + self.posy)

    def animate(self):
        animation = self.animations[self.status + self.idle]
        # Add to frame_index
        if self.idle == "_idle":
            self.frame_index += self.idle_animation_speed
        else:
            self.frame_index += self.animation_speed
        # Avoid out of range
        if self.frame_index >= len(animation):
            self.frame_index = 0
        # Set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    """
    def collision(self,direction):
    		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: self.hitbox.right = sprite.hitbox.left # moving right
					if self.direction.x < 0: self.hitbox.left = sprite.hitbox.right # moving left


		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: self.hitbox.bottom = sprite.hitbox.top # moving down
					if self.direction.y < 0: self.hitbox.top = sprite.hitbox.bottom # moving up
    """

    def update(self):
        self.input()
        self.animate()
        self.rect.center += self.direction  # Move

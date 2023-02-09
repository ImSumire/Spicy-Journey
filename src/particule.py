import pygame
from os import walk
from pygame.locals import *
from pygame import transform
from random import randint, choice


def resize(img, width):
    return transform.scale(
        img, (int(img.get_width() * width), int(img.get_height() * width))
    )


def import_folder(path):
    surface_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            surface_list.append(pygame.image.load(path + "/" + image))
    return surface_list


def create_particules(n, file, x_speed, y_speed, base_size, rotation=False):
    particules = []
    for i in range(n):
        particules.append(Particule(file, x_speed, y_speed, base_size, rotation))
    return particules


def delete_particules():
    global particules
    particules = []


class Particule:
    def __init__(self, folder, x_speed, y_speed, base_size, rotation=False):
        self.x = randint(100, 2000)
        self.y = randint(-600, 600)

        self.vector = (
            -randint(2 * x_speed, 2 * x_speed + 2),
            randint(2 * y_speed, 2 * y_speed + 2),
        )

        self.image = resize(choice(import_folder(folder)), 4 + randint(0, 2))

        if rotation:
            self.rotation_s = choice([-4, -3, -2, -1, 1, 2, 3, 4])
            self.display = self.image
            self.rotation = 1
        else:
            self.rotation = False

    def move(self):
        self.x += self.vector[0]
        self.y += self.vector[1]

        if self.rotation:
            self.rotation += self.rotation_s
            self.image = pygame.transform.rotate(self.display, self.rotation)

        if self.y > 1250 or self.x < -10:
            self.y = randint(-600, 0)
            self.x = randint(100, 2200)

    def display_particules(self, surf):
        surf.blit(self.image, (int(self.x), int(self.y)))
        self.move()

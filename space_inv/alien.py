import pygame
from enum import Enum
from random import choice, randint
from settings import WIDTH, HEIGHT, BORDER


class AlienType(Enum):
    def __new__(cls, file, speed=100):
        obj = object.__new__(cls)
        obj._value_ = file
        obj.speed = speed
        return obj

    RED = ("red.png", 3)
    GREEN = ("green.png", 2)
    YELLOW = ("yellow.png", 6)


class Alien(pygame.sprite.Sprite):
    def __init__(self, _type, pos):
        super().__init__()
        file_path = "./graphics/" + _type.value
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.alien_color = _type.value
        self.speed = _type.speed

    @staticmethod
    def create(_type=None, pos=None):
        if _type is None:
            _type = choice(list(AlienType))

        if pos is None:
            opts = [
                (randint(-BORDER, WIDTH + BORDER), choice([-BORDER, HEIGHT + BORDER])),  # spawn from top or bottom
                (choice([-BORDER, WIDTH + BORDER]), randint(-BORDER, HEIGHT + BORDER)),  # spawn from left or right
            ]
            pos = choice(opts)

        return Alien(_type, pos)



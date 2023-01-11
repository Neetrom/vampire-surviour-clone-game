from random import randint, choice
import pygame
from settings import BORDER, WIDTH, HEIGHT


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        file_path = "./graphics/" + color + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.alien_color = color
        self.health = 1
        self.alien_speed = 3
        self.lasers_hit = pygame.sprite.Group()

    @staticmethod
    def random_position():
        margin = 10

        long_x_spawn = randint(-BORDER, WIDTH + BORDER)
        long_y_spawn = randint(-BORDER, HEIGHT + BORDER)
        opts = [
            (long_x_spawn, randint(-BORDER, margin)),  # top side
            (long_x_spawn, randint(HEIGHT + margin, HEIGHT + BORDER)),  # bottom side
            (randint(-BORDER, margin), long_y_spawn),  # left side
            (randint(WIDTH + margin, WIDTH + BORDER), long_y_spawn)  # right side
        ]
        return choice(opts)


class RedAlien(Alien):
    def __init__(self, x, y, color="red"):
        super().__init__(x, y, color)
        self.health = 1
        self.alien_speed = 3

    @classmethod
    def random_spawn(cls):
        pos = Alien.random_position()
        return cls(x=pos[0], y=pos[1])


class GreenAlien(Alien):
    def __init__(self, x, y, color="green"):
        super().__init__(x, y, color)
        self.health = 2
        self.alien_speed = 2

    @classmethod
    def random_spawn(cls):
        pos = Alien.random_position()
        return cls(x=pos[0], y=pos[1])


class YellowAlien(Alien):
    def __init__(self, x, y, color="yellow"):
        super().__init__(x, y, color)
        self.health = 1
        self.alien_speed = 5

    @classmethod
    def random_spawn(cls):
        pos = Alien.random_position()
        return cls(x=pos[0], y=pos[1])

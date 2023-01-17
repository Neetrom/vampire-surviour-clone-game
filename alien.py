import math
from random import randint, choice
import pygame
from settings import BORDER, WIDTH, HEIGHT


# _Alien class shouldn't be called directly
class _Alien(pygame.sprite.Sprite):
    _default_color = ""

    def __init__(self, x, y, color):
        super().__init__()
        file_path = "./graphics/" + color + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.alien_color = color
        self.health = 1
        self.speed = 3
        self.damage = 2
        self.lasers_hit = pygame.sprite.Group()

    def move_towards(self, target_x, target_y, time_delta):
        x = -(self.pos.x - target_x - 10)
        y = -(self.pos.y - target_y)
        temp_xy = (x * x) + (y * y)
        if temp_xy == 0:
            return

        xy = math.sqrt(temp_xy)  # slightly faster than ** .5, because math.sqrt operates only on real numbers
        self.pos.x += self.speed * (x / xy) * time_delta
        self.pos.y += self.speed * (y / xy) * time_delta

        self.rect.x, self.rect.y = self.pos.x, self.pos.y

    @staticmethod
    def random_position():
        margin = 10

        long_x_spawn = randint(-BORDER, WIDTH + BORDER)
        long_y_spawn = randint(-BORDER, HEIGHT + BORDER)
        opts = [
            (long_x_spawn, randint(-BORDER, -margin)),  # top side
            (long_x_spawn, randint(HEIGHT + margin, HEIGHT + BORDER)),  # bottom side
            (randint(-BORDER, -margin), long_y_spawn),  # left side
            (randint(WIDTH + margin, WIDTH + BORDER), long_y_spawn)  # right side
        ]
        return choice(opts)

    @classmethod
    def random_spawn(cls):
        pos = _Alien.random_position()
        return cls(x=pos[0], y=pos[1], color=cls._default_color)


class RedAlien(_Alien):
    _default_color = "red"

    def __init__(self, x, y, color=_default_color):
        super().__init__(x, y, color)
        self.health = 1
        self.speed = 300
        self.damage = 2


class GreenAlien(_Alien):
    _default_color = "green"

    def __init__(self, x, y, color=_default_color):
        super().__init__(x, y, color)
        self.health = 2
        self.speed = 200
        self.damage = 3


class YellowAlien(_Alien):
    _default_color = "yellow"

    def __init__(self, x, y, color=_default_color):
        super().__init__(x, y, color)
        self.health = 1
        self.damage = 1
        self.speed = 500

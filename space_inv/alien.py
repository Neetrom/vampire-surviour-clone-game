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
        self.speed = 300
        self.damage = 2
        self.lasers_hit = pygame.sprite.Group()

    def move_towards(self, target_x, target_y, time_delta):
        x = -(self.pos.x - target_x - 10)
        y = -(self.pos.y - target_y)
        xy = ((x ** 2) + (y ** 2)) ** 0.5
        if xy == 0:
            speed_x = 0
            speed_y = 0
        else:
            cosi_x = (x / xy)
            cosi_y = (y / xy)
            speed_x = self.speed * cosi_x * time_delta
            speed_y = self.speed * cosi_y * time_delta
        self.pos.x += speed_x
        self.pos.y += speed_y

        self.rect.x, self.rect.y = self.pos.x, self.pos.y

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
        self.damage = 2
        self.speed = 300

    @classmethod
    def random_spawn(cls):
        pos = Alien.random_position()
        return cls(x=pos[0], y=pos[1])


class GreenAlien(Alien):
    def __init__(self, x, y, color="green"):
        super().__init__(x, y, color)
        self.health = 2
        self.damage = 3
        self.speed = 200

    @classmethod
    def random_spawn(cls):
        pos = Alien.random_position()
        return cls(x=pos[0], y=pos[1])


class YellowAlien(Alien):
    def __init__(self, x, y, color="yellow"):
        super().__init__(x, y, color)
        self.health = 1
        self.damage = 1
        self.speed = 500

    @classmethod
    def random_spawn(cls):
        pos = Alien.random_position()
        return cls(x=pos[0], y=pos[1])

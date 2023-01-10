import timeit

import pygame
from settings import WIDTH
import math


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, angle, speed=-8):
        super().__init__()
        self.image = pygame.image.load("./graphics/laser.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.speed = speed
        self.image = pygame.transform.rotate(self.image, angle).convert_alpha()
        self.angle = angle

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= WIDTH + 50 or self.rect.x <= -50 or self.rect.x > WIDTH + 50:
            self.kill()

    def update(self, time_delta):
        x_speed = self.speed * math.sin(math.radians(self.angle)) * time_delta
        y_speed = self.speed * math.cos(math.radians(self.angle)) * time_delta
        self.pos.x += x_speed
        self.pos.y += y_speed

        self.rect.x, self.rect.y = self.pos.x, self.pos.y
        self.destroy()

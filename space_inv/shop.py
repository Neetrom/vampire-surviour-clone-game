import pygame
from settings import *


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, power):
        super().__init__()
        file_path = "./graphics/" + power + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        image_size = (WIDTH-100)//5
        self.image = pygame.transform.scale(self.image, (image_size,image_size))
        self.rect = self.image.get_rect(midleft=(x, y))
        self.power = power

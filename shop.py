from __future__ import annotations
import pygame
from settings import *


class Shop:
    def __init__(self, items: list[Item]):
        self.items = pygame.sprite.Group(items)
        self._is_open = False

    def is_open(self):
        return self._is_open

    def open(self):
        self._is_open = True

    def close(self):
        self._is_open = False

    def toggle(self):
        self._is_open = not self._is_open

    def draw(self, display):
        self.items.draw(display)

    def get_clicked_item(self, mouse_up_event) -> Item | None:
        if mouse_up_event is None:
            return None

        for item in self.items:
            if item.rect.collidepoint(mouse_up_event.pos):
                return item


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, power):
        super().__init__()
        file_path = "./graphics/" + power + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        image_size = (WIDTH-100)//5
        self.image = pygame.transform.scale(self.image, (image_size,image_size))
        self.rect = self.image.get_rect(midleft=(x, y))
        self.power = power

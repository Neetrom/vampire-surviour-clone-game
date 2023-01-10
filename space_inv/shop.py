from __future__ import annotations
import pygame


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

    def get_clicked_item(self) -> Item | None:
        # TODO: replace get_pressed() with MOUSEUP event
        # currently code after this if will be executed every tick - should only once
        if not pygame.mouse.get_pressed()[0]:
            return None

        pos = pygame.mouse.get_pos()
        for item in self.items:
            if item.rect.collidepoint(pos):
                return item


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, power):
        super().__init__()
        file_path = "./graphics/" + power + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        # self.image = pygame.transform.scale(self.image, (200,180))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.power = power

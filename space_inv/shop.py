import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, power):
        super().__init__()
        file_path = "./graphics/" + power + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        # self.image = pygame.transform.scale(self.image, (200,180))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.power = power

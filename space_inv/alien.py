import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        file_path = "./graphics/" + color + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.alien_color = color
        self.health = 1
        self.speed = 3
        self.damage = 2
        self.lasers_hit = pygame.sprite.Group()

class GreenAlien(Alien):
    def __init__(self, x, y, color = "green"):
        super().__init__(x, y, color)
        self.health = 2
        self.damage = 3
        self.alien_speed = 2

class YellowAlien(Alien):
    def __init__(self, x, y, color="yellow"):
        super().__init__(x, y, color)
        self.health = 1
        self.damage = 1
        self.alien_speed = 5

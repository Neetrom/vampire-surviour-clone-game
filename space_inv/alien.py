import pygame
<<<<<<< HEAD
=======

>>>>>>> pr/4

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
<<<<<<< HEAD
        file_path = "randomfun/space_inv/graphics/" + color + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
=======
        file_path = "./graphics/" + color + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
>>>>>>> pr/4
        self.alien_color = color
        self.health = 0
        self.alien_speed = 3

class GreenAlien(Alien):
    def __init__(self, x, y, color = "green"):
        super().__init__(x, y, color)
        self.health = 1
        self.alien_speed = 2

<<<<<<< HEAD
class YellowAlien(Alien):
    def __init__(self, x, y, color = "yellow"):
        super().__init__(x, y, color)
        self.health = 0
        self.alien_speed = 5
=======
class GreenAlien(Alien):
    def __init__(self, x, y, color="green"):
        super().__init__(x, y, color)
        self.health = 1
        self.alien_speed = 2


class YellowAlien(Alien):
    def __init__(self, x, y, color="yellow"):
        super().__init__(x, y, color)
        self.health = 0
        self.alien_speed = 5
>>>>>>> pr/4

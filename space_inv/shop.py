import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, power):
        super().__init__()
<<<<<<< HEAD
        file_path = "randomfun/space_inv/graphics/" + power + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        #self.image = pygame.transform.scale(self.image, (200,180))
        self.rect = self.image.get_rect(topleft = (x,y))
=======
        file_path = "./graphics/" + power + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        # self.image = pygame.transform.scale(self.image, (200,180))
        self.rect = self.image.get_rect(topleft=(x, y))
>>>>>>> pr/4
        self.power = power

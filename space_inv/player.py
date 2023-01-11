import pygame
from laser import Laser
from settings import *
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("./graphics/player.png").convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = 5
        self.right_border = WIDTH - self.image.get_width()
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600
        self.lasers = pygame.sprite.Group()
        self.pos = pygame.math.Vector2(pos)
        self.angle = 0
        self.laser_power = 1
        self.piercing = 1

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90
        self.image = pygame.transform.rotate(self.original_image, int(self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        elif keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        elif keys[pygame.K_a]:
            self.rect.x -= self.speed

        if pygame.mouse.get_pressed()[0] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True
    
    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, int(self.angle), self.piercing))

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH

    def update(self):
        self.lasers.update()
        self.get_input()
        self.recharge()
        self.constraint()
        self.rotate()
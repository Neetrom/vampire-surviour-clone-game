import pygame
from laser import Laser
from settings import *
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("./graphics/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (68,64))
        self.original_image = self.image
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = 500
        self.right_border = WIDTH - self.image.get_width()
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 1  # cooldown in seconds
        self.lasers = pygame.sprite.Group()
        self.pos = pygame.math.Vector2(pos)
        self.angle = 0
        self.laser_power = 1
        self.piercing = 1

        self.hp = 15
        self.max_hp = 15
        self.i_frames = 500
        self.i_frames_timer = 0
        self.damaged = False

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90
        self.image = pygame.transform.rotate(self.original_image, int(self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def invi_frames(self, time_delta):
        if self.damaged:
            self.i_frames_timer -= time_delta
            if self.i_frames_timer <= 0:
                self.damaged = False
                self.image.set_alpha(255)
                self.original_image.set_alpha(255)

    def get_input(self, time_delta):
        keys = pygame.key.get_pressed()
        speed = self.speed * time_delta

        if keys[pygame.K_w]:
            self.pos.y -= speed
        elif keys[pygame.K_s]:
            self.pos.y += speed
        if keys[pygame.K_d]:
            self.pos.x += speed
        elif keys[pygame.K_a]:
            self.pos.x -= speed

        self.rect.x, self.rect.y = self.pos.x, self.pos.y

        if pygame.mouse.get_pressed()[0] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = self.laser_cooldown

    def recharge(self, time_delta):
        if not self.ready:
            self.laser_time -= time_delta
            if self.laser_time <= 0:
                self.ready = True

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, int(self.angle), self.piercing))

    def constraint(self):
        # TODO: because of new way of handling movement, this works only for image, not for actual position
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH

    def update(self, time_delta):
        self.invi_frames(time_delta)
        self.lasers.update(time_delta)
        self.get_input(time_delta)
        self.recharge(time_delta)
        self.constraint()
        self.rotate()

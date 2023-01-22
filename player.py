import pygame
from laser import Laser
from settings import *
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("./graphics/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (68, 64))
        self.original_image = self.image
        self.rect = self.image.get_rect(midbottom=pos)

        self.stats = Stats()
        self.cooldowns = Cooldowns()

        self.hp = self.stats.max_hp
        self._exp = 0
        self.level = 1
        self._next_level = 0

        self.lasers = pygame.sprite.Group()
        self.pos = pygame.math.Vector2(pos)
        self.angle = 0

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90
        self.image = pygame.transform.rotate(self.original_image, int(self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def is_alive(self):
        return self.hp <= 0

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, value):
        self._exp += (value - self._exp) * self.stats.experience_multiplayer

    @property
    def next_level(self):
        return 20 * self.level

    @next_level.setter
    def next_level(self, value):
        self._next_level = value

    def try_level_up(self):
        if self._exp >= self.next_level:
            self._exp -= self.next_level
            self.level += 1
            return True
        return False

    def invi_frames(self):
        if not self.cooldowns.is_still_invincible():
            self.image.set_alpha(255)
            self.original_image.set_alpha(255)

    def get_input(self, time_delta):
        keys = pygame.key.get_pressed()
        speed = self.stats.movement_speed * time_delta

        if keys[pygame.K_w]:
            self.pos.y -= speed
        elif keys[pygame.K_s]:
            self.pos.y += speed
        if keys[pygame.K_d]:
            self.pos.x += speed
        elif keys[pygame.K_a]:
            self.pos.x -= speed

        self.rect.x, self.rect.y = self.pos.x, self.pos.y

        if pygame.mouse.get_pressed()[0] and self.cooldowns.is_laser_ready():
            self.shoot_laser()
            self.cooldowns.laser_timer = self.stats.laser_delay

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, int(self.angle), self.stats.piercing))

    def constraint(self):
        # TODO: because of new way of handling movement, this works only for image, not for actual position
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH

    def update(self, time_delta):
        self.cooldowns.update_timers(time_delta)
        self.invi_frames()
        self.lasers.update(time_delta)
        self.get_input(time_delta)
        self.constraint()
        self.rotate()


class Stats:
    def __init__(self):
        self.movement_speed = 500
        self.laser_delay = 1  # in seconds
        self.laser_speed = 1000
        self.laser_damage = 1
        self.max_hp = 15
        self.invincible_frames = 1.5  # in seconds
        self.piercing = 1
        self.experience_multiplayer = 1

    # currently not in use
    def min_max_check(self):
        self.movement_speed = min(self.movement_speed, 600)


class Cooldowns:
    def __init__(self):
        self.laser_timer = 0
        self.invincible_timer = 0

    def update_timers(self, time_delta):
        for k, v in vars(self).items():
            setattr(self, k, max(v - time_delta, 0))

    def is_laser_ready(self):
        return self.laser_timer <= 0

    def is_still_invincible(self):
        return self.invincible_timer > 0

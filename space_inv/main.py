import os

import pygame
import sys
from player import Player
from settings import *
import obstacle
from alien import Alien, GreenAlien, YellowAlien
from random import randint, choice
from shop import Item


class Game:
    def __init__(self):
        # player setup
        self.player_sprite = Player((WIDTH/2, HEIGHT/2))
        self.player = pygame.sprite.GroupSingle(self.player_sprite)

        # obnstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        # self.obstacle_amount = 4
        # self.obstacle_x_pos = [num * (WIDTH/self.obstacle_amount) for num in range(self.obstacle_amount)]
        # self.create_multiple_obstacles(*self.obstacle_x_pos, x_start = WIDTH/15, y_start = 480)
        self.font = pygame.font.SysFont('Arial', 100)
        # alien setup
        self.aliens = pygame.sprite.Group()
        #self.alien_setup(rows = 6, cols = 8)
        self.alien_speed = 3
        self.border = 100
        self.alien_spawner = 50
        self.exp = 0
        self.game_active = True
        self.shop_active = False

        self.shop_items = pygame.sprite.Group()
        self.shop_items.add(Item(50, HEIGHT/2, "speed"))
        self.shop_items.add(Item(450, HEIGHT/2, "dmg"))
        self.shop_items.add(Item(850, HEIGHT/2, "piercing"))
        self.shop_items.add(Item(1250, HEIGHT/2, "reload"))

        # exp bar setup
        self.empty_bar = pygame.Surface((WIDTH//3, 5))
        self.empty_bar_rect = self.empty_bar.get_rect(center=(WIDTH/2, HEIGHT - 50))
        self.empty_bar.fill((146, 166, 165))
        self.progress_bar = pygame.Surface((0, 5))
        self.progress_bar_rect = self.progress_bar.get_rect(topleft=self.empty_bar_rect.topleft)
        self.level_up = 25

    def show_exp(self, display):
        if self.exp == self.level_up:
            self.exp = 0
            self.open_shop()
        self.progress_bar = pygame.transform.scale(
            self.progress_bar, (((WIDTH//3)/self.level_up)*self.exp, 5))
        self.progress_bar.fill((28, 230, 219))
        display.blit(self.empty_bar, self.empty_bar_rect)
        display.blit(self.progress_bar, self.progress_bar_rect)

    def spawner(self):
        self.alien_spawner -= 1
        if self.alien_spawner == 0:
            self.spawn_alien()
            self.alien_spawner = 50

    def spawn_alien(self):
        x = choice([randint(0, WIDTH), choice([-self.border, WIDTH + self.border])])
        if (x == -self.border) or (x == WIDTH + self.border):
            y = randint(-self.border, HEIGHT + self.border)
        else:
            y = choice([-self.border, HEIGHT + self.border])
        alien_sprite = choice([Alien(x, y, "red"), GreenAlien(x, y), YellowAlien(x, y)])
        self.aliens.add(alien_sprite)

    def kill_alien(self):
        to_add = len(self.aliens)
        for alien in self.aliens:
            for laser in self.player.sprite.lasers:
                if alien.rect.colliderect(laser.rect):
                    if laser not in alien.lasers_hit:
                        alien.health -= self.player.sprite.laser_power
                        if alien.health <= 0:
                            alien.kill()
                        laser.piercing -= 1
                        alien.lasers_hit.add(laser)
        self.exp += to_add - len(self.aliens)

    def alien_goto_player(self):
        for alien in self.aliens:
            x = -(alien.rect.x - self.player.sprite.rect.x - 10)
            y = -(alien.rect.y - self.player.sprite.rect.y)
            xy = ((x**2) + (y**2))**0.5
            if xy == 0:
                speed_x = 0
                speed_y = 0
            else:
                cosi_x = (x / xy)
                cosi_y = (y / xy)
                speed_x = alien.alien_speed * cosi_x
                speed_y = alien.alien_speed * cosi_y
            alien.rect.x += speed_x
            alien.rect.y += speed_y

    def update_aliens(self):
        self.spawner()
        self.alien_goto_player()
        self.kill_alien()

    def run(self, display):
        self.player.update()
        self.update_aliens()
        self.draw_everything(display)

    def draw_everything(self, display):
        self.aliens.draw(display)
        self.player.sprite.lasers.draw(display)
        self.player.draw(display)
        self.show_exp(display)

    def open_shop(self):
        if self.game_active:
            self.game_active = False
            self.shop_active = True
        else:
            self.game_active = True
            self.shop_active = False

    def buy(self):
        if not pygame.mouse.get_pressed()[0]:
            return
        pos = pygame.mouse.get_pos()
        for item in self.shop_items:
            if item.rect.collidepoint(pos):
                if item.power == "dmg":
                    self.player.sprite.laser_power += 1
                elif item.power == "speed":
                    self.player.sprite.speed += 1
                elif item.power == "piercing":
                    self.player.sprite.piercing += 1
                elif item.power == "reload":
                    self.player.sprite.laser_cooldown *= 0.9
                self.open_shop()

    def shop(self, display):
        self.draw_everything(display)
        self.shop_items.draw(display)
        self.buy()

    def shop(self, display):
        self.draw_everything(display)
        self.shop_items.draw(display)
        self.buy()


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.open_shop()

        screen.fill((30, 30, 30))
        if game.game_active:
            game.run(screen)
        elif game.shop_active:
            game.shop(screen)

        pygame.display.update()
        clock.tick(60)

import os
import pygame, sys
from player import Player
from settings import *
import obstacle
from alien import Alien
from random import randint, choice


class Game:
    def __init__(self):
        # player setup
        self.player_sprite = Player((WIDTH / 2, HEIGHT / 2))
        self.player = pygame.sprite.GroupSingle(self.player_sprite)

        # obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        # self.obstacle_amount = 4
        # self.obstacle_x_pos = [num * (WIDTH/self.obstacle_amount) for num in range(self.obstacle_amount)]
        # self.create_multiple_obstacles(*self.obstacle_x_pos, x_start = WIDTH/15, y_start = 480)
        self.font = pygame.font.SysFont('Arial', 100)
        # alien setup
        self.aliens = pygame.sprite.Group()
        # self.alien_setup(rows = 6, cols = 8)
        self.alien_speed = 3
        self.border = 100
        self.alien_spawner = 50
        self.coins = 0

    def show_coins(self, display):
        coins_text = self.font.render(f'{self.coins}', False, 'white')
        coins_text_rect = coins_text.get_rect(center=(WIDTH - 50, 50))
        display.blit(coins_text, coins_text_rect)

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
        alien_sprite = Alien(choice(["red", "yellow", "green"]), x, y)
        self.aliens.add(alien_sprite)

    def kill_alien(self):
        to_add = len(self.aliens)
        for laser in self.player.sprite.lasers:
            if pygame.sprite.spritecollide(laser, self.aliens, True):
                self.coins += to_add - len(self.aliens)
                laser.kill()

    def alien_goto_player(self):
        for alien in self.aliens:
            if alien.alien_color == "yellow":
                self.alien_speed = 6
            elif alien.alien_color == "green":
                self.alien_speed = 2
            elif alien.alien_color == "red":
                self.alien_speed = 3
            x = -(alien.rect.x - self.player.sprite.rect.x - 10)
            y = -(alien.rect.y - self.player.sprite.rect.y)
            xy = ((x ** 2) + (y ** 2)) ** 0.5
            if xy == 0:
                speed_x = 0
                speed_y = 0
            else:
                cosi_x = (x / xy)
                cosi_y = (y / xy)
                speed_x = self.alien_speed * cosi_x
                speed_y = self.alien_speed * cosi_y
            alien.rect.x += speed_x
            alien.rect.y += speed_y

    # def alien_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_offset = 70, y_offset = 100):
    #     for row_index in range(rows):
    #         if row_index == 0: color = "yellow"
    #         elif 1 <= row_index <= 2: color = "green"
    #         else: color = "red"
    #         for col_index in range(cols):
    #             x = col_index * x_distance + x_offset
    #             y = row_index * y_distance + y_offset
    #             alien_sprite = Alien(color, x, y)
    #             self.aliens.add(alien_sprite)

    # def move_alien(self):
    #     for alien in self.aliens:
    #         alien.rect.y += self.alien_speed

    # def create_obstacle(self, x_start, y_start, offset_x):
    #     for row_index, row in enumerate(self.shape):
    #         for col_index, val in enumerate(row):
    #             if val == 'x':
    #                 x = col_index*self.block_size + x_start + offset_x
    #                 y = row_index*self.block_size + y_start
    #                 block = obstacle.Block(self.block_size, (241,79,80), x,y)
    #                 self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def run(self, display):
        self.player.update()

        self.kill_alien()
        self.player.sprite.lasers.draw(display)
        self.player.draw(display)
        self.show_coins(display)

        self.blocks.draw(display)
        self.spawner()
        self.alien_goto_player()
        self.aliens.draw(display)


if __name__ == "__main__":
    # os.chdir(path) changes current working directory. This should help removing user dependent paths in code
    # [your-own-path]/space_inv
    os.chdir(os.getcwd())
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((30, 30, 30))
        game.run(screen)

        pygame.display.update()
        clock.tick(60)

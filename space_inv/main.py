<<<<<<< HEAD
=======
import os

>>>>>>> pr/4
import pygame, sys
from player import Player
from settings import *
import obstacle
from alien import Alien, GreenAlien, YellowAlien
from random import randint, choice
from shop import Item
<<<<<<< HEAD
=======

>>>>>>> pr/4

class Game:
    def __init__(self):
        #player setup
        self.player_sprite = Player((WIDTH/2, HEIGHT/2))
        self.player = pygame.sprite.GroupSingle(self.player_sprite)

        #obnstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        # self.obstacle_amount = 4
        # self.obstacle_x_pos = [num * (WIDTH/self.obstacle_amount) for num in range(self.obstacle_amount)]
        # self.create_multiple_obstacles(*self.obstacle_x_pos, x_start = WIDTH/15, y_start = 480)
        self.font = pygame.font.SysFont('Arial', 100)
        #alien setup
        self.aliens = pygame.sprite.Group()
        #self.alien_setup(rows = 6, cols = 8)
        self.alien_speed = 3
        self.border = 100
        self.alien_spawner = 50
        self.coins = 0
        self.game_active = True
        self.shop_active = False

        self.shop_items = pygame.sprite.Group()
        self.shop_items.add(Item(100, 200, "power"))

    def show_coins(self, display):
        coins_text = self.font.render(f'{self.coins}', False, 'white')
        coins_text_rect = coins_text.get_rect(center = (WIDTH-50, 50))
        display.blit(coins_text, coins_text_rect)

    def spawner(self):
        self.alien_spawner -= 1
        if self.alien_spawner == 0:
            self.spawn_alien()
            self.alien_spawner = 50
    
    def spawn_alien(self):
<<<<<<< HEAD
        x = choice([randint(0,WIDTH), choice([-self.border, WIDTH+self.border])])
        if (x == -self.border) or (x == WIDTH+self.border):
            y = randint(-self.border, HEIGHT+self.border)
        else:
            y = choice([-self.border, HEIGHT+self.border])
        alien_sprite = choice([Alien(x, y, "red"), GreenAlien(x,y), YellowAlien(x,y)])
=======
        x = choice([randint(0, WIDTH), choice([-self.border, WIDTH + self.border])])
        if (x == -self.border) or (x == WIDTH + self.border):
            y = randint(-self.border, HEIGHT + self.border)
        else:
            y = choice([-self.border, HEIGHT + self.border])
        alien_sprite = choice([Alien(x, y, "red"), GreenAlien(x, y), YellowAlien(x, y)])
>>>>>>> pr/4
        self.aliens.add(alien_sprite)
    
    def kill_alien(self):
        to_add = len(self.aliens)
        for alien in self.aliens:
            for laser in self.player.sprite.lasers:
                if alien.rect.colliderect(laser.rect):
                    if alien.health == 0:
                        alien.kill()
                    else:
                        alien.health -= 1
                    laser.kill()
        self.coins += to_add - len(self.aliens)

    def alien_goto_player(self):
        for alien in self.aliens:
            x = -(alien.rect.x - self.player.sprite.rect.x - 10)
            y = -(alien.rect.y - self.player.sprite.rect.y)
            xy = ((x**2) + (y**2))**0.5
            if xy == 0:
                speed_x = 0
                speed_y = 0
            else:
<<<<<<< HEAD
                cosi_x = (x/xy)
                cosi_y = (y/xy)
                speed_x = alien.alien_speed*cosi_x
                speed_y = alien.alien_speed*cosi_y
=======
                cosi_x = (x / xy)
                cosi_y = (y / xy)
                speed_x = alien.alien_speed * cosi_x
                speed_y = alien.alien_speed * cosi_y
>>>>>>> pr/4
            alien.rect.x += speed_x
            alien.rect.y += speed_y

    def update_aliens(self):
        self.spawner()
        self.alien_goto_player()
        self.kill_alien()

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def run(self, display):
        self.player.update()
        self.update_aliens()
        self.draw_everything(display)

<<<<<<< HEAD
    
=======
>>>>>>> pr/4
    def draw_everything(self, display):
        self.aliens.draw(display)
        self.player.sprite.lasers.draw(display)
        self.player.draw(display)
        self.show_coins(display)

    def open_shop(self):
        if self.game_active:
            self.game_active = False
            self.shop_active = True
        else:
            self.game_active = True
            self.shop_active = False
<<<<<<< HEAD
=======

    def buy(self):
        pos = pygame.mouse.get_pos()
        for item in self.shop_items:
            if item.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]:
                    if item.power == "power":
                        self.player.sprite.laser_cooldown -= 100
                        self.open_shop()

    def shop(self, display):
        self.draw_everything(display)
        self.shop_items.draw(display)
        self.buy()
>>>>>>> pr/4

    def buy(self):
        pos = pygame.mouse.get_pos()
        for item in self.shop_items:
            if item.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]:
                    if item.power == "power":
                        self.player.sprite.laser_cooldown -= 100
                        self.open_shop()
    
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
<<<<<<< HEAD
        
        screen.fill((30,30,30))
=======

        screen.fill((30, 30, 30))
>>>>>>> pr/4
        if game.game_active:
            game.run(screen)
        elif game.shop_active:
            game.shop(screen)

        pygame.display.update()
        clock.tick(60)
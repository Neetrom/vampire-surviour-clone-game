import os
from random import choice

import pygame
import sys

import obstacle
from alien import GreenAlien, YellowAlien, RedAlien
from player import Player
from settings import *
from shop import Item, Shop


class Game:
    def __init__(self):
        self.time_delta = 0
        self.events = {}

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
        self.text_surface_lost = self.font.render(f'YOU LOST THE GAME', False, 'white')
        self.text__lost_rect = self.text_surface_lost.get_rect(center=(WIDTH // 2, HEIGHT // 5))
        self.try_again = self.font.render(f'Try again', False, 'white')
        self.try_again_rect = self.try_again.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
        # alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_spawner = 0.9  # cooldown in seconds
        self.exp = 0
        self.game_active = True

        self.shop = Shop([
            Item(50, HEIGHT / 2, "speed"), Item(450, HEIGHT / 2, "dmg"), Item(850, HEIGHT / 2, "piercing"),
            Item(1250, HEIGHT / 2, "reload")
        ])

        # exp bar setup
        self.empty_bar = pygame.Surface((WIDTH // 3, 5))
        self.empty_bar_rect = self.empty_bar.get_rect(center=(WIDTH / 2, HEIGHT - 50))
        self.empty_bar.fill((146, 166, 165))
        self.progress_bar = pygame.Surface((0, 5))
        self.level_up = 25

        # player hp bar
        self.empty_hp_bar = pygame.Surface((WIDTH // 10, 7))
        self.empty_hp_bar_rect = self.empty_hp_bar.get_rect(center=(0 + WIDTH / 10, 50))
        self.empty_hp_bar.fill((146, 166, 165))
        self.hp_bar = pygame.Surface((0, 7))

    def show_exp(self, display):
        if self.exp >= self.level_up:
            self.exp = 0
            self.shop.open()
        self.progress_bar = pygame.transform.scale(self.progress_bar, (((WIDTH // 3) / self.level_up) * self.exp, 5))
        self.progress_bar.fill((28, 230, 219))
        display.blit(self.empty_bar, self.empty_bar_rect)
        display.blit(self.progress_bar, self.empty_bar_rect)

    def show_hp(self, display):
        player = self.player_sprite

        self.hp_bar = pygame.transform.scale(self.hp_bar, (max(((WIDTH // 10) / player.max_hp) * player.hp, 0), 7))
        self.hp_bar.fill("red")
        display.blit(self.empty_hp_bar, self.empty_hp_bar_rect)
        display.blit(self.hp_bar, self.empty_hp_bar_rect)

    def spawner(self):
        self.alien_spawner -= self.time_delta
        if self.alien_spawner <= 0:
            self.spawn_alien()
            self.alien_spawner = 0.9

    def spawn_alien(self):
        alien = choice([RedAlien, GreenAlien, YellowAlien])
        self.aliens.add(alien.random_spawn())

    def kill_alien(self):
        exp_gained = 0
        for alien in self.aliens:
            for laser in self.player_sprite.lasers:
                if not alien.rect.colliderect(laser.rect) or laser in alien.lasers_hit:
                    continue

                break_out_loop = False
                alien.health -= self.player_sprite.laser_power
                if alien.health <= 0:
                    break_out_loop = True
                    exp_gained += 1
                    alien.kill()

                laser.piercing -= 1
                if laser.piercing <= 0:
                    break_out_loop = True
                    laser.kill()

                if break_out_loop:
                    break

                alien.lasers_hit.add(laser)

        self.exp += exp_gained

    def alien_goto_player(self):
        for alien in self.aliens:
            alien.move_towards(self.player_sprite.pos.x, self.player_sprite.pos.y, self.time_delta)

    def alien_collisions(self):
        if not self.player_sprite.damaged:
            for alien in self.aliens:
                if alien.rect.colliderect(self.player_sprite.rect):
                    self.player_sprite.hp -= alien.damage
                    self.player_sprite.i_frames_timer = self.player_sprite.i_frames_duration  # in seconds
                    self.player_sprite.damaged = True
                    self.player_sprite.image.set_alpha(100)
                    self.player_sprite.original_image.set_alpha(100)
                    return

    def game_over(self):
        if self.player_sprite.hp <= 0:
            self.game_active = False

    def update_aliens(self):
        self.spawner()
        self.alien_goto_player()
        self.kill_alien()

    def new_game(self):
        self.aliens.empty()
        self.player.empty()
        self.player_sprite = Player((WIDTH / 2, HEIGHT / 2))
        self.player.add(self.player_sprite)
        self.exp = 0

    def run(self, display, delta):
        self.time_delta = delta
        if not self.shop.is_open():
            self.alien_collisions()
            self.game_over()
            self.player.update(delta)
            self.update_aliens()
        self.draw_everything(display)

        if self.shop.is_open():
            self.run_shop(display)

    def draw_everything(self, display):
        self.aliens.draw(display)
        self.player_sprite.lasers.draw(display)
        self.player.draw(display)
        self.show_exp(display)
        self.show_hp(display)

    def handle_purchase(self, item: Item):
        if item is None:
            return

        if item.power == "dmg":
            self.player_sprite.laser_power += 1
        elif item.power == "speed":
            self.player_sprite.speed += 1
        elif item.power == "piercing":
            self.player_sprite.piercing += 1
        elif item.power == "reload":
            self.player_sprite.laser_cooldown *= 0.9
        self.shop.close()

    def game_over_screen(self, display):
        display.blit(self.text_surface_lost, self.text__lost_rect)
        display.blit(self.try_again, self.try_again_rect)
        mouse_stuff = self.events.get(pygame.MOUSEBUTTONUP)
        if mouse_stuff is None:
            return
        if self.try_again_rect.collidepoint(mouse_stuff.pos):
            self.game_active = True
            self.new_game()

    def run_shop(self, display):
        self.draw_everything(display)
        self.shop.draw(display)
        self.handle_purchase(self.shop.get_clicked_item(self.events.get(pygame.MOUSEBUTTONUP)))


if __name__ == "__main__":
    # os.chdir(path) changes current working directory. This should help removing user dependent paths in code
    # [your-own-path]/space_inv
    os.chdir(os.getcwd())
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    small_font = pygame.font.SysFont("Arial", 12)
    fps_pos = pygame.Rect(0, HEIGHT-12, 50, 12)

    events = {}
    while True:
        delta = clock.tick() / 1000
        fps = round(clock.get_fps())
        for event in pygame.event.get():
            events[event.type] = event

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.shop.toggle()

        screen.fill((30, 30, 30))
        game.events = events
        if game.game_active:
            game.run(screen, delta)
            print(f"\r{fps} FPS", end="")
        else:
            game.game_over_screen(screen)

        pygame.display.flip()
        events.clear()

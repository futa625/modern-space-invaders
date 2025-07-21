import pygame
import random
import sys
from pygame_menu import Theme, Menu, events
from dataclasses import dataclass

# ゲーム設定
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

@dataclass
class Player:
    x: int = SCREEN_WIDTH // 2
    y: int = SCREEN_HEIGHT - 100
    width: int = 60
    height: int = 60
    speed: int = 8
    health: int = 100

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2)

@dataclass
class Bullet:
    x: int
    y: int
    speed: int = 12
    width: int = 4
    height: int = 20

    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))

@dataclass
class Enemy:
    x: int
    y: int
    width: int = 50
    height: int = 50
    health: int = 3
    direction: int = 1
    speed: int = 3

    def move(self):
        self.x += self.speed * self.direction

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2)

    def take_damage(self):
        self.health -= 1
        return self.health <= 0

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Modern Space Invaders")
        self.clock = pygame.time.Clock()
        self.score = 0
        self.level = 1
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
        self.menu = self.create_menu()
        self.initialize_game()

    def create_menu(self):
        theme = Theme(
            background_color=(0, 0, 0, 128),
            title_background_color=(40, 40, 40),
            title_font_shadow=True,
            widget_font=pygame.font.Font(None, 36),
            widget_padding=25,
        )
        menu = Menu(
            'Modern Space Invaders',
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            theme=theme
        )
        menu.add.button('Play', self.initialize_game)
        menu.add.button('Quit', events.EXIT)
        return menu

    def initialize_game(self):
        self.player = Player()
        self.bullets = []
        self.enemies = []
        self.score = 0
        self.level = 1
        self.game_over = False
        self.create_enemies()

    def create_enemies(self):
        rows = 4 + self.level // 2
        cols = 8 + self.level
        for row in range(rows):
            for col in range(cols):
                enemy = Enemy(
                    x=100 + col * 80,
                    y=100 + row * 70,
                    health=3 + self.level // 2,
                    speed=2 + self.level // 2
                )
                self.enemies.append(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    bullet = Bullet(
                        x=self.player.x + self.player.width // 2 - 2,
                        y=self.player.y
                    )
                    self.bullets.append(bullet)

    def update(self):
        keys = pygame.key.get_pressed()
        if not self.game_over:
            # プレイヤーの移動
            if keys[pygame.K_LEFT] and self.player.x > 0:
                self.player.x -= self.player.speed
            if keys[pygame.K_RIGHT] and self.player.x < SCREEN_WIDTH - self.player.width:
                self.player.x += self.player.speed

            # 弾の移動
            for bullet in self.bullets[:]:
                bullet.move()
                if bullet.y < 0:
                    self.bullets.remove(bullet)

            # 敵の移動
            for enemy in self.enemies:
                enemy.move()
                if enemy.x <= 0 or enemy.x >= SCREEN_WIDTH - enemy.width:
                    for e in self.enemies:
                        e.y += 20
                        e.direction *= -1

            # 衝突判定
            for bullet in self.bullets[:]:
                for enemy in self.enemies[:]:
                    if (bullet.x < enemy.x + enemy.width and
                        bullet.x + bullet.width > enemy.x and
                        bullet.y < enemy.y + enemy.height and
                        bullet.y + bullet.height > enemy.y):
                        if enemy.take_damage():
                            self.enemies.remove(enemy)
                            self.score += 100
                        self.bullets.remove(bullet)
                        break

            # ゲームオーバー判定
            for enemy in self.enemies:
                if enemy.y + enemy.height > self.player.y:
                    self.game_over = True

            # レベルアップ判定
            if not self.enemies:
                self.level += 1
                self.create_enemies()

    def draw(self):
        self.screen.fill(BLACK)

        # スコアとレベルの表示
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        level_text = self.font.render(f'Level: {self.level}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))

        # プレイヤーの描画
        self.player.draw(self.screen)

        # 弾の描画
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # 敵の描画
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # ゲームオーバー時の表示
        if self.game_over:
            game_over_text = self.font.render('GAME OVER', True, RED)
            restart_text = self.font.render('Press R to Restart', True, WHITE)
            self.screen.blit(game_over_text, 
                           (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2))
            self.screen.blit(restart_text, 
                           (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

    def run(self):
        while True:
            if not self.game_over:
                self.handle_events()
                self.update()
                self.draw()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.initialize_game()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()

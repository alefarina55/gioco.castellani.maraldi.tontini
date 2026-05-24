import pygame
import sys

from player import Player
from enemy import Enemy
from boss import Boss
from save_system import save_game, load_game

pygame.init()

WIDTH = 1000
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Action Game")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 40)

BACKGROUND = (25, 25, 35)

camera_x = 0

spawn_x, spawn_y = load_game()

player = Player(spawn_x, spawn_y)

enemies = [
    Enemy(600, 480),
    Enemy(1000, 480),
    Enemy(1400, 480),
]

boss = Boss(1700, 430)
final_boss = Boss(2600, 430)

platforms = [
    pygame.Rect(0, 550, 3500, 50),
    pygame.Rect(300, 450, 200, 20),
    pygame.Rect(700, 350, 200, 20),
    pygame.Rect(1100, 420, 250, 20),
    pygame.Rect(1600, 300, 200, 20),
    pygame.Rect(2100, 500, 250, 20),
    pygame.Rect(2600, 420, 250, 20),
]

checkpoint = pygame.Rect(1500, 470, 50, 80)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    player.update(keys, platforms)

    camera_x = player.rect.x - WIDTH // 2

    for e in enemies:
        e.update(player)

    boss.update(player)
    final_boss.update(player)

    # DAMAGE ENEMIES
    for e in enemies:

        if player.attacking and e.alive:
            if player.attack_rect.colliderect(e.rect):
                e.take_damage()

        if player.elemental_attacking and e.alive:
            if player.elemental_rect.colliderect(e.rect):
                e.take_damage()

    # DAMAGE BOSSES
    for b in [boss, final_boss]:

        if player.attacking and b.alive:
            if player.attack_rect.colliderect(b.rect):
                b.take_damage()

        if player.elemental_attacking and b.alive:
            if player.elemental_rect.colliderect(b.rect):
                b.take_damage()

    # ENEMY DAMAGE PLAYER
    for e in enemies:
        e.attack_player(player)

    boss.attack_player(player)
    final_boss.attack_player(player)

    # CHECKPOINT
    if player.rect.colliderect(checkpoint):
        save_game(player.rect.x, player.rect.y)

    # GAME OVER
    if player.health <= 0:
        running = False

    # WIN
    if not final_boss.alive:
        print("WIN!")
        running = False

    # DRAW
    screen.fill(BACKGROUND)

    for p in platforms:
        pygame.draw.rect(screen, (80, 80, 80),
                         pygame.Rect(p.x - camera_x, p.y, p.width, p.height))

    pygame.draw.rect(screen, (80, 255, 80),
                     pygame.Rect(checkpoint.x - camera_x, checkpoint.y, 50, 80))

    # PLAYER DRAW (con camera)
    temp = player.rect.copy()
    temp.x -= camera_x

    original = player.rect
    player.rect = temp

    player.draw(screen)

    player.rect = original
    
    # ENEMIES
    for e in enemies:
        pygame.draw.rect(screen, (200, 60, 60),
                         pygame.Rect(e.rect.x - camera_x, e.rect.y, 50, 70))

    # BOSSES
    pygame.draw.rect(screen, (120, 0, 180),
                     pygame.Rect(boss.rect.x - camera_x, boss.rect.y, 120, 120))

    pygame.draw.rect(screen, (120, 0, 180),
                     pygame.Rect(final_boss.rect.x - camera_x, final_boss.rect.y, 120, 120))

    # HUD
    hp = font.render(f"HP: {player.health}", True, (255, 255, 255))
    screen.blit(hp, (20, 20))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
import pygame
import sys

from player import Player
from enemy import Enemy
from boss import Boss
from save_system import save_game, load_game

pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grape Monster")

clock = pygame.time.Clock()

font_big = pygame.font.SysFont("arial", 80)
font = pygame.font.SysFont("arial", 36)

BACKGROUND = (22, 18, 30)

camera_x = 0

spawn_x, spawn_y = load_game()

player = Player(spawn_x, spawn_y)

enemies = [
    Enemy(700, 520),
    Enemy(1200, 520),
    Enemy(1700, 520),
]

boss = Boss(2400, 430)
final_boss = Boss(4200, 350)

boss_active = False
final_boss_active = False

platforms = [
    pygame.Rect(0, 650, 5500, 70),

    pygame.Rect(400, 520, 200, 20),
    pygame.Rect(850, 430, 200, 20),
    pygame.Rect(1400, 360, 200, 20),

    pygame.Rect(2200, 520, 300, 20),

    pygame.Rect(3200, 500, 300, 20),
    pygame.Rect(3800, 420, 250, 20),
]

checkpoint = pygame.Rect(3000, 570, 60, 80)

state = "menu"

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if state == "menu":
                if event.key == pygame.K_RETURN:
                    state = "game"

            elif state == "win":
                if event.key == pygame.K_ESCAPE:
                    running = False

    # ================= MENU =================

    if state == "menu":

        screen.fill((18, 10, 28))

        title = font_big.render("GRAPE MONSTER", True, (180, 80, 255))
        text = font.render("Premi INVIO per iniziare", True, (255, 255, 255))

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 220))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 420))

        pygame.display.update()
        clock.tick(60)
        continue

    # ================= GAME =================

    if state == "game":

        keys = pygame.key.get_pressed()

        player.update(keys, platforms)

        camera_x = player.rect.x - WIDTH // 2

        # ENEMIES

        for e in enemies:
            e.update(player)

        # PLAYER DAMAGE ENEMIES

        for e in enemies:

            if player.attacking and e.alive:
                if player.attack_rect.colliderect(e.rect):
                    e.take_damage()

            for projectile in player.projectiles:
                if e.alive and projectile.rect.colliderect(e.rect):
                    e.take_damage()
                    projectile.alive = False

        # ACTIVATE MID BOSS

        if not boss_active:

            all_dead = True

            for e in enemies:
                if e.alive:
                    all_dead = False

            if all_dead:
                boss_active = True

        # MID BOSS

        if boss_active and boss.alive:

            boss.update(player)

            if player.attacking:
                if player.attack_rect.colliderect(boss.rect):
                    boss.take_damage()

            for projectile in player.projectiles:
                if projectile.rect.colliderect(boss.rect):
                    boss.take_damage()
                    projectile.alive = False

        # FINAL BOSS

        if boss_active and not boss.alive:
            final_boss_active = True

        if final_boss_active and final_boss.alive:

            final_boss.update(player)

            if player.attacking:
                if player.attack_rect.colliderect(final_boss.rect):
                    final_boss.take_damage()

            for projectile in player.projectiles:
                if projectile.rect.colliderect(final_boss.rect):
                    final_boss.take_damage()
                    projectile.alive = False

        # ENEMY DAMAGE PLAYER

        for e in enemies:
            e.attack_player(player)

        # SAVE

        if player.rect.colliderect(checkpoint):
            save_game(player.rect.x, player.rect.y)

        # GAME OVER

        if player.health <= 0:
            running = False

        # WIN

        if final_boss_active and not final_boss.alive:
            state = "win"

        # DRAW

        screen.fill(BACKGROUND)

        # Background decorations

        for i in range(12):
            pygame.draw.circle(screen, (35, 28, 48), (i * 200 - camera_x // 4, 100), 120)

        # Platforms

        for p in platforms:
            pygame.draw.rect(
                screen,
                (70, 70, 85),
                (p.x - camera_x, p.y, p.width, p.height),
                border_radius=8
            )

        # Checkpoint

        pygame.draw.rect(
            screen,
            (80, 255, 120),
            (checkpoint.x - camera_x, checkpoint.y, 60, 80),
            border_radius=10
        )

        # Player

        player.draw(screen, camera_x)

        # Enemies

        for e in enemies:
            e.draw(screen, camera_x)

        # Mid boss

        if boss_active and boss.alive:
            boss.draw(screen, camera_x)

        # Final boss

        if final_boss_active and final_boss.alive:
            final_boss.draw(screen, camera_x)

        # HUD

        hp = font.render(f"HP: {player.health}", True, (255, 255, 255))
        screen.blit(hp, (20, 20))

        pygame.display.update()

    # ================= WIN SCREEN =================

    if state == "win":

        screen.fill((10, 20, 10))

        title = font_big.render("GRAPE MONSTER", True, (180, 80, 255))
        text1 = font.render("Hai sconfitto l'uva malvagia!", True, (255, 255, 255))
        text2 = font.render("Premi ESC per uscire", True, (255, 255, 255))

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 180))
        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, 350))
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 450))

        pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()
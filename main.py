import pygame
import sys

from player import Player
from enemy import Enemy
from boss import Boss
from save_system import save_game, load_game

pygame.init()

# ================= WINDOW =================

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grape Monster")

clock = pygame.time.Clock()

# ================= FONTS =================

font_big = pygame.font.SysFont("arial", 72)
font = pygame.font.SysFont("arial", 34)
font_small = pygame.font.SysFont("arial", 26)

# ================= COLORS =================

BACKGROUND = (22, 18, 30)

# ================= GAME DATA =================

camera_x = 0

spawn_x, spawn_y = load_game()

player = Player(spawn_x, spawn_y)

# ================= ENEMIES =================

enemies = [
    Enemy(700, 520),
    Enemy(1200, 520),
    Enemy(1700, 520),
]

# ================= BOSSES =================

boss = Boss(2400, 430, False)
final_boss = Boss(5200, 260, True)

boss_active = False
final_boss_active = False

# ================= PLATFORMS =================

platforms = [

    # ground
    pygame.Rect(0, 650, 7000, 70),

    # early platforms
    pygame.Rect(400, 520, 200, 20),
    pygame.Rect(850, 430, 200, 20),
    pygame.Rect(1400, 360, 200, 20),

    # first boss area
    pygame.Rect(2200, 520, 300, 20),

    # final staircase
    pygame.Rect(3600, 580, 180, 20),
    pygame.Rect(3900, 520, 180, 20),
    pygame.Rect(4200, 460, 180, 20),
    pygame.Rect(4500, 400, 180, 20),
    pygame.Rect(4800, 340, 180, 20),

    # final arena
    pygame.Rect(5050, 420, 700, 20),
]

# ================= CHECKPOINT =================

checkpoint = pygame.Rect(3000, 570, 60, 80)

# ================= STATES =================

state = "menu"

story_phase = 0

running = True

# =========================================================
# ======================= LOOP ============================
# =========================================================

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # MENU

            if state == "menu":

                if event.key == pygame.K_RETURN:
                    state = "intro_story"

            # INTRO STORY

            elif state == "intro_story":

                if event.key == pygame.K_RETURN:
                    story_phase += 1

                    if story_phase > 2:
                        state = "game"

            # MID STORY

            elif state == "mid_story":

                if event.key == pygame.K_RETURN:
                    story_phase += 1

                    if story_phase > 4:

                        player.rect.x = 3400
                        player.rect.y = 500

                        state = "final_path"

            # WIN

            elif state == "win":

                if event.key == pygame.K_ESCAPE:
                    running = False

    # =========================================================
    # ======================= MENU =============================
    # =========================================================

    if state == "menu":

        screen.fill((18, 10, 28))

        title = font_big.render("GRAPE MONSTER", True, (180, 80, 255))
        text = font.render("Premi INVIO per iniziare", True, (255, 255, 255))

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 220))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 420))

        pygame.display.update()
        clock.tick(60)
        continue

    # =========================================================
    # =================== INTRO STORY =========================
    # =========================================================

    if state == "intro_story":

        screen.fill((20, 12, 30))

        lines = [

            [
                "In un tranquillo villaggio di acini d'uva",
                "gli abitanti vivevano in pace."
            ],

            [
                "Ma un giorno arrivò un mostro.",
                "Un'entità oscura e misteriosa."
            ],

            [
                "Il mostro ipnotizzò il villaggio,",
                "rendendo tutti violenti e ostili.",
                "",
                "Solo il cavaliere Bödvar può salvarli."
            ]
        ]

        current = lines[story_phase]

        y = 220

        for line in current:

            text = font.render(line, True, (255, 255, 255))

            screen.blit(
                text,
                (WIDTH // 2 - text.get_width() // 2, y)
            )

            y += 60

        continue_text = font_small.render(
            "Premi INVIO per continuare",
            True,
            (180, 180, 180)
        )

        screen.blit(
            continue_text,
            (WIDTH // 2 - continue_text.get_width() // 2, 620)
        )

        pygame.display.update()
        clock.tick(60)
        continue

    # =========================================================
    # ======================= GAME =============================
    # =========================================================

    if state == "game" or state == "final_path":

        keys = pygame.key.get_pressed()

        player.update(keys, platforms)

        camera_x = player.rect.x - WIDTH // 2

        # ================= ENEMIES =================

        for e in enemies:
            e.update(player)

        # player damage enemies

        for e in enemies:

            if player.attacking and e.alive:
                if player.attack_rect.colliderect(e.rect):
                    e.take_damage()

            for projectile in player.projectiles:
                if e.alive and projectile.rect.colliderect(e.rect):
                    e.take_damage()
                    projectile.alive = False

        # ================= MID BOSS ACTIVATION =================

        if not boss_active:

            all_dead = True

            for e in enemies:
                if e.alive:
                    all_dead = False

            if all_dead:
                boss_active = True

        # ================= MID BOSS =================

        if boss_active and boss.alive:

            boss.update(player)

            if player.attacking:
                if player.attack_rect.colliderect(boss.rect):
                    boss.take_damage()

            for projectile in player.projectiles:
                if projectile.rect.colliderect(boss.rect):
                    boss.take_damage()
                    projectile.alive = False

        # ================= MID STORY =================

        if boss_active and not boss.alive and state == "game":

            state = "mid_story"
            story_phase = 3

        # ================= FINAL BOSS =================

        if state == "final_path":

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

        # ================= ENEMY DAMAGE =================

        for e in enemies:
            e.attack_player(player)

        # ================= SAVE =================

        if player.rect.colliderect(checkpoint):
            save_game(player.rect.x, player.rect.y)

        # ================= GAME OVER =================

        if player.health <= 0:
            running = False

        # ================= WIN =================

        if final_boss_active and not final_boss.alive:
            state = "win"

        # ================= DRAW =================

        screen.fill(BACKGROUND)

        # background circles

        for i in range(15):

            pygame.draw.circle(
                screen,
                (35, 28, 48),
                (i * 220 - camera_x // 4, 100),
                120
            )

        # platforms

        for p in platforms:

            pygame.draw.rect(
                screen,
                (70, 70, 85),
                (p.x - camera_x, p.y, p.width, p.height),
                border_radius=8
            )

        # checkpoint

        pygame.draw.rect(
            screen,
            (80, 255, 120),
            (checkpoint.x - camera_x, checkpoint.y, 60, 80),
            border_radius=10
        )

        # player

        player.draw(screen, camera_x)

        # enemies

        for e in enemies:
            e.draw(screen, camera_x)

        # boss

        if boss_active and boss.alive:
            boss.draw(screen, camera_x)

        # final boss

        if final_boss_active and final_boss.alive:
            final_boss.draw(screen, camera_x)

        # hud

        hp = font.render(f"HP: {player.health}", True, (255, 255, 255))
        screen.blit(hp, (20, 20))

        pygame.display.update()

    # =========================================================
    # =================== MID STORY ===========================
    # =========================================================

    if state == "mid_story":

        screen.fill((15, 15, 25))

        lines = [

            [
                "Le truppe del villaggio sono state sconfitte."
            ],

            [
                "Ma il male non è ancora finito."
            ],

            [
                "Bisogna salire la scalinata",
                "verso il castello finale."
            ],

            [
                "..."
            ],

            [
                "Ma forse...",
                "in tutto questo ero io",
                "il vero Grape Monster."
            ]
        ]

        current = lines[story_phase - 3]

        y = 220

        for line in current:

            text = font.render(line, True, (255, 255, 255))

            screen.blit(
                text,
                (WIDTH // 2 - text.get_width() // 2, y)
            )

            y += 60

        continue_text = font_small.render(
            "Premi INVIO per continuare",
            True,
            (180, 180, 180)
        )

        screen.blit(
            continue_text,
            (WIDTH // 2 - continue_text.get_width() // 2, 620)
        )

        pygame.display.update()
        clock.tick(60)
        continue

    # =========================================================
    # ======================= WIN ==============================
    # =========================================================

    if state == "win":

        screen.fill((10, 20, 10))

        title = font_big.render("GRAPE MONSTER", True, (180, 80, 255))

        text1 = font.render(
            "Hai sconfitto l'uva malvagia!",
            True,
            (255, 255, 255)
        )

        text2 = font.render(
            "Premi ESC per uscire",
            True,
            (255, 255, 255)
        )

        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 180)
        )

        screen.blit(
            text1,
            (WIDTH // 2 - text1.get_width() // 2, 350)
        )

        screen.blit(
            text2,
            (WIDTH // 2 - text2.get_width() // 2, 450)
        )

        pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()
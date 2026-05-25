import pygame
import sys

from player import Player
from enemy import Enemy
from boss import Boss
from save_system import save_game, load_game

pygame.init()

# =====================================================
# WINDOW
# =====================================================

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grape Monster")

clock = pygame.time.Clock()

# =====================================================
# FONTS
# =====================================================

font_big = pygame.font.SysFont("arial", 72)
font = pygame.font.SysFont("arial", 34)
font_small = pygame.font.SysFont("arial", 24)

# =====================================================
# COLORS
# =====================================================

BACKGROUND = (22, 18, 30)

# =====================================================
# LOAD SAVE
# =====================================================

spawn_x, spawn_y = load_game()

# =====================================================
# PLAYER
# =====================================================

player = Player(spawn_x, spawn_y)

# =====================================================
# CAMERA
# =====================================================

camera_x = 0

# =====================================================
# ENEMIES
# =====================================================

enemies = [
    Enemy(700, 520),
    Enemy(1200, 520),
    Enemy(1700, 520),
]

# =====================================================
# BOSSES
# =====================================================

boss = Boss(2400, 430, False)
final_boss = Boss(5200, 260, True)

boss_active = False
final_boss_active = False

# =====================================================
# PLATFORMS
# =====================================================

platforms = [

    pygame.Rect(0, 650, 7000, 70),

    pygame.Rect(400, 520, 200, 20),
    pygame.Rect(850, 430, 200, 20),
    pygame.Rect(1400, 360, 200, 20),

    pygame.Rect(2200, 520, 300, 20),

    pygame.Rect(3600, 580, 180, 20),
    pygame.Rect(3900, 520, 180, 20),
    pygame.Rect(4200, 460, 180, 20),
    pygame.Rect(4500, 400, 180, 20),
    pygame.Rect(4800, 340, 180, 20),

    pygame.Rect(5050, 420, 700, 20),
]

# =====================================================
# CHECKPOINTS
# =====================================================

checkpoint_1 = pygame.Rect(3000, 570, 60, 80)
checkpoint_2 = pygame.Rect(4900, 260, 60, 80)

checkpoint_menu = False

# =====================================================
# STATES
# =====================================================

state = "menu"
story_phase = 0

running = True

# =====================================================
# CHECKPOINT NAME
# =====================================================

def get_checkpoint_name(x):

    if x < 4500:
        return "Villaggio iniziale"

    return "Ai piedi del castello"

# =====================================================
# MAIN LOOP
# =====================================================

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # =========================================
            # MENU
            # =========================================

            if state == "menu":

                if event.key == pygame.K_RETURN:
                    state = "intro_story"

            # =========================================
            # INTRO STORY
            # =========================================

            elif state == "intro_story":

                if event.key == pygame.K_RETURN:

                    story_phase += 1

                    if story_phase > 2:
                        state = "game"

            # =========================================
            # MID STORY
            # =========================================

            elif state == "mid_story":

                if event.key == pygame.K_RETURN:

                    story_phase += 1

                    if story_phase > 4:

                        player.rect.x = 3400
                        player.rect.y = 500

                        state = "final_path"

            # =========================================
            # WIN
            # =========================================

            elif state == "win":

                if event.key == pygame.K_ESCAPE:
                    running = False

            # =========================================
            # CHECKPOINT MENU
            # =========================================

            elif state == "game" or state == "final_path":

                if checkpoint_menu:

                    if event.key == pygame.K_RETURN:

                        save_game(player.rect.x, player.rect.y)

                        # HEAL PLAYER
                        player.health = 5

                        checkpoint_menu = False

                    if event.key == pygame.K_ESCAPE:
                        checkpoint_menu = False

                else:

                    touching_checkpoint = (
                        player.rect.colliderect(checkpoint_1)
                        or
                        player.rect.colliderect(checkpoint_2)
                    )

                    if touching_checkpoint:

                        if event.key == pygame.K_e:
                            checkpoint_menu = True

    # =====================================================
    # MENU
    # =====================================================

    if state == "menu":

        screen.fill((18, 10, 28))

        title = font_big.render(
            "GRAPE MONSTER",
            True,
            (180, 80, 255)
        )

        text = font.render(
            "Premi INVIO per iniziare",
            True,
            (255, 255, 255)
        )

        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 220)
        )

        screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, 420)
        )

        pygame.display.update()
        clock.tick(60)
        continue

    # =====================================================
    # INTRO STORY
    # =====================================================

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

            text = font.render(
                line,
                True,
                (255, 255, 255)
            )

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

    # =====================================================
    # MID STORY
    # =====================================================

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

            text = font.render(
                line,
                True,
                (255, 255, 255)
            )

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

    # =====================================================
    # GAME / FINAL PATH
    # =====================================================

    if state == "game" or state == "final_path":

        # =============================================
        # CHECKPOINT MENU
        # =============================================

        if checkpoint_menu:

            screen.fill((15, 15, 25))

            pygame.draw.rect(
                screen,
                (40, 40, 60),
                (290, 150, 700, 400),
                border_radius=20
            )

            title = font_big.render(
                "CHECKPOINT",
                True,
                (120, 255, 120)
            )

            screen.blit(
                title,
                (WIDTH // 2 - title.get_width() // 2, 190)
            )

            location = get_checkpoint_name(player.rect.x)

            location_text = font.render(
                f"Posizione: {location}",
                True,
                (255, 255, 255)
            )

            screen.blit(
                location_text,
                (WIDTH // 2 - location_text.get_width() // 2, 320)
            )

            info1 = font_small.render(
                "INVIO = salva e cura completamente",
                True,
                (220, 220, 220)
            )

            info2 = font_small.render(
                "ESC = chiudi",
                True,
                (220, 220, 220)
            )

            screen.blit(
                info1,
                (WIDTH // 2 - info1.get_width() // 2, 420)
            )

            screen.blit(
                info2,
                (WIDTH // 2 - info2.get_width() // 2, 470)
            )

            pygame.display.update()
            clock.tick(60)
            continue

        # =============================================
        # PLAYER UPDATE
        # =============================================

        keys = pygame.key.get_pressed()

        player.update(keys, platforms)

        camera_x = player.rect.x - WIDTH // 2

        # =============================================
        # ENEMIES UPDATE ONLY IF VISIBLE
        # =============================================

        for e in enemies:

            if abs(e.rect.x - player.rect.x) < WIDTH:
                e.update(player)

        # =============================================
        # PLAYER DAMAGE ENEMIES
        # =============================================

        for e in enemies:

            if player.attacking and e.alive:

                if player.attack_rect.colliderect(e.rect):
                    e.take_damage()

            for projectile in player.projectiles:

                if e.alive and projectile.rect.colliderect(e.rect):

                    e.take_damage()
                    projectile.alive = False

        # =============================================
        # ACTIVATE BOSS
        # =============================================

        if not boss_active:

            all_dead = True

            for e in enemies:

                if e.alive:
                    all_dead = False

            if all_dead:
                boss_active = True

        # =============================================
        # MID BOSS
        # =============================================

        boss_visible = abs(boss.rect.x - player.rect.x) < WIDTH

        if boss_active and boss.alive and boss_visible:

            boss.update(player)

            if player.attacking:

                if player.attack_rect.colliderect(boss.rect):
                    boss.take_damage()

            for projectile in player.projectiles:

                if projectile.rect.colliderect(boss.rect):

                    boss.take_damage()
                    projectile.alive = False

        # =============================================
        # MID STORY
        # =============================================

        if boss_active and not boss.alive and state == "game":

            state = "mid_story"
            story_phase = 3

        # =============================================
        # FINAL BOSS
        # =============================================

        if state == "final_path":
            final_boss_active = True

        final_boss_visible = (
            abs(final_boss.rect.x - player.rect.x) < WIDTH
        )

        if (
            final_boss_active
            and
            final_boss.alive
            and
            final_boss_visible
        ):

            final_boss.update(player)

            if player.attacking:

                if player.attack_rect.colliderect(final_boss.rect):
                    final_boss.take_damage()

            for projectile in player.projectiles:

                if projectile.rect.colliderect(final_boss.rect):

                    final_boss.take_damage()
                    projectile.alive = False

        # =============================================
        # ENEMY DAMAGE PLAYER
        # =============================================

        for e in enemies:

            if abs(e.rect.x - player.rect.x) < WIDTH:
                e.attack_player(player)

        # =============================================
        # GAME OVER
        # =============================================

        if player.health <= 0:
            running = False

        # =============================================
        # WIN
        # =============================================

        if final_boss_active and not final_boss.alive:
            state = "win"

        # =============================================
        # DRAW
        # =============================================

        screen.fill(BACKGROUND)

        # background

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

        # checkpoints

        pygame.draw.rect(
            screen,
            (80, 255, 120),
            (
                checkpoint_1.x - camera_x,
                checkpoint_1.y,
                60,
                80
            ),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            (80, 255, 120),
            (
                checkpoint_2.x - camera_x,
                checkpoint_2.y,
                60,
                80
            ),
            border_radius=10
        )

        # checkpoint prompt

        touching_checkpoint = (
            player.rect.colliderect(checkpoint_1)
            or
            player.rect.colliderect(checkpoint_2)
        )

        if touching_checkpoint:

            interact = font_small.render(
                "Premi E per riposare",
                True,
                (255, 255, 255)
            )

            screen.blit(
                interact,
                (
                    WIDTH // 2 - interact.get_width() // 2,
                    80
                )
            )

        # player

        player.draw(screen, camera_x)

        # enemies

        for e in enemies:

            if abs(e.rect.x - player.rect.x) < WIDTH:
                e.draw(screen, camera_x)

        # bosses

        if boss_active and boss.alive and boss_visible:
            boss.draw(screen, camera_x)

        if (
            final_boss_active
            and
            final_boss.alive
            and
            final_boss_visible
        ):
            final_boss.draw(screen, camera_x)

        # HUD

        hp = font.render(
            f"HP: {player.health}",
            True,
            (255, 255, 255)
        )

        screen.blit(hp, (20, 20))

        pygame.display.update()

    # =====================================================
    # WIN SCREEN
    # =====================================================

    if state == "win":

        screen.fill((10, 20, 10))

        title = font_big.render(
            "GRAPE MONSTER",
            True,
            (180, 80, 255)
        )

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
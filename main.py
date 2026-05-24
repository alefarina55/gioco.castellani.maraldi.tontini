import pygame
import sys

from player import Player
from enemy import Enemy

# Inizializza pygame
pygame.init()

# Dimensioni finestra
WIDTH = 1000
HEIGHT = 600

# Crea finestra
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Action Game")

# Clock FPS
clock = pygame.time.Clock()

# Colori
BACKGROUND_COLOR = (25, 25, 35)

# Player
player = Player(100, 300)

enemy = Enemy(600, 480)

# Piattaforme
platforms = [
    pygame.Rect(0, 550, 1000, 50),
    pygame.Rect(200, 450, 200, 20),
    pygame.Rect(500, 350, 200, 20),
]

# Game loop
running = True

while running:

    # Eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input tastiera
    keys = pygame.key.get_pressed()

    # Update player
    player.update(keys, platforms)

    if player.attacking and enemy.alive:

        if player.attack_rect.colliderect(enemy.rect):

            enemy.take_damage()

    # Disegna sfondo
    screen.fill(BACKGROUND_COLOR)

    # Disegna piattaforme
    for platform in platforms:
        pygame.draw.rect(screen, (80, 80, 80), platform)

    # Disegna player
    player.draw(screen)

    enemy.draw(screen)
    
    # Aggiorna schermo
    pygame.display.update()

    # FPS
    clock.tick(60)

pygame.quit()
sys.exit()
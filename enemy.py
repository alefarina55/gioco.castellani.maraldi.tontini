import pygame

class Enemy:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 50, 70)

        self.health = 3
        self.alive = True

        self.speed = 2

        self.damage_cooldown = 0

    def update(self, player):

        if not self.alive:
            return

        if player.rect.x > self.rect.x:
            self.rect.x += self.speed

        if player.rect.x < self.rect.x:
            self.rect.x -= self.speed

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

    def attack_player(self, player):

        if not self.alive:
            return

        if self.rect.colliderect(player.rect):

            if self.damage_cooldown == 0:

                player.take_damage()

                self.damage_cooldown = 60

    def take_damage(self):

        self.health -= 1

        if self.health <= 0:
            self.alive = False

    def draw(self, screen, camera_x):

        if not self.alive:
            return

        pygame.draw.rect(
            screen,
            (200, 60, 60),
            (
                self.rect.x - camera_x,
                self.rect.y,
                self.rect.width,
                self.rect.height
            ),
            border_radius=10
        )

        # eyes

        pygame.draw.circle(
            screen,
            (0, 0, 0),
            (
                self.rect.x - camera_x + 15,
                self.rect.y + 20
            ),
            4
        )

        pygame.draw.circle(
            screen,
            (0, 0, 0),
            (
                self.rect.x - camera_x + 35,
                self.rect.y + 20
            ),
            4
        )
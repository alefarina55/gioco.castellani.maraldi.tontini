import pygame
from projectile import Projectile

class Boss:

    def __init__(self, x, y, final_boss=False):

        self.rect = pygame.Rect(x, y, 140, 140)

        self.health = 30
        self.alive = True

        self.speed = 2

        self.projectiles = []

        self.attack_cooldown = 0

        self.final_boss = final_boss

    def update(self, player):

        if not self.alive:
            return

        distance = player.rect.centerx - self.rect.centerx

        # movement

        if abs(distance) > 320:

            if distance > 0:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed

        # attack cooldown

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # shoot projectile

        if abs(distance) <= 420 and self.attack_cooldown == 0:

            direction = 1

            if distance < 0:
                direction = -1

            color = (255, 80, 80)

            if self.final_boss:
                color = (180, 80, 255)

            projectile = Projectile(
                self.rect.centerx,
                self.rect.centery,
                direction,
                color,
                8
            )

            self.projectiles.append(projectile)

            self.attack_cooldown = 50

        # update projectiles

        for projectile in self.projectiles:

            projectile.update()

            if projectile.rect.colliderect(player.rect):

                player.take_damage()

                projectile.alive = False

        self.projectiles = [p for p in self.projectiles if p.alive]

    def take_damage(self):

        self.health -= 1

        if self.health <= 0:
            self.alive = False

    def draw(self, screen, camera_x):

        if not self.alive:
            return

        # FINAL BOSS = EVIL GRAPE

        if self.final_boss:

            # aura

            pygame.draw.circle(
                screen,
                (90, 20, 120),
                (
                    self.rect.centerx - camera_x,
                    self.rect.centery
                ),
                95
            )

            # grape body

            pygame.draw.circle(
                screen,
                (140, 0, 180),
                (
                    self.rect.centerx - camera_x,
                    self.rect.centery
                ),
                70
            )

            # eyes

            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (
                    self.rect.centerx - camera_x - 25,
                    self.rect.centery - 15
                ),
                10
            )

            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (
                    self.rect.centerx - camera_x + 25,
                    self.rect.centery - 15
                ),
                10
            )

            # mouth

            pygame.draw.arc(
                screen,
                (0, 0, 0),
                (
                    self.rect.centerx - camera_x - 30,
                    self.rect.centery + 10,
                    60,
                    40
                ),
                3.14,
                0,
                4
            )

        # NORMAL BOSS

        else:

            pygame.draw.rect(
                screen,
                (180, 50, 50),
                (
                    self.rect.x - camera_x,
                    self.rect.y,
                    self.rect.width,
                    self.rect.height
                ),
                border_radius=18
            )

            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (
                    self.rect.x - camera_x + 40,
                    self.rect.y + 40
                ),
                8
            )

            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (
                    self.rect.x - camera_x + 100,
                    self.rect.y + 40
                ),
                8
            )

        # projectiles

        for projectile in self.projectiles:
            projectile.draw(screen, camera_x)
import pygame
from projectile import Projectile

class Player:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 50, 70)

        # movement
        self.speed = 5
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_power = 10
        self.on_ground = False
        self.facing_right = True

        # health
        self.health = 5
        self.damage_cooldown = 0

        # sword attack
        self.attacking = False
        self.attack_timer = 0
        self.attack_rect = pygame.Rect(0, 0, 45, 20)

        # elemental projectiles
        self.projectiles = []
        self.elemental_cooldown = 0

        # dash
        self.dashing = False
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.dash_speed = 15

        # parry
        self.parrying = False
        self.parry_timer = 0

    # ================= MOVEMENT =================

    def move(self, keys):

        if self.dashing:
            return

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.facing_right = False

        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.facing_right = True

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False

    # ================= GRAVITY =================

    def apply_gravity(self):

        self.vel_y += self.gravity

        if self.vel_y > 15:
            self.vel_y = 15

        self.rect.y += self.vel_y

    # ================= COLLISIONS =================

    def check_collision(self, platforms):

        self.on_ground = False

        for p in platforms:

            if self.rect.colliderect(p):

                if self.vel_y > 0:
                    self.rect.bottom = p.top
                    self.vel_y = 0
                    self.on_ground = True

    # ================= SWORD ATTACK =================

    def attack(self, keys):

        if keys[pygame.K_j] and not self.attacking:
            self.attacking = True
            self.attack_timer = 15

        if self.attacking:

            self.attack_timer -= 1

            if self.facing_right:
                self.attack_rect.x = self.rect.right
            else:
                self.attack_rect.x = self.rect.left - self.attack_rect.width

            self.attack_rect.y = self.rect.y + 20

            if self.attack_timer <= 0:
                self.attacking = False

    # ================= ELEMENTAL ATTACK =================

    def elemental_attack(self, keys):

        if self.elemental_cooldown > 0:
            self.elemental_cooldown -= 1

        if keys[pygame.K_l] and self.elemental_cooldown == 0:

            direction = 1

            if not self.facing_right:
                direction = -1

            projectile = Projectile(
                self.rect.centerx,
                self.rect.centery,
                direction,
                (100, 180, 255),
                12
            )

            self.projectiles.append(projectile)

            self.elemental_cooldown = 30

        for projectile in self.projectiles:
            projectile.update()

        self.projectiles = [p for p in self.projectiles if p.alive]

    # ================= DASH =================

    def dash(self, keys):

        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        if keys[pygame.K_LSHIFT] and not self.dashing and self.dash_cooldown == 0:

            self.dashing = True
            self.dash_timer = 10
            self.dash_cooldown = 40

        if self.dashing:

            if self.facing_right:
                self.rect.x += self.dash_speed
            else:
                self.rect.x -= self.dash_speed

            self.dash_timer -= 1

            if self.dash_timer <= 0:
                self.dashing = False

    # ================= PARRY =================

    def parry(self, keys):

        if keys[pygame.K_k] and not self.parrying:

            self.parrying = True
            self.parry_timer = 15

        if self.parrying:

            self.parry_timer -= 1

            if self.parry_timer <= 0:
                self.parrying = False

    # ================= DAMAGE =================

    def take_damage(self):

        if self.parrying:
            return

        if self.damage_cooldown == 0:

            self.health -= 1
            self.damage_cooldown = 60

    # ================= UPDATE =================

    def update(self, keys, platforms):

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        self.move(keys)
        self.attack(keys)
        self.elemental_attack(keys)
        self.dash(keys)
        self.parry(keys)

        self.apply_gravity()
        self.check_collision(platforms)

    # ================= DRAW =================

    def draw(self, screen, camera_x):

        # body
        color = (220, 220, 220)

        if self.dashing:
            color = (80, 180, 255)

        if self.parrying:
            color = (255, 255, 100)

        pygame.draw.rect(
            screen,
            color,
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
            (255, 255, 255),
            (self.rect.x - camera_x + 15, self.rect.y + 20),
            4
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (self.rect.x - camera_x + 35, self.rect.y + 20),
            4
        )

        # sword attack
        if self.attacking:

            pygame.draw.rect(
                screen,
                (255, 80, 80),
                (
                    self.attack_rect.x - camera_x,
                    self.attack_rect.y,
                    self.attack_rect.width,
                    self.attack_rect.height
                ),
                border_radius=6
            )

        # projectiles
        for projectile in self.projectiles:
            projectile.draw(screen, camera_x)
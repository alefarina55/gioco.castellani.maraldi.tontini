import pygame

class Enemy:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 50, 70)

        self.health = 3
        self.alive = True

        self.speed = 2

    def move_towards_player(self, player):

        if not self.alive:
            return

        if player.rect.x > self.rect.x:
            self.rect.x += self.speed

        if player.rect.x < self.rect.x:
            self.rect.x -= self.speed

    def take_damage(self):

        self.health -= 1

        if self.health <= 0:
            self.alive = False

    def attack_player(self, player):

        if self.alive and self.rect.colliderect(player.rect):

            player.take_damage()

    def update(self, player):

        self.move_towards_player(player)

        self.attack_player(player)

    def draw(self, screen):

        if self.alive:
            pygame.draw.rect(screen, (200, 60, 60), self.rect)
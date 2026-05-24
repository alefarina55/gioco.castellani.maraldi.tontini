import pygame

class Enemy:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 50, 70)

        self.health = 3

        self.alive = True

    def take_damage(self):

        self.health -= 1

        if self.health <= 0:
            self.alive = False

    def draw(self, screen):

        if self.alive:
            pygame.draw.rect(screen, (200, 60, 60), self.rect)
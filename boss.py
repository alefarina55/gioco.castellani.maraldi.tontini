import pygame

class Boss:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 120, 120)

        self.health = 15
        self.alive = True

        self.speed = 2

        self.attack_cooldown = 0

    def move_towards_player(self, player):

        if not self.alive:
            return

        if player.rect.x > self.rect.x:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def take_damage(self):

        self.health -= 1

        if self.health <= 0:
            self.alive = False

    def attack_player(self, player):

        if not self.alive:
            return

        if self.rect.colliderect(player.rect):

            player.take_damage()

    def update(self, player):

        self.move_towards_player(player)
        self.attack_player(player)

    def draw(self, screen):

        if self.alive:
            pygame.draw.rect(screen, (120, 0, 180), self.rect)
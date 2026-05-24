import pygame

class Projectile:

    def __init__(self, x, y, direction, color, speed):

        self.rect = pygame.Rect(x, y, 20, 12)

        self.direction = direction
        self.speed = speed

        self.color = color

        self.alive = True

    def update(self):

        self.rect.x += self.speed * self.direction

        if self.rect.x < -200 or self.rect.x > 6000:
            self.alive = False

    def draw(self, screen, camera_x):

        pygame.draw.ellipse(
            screen,
            self.color,
            (
                self.rect.x - camera_x,
                self.rect.y,
                self.rect.width,
                self.rect.height
            )
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (
                self.rect.x - camera_x + 5,
                self.rect.y + 5
            ),
            2
        )
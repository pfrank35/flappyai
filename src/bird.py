
import pygame


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.radius = 18

        # Physics
        self.velocity = 0
        self.gravity = 1500
        self.flap_strength = -450

    def flap(self):
        self.velocity = self.flap_strength

    def update(self, dt):
        # Apply gravity
        self.velocity += self.gravity * dt

        # Update vertical position
        self.y += self.velocity * dt

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 220, 50),
            (int(self.x), int(self.y)),
            self.radius
        )

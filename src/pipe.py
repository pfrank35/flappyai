
import pygame
import random


class Pipe:
    def __init__(self, x, screen_height):
        self.x = x
        self.width = 80
        self.gap = 180
        self.speed = 220

        # Randomize the vertical position of the gap
        self.top_height = random.randint(
            80,
            screen_height - self.gap - 80
        )

        self.passed = False

    def update(self, dt):
        self.x -= self.speed * dt

    def draw(self, screen, screen_height):
        green = (50, 180, 70)

        # Top pipe
        pygame.draw.rect(
            screen,
            green,
            (self.x, 0, self.width, self.top_height)
        )

        # Bottom pipe
        bottom_y = self.top_height + self.gap

        pygame.draw.rect(
            screen,
            green,
            (
                self.x,
                bottom_y,
                self.width,
                screen_height - bottom_y
            )
        )

    def collides_with(self, bird):
        bird_rect = pygame.Rect(
            bird.x - bird.radius,
            bird.y - bird.radius,
            bird.radius * 2,
            bird.radius * 2
        )

        top_pipe = pygame.Rect(
            self.x, 0, self.width, self.top_height
        )

        bottom_pipe = pygame.Rect(
            self.x,
            self.top_height + self.gap,
            self.width,
            1000
        )

        return (
            bird_rect.colliderect(top_pipe)
            or bird_rect.colliderect(bottom_pipe)
        )

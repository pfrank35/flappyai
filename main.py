
import pygame

from src.bird import Bird
from src.pipe import Pipe
from src.neural_network import choose_action

pygame.init()

# Window settings
WIDTH = 500
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird AI")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 36)

# Game setup
bird = Bird(150, 300)
pipes = [Pipe(WIDTH + 100, HEIGHT)]

score = 0
game_over = False
started = False
ai_mode = False

running = True

while running:

    dt = min(clock.tick(60) / 1000, 0.05)

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and not game_over:
                if not started:
                    started = True

                bird.flap()

            if event.key == pygame.K_r and game_over:
                bird = Bird(150, 300)
                pipes = [Pipe(WIDTH + 100, HEIGHT)]
                score = 0
                game_over = False
                started = False
            if event.key == pygame.K_a:
                ai_mode = not ai_mode

    # Update game
    if started and not game_over:

        bird.update(dt)

        for pipe in pipes:
            pipe.update(dt)

            if pipe.collides_with(bird):
                game_over = True

            if not pipe.passed and pipe.x + pipe.width < bird.x:
                pipe.passed = True
                score += 1
        if ai_mode:
            next_pipe = next(
                (pipe for pipe in pipes if pipe.x + pipe.width > bird.x),
                None
             )

            if next_pipe:
                if choose_action(bird, next_pipe):
                    bird.flap()

        # Generate new pipes
        if pipes[-1].x < WIDTH - 250:
            pipes.append(Pipe(WIDTH + 100, HEIGHT))

        # Remove old pipes
        pipes = [
            pipe for pipe in pipes
            if pipe.x + pipe.width > 0
        ]

        # Screen boundaries
        if bird.y - bird.radius < 0 or bird.y + bird.radius > HEIGHT:
            game_over = True

    # Draw everything
    screen.fill((100, 180, 230))

    for pipe in pipes:
        pipe.draw(screen, HEIGHT)

    bird.draw(screen)

    # Score
    score_text = font.render(
        str(score), True, (255, 255, 255)
    )
    screen.blit(
        score_text,
        (WIDTH // 2 - score_text.get_width() // 2, 30)
    )

    # Start screen
    if not started and not game_over:
        start_text = font.render(
            "PRESS SPACE TO START",
            True,
            (255, 255, 255)
        )
        screen.blit(
            start_text,
            (WIDTH // 2 - start_text.get_width() // 2, 350)
        )

    # Game over
    if game_over:
        game_over_text = font.render(
            "GAME OVER", True, (255, 50, 50)
        )
        restart_text = pygame.font.SysFont(
            "Arial", 20
        ).render(
            "Press R to restart", True, (255, 255, 255)
        )

        screen.blit(
            game_over_text,
            (WIDTH // 2 - game_over_text.get_width() // 2, 300)
        )
        screen.blit(
            restart_text,
            (WIDTH // 2 - restart_text.get_width() // 2, 350)
        )

    pygame.display.flip()

pygame.quit()

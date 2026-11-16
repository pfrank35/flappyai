
import pygame
import neat
from pathlib import Path

from src.bird import Bird
from src.pipe import Pipe

# --------------------------------
# WINDOW SETTINGS
# --------------------------------

WIDTH = 500
HEIGHT = 700

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird AI Training")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)
hud_font = pygame.font.SysFont("Arial", 17)

# --------------------------------
# HIGH SCORE STORAGE
# --------------------------------

HIGH_SCORE_FILE = Path("high_score.txt")

try:
    ALL_TIME_HIGH_SCORE = int(
        HIGH_SCORE_FILE.read_text().strip()
    )
except (FileNotFoundError, ValueError):
    ALL_TIME_HIGH_SCORE = 0

GENERATION_NUMBER = 0


def save_high_score():
    HIGH_SCORE_FILE.write_text(str(ALL_TIME_HIGH_SCORE))


# --------------------------------
# NEURAL NETWORK INPUTS
# --------------------------------

def get_ai_inputs(bird, pipe):
    """
    Convert game information into four normalized
    numerical inputs for the neural network.
    """

    gap_center = pipe.top_height + pipe.gap / 2

    bird_y = bird.y / HEIGHT
    bird_velocity = bird.velocity / 500
    pipe_distance = (pipe.x - bird.x) / WIDTH
    gap_center = gap_center / HEIGHT

    return (
        bird_y,
        bird_velocity,
        pipe_distance,
        gap_center
    )


# --------------------------------
# DEBUG DISPLAY
# --------------------------------

def draw_ai_inputs(screen, inputs):

    labels = [
        "Bird Y",
        "Velocity",
        "Pipe Distance",
        "Gap Center"
    ]

    for i, (label, value) in enumerate(zip(labels, inputs)):

        text = font.render(
            f"{label}: {value:.3f}",
            True,
            (255, 255, 255)
        )

        screen.blit(text, (10, 85 + i * 30))


# --------------------------------
# TRAINING HUD
# --------------------------------

def draw_hud(
    screen,
    generation,
    birds_alive,
    current_score,
    generation_best
):

    pygame.draw.rect(
        screen,
        (30, 40, 50),
        (0, 0, WIDTH, 65)
    )

    line_one = hud_font.render(
        f"Generation: {generation}    "
        f"Birds Alive: {birds_alive}",
        True,
        (255, 255, 255)
    )

    line_two = hud_font.render(
        f"Current: {current_score}    "
        f"Gen Best: {generation_best}    "
        f"All-Time: {ALL_TIME_HIGH_SCORE}",
        True,
        (255, 220, 80)
    )

    screen.blit(line_one, (10, 7))
    screen.blit(line_two, (10, 37))


# --------------------------------
# GENOME EVALUATION
# --------------------------------

def eval_genomes(genomes, config):

    global ALL_TIME_HIGH_SCORE
    global GENERATION_NUMBER

    generation = GENERATION_NUMBER

    # Create lists for every bird
    birds = []
    networks = []
    genome_list = []

    # Track pipe progress independently
    passed_pipes = []
    pipe_scores = []

    # Create a bird and network for every genome
    for genome_id, genome in genomes:

        genome.fitness = 0

        network = neat.nn.FeedForwardNetwork.create(
            genome, config
        )

        bird = Bird(150, 300)

        birds.append(bird)
        networks.append(network)
        genome_list.append(genome)

        passed_pipes.append(set())
        pipe_scores.append(0)

    # Create first pipe
    pipes = [Pipe(WIDTH + 100, HEIGHT)]

    generation_best = 0

    running = True

    while running:

        dt = min(clock.tick(60) / 1000, 0.05)

        # ----------------------------
        # EVENTS
        # ----------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                save_high_score()
                pygame.quit()
                raise SystemExit

        # Keep at least one pipe available
        if not pipes:
            pipes.append(Pipe(WIDTH + 100, HEIGHT))

        # ----------------------------
        # UPDATE BIRDS
        # ----------------------------

        for i, bird in enumerate(birds):

            # Small survival reward
            genome_list[i].fitness += 0.1

            # Find the next pipe
            next_pipe = next(
                (
                    pipe for pipe in pipes
                    if pipe.x + pipe.width > bird.x
                ),
                pipes[-1]
            )

            # Get neural network inputs
            inputs = get_ai_inputs(bird, next_pipe)

            # Activate neural network
            output = networks[i].activate(inputs)

            # Flap based on network output
            if output[0] > 0.5:
                bird.flap()

            bird.update(dt)

        # ----------------------------
        # UPDATE PIPES
        # ----------------------------

        for pipe in pipes:
            pipe.update(dt)

        # ----------------------------
        # REMOVE DEAD BIRDS
        # ----------------------------

        for i in range(len(birds) - 1, -1, -1):

            bird = birds[i]

            dead = (
                bird.y - bird.radius < 0
                or bird.y + bird.radius > HEIGHT
                or any(
                    pipe.collides_with(bird)
                    for pipe in pipes
                )
            )

            if dead:

                birds.pop(i)
                networks.pop(i)
                genome_list.pop(i)
                passed_pipes.pop(i)
                pipe_scores.pop(i)

        # ----------------------------
        # PIPE PASSING REWARDS
        # ----------------------------

        for i, bird in enumerate(birds):

            for pipe in pipes:

                if (
                    pipe not in passed_pipes[i]
                    and pipe.x + pipe.width < bird.x
                ):

                    # Reward successful pipe navigation
                    genome_list[i].fitness += 5

                    # Remember this pipe
                    passed_pipes[i].add(pipe)

                    # Update individual score
                    pipe_scores[i] += 1

        # ----------------------------
        # UPDATE HIGH SCORES
        # ----------------------------

        if pipe_scores:

            generation_best = max(
                generation_best,
                max(pipe_scores)
            )

            current_best = max(pipe_scores)

            if current_best > ALL_TIME_HIGH_SCORE:

                ALL_TIME_HIGH_SCORE = current_best
                save_high_score()

        # ----------------------------
        # SPAWN NEW PIPES
        # ----------------------------

        if pipes[-1].x < WIDTH - 250:
            pipes.append(Pipe(WIDTH + 100, HEIGHT))

        # Remove pipes that leave screen
        pipes = [
            pipe for pipe in pipes
            if pipe.x + pipe.width > 0
        ]

        # ----------------------------
        # CHECK POPULATION
        # ----------------------------

        if not birds:
            running = False

        # ----------------------------
        # DRAW EVERYTHING
        # ----------------------------

        screen.fill((100, 180, 230))

        # Draw pipes
        for pipe in pipes:
            pipe.draw(screen, HEIGHT)

        # Draw birds
        for bird in birds:
            bird.draw(screen)

        # Find current best bird
        if birds and pipes:

            best_index = max(
                range(len(pipe_scores)),
                key=lambda i: pipe_scores[i]
            )

            debug_bird = birds[best_index]

            next_pipe = next(
                (
                    pipe for pipe in pipes
                    if pipe.x + pipe.width > debug_bird.x
                ),
                None
            )

            if next_pipe is not None:

                inputs = get_ai_inputs(
                    debug_bird,
                    next_pipe
                )

                draw_ai_inputs(screen, inputs)

        # Current best surviving bird's score
        current_score = max(pipe_scores, default=0)

        # Draw HUD
        draw_hud(
            screen,
            generation,
            len(birds),
            current_score,
            generation_best
        )

        pygame.display.flip()

    # Move to next generation
    GENERATION_NUMBER += 1


# --------------------------------
# RUN NEAT
# --------------------------------

def run():

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "neat_config.txt"
    )

    population = neat.Population(config)

    population.add_reporter(
        neat.StdOutReporter(True)
    )

    winner = population.run(eval_genomes, 200)

    save_high_score()

    print("\nTraining complete!")
    print("All-time high score:", ALL_TIME_HIGH_SCORE)

    pygame.quit()


if __name__ == "__main__":
    run()

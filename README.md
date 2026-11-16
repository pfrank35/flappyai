# Flappy Bird AI

A Flappy Bird-style game built with Python and Pygame. It has a manual-play mode, a simple gap-following AI, and a separate mode that evolves bird controllers with NEAT. This project was inspired by the YouTuber Code Bullet. Their game looks much nicer, and their learning algorithm runs much faster than mine, but my goal was to learn NEAT.

## Demo

[Watch the demo on YouTube](https://youtu.be/oIpW7BD1_HQ)

## What I built

- Implemented the game loop, bird movement and gravity, randomized pipes, collision detection, scoring, and restart behavior.
- Added keyboard controls for playing and a basic AI controller that steers toward the next pipe's gap.
- Built a NEAT training mode that evolves a population of neural networks. Each network uses four game-state inputs: bird height, bird velocity, distance to the next pipe, and gap center. Fitness rewards survival and passing pipes.
- Added a training display for generation progress and high scores.

## What was challenging

One challenge was learning NEAT. My first few runs went through 50 generations without any birds making it past the second pipe. I spent a lot of time trying to figure out why. In the end, I increased the population size from 50 to 100 and eventually to 1,000. I think that with only 50 individuals, I wasn't getting enough variation for one to stumble upon a viable solution. With 1,000, that changed, and now I get fairly reliable results.

## Run it

You need Python 3 and Git. From a terminal:

```shell
git clone https://github.com/pfrank35/flappyai.git
cd flappyai
```

Create and activate a virtual environment (recommended):

**Windows PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies and start the game:

```shell
python -m pip install -r requirements.txt
python main.py
```

### Play

- Press **Space** to start and flap.
- Press **A** to toggle the simple AI controller.
- After a collision, press **R** to restart.
- Close the game window to quit.

### Run NEAT training

From the project directory with the virtual environment active:

```shell
python -m src.training
```

Training displays a population of birds and their progress. The current configuration uses a population of 1,000, so training may take a while. The all-time high score is saved in `high_score.txt`.

## Project files

- `main.py` — playable game and simple AI mode
- `src/training.py` — NEAT population training
- `neat_config.txt` — NEAT algorithm and population settings

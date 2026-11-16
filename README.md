# Flappy Bird AI

A Flappy Bird-style game built with Python and Pygame. It has a manual-play mode, a simple gap-following AI, and a separate mode that evolves bird controllers with NEAT.

## Demo

Add the demo recording at `assets/demo.mp4` to display it here:

<video controls width="640">
  <source src="assets\Timeline 1.mp4" type="video/mp4">
  Your browser does not support embedded video. You can also <a href="assets\Timeline 1.mp4">open the demo video</a>.
</video>

## What I built

- Implemented the game loop, bird movement and gravity, randomized pipes, collision detection, scoring, and restart behavior.
- Added keyboard controls for playing and a basic AI controller that steers toward the next pipe's gap.
- Built a NEAT training mode that evolves a population of neural networks. Each network uses four game-state inputs: bird height, bird velocity, distance to the next pipe, and gap center. Fitness rewards survival and passing pipes.
- Added a training display for generation progress and high scores.

## What was challenging

One challenge was turning the bird and pipe positions into useful, normalized inputs for a neural network. The training loop was also more involved than the single-bird game: each bird needs its own network and score, and those records must stay aligned as birds are eliminated. I also had to make fitness rewards encourage both staying alive and successfully navigating pipes.

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
- `assets/demo.mp4` — add the demo recording here

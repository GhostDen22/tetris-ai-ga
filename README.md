# TetrisGA — Autonomous Tetris Player with Genetic Algorithm

## Project overview

TetrisGA is a Python project that implements an autonomous Tetris player.

The bot plays Tetris by evaluating possible moves using board features and heuristic weights. These weights can be optimized using a genetic algorithm.

The project contains:

- a Tetris game engine,
- a heuristic AI bot,
- feature extraction from the board,
- genetic algorithm training,
- audit logging,
- command-line modes,
- a Pygame graphical interface,
- automatic tests.

The graphical interface includes two modes:

- **Demo Mode** — shows one trained bot playing Tetris.
- **Train Mode** — visualizes how multiple genomes perform during a simplified GA training process.

---

## Technologies

The project uses:

```text
Python 3.12
Pygame
pytest
```

Python 3.12 is recommended because `pygame` may not install correctly on newer Python versions such as Python 3.14.

---

## Project structure

```text
tetris-ai-ga/
│
├── ai/
│   ├── bot.py              # Heuristic bot and move scoring
│   └── features.py         # Board feature extraction
│
├── audit/
│   └── logger.py           # Append-only audit logger
│
├── core/
│   ├── board.py            # Tetris board logic
│   ├── game.py             # Main game state and actions
│   └── piece.py            # Tetromino definitions and rotations
│
├── data/
│   └── seeds.py            # Train / validation / test seeds
│
├── ga/
│   ├── evaluation.py       # Evaluation on train / validation / test sets
│   ├── fitness.py          # Fitness calculation
│   ├── genome.py           # Genome representation
│   ├── operators.py        # Selection, crossover, mutation
│   ├── population.py       # Population creation and evaluation
│   ├── storage.py          # Saving and loading best genome
│   └── trainer.py          # Genetic algorithm training loop
│
├── simulation/
│   └── runner.py           # Runs complete bot games
│
├── ui/
│   ├── panels.py           # UI panels and dashboard rendering
│   └── renderer.py         # Tetris board rendering
│
├── tests/                  # pytest test files
├── assets/                 # UI assets, such as logo files
│
├── main.py                 # CLI entry point
├── run_ui.py               # Pygame UI entry point
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd tetris-ai-ga
```

### 2. Create a virtual environment

Recommended Python version:

```text
Python 3.12
```

Create the environment:

```bash
py -3.12 -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the project

### Show available commands

```bash
python main.py help
```

### Run demo from CLI

```bash
python main.py demo
```

You can also specify a move limit:

```bash
python main.py demo 500
```

One move means one placed tetromino.  
For example, `500` means that the bot can place up to 500 pieces.

### Train the genetic algorithm

```bash
python main.py train
```

You can also specify the move limit used during training:

```bash
python main.py train 100
```

The training process saves the best genome to:

```text
models/best_genome.json
```

This file is generated locally and should not be committed to the repository.

### Evaluate saved genome

```bash
python main.py eval
```

or with a custom move limit:

```bash
python main.py eval 500
```

Evaluation checks the saved genome on:

```text
train seeds
validation seeds
test seeds
```

### Run graphical UI

```bash
python run_ui.py
```

The UI contains:

```text
Demo Mode
Train Mode
Start / Pause / Reset controls
Seed input
Speed controls
Tetris board
Bot metrics
Board features
Top 3 decision reasons
Recent logs
```

---

## Demo Mode

Demo Mode shows one bot playing Tetris.

The bot uses:

```text
models/best_genome.json
```

if the file exists.

If there is no trained genome file, the bot falls back to default heuristic weights.

Demo Mode displays:

```text
score
lines
moves
current piece
last placed piece
last decision
decision score
features
top 3 reasons
recent logs
```

The seed field controls the Tetris piece sequence.  
Changing the seed changes the order of generated pieces.

---

## Train Mode in UI

Train Mode is a visual demonstration of the genetic algorithm.

It shows multiple genomes playing in parallel on mini boards. Each genome has its own:

```text
Game
Bot
weights
moves
lines
fitness
status
```

Train Mode is simplified for visualization purposes. It is not the same as the full CLI training.

The full training is done with:

```bash
python main.py train
```

UI Train Mode is used to show the idea of genetic evolution:

```text
many genomes play
each genome receives fitness
the best genome is highlighted
a new generation can be created
selection, crossover and mutation are used
```

This makes the GA process easier to understand visually.

---

## Tetris bot logic

For every current piece, the bot:

1. Generates possible rotations and positions.
2. Simulates placing the piece.
3. Extracts board features.
4. Calculates a decision score.
5. Selects the move with the highest score.

The decision score is calculated as:

```text
score = sum(feature_value * feature_weight)
```

The bot also stores the top 3 reasons for its decision.  
These are the features with the highest absolute contribution:

```text
abs(feature_value * feature_weight)
```

---

## Board features

The bot uses the following board features:

### holes

The number of empty cells that have at least one filled cell above them in the same column.  
Holes are usually bad because they are hard to clear.

### aggregate_height

The sum of all column heights.  
A higher value means that the board is more filled.

### max_height

The height of the tallest column.  
A high value means a higher risk of game over.

### bumpiness

The sum of height differences between neighboring columns.  
A high value means the surface is uneven.

### lines_cleared

The number of lines cleared after a move.  
This is usually a positive feature.

### well_sums

The sum of well depths.  
A well is a low column between higher columns.

### row_transitions

The number of transitions between empty and filled cells in rows.  
A high value usually means a chaotic row structure.

### column_transitions

The number of transitions between empty and filled cells in columns.  
A high value can indicate holes and unstable structures.

---

## Genetic algorithm

Each genome represents a set of weights for the board features.

Example:

```json
{
  "holes": -4.0,
  "aggregate_height": -0.5,
  "max_height": -0.8,
  "bumpiness": -0.7,
  "lines_cleared": 3.0,
  "well_sums": -0.4,
  "row_transitions": -0.3,
  "column_transitions": -0.3
}
```

The genetic algorithm uses:

```text
initial random population
fitness evaluation
tournament selection
crossover
mutation
elitism
multiple generations
```

The default full training uses:

```text
population size: 30
generations: 20
elitism: 1
```

---

## Seeds

The project uses two types of seeds.

### GA seed

Controls the randomness of the genetic algorithm:

```text
initial random weights
parent selection
crossover
mutation
```

### Game seeds

Control the Tetris piece sequence.

The project separates seeds into:

```text
TRAIN_SEEDS
VALIDATION_SEEDS
TEST_SEEDS
```

This is done so that the bot is not evaluated only on one piece sequence.

---

## Fitness

Fitness is calculated using several values:

```text
average score
average lines cleared
average moves survived
stability penalty
```

The stability penalty reduces the fitness of genomes that perform very unevenly across different seeds.

This means that a stable bot is preferred over a bot that performs very well on one seed but poorly on others.

---

## Audit logging

The project contains an append-only audit logger.

Audit events are saved to:

```text
audit/audit_log.jsonl
```

The logger can store:

```text
training start
best genome per generation
training finished
bot decisions
game results
```

Each decision can include:

```text
move
score
features
top 3 reasons
timestamp
```

The audit log is generated locally and should not be committed to the repository.

---

## Tests

Run tests with:

```bash
pytest
```

The test suite checks:

```text
board size
piece placement
board boundaries
line clearing
feature extraction
runner behavior
piece rotations
determinism
```

A correct result should look similar to:

```text
15 passed
```

---

## Files not committed to repository

The following files and folders should not be committed:

```text
.venv/
__pycache__/
.pytest_cache/
audit/audit_log.jsonl
models/best_genome.json
```

`models/best_genome.json` is generated by:

```bash
python main.py train
```

---

## Typical workflow

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run tests

```bash
pytest
```

### 3. Train the bot

```bash
python main.py train 100
```

### 4. Evaluate the trained genome

```bash
python main.py eval 500
```

### 5. Run the UI

```bash
python run_ui.py
```

---


## Authors

Project created for academic purposes as a Tetris AI / Genetic Algorithm project.

- Daniel Šapovalov
- Dmytro Nesvitailo
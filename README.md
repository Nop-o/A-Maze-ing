*This project has been created as part of the 42 curriculum by [aslimani](https://github.com/devamine-42), [adamez-f](https://github.com/Nop-o).*

# A-Maze-ing

## Table of Contents

- [Description](#description)
- [Instructions](#instructions)
- [Configuration](#configuration)
- [Algorithm](#algorithm)
- [Reusable Components](#reusable-components)
- [Team](#team)
- [Resources](#resources)

---

## Description

A-Maze-ing is a maze generator written in Python 3. Its goal is to procedurally generate mazes — either **perfect** (no loops, exactly one path between any two cells) or **imperfect** (with loops and multiple paths) — based on a user-defined configuration file.

The program:
- Generates mazes using a **Depth-First Search (DFS)** algorithm with iterative backtracking
- Solves them using a **Breadth-First Search (BFS)** algorithm to find the shortest path
- Renders them in the **terminal** with full ANSI color and style support
- Exports them to a file in **hexadecimal format**
- Embeds a visible **"42" pattern** made of fully closed cells inside the maze

This project was designed to be modular: the generator, the solver, the display, and the configuration parser are independent components that can be reused separately.

---

## Instructions

### Prerequisites

- Python 3.10+
- `make`
- `pip`

### Setup — create virtual environment and install dependencies

```bash
make setup
```

This creates a virtual environment named `maze` and installs all dependencies from `requirements.txt`.

### Installation — install dependencies only

```bash
make install
```

### Running the project

```bash
make run
```

### Build the package

```bash
make build
```

This generates `dist/mazegen-1.0.0-py3-none-any.whl` and `dist/mazegen-1.0.0.tar.gz`.

### All available commands

| Command            | Description                                    |
|--------------------|------------------------------------------------|
| `make setup`       | Create venv and install dependencies           |
| `make install`     | Install dependencies from requirements.txt     |
| `make run`         | Generate and display the maze                  |
| `make debug`       | Run with Python debugger (pdb)                 |
| `make build`       | Build the mazegen pip package                  |
| `make lint`        | Run flake8 and mypy                            |
| `make lint-strict` | Run flake8 and mypy in strict mode             |
| `make clean`       | Remove all temporary files and caches          |

---

## Configuration

The configuration file uses a simple `KEY=VALUE` format. Lines starting with `#` are treated as comments. The default configuration file is `config.txt`.

### Example

```ini
# Maze dimensions
WIDTH=20
HEIGHT=15
# Entry and exit positions
ENTRY=0,0
EXIT=19,14
# Output
OUTPUT_FILE=maze.txt
# Maze type
PERFECT=True
SEED=42
# Display
DISPLAY_MODE=thin
DISPLAY_SOLUTION=True
# Colors (ANSI codes)
STYLE=1
TUNNEL=36
WALL=44
ENTRY=41
EXIT=42
LOGO=45
SOLUTION=40
```

### Maze Settings

| Key           | Type            | Description                        | Example                |
|---------------|-----------------|------------------------------------|------------------------|
| `WIDTH`       | `int`           | Number of columns                  | `WIDTH=20`             |
| `HEIGHT`      | `int`           | Number of rows                     | `HEIGHT=15`            |
| `ENTRY`       | `x,y`           | Entry cell coordinates             | `ENTRY=0,0`            |
| `EXIT`        | `x,y`           | Exit cell coordinates              | `EXIT=19,14`           |
| `OUTPUT_FILE` | `string`        | Name of the export file            | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | `bool`          | Generate a perfect maze (no loops) | `PERFECT=True`         |
| `SEED`        | `int` or `None` | Random seed for reproducibility    | `SEED=42`              |

### Display & Color Settings

Colors are specified as ANSI escape code values.
The format used internally is `\033[{STYLE};{color.text};{color.background}m<TEXT>\033[0m`.

| Key                | Description                                     | Example                    |
|--------------------|-------------------------------------------------|----------------------------|
| `STYLE`            | Text style                                      | `STYLE=1` *(bold)*         |
| `TUNNEL`           | Passage color                                   | `TUNNEL=36` *(cyan)*       |
| `WALL`             | Wall background color                           | `WALL=44` *(blue)*         |
| `ENTRY`            | Entry cell color                                | `ENTRY=41` *(red)*         |
| `EXIT`             | Exit cell color                                 | `EXIT=42` *(green)*        |
| `LOGO`             | "42" pattern color                              | `LOGO=45` *(magenta)*      |
| `SOLUTION`         | Solution path color                             | `SOLUTION=40` *(black)*    |
| `DISPLAY_MODE`     | Rendering style (`thin` or `large` or `None`)   | `DISPLAY_MODE=thin`        |
| `DISPLAY_SOLUTION` | Overlay the shortest path on the maze           | `DISPLAY_SOLUTION=True`    |

---

## Algorithm

### Maze Generation — Iterative Backtracker (DFS)

The maze is generated using a depth-first search algorithm with backtracking, implemented iteratively using an explicit stack.

**How it works:**
1. Place the "42" pattern, as fully closed cells before generation, if possible
2. Start from the entry cell, mark it as visited and push it onto the stack
3. While the stack is not empty:
   - Look at the current cell's unvisited neighbors
   - If any exist: pick one at random, remove the wall between them, push the neighbor onto the stack
   - If none exist: backtrack by popping the stack
4. Repeat until all cells have been visited
5. For imperfect mazes: randomly remove additional walls, checking the no 3x3 open area constraint after each removal

**Why this algorithm:**
- Simple to understand and implement
- Produces long winding corridors and naturally guarantees a perfect maze
- Runs efficiently even on large grids
- Seed support makes generation fully reproducible

### Maze Solving — BFS (Breadth-First Search)

The shortest path between entry and exit is found using breadth-first search.

**How it works:**
1. Start from the entry cell
2. Explore all reachable neighbors level by level using a queue
3. Track the parent of each visited cell
4. When the exit is reached, reconstruct the path by following parents back to the start
5. Encode the path as cardinal directions: `N`, `E`, `S`, `W`

**Why BFS:**
- Always finds the shortest path in an unweighted graph
- Works on any maze structure, perfect or not

---

## Reusable Components

The maze generation logic is packaged as a standalone pip package called `mazegen`, installable independently of this project.

### Architecture

The package exposes two classes:

- `MazeGenerator` — abstract base class defining the interface. Any custom generator must inherit from it and implement `generate()` and `solve()`.
- `DepthFirstSearch` — concrete implementation using the DFS algorithm for generation and BFS for solving.

### Build from source

```bash
pip install build
python3 -m build
```

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage

```python
from mazegen import DepthFirstSearch

gen = DepthFirstSearch(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    perfect=True,
    seed=42
)
gen.generate()
```

### Access the maze structure

```python
# Raw grid — list[list[int]], accessed as grid[y][x]
grid = gen.grid.cells

# Hex representation — list[str]
hex_maze = gen.create_hexa_maze()
```

### Access the solution

```python
# List of (x, y) coordinates
path = gen.solver()

# Cardinal directions string (N, E, S, W)
cardinal = gen.find_cardinal_path(path)
```

### Custom parameters

| Parameter | Type             | Description       | Example   |
|-----------|------------------|-------------------|-----------|
| `width`   | `int`            | Number of columns | `20`      |
| `height`  | `int`            | Number of rows    | `15`      |
| `entry`   | `tuple[int,int]` | Entry coordinates | `(0, 0)`  |
| `exit`    | `tuple[int,int]` | Exit coordinates  | `(19,14)` |
| `perfect` | `bool`           | Perfect maze?     | `True`    |
| `seed`    | `int` or `None`  | Random seed       | `42`      |

### Create your own generator

```python
from mazegen import MazeGenerator

class MyGenerator(MazeGenerator):

    def generate(self) -> None:
        # implement your own algorithm here
        pass

    def solver(self) -> list[tuple[int, int]] | None:
        # implement your own solver here
        pass
```
---

## Team

### Roles

| Member       | Responsibilities                                                       |
|--------------|------------------------------------------------------------------------|
| **aslimani** | MazeGenerator, DepthFirstSearch, Grid structure, BFS             |
| **adamez-f** | Config parser, terminal display, user interactions                     |

### Planning

| Day   | Planned                          | Actual                                                     |
|-------|----------------------------------|------------------------------------------------------------|
| Day 1 | Grid base + interface definition | Done as planned                                            |
| Day 2 | DFS generator + ASCII display    | Done — display took longer than expected                   |
| Day 3 | BFS solver + output file         | Done — solver was straightforward once grid was solid      |
| Day 4 | Pattern 42 + no 3x3 constraint   | Done — constraint logic required extra debugging           |
| Day 5 | Assembly                         | Done — some integration issues resolved during this day    |
| Day 6 | Tests + packaging                | Done — linting took more time than anticipated             |

### What Worked Well

- **Separation of concerns:** splitting the grid, generator, solver, and display into distinct modules made integration and debugging easier.
- **Abstract class design:** using `MazeGenerator` as an abstract base class made the architecture clean and extensible.
- **Seed support:** being able to reproduce the same maze at any point was very helpful for testing.
- **BFS solver:** once the grid structure was stable, the solver was fast to implement and produced correct results immediately.

### What Could Be Improved
- **Structural problem:** We had to refactor both parsing, maze generation and color display.
- **Display portability:** ANSI color rendering is terminal-dependent and may not render correctly on all environments.

### Tools Used

| Tool          | Usage                              |
|---------------|------------------------------------|
| **Git**       | Version control and collaboration  |
| **Make**      | Build automation                   |
| **flake8**    | Code style enforcement             |
| **mypy**      | Static type checking               |
| **pip/build** | Python packaging                   |

---

## Resources

### Maze Generation

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Labyrinthes — Blaise Pascal](https://info.blaisepascal.fr/nsi-labyrinthes/)
- [Parcours en profondeur — Lyon 1](https://math.univ-lyon1.fr/irem/Formation_ISN/formation_parcours_graphes/profondeur/3_python2.html)
- [Génération de labyrinthes — Johan Segura](https://www.johan-segura.fr/mathsoup.xyz/content/Informatique/Fiche%20d'activit%C3%A9%204%20-%20g%C3%A9n%C3%A9ration-labyrinthe/g%C3%A9n%C3%A9ration-labyrinthes%20-%20%C3%A9l%C3%A8ves.html)
- [Think Labyrinth — Walter D. Pullen](http://www.astrolog.org/labyrnth/algrithm.htm)
- [Maze algorithms — Jamis Buck](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)

### Maze Solving (BFS)

- [Parcours en largeur — Lyon 1](https://math.univ-lyon1.fr/irem/Formation_ISN/formation_parcours_graphes/largeur/3_python1.html)
- [Parcours de graphes en Python — Marc Area](https://marcarea.com/weblog/2019/02/17/parcours-de-graphes-en-python)
- [BFS — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)

### Terminal Colors

- [ANSI escape codes — Stack Overflow](https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux)

### AI Usage

All generated content was reviewed, tested and fully understood before use. No functional code was copied directly from AI output.
*This project has been created as part of the 42 curriculum by [aslimani](https://github.com/devamine-42), [adamez-f](https://github.com/Nop-o).*

# 🌀 A-Maze-ing

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

This project was designed to be modular: the generator, the solver, the display, and the configuration parser are independent components that can be reused separately.

---

## Instructions

### Prerequisites

- Python 3.x
- `make`
- `pip`

### Installation

```bash
make install
```

### Running the project

```bash
make run
```

### Other commands

| Command      | Description                     |
|--------------|---------------------------------|
| `make run`   | Generate and display the maze   |
| `make debug` | Run with debug output           |
| `make lint`  | Run the linter                  |

---

## Configuration

The configuration file uses a simple `KEY=VALUE` format. Lines starting with `#` are treated as comments.

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

| Key           | Type      | Description                          | Example              |
|---------------|-----------|--------------------------------------|----------------------|
| `WIDTH`       | `int`     | Number of columns                    | `WIDTH=20`           |
| `HEIGHT`      | `int`     | Number of rows                       | `HEIGHT=15`          |
| `ENTRY`       | `x,y`     | Entry cell coordinates               | `ENTRY=0,0`          |
| `EXIT`        | `x,y`     | Exit cell coordinates                | `EXIT=19,14`         |
| `OUTPUT_FILE` | `string`  | Name of the export file              | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | `bool`    | Generate a perfect maze (no loops)   | `PERFECT=True`       |
| `SEED`        | `int`     | Random seed for reproducibility      | `SEED=42`            |

### Display & Color Settings

Colors are specified as ANSI escape code values. The format used internally is:

```
\033[{style};{text_color};{bg_color}m
```

For example: `\033[1;30;47m` → Bold, dark text, white background.

| Key                | Type     | Description                              | Example                     |
|--------------------|----------|------------------------------------------|-----------------------------|
| `STYLE`            | `string` | Text style (0–9)                         | `STYLE='1'` *(Bold)*        |
| `TUNNEL`           | `string` | Tunnel (passage) color                   | `TUNNEL='36'` *(Cyan)*      |
| `WALL`             | `string` | Wall background color                    | `WALL='44'` *(Blue bg)*     |
| `ENTRY`            | `string` | Entry cell color                         | `ENTRY='41'` *(Red bg)*     |
| `EXIT`             | `string` | Exit cell color                          | `EXIT='42'` *(Green bg)*    |
| `LOGO`             | `string` | Logo color                               | `LOGO='45'` *(Magenta bg)*  |
| `SOLUTION`         | `string` | Solution path color                      | `SOLUTION='40'` *(Black bg)*|
| `DISPLAY_MODE`     | `string` | Rendering style (`thin` or other)        | `DISPLAY_MODE='thin'`       |
| `DISPLAY_SOLUTION` | `bool`   | Overlay the shortest path on the maze    | `DISPLAY_SOLUTION=True`     |

---

## Algorithm

### Maze Generation — Iterative Backtracker (DFS)

The maze is generated using a **depth-first search** algorithm with backtracking, implemented iteratively using an explicit stack.

**How it works:**
1. Start from the entry cell and mark it as visited
2. Push it onto the stack
3. While the stack is not empty:
   - Look at the current cell's unvisited neighbors
   - If any exist: pick one at random, remove the wall between them, push the neighbor onto the stack, mark it as visited
   - If none exist: backtrack (pop the stack)
4. Repeat until all cells have been visited

**Why this algorithm?**
- **Simplicity:** the logic is easy to understand and implement
- **Quality:** it produces long, winding corridors and naturally guarantees a perfect maze
- **Performance:** it runs efficiently even on large grids
- **Controllability:** adding a seed makes the generation fully reproducible, which is useful for debugging and sharing mazes

For **imperfect** mazes, additional walls are randomly removed after the DFS pass to create loops and multiple paths.

---

### Maze Solving — BFS (Breadth-First Search)

The shortest path between entry and exit is found using **breadth-first search**.

**How it works:**
1. Start from the entry cell
2. Explore all reachable neighbors level by level using a queue
3. Track the parent of each visited cell
4. When the exit is reached, reconstruct the path by following parents back to the start
5. Encode the path as cardinal directions: `N`, `E`, `S`, `W`

**Why BFS?**
- It always finds the **shortest path** in an unweighted graph
- Simple to implement and easy to verify
- Works on any maze structure, perfect or not

---

## Reusable Components



## Team

### Roles

| Member        | Responsibilities                                              |
|---------------|---------------------------------------------------------------|
| **aslimani**  | `MazeGenerator`, `Grid` structure, DFS algorithm, BFS solver |
| **adamez-f**  | Config parser, terminal display, user interactions           |

### Planning

| Day   | Planned                                    | Actual                                                      |
|-------|--------------------------------------------|-------------------------------------------------------------|
| Day 1 | Grid base + interface definition           | ✅ Done as planned                                           |
| Day 2 | DFS generator + ASCII display              | ✅ Done — display took longer than expected                  |
| Day 3 | BFS solver + output file                   | ✅ Done — solver was straightforward once the grid was solid |
| Day 4 | Pattern 42 + no 3×3 constraint             | ✅ Done — constraint logic required extra debugging          |
| Day 5 | Assembly                                   | ✅ Done — some integration issues resolved during this day   |
| Day 6 | Tests + packaging                          | ✅ Done — linting took more time than anticipated            |

### What Worked Well

- **Separation of concerns:** splitting the grid, generator, solver, and display into distinct modules made integration straightforward and debugging easier.
- **Seed support:** being able to reproduce the same maze at any point was very helpful for testing and comparing outputs.
- **BFS solver:** once the grid structure was stable, implementing the solver was fast and produced correct results immediately.

### What Could Be Improved

- **Testing:** unit tests were written at the end of the project. Writing them earlier would have caught integration bugs sooner.
- **Config validation:** the config parser currently has minimal error handling. Invalid values can cause cryptic errors.
- **Display portability:** the ANSI color rendering is terminal-dependent and may not render correctly in all environments (e.g., Windows without ANSI support).

### Tools Used

| Tool          | Usage                                           |
|---------------|-------------------------------------------------|
| **Git**       | Version control and collaboration               |
| **Make**      | Build automation (install, run, lint)           |
| **pylint**    | Code linting and style enforcement              |
| **pip/build** | Python packaging                                |

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

AI tools (Claude) were used in the following ways during this project:

| Task                             | Part of the project concerned |
|----------------------------------|-------------------------------|
| README drafting & formatting     | Documentation                 |
| Proofreading and section writing | Documentation                 |

AI was **not** used to write any functional code. All algorithms, data structures, and logic were implemented by the team.
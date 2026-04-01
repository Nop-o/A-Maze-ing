*This project has been created as part of the 42 curriculum by aslimani and adamez-f*

## Description
A-Maze-ing is a maze generator written in Python 3.
It generates perfect or imperfect mazes from a configuration file,
displays them in the terminal, and exports them in hexadecimal format.


## Instructions

### Installation
```bash
make install
```
### Run
```bash
make run
```
### Debug
```bash
make debug
```
### Lint
```bash
make lint
```

## Configuration

The configuration file uses KEY=VALUE format. Lines starting with # are comments.

| Key         | Description              | Example             |
|-------------|--------------------------|---------------------|
| WIDTH       | Maze width (cells)       | WIDTH=20            |
| HEIGHT      | Maze height (cells)      | HEIGHT=15           |
| ENTRY       | Entry coordinates (x,y)  | ENTRY=0,0           |
| EXIT        | Exit coordinates (x,y)   | EXIT=19,14          |
| OUTPUT_FILE | Output filename          | OUTPUT_FILE=maze.txt|
| PERFECT     | Perfect maze ?           | PERFECT=True        |
| SEED        | Random seed              | SEED=42             |


## Algorithm

### Maze generation : Iterative Backtracker (DFS)

The maze is generated using a depth-first search algorithm with backtracking.

**How it works :**
1. Start from the entry cell
2. Pick a random unvisited neighbor
3. Remove the wall between current cell and neighbor
4. Move to the neighbor
5. If no unvisited neighbors → backtrack
6. Repeat until all cells are visited

**Why this algorithm :**
- Simple to implement
- Generates long winding corridors
- Naturally produces perfect mazes
- Fast on large grids

### Maze solving : BFS (Breadth-First Search)

The shortest path between entry and exit is found using a breadth-first search.

**How it works :**
1. Start from the entry cell
2. Explore all neighbors level by level
3. Track the parent of each visited cell
4. When the exit is reached, reconstruct the path by going back through parents
5. Encode the path as cardinal directions (N, E, S, W)

**Why this algorithm :**
- Always finds the shortest path
- Simple to implement
- Works on any valid maze, perfect or not


## Reusable module

The maze generation logic is packaged as a standalone pip package called `mazegen`.
It can be installed and used independently of this project.

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
    exit_=(19, 14),
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
path = gen.solver_bfs()

# Cardinal directions string (N, E, S, W)
cardinal = gen.find_cardinal_path(path)
```

### Custom parameters
| Parameter | Type | Description | Example |
|---|---|---|---|
| width | int | Number of columns | 20 |
| height | int | Number of rows | 15 |
| entry | tuple[int, int] | Entry coordinates | (0, 0) |
| exit_ | tuple[int, int] | Exit coordinates | (19, 14) |
| perfect | bool | Perfect maze ? | True |
| seed | int or None | Random seed | 42 |

### Build the package
```bash
pip install build
python3 -m build
```

## Team

### Roles
- **aslimani** : MazeGenerator, Grid, DFS algorithm, BFS solver
- **adamez-f** : Config parser, terminal display, interactions

### Planning
- Day 1 : Grid base + interface definition
- Day 2 : DFS generator + ASCII display
- Day 3 : BFS solver + output file
- Day 4 : Pattern 42 + no 3x3 constraint
- Day 5 : Assembly
- Day 6:  Tests + packaging

## Resources

#### Maze generation
- [Maze generation algorithms - Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Labyrinthes - Blaise Pascal](https://info.blaisepascal.fr/nsi-labyrinthes/)
- [Parcours en profondeur - Lyon 1](https://math.univ-lyon1.fr/irem/Formation_ISN/formation_parcours_graphes/profondeur/3_python2.html)
- [Génération de labyrinthes - Johan Segura](https://www.johan-segura.fr/mathsoup.xyz/content/Informatique/Fiche%20d'activit%C3%A9%204%20-%20g%C3%A9n%C3%A9ration-labyrinthe/g%C3%A9n%C3%A9ration-labyrinthes%20-%20%C3%A9l%C3%A8ves.html)
- [Think Labyrinth - Walter D. Pullen](http://www.astrolog.org/labyrnth/algrithm.htm)
- [Maze algorithms - Jamis Buck](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)

#### Maze solving (BFS)
- [Parcours en largeur - Lyon 1](https://math.univ-lyon1.fr/irem/Formation_ISN/formation_parcours_graphes/largeur/3_python1.html)
- [Parcours de graphes en Python - Marc Area](https://marcarea.com/weblog/2019/02/17/parcours-de-graphes-en-python)
- [BFS - Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)


### Terminal color 
[How to change the output color](https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux)

text coloring: 
début de séquence  : \033[
fin de séquence    : \033[0m 	(le 0 remet tous les settings à jour
milieu de séquence : 1;32;40m 	
	- 1er élément  : style d'écriture (0-9)
	- 2ème élément : text color (30-47 et 90-97(Bright))
	- 3ème élément : background color (40-47 et 100-107(Birght))

exemple : print("\033[1;30;47mBright Green\033[0m")
!

### AI usage
AI tools were used exclusively to assist with README documentation and formatting.
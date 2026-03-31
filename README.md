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

### Choice : Iterative Backtracker (DFS)

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



## Team

### Roles
- **aslimani** : MazeGenerator, Grid, DFS algorithm, BFS solver
- **adamez-f** : Config parser, terminal display, interactions

### Planning
- Day 1 : Grid base + interface definition
- Day 2 : DFS generator + ASCII display
- Day 3 : BFS solver + output file
- Day 4 : Pattern 42 + no 3x3 constraint
- Day 5 : Assembly + tests + packaging

## Resources

### Maze generation
- Maze generation algorithms:
https://en.wikipedia.org/wiki/Maze_generation_algorithm
https://info.blaisepascal.fr/nsi-labyrinthes/
https://math.univ-lyon1.fr/irem/Formation_ISN/formation_parcours_graphes/profondeur/3_python2.html
https://www.johan-segura.fr/mathsoup.xyz/content/Informatique/Fiche%20d'activit%C3%A9%204%20-%20g%C3%A9n%C3%A9ration-labyrinthe/g%C3%A9n%C3%A9ration-labyrinthes%20-%20%C3%A9l%C3%A8ves.html

- Maze generation solver (BFS): 
https://math.univ-lyon1.fr/irem/Formation_ISN/formation_parcours_graphes/largeur/3_python1.html
https://marcarea.com/weblog/2019/02/17/parcours-de-graphes-en-python

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
![alt text](image.png)

### AI usage
AI tools were used exclusively to assist with README documentation and formatting.
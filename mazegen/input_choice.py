from a_maze_ing import a_maze_ing
import sys
from mazegen.maze_algo.maze_generator import MazeGenerator
from mazegen.maze_display.ascii_rendering import ASCIIRendering
import os


def turn_on_off(switch: bool) -> bool:
    if switch is True:
        return False
    return True


def set_index(actual_index: int) -> int:
    if actual_index < 4:
        return actual_index + 1
    return 0


def input_choices(maze: MazeGenerator,
                  maze_color: ASCIIRendering,
                  hexa_maze: list[str],
                  maze_solution: list[tuple[int, int]],
                  index: int) -> None:
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze colors")
    print("4. Quit")
    print(f"maze is safe : {not maze.verif_3x3_end()}")

    interface = input("Choice? (1-4)")
    os.system("clear")
    if interface == '1':
        a_maze_ing('input.txt')

    elif interface == '2':
        maze_color.display_solution = turn_on_off(maze_color.display_solution)
        maze_color.display_maze(maze, hexa_maze, maze_solution)
        input_choices(maze, maze_color, hexa_maze, maze_solution, index)

    elif interface == '3':
        index = set_index(index)
        maze_color_set = ASCIIRendering.get_maze_color_set()
        maze_color_set[index].display_maze(maze, hexa_maze, maze_solution)
        input_choices(maze, maze_color_set[index], hexa_maze,
                      maze_solution, index)

    elif interface == '4':
        sys.exit()

    else:
        maze_color.display_maze(maze, hexa_maze, maze_solution)
        input_choices(maze, maze_color, hexa_maze, maze_solution, index)

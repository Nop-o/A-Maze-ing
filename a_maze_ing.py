from maze_generator import MazeGenerator
from parsing.parsing_file import parse_input_file
import sys
from image_rendering import MazeDisplay


def a_maze_ing(file_name: str) -> None:
    maze_setting = parse_input_file(file_name)
    if not maze_setting:
        return
    try:
        maze = MazeGenerator(maze_setting.width,
                             maze_setting.height,
                             (maze_setting.entry_x, maze_setting.entry_x),
                             (maze_setting.exit_x, maze_setting.exit_x),
                             perfect=maze_setting.is_perfect,
                             seed=maze_setting.seed)
    except ValueError as e:
        print(e)

    maze.generate_maze_dfs()
    hexa_maze = maze.create_hexa_maze()
    perfect_maze_path = maze.solver_bfs()
    try:
        cardinal_path = maze.find_cardinal_path(perfect_maze_path)
    except ValueError as e:
        print(e)
    else:
        maze.print_maze_to_file(maze_setting.output_filename,
                                hexa_maze, cardinal_path)
    print(maze.solver_bfs())

    MazeDisplay.display_maze_from_hexa2(hexa_maze)
    print("\n\n")
    MazeDisplay.display_maze_from_hexa(hexa_maze)
    maze.grid.display()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(-1)
    a_maze_ing(sys.argv[1])

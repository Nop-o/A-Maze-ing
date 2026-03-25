from maze_generator import MazeGenerator
from parsing.parsing_file import parse_input_file
from os import sys
from image_rendering import display_maze_from_hexa, display_maze_from_hexa2

def a_maze_ing(file_name: str) -> None:
    maze_setting = parse_input_file(file_name)
    if not maze_setting:
        return
    maze = MazeGenerator(maze_setting.width,
                         maze_setting.height,
                         (maze_setting.entry_x, maze_setting.entry_x),
                         (maze_setting.exit_x, maze_setting.exit_x),
                         perfect=maze_setting.is_perfect,
                         seed=maze_setting.seed)
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

    palette = {'0': ("    ", "    "),
               '1': ("▀▀▀▀", "    "),
               '2': ("   █", "   █"),
               '3': ("▀▀▀█", "   █"),
               '4': ("    ", "▄▄▄▄"),
               '5': ("▀▀▀▀", "▄▄▄▄"),
               '6': ("   █", "▄▄▄█"),
               '7': ("▀▀▀█", "▄▄▄█"),
               '8': ("█   ", "█   "),
               '9': ("█▀▀▀", "█   "),
               'A': ("█  █", "█  █"),
               'B': ("█▀▀█", "█  █"),
               'C': ("█   ", "█▄▄▄"),
               'D': ("█▀▀▀", "█▄▄▄"),
               'E': ("█  █", "█▄▄█"),
               'F': ("█▀▀█", "█▄▄█"),
               }

    small_palette = {'empty': ("    ", "    "),
                     'top_only': ("▀▀▀▀", "    "),
                     'left_only': ("█   ", "█   "),
                     'both': ("█▀▀▀", "█   "),
                     }

    display_maze_from_hexa2(hexa_maze, small_palette)
    print("\n\n")
    display_maze_from_hexa(hexa_maze, palette)
    maze.grid.display()


if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     sys.exit(-1)
    a_maze_ing("input.txt")
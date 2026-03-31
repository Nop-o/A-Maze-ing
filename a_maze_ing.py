from parsing.parsing_file import parse_input_file
from error_message import possible_file_input_error_message
from algo_dfs import DepthFirstSearch
from ascii_rendering import ASCIIRendering
import sys


def a_maze_ing(file_name: str) -> None:
    from input_choice import input_choices
    try:
        maze_setting, maze_color = parse_input_file(file_name)
    except ValueError as e:
        print(e)
        return

    try:
        maze = DepthFirstSearch(width=maze_setting.width,
                                height=maze_setting.height,
                                entry=(maze_setting.entry_x,
                                       maze_setting.entry_y),
                                exit=(maze_setting.exit_x,
                                      maze_setting.exit_y),
                                perfect=maze_setting.is_perfect,
                                seed=maze_setting.seed,
                                algorithm=maze_setting.algorithm,
                                display_mode=maze_setting.display_mode,
                                display_solution=maze_setting.display_solution)
        maze_color = ASCIIRendering(style=maze_color.style,
                                    wall=maze_color.wall,
                                    tunnel=maze_color.tunnel,
                                    entry=maze_color.entry,
                                    exit=maze_color.exit,
                                    logo=maze_color.logo,
                                    solution=maze_color.solution,)
    except Exception as e:
        print(e)
        return

    maze.generate()
    hexa_maze = maze.create_hexa_maze()
    perfect_maze_path = maze.solver()
    try:
        cardinal_path = maze.find_cardinal_path(perfect_maze_path)
    except ValueError as e:
        print(e)
        return
    maze.print_maze_to_file(maze_setting.output_filename,
                            hexa_maze, cardinal_path)
    solution = maze.solver()
    maze_color.display_maze(maze, hexa_maze, solution)
    print("\n\n")
    input_choices(maze, maze_color, hexa_maze, solution, 0)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("You can't have more than 1 argument.\n")
        possible_file_input_error_message()
        sys.exit(-1)

    if len(sys.argv) == 1:
        print("You can't have no argument.")
        possible_file_input_error_message()
        sys.exit(-1)

    a_maze_ing(sys.argv[1])

from algo_dfs import DepthFirstSearch
from parsing.parsing_file import parse_input_file
import sys
from ascii_rendering import ASCIIRendering


def a_maze_ing(file_name: str) -> None:
    maze_setting = parse_input_file(file_name)
    if not maze_setting:
        return
    try:
        dfs = DepthFirstSearch(maze_setting.width,
                               maze_setting.height,
                               (maze_setting.entry_x, maze_setting.entry_x),
                               (maze_setting.exit_x, maze_setting.exit_x),
                               perfect=maze_setting.is_perfect,
                               seed=maze_setting.seed)
    except ValueError as e:
        print(e)

    dfs.generate()
    hexa_maze = dfs.create_hexa_maze()
    perfect_maze_path = dfs.solver()
    try:
        cardinal_path = dfs.find_cardinal_path(perfect_maze_path)
    except ValueError as e:
        print(e)
    else:
        dfs.print_maze_to_file(maze_setting.output_filename,
                               hexa_maze, cardinal_path)
    print(dfs.solver())

    ASCIIRendering.display_large_maze(hexa_maze)
    print("\n\n")
    ASCIIRendering.display_thin_maze(hexa_maze)
    dfs.grid.display()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(-1)
    a_maze_ing(sys.argv[1])

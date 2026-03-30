from parsing.parsing_file import parse_input_file
from algo_dfs import DepthFirstSearch
import sys
from ascii_rendering import ASCIIRendering


def a_maze_ing(file_name: str) -> None:

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
                                seed=maze_setting.seed,)
        maze_color = ASCIIRendering(style=maze_color.style,
                                    tunnel=maze_color.tunnel,
                                    wall=maze_color.wall,
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
    print(maze.solver())

    maze_color.display_large_maze(maze, hexa_maze)
    print("\n\n")
    maze_color.display_thin_maze(maze, hexa_maze)

    print("""
1. Re-generate a new maze
2. Show/Hide path from entry to exit
3. Rotate maze colors
4. Quit """)

    interface = input("Choice? (1-4)")
    if interface == '1':
        a_maze_ing('input.txt')
    elif interface == '2':
        pass
    elif interface == '3':
        pass
    elif interface == '4':
        sys.exit()
    else:
        print("Error out of range")
        sys.exit()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("bye")
        sys.exit(-1)
    a_maze_ing(sys.argv[1])

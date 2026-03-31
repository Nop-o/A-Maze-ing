from algo_dfs import DepthFirstSearch
from maze_generator import MazeGenerator
from coloring_text import ColoringText, Style, Text, Background
from color import Color


class ASCIIRendering(Color):

    large_palette = {'0': ("    ", "    "),
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
                     'corner': ("▀   ", "    "),
                     }

    thin_palette = {'0': ("    ", "    "),
                    '1': ("▀▀▀▀", "    "),
                    '2': ("    ", "    "),
                    '3': ("▀▀▀▀", "    "),
                    '4': ("    ", "    "),
                    '5': ("▀▀▀▀", "    "),
                    '6': ("    ", "    "),
                    '7': ("▀▀▀▀", "    "),
                    '8': ("█   ", "█   "),
                    '9': ("█▀▀▀", "█   "),
                    'A': ("█   ", "█   "),
                    'B': ("█▀▀▀", "█   "),
                    'C': ("█   ", "█   "),
                    'D': ("█▀▀▀", "█   "),
                    'E': ("█   ", "█   "),
                    'F': ("█▀▀▀", "█   "),
                    'corner': ("▀   ", "    "),
                    }

    def __init__(self,
                 style: Style,
                 wall: Text,
                 tunnel: Background,
                 entry: Background,
                 exit: Background,
                 logo: Background,
                 solution: Background) -> None:
        super().__init__(style, wall, tunnel, entry, exit, logo, solution)

    def display_maze(self,
                     maze: MazeGenerator,
                     hexa_maze: list[str],
                     maze_solution: list[tuple[int, int]]) -> None:

        if maze.display_mode == "thin":
            palette = ASCIIRendering.thin_palette
        else:
            palette = ASCIIRendering.large_palette

        for y, line in enumerate(hexa_maze):
            second_row: list[str] = []

            for x, column in enumerate(line):
                func = self.get_cell_color()
                cell_first_row, cell_second_row = func(maze,
                                                       hexa_maze,
                                                       (x, y),
                                                       column,
                                                       palette,
                                                       maze_solution)
                print(cell_first_row, end="")
                second_row.append(cell_second_row)
            self.display_second_row(second_row)
        self.display_maze_bottom_row(hexa_maze)

    def get_cell_color(self, maze: MazeGenerator, hexa_maze: list[str],
                       position: tuple[int, int], key: str,
                       palette: dict[str, tuple[str, str]],
                       maze_solution: list[tuple[int, int]]
                       ) -> tuple[str, str]:
        x, y = position

        if (x, y) in maze.logo:
            colored_logo = self.create_colored_palette(palette, self.logo)
            return colored_logo[key]
        elif (x, y) == maze.entry:
            colored_entry = self.create_colored_palette(palette, self.entry)
            return colored_entry[key]
        elif (x, y) == maze.exit:
            colored_exit = self.create_colored_palette(palette, self.exit)
            return colored_exit[key]
        elif maze.display_solution and (x, y) in maze_solution:
            colored_solution = self.create_colored_palette(palette,
                                                           self.solution)
            return colored_solution[key]
        elif key in ("0", "2", "4", "6"):
            if ASCIIRendering.is_there_a_corner(hexa_maze, x, x - 1, y, y - 1):
                colored_corner = self.create_colored_palette(palette,
                                                             self.tunnel)
                return colored_corner["corner"]

        colored_palette = self.create_colored_palette(palette, self.tunnel)
        return colored_palette[key]

    def create_colored_palette(
            self,
            palette: dict[str, tuple[str, str]],
            background: Background) -> dict[str, tuple[str, str]]:

        colored_palette: dict[str, tuple[str, str]] = {}
        for key, value in palette.items():
            first_line, second_line = value
            colored_line_1 = ColoringText(first_line, self.style,
                                          self.wall, background)
            colored_line_2 = ColoringText(second_line, self.style,
                                          self.wall, background)
            colored_palette[key] = (colored_line_1.colored_text,
                                    colored_line_2.colored_text)

        return colored_palette

    def display_second_row(self, second_row: list[ColoringText]) -> None:
        colored_wall = ColoringText("█", self.style, self.wall, self.tunnel)

        print(colored_wall.colored_text)
        print("".join(second_row), end="")
        print(colored_wall.colored_text)

    def display_maze_bottom_row(self, hexa_maze: list[str]) -> None:
        colored_roof = ColoringText("▀", self.style, self.wall,
                                    Background.BLACK)

        for y in range(len(hexa_maze[0])):
            for x in range(4):
                print(colored_roof.colored_text, end="")
        print(colored_roof.colored_text)

    @staticmethod
    def is_there_a_corner(hexa_maze: list[str],
                          x: int, previous_x:
                          int, y: int, previous_y: int) -> bool:
        if x > 0:
            if (hexa_maze[y][previous_x] in ("1", "3", "5", "7",
                                             "9", "B", "D", "F")):
                return True
        if y > 0:
            if (hexa_maze[previous_y][x] in ("8", "9", "A", "B",
                                             "D", "E", "F")):
                return True
        return False

    @staticmethod
    def get_maze_color_set() -> list['ASCIIRendering']:
        set1 = ASCIIRendering(style=Style.BOLD, wall=Text.WHITE,
                              tunnel=Background.BLACK, logo=Background.RED,
                              entry=Background.GREEN, exit=Background.BLUE,
                              solution=Background.CYAN)
        set2 = ASCIIRendering(style=Style.BOLD, wall=Text.YELLOW,
                              tunnel=Background.WHITE, logo=Background.GREEN,
                              entry=Background.RED, exit=Background.MAGENTA,
                              solution=Background.BLACK)
        set3 = ASCIIRendering(style=Style.BOLD, wall=Text.GREEN,
                              tunnel=Background.RED, logo=Background.BLUE,
                              entry=Background.WHITE, exit=Background.BLACK,
                              solution=Background.MAGENTA)
        set4 = ASCIIRendering(style=Style.BOLD, wall=Text.GREEN,
                              tunnel=Background.BLACK, logo=Background.MAGENTA,
                              entry=Background.RED, exit=Background.WHITE,
                              solution=Background.BLUE)
        set5 = ASCIIRendering(style=Style.BOLD, wall=Text.BLACK,
                              tunnel=Background.YELLOW, logo=Background.WHITE,
                              entry=Background.MAGENTA, exit=Background.RED,
                              solution=Background.GREEN)
        return [set1, set2, set3, set4, set5]


if __name__ == "__main__":
    try:
        mg = DepthFirstSearch(25, 25, (0, 0), (20, 20), perfect=True, seed=42,
                              algorithm="dfs", display_mode="thin",
                              display_solution=True)
        ascii = ASCIIRendering(style=Style.STRIKETROUGH, wall=Text.WHITE,
                               tunnel=Background.BLACK, logo=Background.BLUE,
                               entry=Background.GREEN, exit=Background.RED,
                               solution=Background.MAGENTA)
    except ValueError as e:
        print(e)
    else:
        mg.generate()
        hexa_maze = mg.create_hexa_maze()
        solution = mg.solver()
        ascii.display_maze(mg, hexa_maze, solution)
        print("\n\n")
    # mg.grid.display()
    # print(hexa_maze)

from algo_dfs import DepthFirstSearch
from maze_generator import MazeGenerator
from coloring_text import ColoringText, Style, Text, Background
from color import Color


class ASCIIRendering(Color):
    char_list: dict[str, list[str]] = {
        "empty": ['0', '2', '4', '6'],
        "top_only": ['1', '3', '5', '7'],
        "left_only": ['8', 'A', 'C', 'E'],
        "both": ['9', 'B', 'D', 'F'],
        }

    def __init__(self,
                 style: Style,
                 tunnel: Text,
                 wall: Background,
                 entry: Background,
                 exit: Background,
                 logo: Background,
                 solution: Background) -> None:
        super().__init__(style, tunnel, wall, entry, exit, logo, solution)

    def display_large_maze(self,
                           maze: MazeGenerator,
                           hexa_maze: list[str]) -> None:
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

        colored_palette = self.create_colored_palette(palette, self.wall)
        colored_entry = self.create_colored_palette(palette, self.entry)
        colored_exit = self.create_colored_palette(palette, self.exit)
        colored_logo = self.create_colored_palette(palette, self.logo)

        for y, line_part_1 in enumerate(hexa_maze):
            line_part_2: list[str] = []
            for x in range(len(line_part_1)):
                if (x, y) in maze.logo:
                    print(colored_logo[line_part_1[x]][0], end="")
                    line_part_2.append(colored_logo[line_part_1[x]][1])
                elif (x, y) == maze.entry:
                    print(colored_entry[line_part_1[x]][0], end="")
                    line_part_2.append(colored_entry[line_part_1[x]][1])
                elif (x, y) == maze.exit:
                    print(colored_exit[line_part_1[x]][0], end="")
                    line_part_2.append(colored_exit[line_part_1[x]][1])
                else:
                    print(colored_palette[line_part_1[x]][0], end="")
                    line_part_2.append(colored_palette[line_part_1[x]][1])
            print()
            print("".join(line_part_2))

    def display_thin_maze(self,
                          maze: MazeGenerator,
                          hexa_maze: list[str]) -> None:

        palette = {'empty': ("    ", "    "),
                   'top_only': ("▀▀▀▀", "    "),
                   'left_only': ("█   ", "█   "),
                   'both': ("█▀▀▀", "█   "),
                   }
        colored_palette = self.create_colored_palette(palette, self.wall)
        colored_entry = self.create_colored_palette(palette, self.entry)
        colored_exit = self.create_colored_palette(palette, self.exit)
        colored_wall = ColoringText("█", self.style, self.tunnel, self.wall)
        colored_roof = ColoringText("▀", self.style, self.tunnel,
                                    Background.BLACK)
        colored_corner = ColoringText("▀   ", self.style, self.tunnel,
                                      self.wall)
        colored_void = ColoringText("    ", self.style, self.tunnel, self.wall)
        colored_logo_high = ColoringText("█▀▀▀", self.style, self.tunnel,
                                         self.logo)
        colored_logo_low = ColoringText("█   ", self.style, self.tunnel,
                                        self.logo)

        for y, line_part_1 in enumerate(hexa_maze, 0):
            line_part_2: list[str] = []

            for x in range(len(line_part_1)):
                for key, value in ASCIIRendering.char_list.items():
                    if line_part_1[x] in value:
                        if key == "empty":
                            if ASCIIRendering.is_there_a_corner(hexa_maze,
                                                                y, y - 1,
                                                                x, x - 1):
                                print(colored_corner.colored_text, end="")
                                line_part_2.append(colored_void.colored_text)
                                break
                        if self.is_there_a_hybrid_color_cell(maze, (x, y)):
                            mixed_color_cell_1, mixed_color_cell_2 = self.get_hybrid_color(maze, (x, y), (palette[key][0], palette[key][1]))
                            print(mixed_color_cell_1.colored_text, end="")
                            line_part_2.append(mixed_color_cell_2.colored_text)
                        elif (x, y) in maze.logo:
                            print(colored_logo_high.colored_text, end="")
                            line_part_2.append(colored_logo_low.colored_text)
                        elif (x, y) in maze.entry:
                            print(colored_entry[key][0], end="")
                            line_part_2.append(colored_entry[key][1])
                        elif (x, y) in maze.exit:
                            print(colored_exit[key][0], end="")
                            line_part_2.append(colored_exit[key][1])
                        else:
                            print(colored_palette[key][0], end="")
                            line_part_2.append(colored_palette[key][1])

            print(colored_wall.colored_text)
            print("".join(line_part_2), end="")
            print(colored_wall.colored_text)

        for y in range(len(hexa_maze[0])):
            for x in range(4):
                print(colored_roof.colored_text, end="")
        print(colored_roof.colored_text)
    
    def is_there_a_hybrid_color_cell(self, maze: MazeGenerator, cell: tuple[int, int]) -> bool:
        x, y = cell
        looking_for: list[tuple[int, int]] = maze.logo
        looking_for.append(maze.entry)
        looking_for.append(maze.exit)

        if (x, y) not in looking_for:
            if x > 0:
                if (x - 1, y) in looking_for:
                    return True
            if y > 0:
                if (x, y - 1) in looking_for:
                    return True
        return False
    
    def get_hybrid_color(self, maze: MazeGenerator, cell: tuple[int, int],
                         cell_palette: tuple[str, str],
                         ) -> tuple[ColoringText, ColoringText]:
        x, y = cell

        if y > 0 and (x, y - 1) in maze.entry:
            first_row = ColoringText(cell_palette[0], self.style,
                                      self.tunnel, self.entry)
        elif y > 0 and (x, y - 1) in maze.exit:
            first_row = ColoringText(cell_palette[0], self.style,
                                      self.tunnel, self.exit)
        elif y > 0 and (x, y - 1) in maze.logo:
            first_row = ColoringText(cell_palette[0], self.style,
                                      self.tunnel, self.logo)
        else:
            first_row = ColoringText(cell_palette[0], self.style,
                                      self.tunnel, self.wall)

        if x > 0 and (x - 1, y) in maze.entry:
            second_row = ColoringText(cell_palette[1], self.style,
                                      self.tunnel, self.entry)
        elif x > 0 and (x - 1, y) in maze.exit:
            second_row = ColoringText(cell_palette[1], self.style,
                                      self.tunnel, self.exit)
        elif x > 0 and (x - 1, y) in maze.logo:
            second_row = ColoringText(cell_palette[1], self.style,
                                      self.tunnel, self.logo)
        else:
            second_row = ColoringText(cell_palette[1], self.style,
                                      self.tunnel, self.wall)

        return (first_row, second_row)

    def create_colored_palette(
            self, 
            palette: dict[str, tuple[str, str]],
            background: Background) -> dict[str, tuple[str, str]]:

        colored_palette: dict[str, tuple[str, str]] = {}
        for key, value in palette.items():
            first_line, second_line = value
            colored_line_1 = ColoringText(first_line, self.style,
                                          self.tunnel, background)
            colored_line_2 = ColoringText(second_line, self.style,
                                          self.tunnel, background)
            colored_palette[key] = (colored_line_1.colored_text,
                                    colored_line_2.colored_text)

        return colored_palette

    @staticmethod
    def is_there_a_corner(hexa_maze: list[str],
                          x: int, previous_x:
                          int, y: int, previous_y: int) -> bool:
        if x > 0:
            if (hexa_maze[previous_x][y] in
                    ASCIIRendering.char_list["top_only"] or
                    hexa_maze[previous_x][y] in
                    ASCIIRendering.char_list["both"]):
                return True
        if y > 0:
            if (hexa_maze[x][previous_y] in
                    ASCIIRendering.char_list["left_only"] or
                    hexa_maze[x][previous_y] in
                    ASCIIRendering.char_list["both"]):
                return True
        return False

    @staticmethod
    def create_colored_palette(
            palette: dict[str, tuple[str, str]],
            style: Style,
            text: Text,
            background: Background) -> dict[str, tuple[str, str]]:

        colored_palette: dict[str, tuple[str, str]] = {}
        for key, value in palette.items():
            first_line, second_line = value
            colored_line_1 = ColoringText(first_line, style, text, background)
            colored_line_2 = ColoringText(second_line, style, text, background)
            colored_palette[key] = (colored_line_1.colored_text,
                                    colored_line_2.colored_text)

        return colored_palette


if __name__ == "__main__":
    try:
        mg = DepthFirstSearch(30, 30, (0, 0), (7, 5), perfect=True, seed=42)
        ascii = ASCIIRendering(style=Style.BOLD,
                               tunnel=Text.WHITE,
                               wall=Background.BLACK,
                               logo=Background.RED,
                               entry=Background.YELLOW,
                               exit=Background.GREEN,
                               solution=Background.CYAN)
    except ValueError as e:
        print(e)
   
    ascii.is_there_a_hybrid_color_cell(mg, (3, 3))
    # else:
    #     mg.generate()
    #     hexa_maze = mg.create_hexa_maze()
    #     ascii.display_large_maze(mg, hexa_maze)
    #     print("\n\n")
    #     ascii.display_thin_maze(mg, hexa_maze)
    # mg.grid.display()
    # print(hexa_maze)

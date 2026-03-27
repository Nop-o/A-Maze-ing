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

        colored_palette = ASCIIRendering.create_colored_palette(palette,
                                                                self.style,
                                                                self.tunnel,
                                                                self.wall)
        colored_entry = ASCIIRendering.create_colored_palette(palette,
                                                              self.style,
                                                              self.tunnel,
                                                              self.entry)
        colored_exit = ASCIIRendering.create_colored_palette(palette,
                                                             self.style,
                                                             self.tunnel,
                                                             self.exit)
        colored_logo = ASCIIRendering.create_colored_palette(palette,
                                                             self.style,
                                                             self.tunnel,
                                                             self.logo)
        for i, lign_part_1 in enumerate(hexa_maze):
            lign_part_2: list[str] = []
            for j in range(len(lign_part_1)):
                if (j, i) in maze.logo:
                    print(colored_logo[lign_part_1[j]][0], end="")
                    lign_part_2.append(colored_logo[lign_part_1[j]][1])
                elif (j, i) == maze.entry:
                    print(colored_entry[lign_part_1[j]][0], end="")
                    lign_part_2.append(colored_entry[lign_part_1[j]][1])
                elif (j, i) == maze.exit:
                    print(colored_exit[lign_part_1[j]][0], end="")
                    lign_part_2.append(colored_exit[lign_part_1[j]][1])
                else:
                    print(colored_palette[lign_part_1[j]][0], end="")
                    lign_part_2.append(colored_palette[lign_part_1[j]][1])
            print()
            print("".join(lign_part_2))

    def display_thin_maze(self,
                          maze: MazeGenerator,
                          hexa_maze: list[str]) -> None:

        palette = {'empty': ("    ", "    "),
                   'top_only': ("▀▀▀▀", "    "),
                   'left_only': ("█   ", "█   "),
                   'both': ("█▀▀▀", "█   "),
                   }
        colored_palette = ASCIIRendering.create_colored_palette(
                                                               palette,
                                                               self.style,
                                                               self.tunnel,
                                                               self.wall)
        colored_entry = ASCIIRendering.create_colored_palette(palette,
                                                              self.style,
                                                              self.tunnel,
                                                              self.entry)
        colored_exit = ASCIIRendering.create_colored_palette(palette,
                                                             self.style,
                                                             self.tunnel,
                                                             self.exit)
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

        for i, lign_part_1 in enumerate(hexa_maze, 0):
            lign_part_2: list[str] = []

            for j in range(len(lign_part_1)):
                for key, value in ASCIIRendering.char_list.items():
                    if lign_part_1[j] in value:
                        if key == "empty":
                            if ASCIIRendering.is_there_a_corner(hexa_maze,
                                                                i, i - 1,
                                                                j, j - 1):
                                print(colored_corner.colored_text, end="")
                                lign_part_2.append(colored_void.colored_text)
                                break
                        if (j, i) in maze.logo:
                            print(colored_logo_high.colored_text, end="")
                            lign_part_2.append(colored_logo_low.colored_text)
                        elif (j, i) == maze.entry:
                            print(colored_entry[key][0], end="")
                            lign_part_2.append(colored_entry[key][1])
                        elif (j, i) == maze.exit:
                            print(colored_exit[key][0], end="")
                            lign_part_2.append(colored_exit[key][1])
                        else:
                            print(colored_palette[key][0], end="")
                            lign_part_2.append(colored_palette[key][1])

            print(colored_wall.colored_text)
            print("".join(lign_part_2), end="")
            print(colored_wall.colored_text)

        for i in range(len(hexa_maze[0])):
            for j in range(4):
                print(colored_roof.colored_text, end="")
        print(colored_roof.colored_text)

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
            first_lign, second_lign = value
            colored_lign_1 = ColoringText(first_lign, style, text, background)
            colored_lign_2 = ColoringText(second_lign, style, text, background)
            colored_palette[key] = (colored_lign_1.colored_text,
                                    colored_lign_2.colored_text)

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
    else:
        mg.generate()
        hexa_maze = mg.create_hexa_maze()
        ascii.display_large_maze(mg, hexa_maze)
        print("\n\n")
        ascii.display_thin_maze(mg, hexa_maze)
    # mg.grid.display()
    # print(hexa_maze)

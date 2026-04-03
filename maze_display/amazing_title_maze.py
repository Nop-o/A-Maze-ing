from maze_display.coloring_text import (ColoringText, Style,
                                        Text, Background)
from mazegen.maze_algo.maze_generator import MazeGenerator


class AMazeIngTitle:

    hexa_title = [
        "000000000000000000000000000000000000000000000000000000000000",
        "006FFC000002FFC0006FF806FFC02FFFFAFFFF80002FAFFC002F806FFFC0",
        "06F93FC00002FBFC06FBF86F93FC2F93FAFFFF80002FAFBF802F86F913F8",
        "0F9003F80002F83FEF92FAF9003F8106FAFF5500002FAFAFC02FAFF80010",
        "0FC446F84442F803F902FAFC446F806F92FFFF84442FAF83F82FAF900440",
        "0FFFFFFAFFFAF8001002FAFFFFFF86F902FFFFAFFFAFAF82FC2FAFC02FF8",
        "0F9113F81112F8000002FAF9113FAF9042FF5501112FAF803FAFAFF803F8",
        "0F8002F80002F8000002FAF8002FAFC6FAFFFF80002FAF802FEF83FC46F8",
        "0F8002F80002F8000002FAF8002FAFFFFAFFFF80002FAF8003FF803FFFF8",
        "010000100000100000001010000101111011110000010100001100011110",
    ]

    def __init__(self,
                 style: Style,
                 wall: Text,
                 tunnel: Background) -> None:
        self.style = style
        self.wall = wall
        self.tunnel = tunnel

    def display_title(self, maze: MazeGenerator) -> None:
        from maze_display.ascii_rendering import ASCIIRendering

        palette = ASCIIRendering.thin_palette
        full_colored_palette = self.create_colored_palette(palette,
                                                           self.tunnel)
        half_colored_palette = self.create_colored_palette(palette,
                                                           Background.BLACK)

        for y in AMazeIngTitle.hexa_title:
            second_row: list[str] = []
            self.center_title(maze)
            for x in y:
                if x == 'F':
                    cell_first_row, cell_second_row = full_colored_palette[x]
                else:
                    cell_first_row, cell_second_row = half_colored_palette[x]
                print(cell_first_row, end="")
                second_row.append(cell_second_row)
            print()
            self.center_title(maze)
            print("".join(second_row))
        print("\n\n")

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

    @staticmethod
    def center_title(maze: MazeGenerator) -> None:
        empty_space_size = ((maze.width * 2) -
                            (len(AMazeIngTitle.hexa_title[0]) * 2))

        for i in range(empty_space_size):
            print(" ", end="")

from maze_display.coloring_text import Style, Text, Background


class Color:
    def __init__(self,
                 style: Style,
                 wall: Text,
                 tunnel: Background,
                 entry: Background,
                 exit: Background,
                 logo: Background,
                 solution: Background,
                 display_mode: str,
                 display_solution: bool) -> None:

        self.style = style
        self.tunnel = tunnel
        self.wall = wall
        self.entry = entry
        self.exit = exit
        self.logo = logo
        self.solution = solution
        self.display_mode = display_mode
        self.display_solution = display_solution

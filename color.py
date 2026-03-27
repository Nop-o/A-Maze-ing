from coloring_text import Style, Text, Background


class Color:
    def __init__(self,
                 style: Style,
                 tunnel: Text,
                 wall: Background,
                 entry: Background,
                 exit: Background,
                 logo: Background,
                 solution: Background) -> None:

        self.style = style
        self.tunnel = tunnel
        self.wall = wall
        self.entry = entry
        self.exit = exit
        self.logo = logo
        self.solution = solution

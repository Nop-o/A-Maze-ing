class Grid:
    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000

    OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
    DELTA = {NORTH: (0, -1), SOUTH: (0, 1), EAST: (1, 0), WEST: (-1, 0)}

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells: list[list[int]] = []
        self.create_grid()

    def create_grid(self) -> None:
        self.cells = []
        for y in range(self.height):  # for each line
            line: list[int] = []
            for x in range(self.width):  # for each column
                line.append(0xF)
            self.cells.append(line)  # grid[y][x]

    def remove_wall(self, x: int, y: int, direction: int) -> None:
        # direction to go towards the neighboring cell
        dx, dy = self.DELTA[direction]
        nx = x + dx
        ny = y + dy

        if not self.is_valid(nx, ny):
            return

        self.cells[y][x] &= ~direction  # breaks down the cell wall
        self.cells[ny][nx] &= ~self.OPPOSITE[direction]
        # breaks down the wall of the neighboring cell

    def add_wall(self, x: int, y: int, direction: int) -> None:
        dx, dy = self.DELTA[direction]
        nx = x + dx
        ny = y + dy

        if not self.is_valid(nx, ny):
            return

        self.cells[y][x] |= direction
        self.cells[ny][nx] |= self.OPPOSITE[direction]

    def is_valid(self, x: int, y: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def display(self) -> None:
        # function that tests the grid by displaying in ASCII
        print("+" + "---+" * self.width)  # top line

        for y in range(self.height):  # middle line
            row = "|"
            for x in range(self.width):
                row += "   "
                row += "|" if self.cells[y][x] & self.EAST else " "
            print(row)

            bot = "+"
            for x in range(self.width):  # bot line
                bot += "---+" if self.cells[y][x] & self.SOUTH else "   +"
            print(bot)


if __name__ == "__main__":  # main test
    g = Grid(5, 5)
    print(g.cells[0][0])
    print(g.cells[0][1])

    g.remove_wall(0, 0, Grid.EAST)
    g.remove_wall(0, 1, Grid.SOUTH)

    print(g.cells[0][0])
    print(g.cells[0][1])

    g.display()

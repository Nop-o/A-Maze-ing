import random
from grid import Grid
from collections import deque


class MazeGenerator:
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int] | None,
                 perfect: bool, seed: int | None) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.grid = Grid(width, height)
        if seed is not None:
            random.seed(seed)

    def generate_maze_dfs(self) -> None:
        stack = [self.entry]
        visited = {self.entry}

        while stack:
            current_cell = stack[-1]
            neighbors = self.get_unvisited_neighbors(current_cell, visited)
            if neighbors:
                direction = random.choice(neighbors)
                x, y = current_cell
                self.grid.remove_wall(x, y, direction)
                dx, dy = self.grid.DELTA[direction]
                nx, ny = x + dx, y + dy
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

    def get_unvisited_neighbors(self, cell: tuple[int, int],
                                visited: set[tuple[int, int]]) -> list[int]:
        g = self.grid
        x, y = cell
        neighbors = []

        for direction in [g.NORTH, g.SOUTH, g.EAST, g.WEST]:
            dx, dy = g.DELTA[direction]
            nx, ny = x + dx, y + dy
            if g.is_valid(nx, ny) and (nx, ny) not in visited:
                neighbors.append(direction)
        return neighbors

    def solver_bfs(self) -> list[tuple[int, int]] | None:
        parent: dict[tuple[int, int],
                     tuple[int, int] | None] = {self.entry: None}
        visited: set[tuple[int, int]] = {self.entry}
        file: deque[tuple[int, int]] = deque([self.entry])

        while file:
            current_cell: tuple[int, int] = file.popleft()
            if current_cell == self.exit:
                return self.get_path_way(parent)
            x, y = current_cell
            for neighbor in self.get_neighbors(x, y):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current_cell
                    file.append(neighbor)
        return None

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        g = self.grid
        neighbors = []

        for direction in [g.NORTH, g.SOUTH, g.EAST, g.WEST]:
            if not (g.cells[y][x] & direction):
                dx, dy = g.DELTA[direction]
                nx, ny = x + dx, y + dy
                if g.is_valid(nx, ny):
                    neighbors.append((nx, ny))
        return neighbors

    def get_path_way(self,
                     parent: dict[tuple[int, int],
                                  tuple[int, int]
                                  | None]) -> list[tuple[int, int]]:
        path = []
        current = self.exit

        while current:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path

    def create_hexa_maze(self) -> list[str]:
        hexa_maze: list[str] = []
        hexa = "0123456789ABCDEF"

        for ligns in self.grid.cells:
            new_lign: list[str] = []
            for cells in ligns:
                new_cell = hexa[cells]
                new_lign.append(new_cell)
            hexa_maze.append("".join(new_lign))

        return hexa_maze

    def print_maze_to_file(self, file_name: str, hexa_maze: list[str],
                           entry_to_exit_path: str) -> None:
        if self.exit is None:
            raise ValueError("Can't print the maze : there is no exit")

        x, y = self.entry
        x2, y2 = self.exit

        try:
            with open(file_name, "w") as file:
                file.write("\n".join(hexa_maze))
                file.write("\n\n")
                file.write(f"{x},{y}\n")
                file.write(f"{x2},{y2}\n")
                file.write(entry_to_exit_path + '\n')
        except OSError as e:
            print(e)

    def find_cardinal_path(self, path: list[tuple[int, int]] | None) -> str:
        if path is None:
            raise ValueError("Can't create a cardinal path : there is no path")

        if self.perfect is False:
            raise ValueError(
                "Can't create a cardinal path : the maze isn't perfect")

        cardinal_path: list[str] = []
        for cell, next_cell in zip(path, path[1:]):
            x, y = cell
            x2, y2 = next_cell
            if x > x2:
                cardinal_path.append('W')
            if x2 > x:
                cardinal_path.append('E')
            if y > y2:
                cardinal_path.append('N')
            if y2 > y:
                cardinal_path.append('S')

        return "".join(cardinal_path)


if __name__ == "__main__":
    mg = MazeGenerator(10, 10, (0, 0), (9, 9), perfect=True, seed=None)
    mg.generate_maze_dfs()
    hexa_maze = mg.create_hexa_maze()
    perfect_maze_path = mg.solver_bfs()
    try:
        cardinal_path = mg.find_cardinal_path(perfect_maze_path)
    except ValueError as e:
        print(e)
    else:
        mg.print_maze_to_file("file.txt", hexa_maze, cardinal_path)
    mg.grid.display()
    print(mg.solver_bfs())

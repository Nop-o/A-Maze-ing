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
        queue: deque[tuple[int, int]] = deque([self.entry])

        while queue:
            current_cell: tuple[int, int] = queue.popleft()
            if current_cell == self.exit:
                return self.get_path_way(parent)
            x, y = current_cell
            for neighbor in self.get_neighbors(x, y):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current_cell
                    queue.append(neighbor)
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

        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path

    def create_hexa_maze(self) -> list[list[str]]:
        hexa_maze: list[list[str]] = []
        hexa = "0123456789ABCDEF"

        for ligns in self.grid.cells:
            new_lign: list[str] = []
            for cells in ligns:
                new_cell = hexa[cells]
                new_lign.append(new_cell)
            hexa_maze.append(new_lign)

        return hexa_maze


if __name__ == "__main__":
    mg = MazeGenerator(15, 15, (0, 0), (9, 9), perfect=True, seed=None)
    mg.generate_maze_dfs()
    hexa_maze = mg.create_hexa_maze()
    print(hexa_maze)
    print("------------------------")
    # print(mg.grid.cells)
    # # mg.grid.display()
    # # print(mg.solver_bfs())

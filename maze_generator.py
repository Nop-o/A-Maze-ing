import random
from grid import Grid
from collections import deque


class MazeGenerator:
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int],
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
                                visited: set) -> list:
        g = self.grid
        x, y = cell
        neighbors = []

        for direction in [g.NORTH, g.SOUTH, g.EAST, g.WEST]:
            dx, dy = g.DELTA[direction]
            nx, ny = x + dx, y + dy
            if g.is_valid(nx, ny) and (nx, ny) not in visited:
                neighbors.append(direction)
        return neighbors

    def solver_bfs(self):
        parent = {self.entry: None}
        visited = {self.entry}
        queue = deque([self.entry])

        while queue:
            print("1")
            current_cell = queue.popleft()
            if current_cell == self.exit:
                return parent
            print("2")
            x, y = current_cell
            for neighbor in self.get_neighbors(x, y):
                print(self.get_neighbors(x, y))
                print("3")
                if neighbor not in visited:
                    print("5")
                    visited.add(neighbor)
                    parent[neighbor] = current_cell
                    queue.append(neighbor)
                    print("4")
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

    def get_path_way(parent: dict) -> dict:
        pass


if __name__ == "__main__":
    mg = MazeGenerator(10, 10, (0, 0), (9, 9), perfect=True, seed=None)
    mg.generate_maze_dfs()
    mg.grid.display()
    print(mg.solver_bfs())

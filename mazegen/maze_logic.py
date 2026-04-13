from .render_maze import PATTERN_42, RESET, Renderer
from collections import deque
import random


class Maze():
    """A maze structure with generation and pathfinding capabilities."""
    def __init__(self, config: dict):
        """Initialize the maze and load configuration values."""
        self.config: dict = config
        self.height: int
        self.width: int
        self.is_perfect: bool
        self.entry: tuple[int, int]
        self.exit: tuple[int, int]
        self._load_conf(config)
        self.path: list[tuple] = []
        self.maze = self.create_maze()

    def _load_conf(self, config: dict) -> list:
        """Load the maze configuration values from the parsed config dict."""
        self.height = config["HEIGHT"]
        self.width = config["WIDTH"]
        self.is_perfect = config["PERFECT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]

        return [
            self.height,
            self.width,
            self.is_perfect,
            self.entry,
            self.exit
            ]

    def create_maze(self) -> list:
        """Build the initial maze grid with walls and empty cells."""
        maze = []
        for i in range(self.height * 2 + 1):
            lst_temp: list[Cell] = []
            for j in range(self.width * 2 + 1):
                if i == self.entry[0] * 2 + 1 and j == self.entry[1] * 2 + 1:
                    lst_temp.append(Entry())
                elif i == self.exit[0] * 2 + 1 and j == self.exit[1] * 2 + 1:
                    lst_temp.append(Exit())
                else:
                    true_or_false = i % 2 == 0 or j % 2 == 0
                    lst_temp.append(Cell(true_or_false))
            maze.append(lst_temp)

        self.maze = maze

        if self.height >= 8 and self.width >= 8:
            if self.check_inject_42():
                self.inject_42()

        return maze

    def _get_unvisited_neighbors(self,
                                 current_y: int,
                                 current_x: int) -> list[tuple]:
        """Return unvisited neighbor cells two steps away for path carving."""
        unvisitied_neighbors = []
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]

        for dy, dx in directions:
            next_y, next_x = current_y + dy, current_x + dx
            if 0 <= next_x < self.width * 2 + 1 \
                    and 0 <= next_y < self.height * 2 + 1:
                neighbor = self.maze[next_y][next_x]
                if not neighbor.is_wall and not neighbor.is_visited:
                    unvisitied_neighbors.append((next_y, next_x))
        return unvisitied_neighbors

    def _break_wall(self, cell1: tuple[int, int],
                    cell2: tuple[int, int]) -> None:
        """Remove the wall between two adjacent path cells."""
        y_wall = (cell1[0] + cell2[0]) // 2
        x_wall = (cell1[1] + cell2[1]) // 2
        self.maze[y_wall][x_wall].is_wall = False

    def create_paths(self) -> None:
        """Generate paths through the maze using depth-first search."""
        stack = [(1, 1)]
        self.maze[1][1].is_visited = True
        while stack:
            current_y, current_x = stack[-1]
            neighbors = self._get_unvisited_neighbors(current_y, current_x)
            if neighbors:
                pos_y, pos_x = random.choice(neighbors)
                self._break_wall(stack[-1], (pos_y, pos_x))
                self.maze[pos_y][pos_x].is_visited = True
                stack.append((pos_y, pos_x))
            else:
                stack.pop()

    def check_inject_42(self) -> bool:
        """Return True if the 42 pattern can be injected into the maze."""
        pattern = PATTERN_42
        offset_y = (self.height - len(pattern)) // 2
        offset_x = (self.width - len(pattern[0])) // 2

        for py, row in enumerate(pattern):
            for px, char in enumerate(row):
                y = (offset_y + py) * 2 + 1
                x = (offset_x + px) * 2 + 1
                cell = self.maze[y][x]

                if char == "X" and (cell.entry_point or cell.exit_point):
                    return False

        return True

    def inject_42(self) -> None:
        """Embed the 42 pattern into the maze grid when possible."""
        if self.height < 5 or self.width < 5:
            print("Maze too small to show 42")
            return
        pattern = PATTERN_42
        offset_y = (self.height - len(pattern)) // 2
        offset_x = (self.width - len(pattern[0])) // 2

        for py, row in enumerate(pattern):
            for px, char in enumerate(row):
                y = (offset_y + py) * 2 + 1
                x = (offset_x + px) * 2 + 1
                cell = self.maze[y][x]
                if char == "X":
                    cell.is_wall = True
                    cell.is_42 = True
                    cell.is_visited = True
                elif char == " ":
                    cell.is_wall = False
                    cell.is_visited = False

    def _get_walkable_neighbors(self, cell: tuple[int, int]) -> list[tuple]:
        """Return accessible neighboring cells for solution search."""
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        neighbors = []
        for dy, dx in directions:
            next_y, next_x = cell[0] + dy, cell[1] + dx
            if 0 <= next_y < self.height * 2 + 1 \
                    and 0 <= next_x < self.width * 2 + 1:
                if not self.maze[next_y][next_x].is_wall:
                    neighbors.append(tuple([next_y, next_x]))
        return neighbors

    def _reconstruct_path(self,
                          moves: dict[tuple[int, int], tuple[int, int] | None],
                          target: tuple[int, int]
                          ) -> list[tuple[int, int]]:
        """Reconstruct the solution path from the parent move map."""
        path = []
        current: tuple[int, int] | None = target
        while current is not None:
            path.append(current)
            self.maze[current[0]][current[1]].is_path = True
            current = moves[current]
        self.path = path[::-1]
        return path[::-1]

    def find_solution(self) -> list[tuple[int, int]] | None:
        """Find a path from entry to exit using breadth-first search."""
        for row in self.maze:
            for cell in row:
                cell.is_path = False

        entry: tuple[int, int] = (self.entry[0] * 2 + 1,
                                  self.entry[1] * 2 + 1)
        target: tuple[int, int] = (self.exit[0] * 2 + 1,
                                   self.exit[1] * 2 + 1)
        moves: dict[tuple[int, int], tuple[int, int] | None] = {entry: None}
        queue = deque([entry])

        while queue:
            current = queue.popleft()
            if current == target:
                return self._reconstruct_path(moves, target)
            for neighbor in self._get_walkable_neighbors(current):
                if neighbor not in moves:
                    moves[neighbor] = current
                    queue.append(neighbor)
        return None

    def switch_path(self, show: bool) -> None:
        """Show or hide the discovered solution path in the maze."""
        if not hasattr(self, 'path') or not self.path:
            return
        for curr_y, curr_x in self.path:
            self.maze[curr_y][curr_x].is_path = show

    def not_perfect(self) -> None:
        """Carve extra openings in the maze to make it imperfect."""
        for y in range(1, len(self.maze) - 1):
            for x in range(1, len(self.maze[y]) - 1):
                cell = self.maze[y][x]

                if cell.is_wall and not cell.is_42:
                    if y % 2 == 0 and x % 2 == 0:
                        continue

                    v_pass = not self.maze[y-1][x].is_wall and \
                        not self.maze[y+1][x].is_wall
                    h_pass = not self.maze[y][x-1].is_wall and \
                        not self.maze[y][x+1].is_wall

                    if v_pass ^ h_pass:
                        if random.randint(1, 15) == 1:
                            cell.is_wall = False
        for y in range(1, len(self.maze) - 1):
            for x in range(1, len(self.maze[y]) - 1):
                cell = self.maze[y][x]

                if cell.is_wall and not cell.is_42:
                    if y % 2 == 0 and x % 2 == 0:
                        continue

                    v_pass = not self.maze[y-1][x].is_wall and \
                        not self.maze[y+1][x].is_wall
                    h_pass = not self.maze[y][x-1].is_wall and \
                        not self.maze[y][x+1].is_wall

                    if v_pass ^ h_pass:
                        cell.is_wall = False
                        return


class Cell():
    """A cell in the maze, which may be a wall, path, or special marker."""
    def __init__(self, is_wall: bool = False,
                 is_visited: bool = False,
                 is_42: bool = False,
                 is_path: bool = False,
                 exit_point: bool = False,
                 entry_point: bool = False,
                 ):
        self.is_wall = is_wall
        self.is_visited = is_visited
        self.is_42 = is_42
        self.is_path = is_path
        self.w_north = False
        self.w_south = False
        self.w_east = False
        self.w_west = False
        self.exit_point = exit_point
        self.entry_point = entry_point

    def print_self(self, renderer: Renderer) -> None:
        """Print the cell using renderer colors and terminal output."""
        if self.is_path:
            print(f"{renderer.path_color.value}  {RESET}", end="")
        elif self.is_42:
            print(f"{renderer.is42_color.value}  {RESET}", end="")
        elif self.is_wall:
            print(f"{renderer.wall_color.value}  {RESET}", end="")
        elif self.exit_point:
            print(f"{renderer.exit_color.value}  {RESET}", end="")
        elif self.entry_point:
            print(f"{renderer.entry_color.value}  {RESET}", end="")
        else:
            print("  ", end="")

    def get_neighbors(self, maze: list, y: int, x: int) -> dict[str, bool]:
        """Return wall presence for the four neighbors of a grid cell."""
        neighbors = {}
        directions = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
        if y % 2 == 0 or x % 2 == 0:
            return {'N': True, 'S': True, 'E': True, 'W': True}
        for dir, (dy, dx) in directions.items():
            ny, nx = y + dy, x + dx
            if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]):
                neighbors[dir] = maze[ny][nx].is_wall
            else:
                neighbors[dir] = True

        return neighbors


class Entry(Cell):
    """A maze entry cell with special rendering and path behavior."""
    def __init__(self, is_wall: bool = False,
                 is_visited: bool = False,
                 is_42: bool = False,
                 is_path: bool = True,
                 exit_point: bool = False,
                 entry_point: bool = True) -> None:
        super().__init__(is_wall, is_visited, is_42,
                         is_path,
                         exit_point, entry_point)

    def print_self(self, renderer: Renderer) -> None:
        print(f"{renderer.entry_color.value}  {RESET}", end="")


class Exit(Cell):
    """A maze exit cell with special rendering and path behavior."""
    def __init__(self, is_wall: bool = False,
                 is_visited: bool = False,
                 is_42: bool = False,
                 is_path: bool = True,
                 exit_point: bool = True,
                 entry_point: bool = False) -> None:
        super().__init__(is_wall, is_visited, is_42,
                         is_path,
                         exit_point, entry_point)

    def print_self(self, renderer: Renderer) -> None:
        print(f"{renderer.exit_color.value}  {RESET}", end="")


def path_to_directions(path: list[tuple[int, int]] | None) -> str:
    """Convert a path of maze coordinates into cardinal direction letters."""
    moves = []
    if path is None:
        return "No path found"
    for i in range(1, len(path)):
        y0, x0 = path[i-1]
        y1, x1 = path[i]

        if y1 < y0:
            moves.append("N")
        elif y1 > y0:
            moves.append("S")
        elif x1 < x0:
            moves.append("W")
        elif x1 > x0:
            moves.append("E")

    return "".join(moves)

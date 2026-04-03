from render_maze import BG_RED, BG_BLUE, BG_GREEN, RESET, BG_CYAN, PATTERN_42, Renderer
import time
import random
from collections import deque


class Maze():
    def __init__(self, config: dict):
        self.config: dict = config
        self.height: int
        self.width: int
        self.is_perfect: bool
        self.entry: list[int, int]
        self.exit: list[int, int]
        self._load_conf(config)
        self.path: list[tuple] = []
        self.maze = self.create_maze()

    def _load_conf(self, config: dict) -> str:
    #"""mettre des raises au lieu de try except"""
        try:
            self.height = config.get("HEIGHT")
            self.width = config.get("WIDTH")
            self.is_perfect = config.get("IS_PERFECT")
            self.entry = config.get("ENTRY")
            self.exit = config.get("EXIT")

            return f"{[self. height, self.width, self.is_perfect, self.entry, self.exit]}"
        except Exception as e:
            return f"Error: {e}"

    def create_maze(self) -> list:
        maze = []
        for i in range(self.height * 2 + 1):
            lst_temp = []
            for j in range(self.width * 2 + 1):
                if i == self.entry[0] and j == self.entry[1]:
                    lst_temp.append(Entry())
                elif i == self.exit[0] and j == self.exit[1]:
                    lst_temp.append(Exit())
                else:
                    true_or_false = i % 2 == 0 or j % 2 == 0
                    lst_temp.append(Cell(true_or_false))
            maze.append(lst_temp)
        return maze

    def _get_unvisited_neighbors(self, current_y, current_x) -> list[tuple]:
        unvisitied_neighbors = []
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]

        for dy, dx in directions:
            next_y, next_x = current_y + dy, current_x + dx

            if 0 <= next_x < self.width * 2 + 1 and 0 <= next_y < self.height * 2 + 1:
                neighbor = self.maze[next_y][next_x]
                if not neighbor.is_wall and not neighbor.is_visited:
                    unvisitied_neighbors.append((next_y, next_x))

        return unvisitied_neighbors

    def _break_wall(self, cell1: tuple[int, int], cell2: tuple[int, int]) -> None:
        y_wall = (cell1[0] + cell2[0]) // 2
        x_wall = (cell1[1] + cell2[1]) // 2
        self.maze[y_wall][x_wall].is_wall = False

    def create_paths(self):
        stack = [(1, 1)]
        self.maze[1][1].is_visited = True
        while stack:
            neighbors = self._get_unvisited_neighbors(stack[-1][0], stack[-1][1])
            if neighbors:
                pos_y, pos_x = random.choice(neighbors)
                self._break_wall(stack[-1], (pos_y, pos_x))
                self.maze[pos_y][pos_x].is_visited = True
                stack.append((pos_y, pos_x))
            else:
                stack.pop()

    def inject_42(self):
        maze_height = len(self.maze)
        maze_width = len(self.maze[0])

        pattern_height = len(PATTERN_42)
        pattern_width = len(PATTERN_42[0])

        offset_y = (maze_height - pattern_height) // 2
        offset_x = (maze_width - pattern_width) // 2
        if self.height < 5 or self.width < 5:
            return

        for y, line in enumerate(PATTERN_42):
            for x, char in enumerate(line):
                target_y = offset_y + y
                target_x = offset_x + x

                if target_y < len(self.maze) and target_x < len(self.maze[0]):
                    if char == "X":
                        self.maze[target_y][target_x].is_wall = True
                        self.maze[target_y][target_x].is_42 = True
                        self.maze[target_y][target_x].is_visited = True
                    elif char == " ":
                        self.maze[target_y][target_x].is_wall = False
                        self.maze[target_y][target_x].is_visited = True
                    elif char == ".":
                        self.maze[target_y][target_x].is_wall = True


    def _get_walkable_neighbors(self, cell: tuple[int, int]) -> list[tuple]:
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        neighbors = []
        for dy, dx in directions:
            next_y, next_x = cell[0] + dy, cell[1] + dx
            if 0 <= next_y < self.height * 2 + 1 and 0 <= next_x < self.width * 2 + 1:
                if not self.maze[next_y][next_x].is_wall:
                    neighbors.append(tuple([next_y, next_x]))
        return neighbors


    def _reconstruct_path(self, moves, target):
        path = []
        current = target
        while current is not None:
            path.append(current)
            self.maze[current[0]][current[1]].is_path = True
            current = moves[current]
        self.path = path[::-1]
        return path[::-1]

    def find_solution(self):
        entry = tuple(self.entry)
        target = tuple(self.exit)

        moves = {entry: None}
        queue = []
        queue.append(entry)

        while queue:
            current = queue[0]
            queue.remove(queue[0])

            if current == target:
                return self._reconstruct_path(moves, target)

            for neighbor in self._get_walkable_neighbors(current):
                if neighbor not in moves:
                    moves[neighbor] = current
                    queue.append(neighbor)

        return None

    def switch_path(self, show: bool) -> None:
        if not hasattr(self, 'path') or not self.path:
            return
        for curr_y, curr_x in self.path:
            self.maze[curr_y][curr_x].is_path = show

    def not_perfect(self):
        for y in range(1, len(self.maze) - 1):
            for x in range(1, len(self.maze[y]) - 1):
                cell = self.maze[y][x]

                if cell.is_wall and not cell.is_42:
                    if y % 2 == 0 and x % 2 == 0:
                        continue

                    v_pass = not self.maze[y-1][x].is_wall and not self.maze[y+1][x].is_wall
                    h_pass = not self.maze[y][x-1].is_wall and not self.maze[y][x+1].is_wall

                    if v_pass ^ h_pass:
                        if random.randint(1, 15) == 1:
                            cell.is_wall = False



class Cell():
    def __init__(self, is_wall: bool = False):
        self.is_wall = is_wall
        self.is_visited = False
        self.is_42 = False
        self.is_path = False

    def print_self(self):
        if self.is_path:
            print(f"{BG_CYAN}  {RESET}", end="")
        elif self.is_42:
            print(f"\033[43m  \033[0m", end="")
        elif self.is_wall is True:
            print(f"{BG_RED}  {RESET}", end="")
        else:
            print(f"  ", end="")

class Entry(Cell):
    def print_self(self):
        print(f"{BG_BLUE}  {RESET}", end="")


class Exit(Cell):
    def print_self(self):
        print(f"{BG_GREEN}  {RESET}", end="")



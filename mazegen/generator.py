import random
from .maze_logic import Maze


class MazeGenerator():
    def __init__(self, width: int, height: int,
                 perfect: bool = True, seed: int = None):
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.output_file = None

        if seed is not None:
            random.seed(seed)

    def generate(self):
        config = {
            "WIDTH": self.width,
            "HEIGHT": self.height,
            "PERFECT": self.perfect,
            "SEED": self.seed,
            "ENTRY": [1, 1],
            "EXIT": [self.height * 2 - 1, self.width * 2 - 1],
        }

        maze = Maze(config)
        maze.create_paths()

        if not self.perfect:
            maze.not_perfect()

        self.path = maze.find_solution()
        self.maze = maze.maze

    def get_maze(self):
        return self.maze

    def get_solution(self):
        return self.path

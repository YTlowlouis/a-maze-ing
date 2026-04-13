import random
from .maze_logic import Maze
from typing import Any


class MazeGenerator():
    """Create and generate maze layouts from given parameters."""
    def __init__(self, width: int, height: int,
                 perfect: bool = True,
                 seed: int | None = None) -> None:
        """Initialize a maze generator with dimensions and options."""
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.output_file = None

        if seed is not None:
            random.seed(seed)

    def generate(self) -> None:
        """Generate the maze and compute its solution path."""
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

    def get_maze(self) -> list[Any]:
        """Return the generated maze grid."""
        return self.maze

    def get_solution(self) -> list[tuple[int, int]] | None:
        """Return the computed path through the maze, if any."""
        return self.path

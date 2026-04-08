from enum import Enum
import random


class Colors(Enum):
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_CYAN = "\033[46m"


RESET = "\033[0m"


def random_color() -> str:
    return random.choice(list(Colors)).value


PATTERN_42 = [
    "X   XXX",
    "X     X",
    "XXX XXX",
    "  X X  ",
    "  X XXX"
]


class Renderer():
    def __init__(self) -> None:
        list_colors = list(Colors)
        self.wall_color = random.choice(list_colors)
        list_colors.remove(self.wall_color)
        self.path_color = random.choice(list_colors)
        list_colors.remove(self.path_color)
        self.entry_color = random.choice(list_colors)
        list_colors.remove(self.entry_color)
        self.exit_color = random.choice(list_colors)
        list_colors.remove(self.exit_color)
        self.is42_color = random.choice(list_colors)
        list_colors.remove(self.is42_color)

    def render_maze(self, maze: list[list]) -> None:
        for row in maze:
            for cell in row:
                cell.print_self(self)
            print()

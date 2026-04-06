BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_CYAN = "\033[46m"
RESET = "\033[0m"

PATTERN_42 = [
    "X   XXX",
    "X     X",
    "XXX XXX",
    "  X X  ",
    "  X XXX"
]


class Renderer():
    def __init__(self):
        pass

    def render_maze(self, maze) -> None:
        x = 0
        for i in maze:
            for j in i:
                j.print_self()
            print("")

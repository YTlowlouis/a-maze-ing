_This project has been created as part of the 42 curriculum by <login1>[, <login2>[, <login3>[...]]]._\

# A-Maze-ing

## Description

A-Maze-ing is a Python maze generator and visualizer designed for the 42 curriculum. The application reads a simple configuration file, builds a maze grid, generates a solvable path using a depth-first search backtracking algorithm, and displays the result in the terminal. It also writes a maze output file in a hex-coded format and supports optional imperfect maze generation with loops.

The project includes: 
- a configuration-driven maze generator,
- a terminal renderer with color support,
- a BFS solver to find the shortest path,
- an interactive menu for regenerating mazes, showing/hiding the solution, and rotating colors,
- a special 42-pattern injection feature for visual design.

## Instructions

### Requirements

- Python 3.8+ (Python 3.11 recommended)
- No external dependencies beyond the Python standard library

### Run the project

1. Open a terminal in the project folder.
2. Use a config file such as `config.txt`.
3. Execute:

```bash
python3 main.py config.txt
```

### Menu options

After generation, the application provides an interactive menu:
- `1` — regenerate a new maze with the same config
- `2` — show or hide the solution path
- `3` — rotate the maze colors
- `4` — exit

### Output

The generated maze is written to the file defined by `OUTPUT_FILE` in the config. The output includes the maze in hex-coded row format, followed by the `ENTRY` and `EXIT` coordinates, and the solution path directions.

## Config file structure

The config file is a plain text file with `KEY=VALUE` entries. Blank lines and lines starting with `#` are ignored.

Required keys:
- `WIDTH` — maze width in cells (minimum 3)
- `HEIGHT` — maze height in cells (minimum 3)
- `ENTRY` — entry coordinates in the final grid, written as `row,column`
- `EXIT` — exit coordinates in the final grid, written as `row,column`
- `OUTPUT_FILE` — output file path ending in `.txt`
- `PERFECT` — `True` or `False`
- `SEED` — optional integer seed for reproducible generation

Example `config.txt`:

```text
WIDTH=4
HEIGHT=4
ENTRY=1,4
EXIT=6,6
OUTPUT_FILE=test.txt
PERFECT=False
SEED=9
```

Notes:
- `ENTRY` and `EXIT` coordinates must be inside the final grid of size `(HEIGHT * 2 + 1)` by `(WIDTH * 2 + 1)`.
- If `PERFECT=False`, the generator adds extra openings to create loops and make the maze imperfect.
- If `SEED` is omitted, the application generates and logs a random seed.

## Maze generation algorithm

The maze generator uses a depth-first search backtracking algorithm (also known as the recursive backtracker).

### Why this algorithm?

- It is simple and reliable for grid-based mazes.
- It produces perfect mazes with exactly one path between any two points.
- It is easy to implement and debug in Python.
- The algorithm works well with config-driven generation and allows optional imperfect maze modifications.

## Reusable code

The following components are reusable in other projects:

- `config_loader.py` — generic configuration parsing and validation for text-based `KEY=VALUE` files.
- `mazegen/maze_logic.py` — maze construction, path generation, and BFS solving logic.
- `mazegen/render_maze.py` — terminal rendering with reusable color logic and display abstraction.
- `main.py` — orchestration code that wires config loading, maze generation, rendering, and output writing.

These parts can be reused in other maze applications, game prototypes, or command-line visualization tools.

## Advanced features

- Interactive terminal menu
- Solution path toggle
- Random terminal color rotation
- Optional imperfect maze generation
- `42` pattern injection into the maze if the grid is large enough

## Team and project management

- Team members and roles:
  - `<login1>` — project design, maze generation, config validation, documentation
  - `<login2>` — optional teammate role if applicable

- Planning and evolution:
  - Initial plan: parse configuration, build grid, generate maze, render output.
  - Mid-project evolution: add solver support, output file generation, terminal interaction, and the 42-pattern display.
  - Final result: a configurable maze generator with interactive CLI features.

- What worked well:
  - The configuration-driven design made it easy to change maze size and behavior.
  - The DFS backtracker produced clean maze generation results.
  - The interactive menu improved usability.

- What could be improved:
  - Add multiple maze algorithms (Prim, Kruskal, Wilson).
  - Add command-line arguments instead of only config file input.
  - Add unit tests for config parsing and maze validity.
  - Improve output format documentation for external tools.

- Tools used:
  - Python 3
  - VS Code or any code editor
  - Terminal / shell for execution
  - Git for version control

## Resources

- Python documentation: https://docs.python.org/3/
- Maze generation overview: https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Recursive backtracker explanation: https://www.redblobgames.com/articles/maze-generating/
- 42 curriculum style and project expectations

### AI usage

This README was drafted with the help of AI for documentation structure, requirements compliance, and wording. No source code was changed by AI; the AI support was limited to writing and organizing the README content.

import sys
import random
from config_loader import MazeGenerator, ConfigError
from mazegen.maze_logic import Maze, path_to_directions
from mazegen.render_maze import Renderer


def convert_to_hex(neighbors: dict) -> str:
    n = '0' if not neighbors['N'] else '1'
    e = '0' if not neighbors['E'] else '1'
    s = '0' if not neighbors['S'] else '1'
    w = '0' if not neighbors['W'] else '1'

    binary = w + s + e + n
    return hex(int(binary, 2))[2:].upper()


def main() -> None:
    # 1. Initialisation des outils
    render = Renderer()
    generator = MazeGenerator()

    # 2. Vérification de l'argument (Le fichier config)
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <config_file.txt>")
        return

    conf_file = sys.argv[1]

    # 3. Chargement et Validation de la configuration
    try:
        # On récupère les données brutes
        raw_conf = generator.get_conf(conf_file)
        # On valide et on transforme (str -> int/list/bool)
        validated_conf = generator.validate_conf(raw_conf)

        seed = validated_conf.get("SEED")
        print(f"seed = {seed}")
        if seed is not None:
            random.seed(seed)
            print(f"Seed set as: {seed}")
        else:
            new_seed = random.randint(0, 100000)
            random.seed(new_seed)
            print(f"Génération avec nouvelle seed: {new_seed}")

        # On crée l'objet labyrinthe avec la config propre
        mazee = Maze(validated_conf)
    except ConfigError as e:
        print(f"Config Error: {e}")
        return
    except Exception as e:
        print(f"Unexpected Error during initialization: {e}")
        return

    # 4. Génération initiale
    print("Generating maze...")
    mazee.create_paths()

    if not validated_conf.get("PERFECT", True):
        mazee.not_perfect()
    raw_path = mazee.find_solution()
    path_directions = path_to_directions(raw_path)
    path_directions = path_directions[::-1]
    mazee.switch_path(False)
    render.render_maze(mazee.maze)
    path_hidden = True

    with open(validated_conf["OUTPUT_FILE"], 'w') as f:
        for y, row in enumerate(mazee.maze):
            to_write = ""
            for x, cell in enumerate(row):
                neighbors = cell.get_neighbors(mazee.maze, y, x)
                to_write += convert_to_hex(neighbors)
            f.write(to_write)
            f.write('\n')
        f.write('\n')
        f.write(f"{mazee.entry[0]},{mazee.entry[1]}\n")
        f.write(f"{mazee.exit[0]},{mazee.exit[1]}\n")
        f.write(str(path_directions[::-1]))

    # 5. Boucle d'interaction (Menu)

    while True:
        print("\n=== A-MAZE-ING MENU ===")
        print("1. Regenerate new maze")
        print("2. Show/Hide solution path")
        print("3. Rotate maze colors (Bonus)")
        print("4. Exit")

        try:
            choice = input("\nChoice? (1-4): ").strip()

            if choice == "4":
                print("Goodbye!")
                break

            elif choice == "1":
                print("Regenerating a new maze...")
                mazee = Maze(validated_conf)
                mazee.create_paths()
                if not validated_conf.get("PERFECT"):
                    mazee.not_perfect()
                raw_path = mazee.find_solution()

                if raw_path is None:
                    print("No path found")
                    return

                path_directions = path_to_directions(raw_path)
                path_directions = path_directions[::-1]
                mazee.switch_path(False)
                path_hidden = True
                render.render_maze(mazee.maze)
                with open(validated_conf["OUTPUT_FILE"], 'w') as f:
                    for y, row in enumerate(mazee.maze):
                        to_write = ""
                        for x, cell in enumerate(row):
                            neighbors = cell.get_neighbors(mazee.maze, y, x)
                            to_write += convert_to_hex(neighbors)
                        f.write(to_write)
                        f.write('\n')
                    f.write('\n')
                    f.write(f"{mazee.entry[0]},{mazee.entry[1]}\n")
                    f.write(f"{mazee.exit[0]},{mazee.exit[1]}\n")
                    f.write(str(path_directions[::-1]))

            elif choice == "2":
                path_hidden = not path_hidden
                mazee.switch_path(not path_hidden)
                render.render_maze(mazee.maze)

            elif choice == "3":
                render = Renderer()
                render.render_maze(mazee.maze)
                print("Colors rotated!")

            else:
                print("Invalid choice, please enter 1, 2, 3 or 4.")

        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

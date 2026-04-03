import sys
import random
from config_loader import MazeGenerator, ConfigError
from maze_logic import Maze
from render_maze import Renderer

def main():
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

    # Si la config demande un labyrinthe NON-parfait (False)
    if not validated_conf.get("PERFECT", True):
        mazee.not_perfect()

    mazee.inject_42()      # On dessine le "42"
    mazee.find_solution()  # On calcule la solution (BFS)
    mazee.switch_path(False) # Cache le chemin par défaut

    render.render_maze(mazee.maze)

    # État du chemin : 1 = Caché, 0 = Visible (selon ta logique de switch)
    path_hidden = True 

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
                # On recrée l'objet
                mazee = Maze(validated_conf)

                mazee.inject_42()
                mazee.create_paths()

                # On respecte la règle PERFECT du sujet [cite: 122, 141]
                if not validated_conf.get("PERFECT"):
                    mazee.not_perfect()


                # CRUCIAL : On calcule la solution tout de suite pour l'avoir en mémoire [cite: 157, 224]
                mazee.find_solution() 

                # On s'assure que le chemin est caché au départ
                mazee.switch_path(False)
                path_hidden = True

                # On affiche le nouveau labyrinthe vide de solution
                render.render_maze(mazee.maze)

            elif choice == "2":
                # Si path_hidden est True, on passe à False (on montre)
                # Si path_hidden est False, on passe à True (on cache)
                path_hidden = not path_hidden

                # On appelle l'animation ou l'affichage simple
                mazee.switch_path(not path_hidden)

                # On redessine pour voir le changement
                render.render_maze(mazee.maze)

            elif choice == "3":
                # Option Bonus : Change la couleur des murs dans le Renderer
                colors = ["\033[41m", "\033[42m", "\033[44m", "\033[45m", "\033[46m"]
                render.wall_color = random.choice(colors)
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

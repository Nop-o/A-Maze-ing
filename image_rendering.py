from maze_generator import MazeGenerator


def display_maze_from_hexa(hexa_maze: list[str],
                           palette: dict[str, tuple[str]]) -> None:
    for lign_part_1 in hexa_maze:
        lign_part_2: list[str] = []
        for i in range(len(lign_part_1)):
            print(palette[lign_part_1[i]][0], end="")
            lign_part_2.append(palette[lign_part_1[i]][1])
        print()
        print("".join(lign_part_2))


def display_maze_from_hexa2(hexa_maze: list[str],
                            palette: dict[str, tuple[str]]) -> None:
    palette_list: dict[str, list[str]] = {
        "empty": ['0', '2', '4', '6'],
        "top_only": ['1', '3', '5', '7'],
        "left_only": ['8', 'A', 'C', 'E'],
        "both": ['9', 'B', 'D', 'F'],
        }

    for lign_part_1 in hexa_maze:
        lign_part_2: list[str] = []

        for i in range(len(lign_part_1)):
            for key, value in palette_list.items():
                if lign_part_1[i] in value:
                    print(palette[key][0], end="")
                    lign_part_2.append(palette[key][1])
                    break
        print("█")
        print("".join(lign_part_2), end="")
        print("█")

    for i in range(len(hexa_maze[0])):
        print("▀▀▀▀", end="")


if __name__ == "__main__":
    palette = {'0': ("    ", "    "),
               '1': ("▀▀▀▀", "    "),
               '2': ("   █", "   █"),
               '3': ("▀▀▀█", "   █"),
               '4': ("    ", "▄▄▄▄"),
               '5': ("▀▀▀▀", "▄▄▄▄"),
               '6': ("   █", "▄▄▄█"),
               '7': ("▀▀▀█", "▄▄▄█"),
               '8': ("█   ", "█   "),
               '9': ("█▀▀▀", "█   "),
               'A': ("█  █", "█  █"),
               'B': ("█▀▀█", "█  █"),
               'C': ("█   ", "█▄▄▄"),
               'D': ("█▀▀▀", "█▄▄▄"),
               'E': ("█  █", "█▄▄█"),
               'F': ("█▀▀█", "█▄▄█"),
               }

    small_palette = {'empty': ("    ", "    "),
                     'top_only': ("▀▀▀▀", "    "),
                     'left_only': ("█   ", "█   "),
                     'both': ("█▀▀▀", "█   "),
                     }

    mg = MazeGenerator(15, 15, (0, 0), (9, 9), perfect=True, seed=None)
    mg.generate_maze_dfs()
    hexa_maze = mg.create_hexa_maze()
    display_maze_from_hexa2(hexa_maze, small_palette)
    print("\n\n")
    display_maze_from_hexa(hexa_maze, palette)
    mg.grid.display()
    print(hexa_maze)

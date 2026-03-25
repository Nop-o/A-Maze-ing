palette = {'0': ("  ", "  "),
        '1': ("--", "  "),
        '2': (" |", " |"),
        '3': ("-+", " |"),
        '4': ("  ", "--"),
        '5': ("--", "--"),
        '6': (" |", "-+"),
        '7': ("-+", "-+"),
        '8': ("| ", "| "),
        '9': ("+-", "| "),
        'a': ("||", "||"),
        'b': ("++", "||"),
        'c': ("| ", "+-"),
        'd': ("+-", "+-"),
        'e': ("||", "++"),
        'f': ("++", "++"),
}

def display_maze_from_hexa(hexa_maze: list[str], palette: dict[str, tuple[str]]) -> None:
    for lign_part_1 in hexa_maze:
        lign_part_2: list[str] = []
        for i in range(len(lign_part_1)):
            print(palette[lign_part_1[i]][0])
            lign_part_2.append(palette[lign_part_1[i]][0])
        print()
        print("".join(lign_part_2))

from maze_generator import MazeGenerator
from parsing.parsing_file import parse_input_file


def a_maze_ing() -> None:
    parsed_input = parse_input_file("input.txt")
    MazeGenerator(**parsed_input)

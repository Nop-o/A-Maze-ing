from typing import Any
from parsing import ValidFileInput, ValidColorInput
from pydantic import ValidationError
import sys

def get_file_content(file_name: str) -> list[str]:
    with open(file_name, 'r') as file:
        content = file.readlines()

    file_content = [line.strip('\n') for line in content]
    return file_content


def transform_input(file_name: str, file_content: list[str]) -> dict[str, Any]:
    settings = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT",
                "SEED", "ALGORITHM", "DISPLAY_MODE", "DISPLAY_SOLUTION",
                "STYLE", "WALL_COLOR", "TUNNEL_COLOR","ENTRY_COLOR",
                "EXIT_COLOR", "LOGO_COLOR", "SOLUTION_COLOR"]

    return_value: dict[str, Any] = {}
    for data in file_content:
        if not data:
            raise ValueError("File input is invalid : "
                             "no empty lines are allowed")
        if data[0] == '#':
            continue
        if '=' not in data:
            raise ValueError("File input is invalid : wrong input given")

        key, value = data.split("=", 1)
        if not key or key not in settings:
            raise ValueError("File input is invalid : wrong key given")

        if key in ("ENTRY", "EXIT"):
            if ',' not in value:
                raise ValueError("File input is invalid : wrong value given")
            x, y = value.split(',', 1)
            if not x or not y:
                raise ValueError("File input is invalid : wrong value given")
            return_value[key] = (x, y)
        else:
            return_value[key] = value
        settings.remove(key)

    if settings:
        raise ValueError(
            f"Missing settings to create the maze: {', '.join(settings)}")

    if file_name == return_value["OUTPUT_FILE"]:
        raise ValueError("Input and output files can't be the same")

    return return_value


def parse_input_file(file_name: str
        ) -> tuple[ValidFileInput, ValidColorInput] | None:
    try:
        file_content = get_file_content(file_name)
        settings = transform_input(file_name, file_content)
        maze_input = ValidFileInput(width=settings["WIDTH"],
                                    height=settings["HEIGHT"],
                                    entry_x=settings["ENTRY"][0],
                                    entry_y=settings["ENTRY"][1],
                                    exit_x=settings["EXIT"][0],
                                    exit_y=settings["EXIT"][1],
                                    output_filename=settings["OUTPUT_FILE"],
                                    is_perfect=settings["PERFECT"],
                                    seed=settings["SEED"],
                                    algorithm=settings["ALGORITHM"],
                                    display_mode=settings["DISPLAY_MODE"],
                                    display_solution=settings["DISPLAY_SOLUTION"],
                                    )
        color_input = ValidColorInput(style=settings["STYLE"],
                                      wall=settings["WALL_COLOR"],
                                      tunnel=settings["TUNNEL_COLOR"],
                                      entry=settings["ENTRY_COLOR"],
                                      exit=settings["EXIT_COLOR"],
                                      logo=settings["LOGO_COLOR"],
                                      solution=settings["SOLUTION_COLOR"],
                                     )
    except ValidationError as e:
        print(e.errors()[0]["msg"])
        sys.exit(-1)
    except Exception as e:
        print(e)
        sys.exit(-1)

    return (maze_input, color_input)


if __name__ == "__main__":
    parsed_input = parse_input_file("input.txt")
    if parsed_input:
        print(parsed_input)

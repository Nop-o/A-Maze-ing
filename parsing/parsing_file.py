from pydantic import Field, BaseModel, model_validator, ValidationError
from typing import Dict, List, Any


class ValidFileInput(BaseModel):
    maze_width: int = Field(ge=2)
    maze_height: int = Field(ge=2)
    maze_entry_x: int = Field(ge=0)
    maze_entry_y: int = Field(ge=0)
    maze_exit_x: int = Field(ge=0)
    maze_exit_y: int = Field(ge=0)
    maze_output_filename: str
    is_maze_perfect: bool
    maze_seed: int | None
    maze_algorithm: str
    maze_display_mode: str

    @model_validator(mode='after')
    def validate_input(self) -> 'ValidFileInput':
        if (self.maze_entry_x == self.maze_exit_x and
                self.maze_entry_y == self.maze_exit_y):
            raise ValueError("The maze entry and exit can't be in "
                             "the same file")

        if (self.maze_entry_x > self.maze_width or
                self.maze_entry_y > self.maze_height):
            raise ValueError("The maze entry needs to be inside the maze")

        if (self.maze_exit_x > self.maze_width or
                self.maze_exit_y > self.maze_height):
            raise ValueError("The maze exit needs to be inside the maze")
        return self


def get_file_content(file_name: str) -> List[str]:
    with open(file_name, 'r') as file:
        if not file:
            raise FileNotFoundError("The file doesn't exist, create one first "
                                    "or use the default config")
        file_content = file.readlines()

    return file_content


def transform_input(file_content: List[str]) -> Dict[str, Any]:
    return_value: Dict[str, Any] = {
                          "WIDTH": None,
                          "HEIGHT": None,
                          "ENTRY_X": None,
                          "ENTRY_Y": None,
                          "EXIT_X": None,
                          "EXIT_Y": None,
                          "OUTPUT_FILE": None,
                          "PERFECT": "True",
                          "SEED": None,
                          "ALGORITHM": "Basic",
                          "DISPLAY_MODE": "Basic",
                          }
    settings = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
                "PERFECT", "SEED", "ALGORITHM", "DISPLAY_MODE"]

    for data in file_content:
        if not data:
            raise ValueError("File input is invalid : "
                             "no empty lignes are allowed")
        if data[0] == '#':
            file_content.remove(data)
        if '=' not in data:
            raise ValueError("File input is invalid : wrong input given")

        key, value = data.split("=", 1)
        if not value:
            raise ValueError("File input is invalid : wrong value given")
        if not key or key not in settings:
            raise ValueError("File input is invalid : wrong key given")

        if key == "ENTRY" or key == "EXIT":
            if ',' not in value:
                raise ValueError("File input is invalid : wrong value given")
            x, y = value.split(',', 1)
            if not x or not y:
                raise ValueError("File input is invalid : wrong value given")
            return_value.update({key: (x, y)})
        else:
            return_value.update({key: value})
        settings.remove(key)

    return return_value


def validate_file_content(
        file_content: Dict[str, Any], file_name: str) -> None:
    int_settings = ["WIDTH", "HEIGHT", "SEED"]
    tuple_settings = ["ENTRY", "EXIT"]
    bool_settings = ["PERFECT"]
    for key, value in file_content.items():
        if key in int_settings:
            try:
                file_content[key] = int(value)
            except ValueError as e:
                print(e)

        if key in tuple_settings:
            try:
                x, y = value
                file_content[key] = (int(x), int(y))
            except ValueError as e:
                print(e)

        if key in bool_settings:
            if value != "True" and value != "False":
                raise ValueError("File input is invalid : wrong boolean value")

    if file_name == file_content["OUTPUT_FILE"]:
        raise ValueError("Input and output files can't be the same")


def parse_input_file(file_name: str) -> ValidFileInput | None:
    try:
        file_content = get_file_content(file_name)
        maze_settings = transform_input(file_content)
        validate_file_content(maze_settings, file_name)
        validated_file_content = ValidFileInput(
                            maze_width=maze_settings["WIDTH"],
                            maze_height=maze_settings["HEIGHT"],
                            maze_entry_x=maze_settings["ENTRY"][0],
                            maze_entry_y=maze_settings["ENTRY"][1],
                            maze_exit_x=maze_settings["EXIT"][0],
                            maze_exit_y=maze_settings["EXIT"][1],
                            maze_output_filename=maze_settings["OUTPUT_FILE"],
                            is_maze_perfect=maze_settings["PERFECT"],
                            maze_seed=maze_settings["SEED"],
                            maze_algorithm=maze_settings["ALGORITHM"],
                            maze_display_mode=maze_settings["DISPLAY_MODE"]
                                                )
    except (ValidationError, FileNotFoundError, ValueError) as e:
        print(e)
        return None

    return validated_file_content


if __name__ == "__main__":
    parsed_input = parse_input_file("input.txt")
    if parsed_input:
        print(parsed_input)

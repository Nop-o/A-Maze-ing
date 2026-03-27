from pydantic import Field, BaseModel, model_validator, ValidationError
from typing import Dict, List, Any


class ValidFileInput(BaseModel):
    width: int = Field(ge=0)
    height: int = Field(ge=0)
    entry_x: int = Field(ge=0)
    entry_y: int = Field(ge=0)
    exit_x: int = Field(ge=0)
    exit_y: int = Field(ge=0)
    output_filename: str
    is_perfect: bool
    seed: int | None
    algorithm: str
    display_mode: str

    @model_validator(mode='after')
    def validate_input(self) -> 'ValidFileInput':
        if (self.entry_x == self.exit_x and
                self.entry_y == self.exit_y):
            raise ValueError("The maze entry and exit can't be in "
                             "the same file")

        if (self.entry_x > self.width or
                self.entry_y > self.height):
            raise ValueError("The maze entry needs to be inside the maze")

        if (self.exit_x > self.width or
                self.exit_y > self.height):
            raise ValueError("The maze exit needs to be inside the maze")

        if self.width < 9:
            raise ValueError(
                "The maze width is too small to create a maze with the 42 logo"
                )
        if self.height < 7:
            raise ValueError(
                "The maze height is too small to create a maze with the 42 "
                "logo")
        return self


def get_file_content(file_name: str) -> List[str]:
    with open(file_name, 'r') as file:
        if not file:
            raise FileNotFoundError("The file doesn't exist, create one first "
                                    "or use the default config")
        content = file.readlines()

    file_content = []
    for lign in content:
        file_content.append(lign.strip('\n'))
    return file_content


def transform_input(file_content: List[str]) -> Dict[str, Any]:
    settings = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
                "PERFECT", "SEED", "ALGORITHM", "DISPLAY_MODE",
                "ENTRY_COLOR", "EXIT_COLOR", "LOGO_COLOR", "TUNNEL_COLOR",
                "WALL_COLOR"]

    return_value: Dict[str, Any] = {}
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
                            width=maze_settings["WIDTH"],
                            height=maze_settings["HEIGHT"],
                            entry_x=maze_settings["ENTRY"][0],
                            entry_y=maze_settings["ENTRY"][1],
                            exit_x=maze_settings["EXIT"][0],
                            exit_y=maze_settings["EXIT"][1],
                            output_filename=maze_settings["OUTPUT_FILE"],
                            is_perfect=maze_settings["PERFECT"],
                            seed=maze_settings["SEED"],
                            algorithm=maze_settings["ALGORITHM"],
                            display_mode=maze_settings["DISPLAY_MODE"]
                                                )
    except (ValidationError, FileNotFoundError, ValueError) as e:
        print(e)
        return None

    return validated_file_content


if __name__ == "__main__":
    parsed_input = parse_input_file("input.txt")
    if parsed_input:
        print(parsed_input)

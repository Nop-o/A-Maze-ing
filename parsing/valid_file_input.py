from pydantic import Field, BaseModel, model_validator
from typing import Any


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
    display_solution: bool

    @model_validator(mode='before')
    @classmethod
    def transform_input(cls, data: dict[str, Any]) -> dict[str, Any]:
        display_list = ["thin", "large"]
        algorithm_list = ["dfs"]

        if data["seed"] == "None":
            data["seed"] = None

        if data["algorithm"] == "None":
            data["algorithm"] = "dfs"
        elif data["algorithm"] not in algorithm_list:
            raise ValueError("This is not a valid algorithm choice.\n "
                             "The possible choices are dfs and ")

        if data["display_mode"] == "None":
            data["display_mode"] = "thin"
        elif data["display_mode"] not in display_list:
            raise ValueError("This is not a valid maze display choice.\n "
                             "The possible choices are large and thin")
        return data

    @model_validator(mode='after')
    def validate_input(self) -> 'ValidFileInput':
        if (self.entry_x == self.exit_x and
                self.entry_y == self.exit_y):
            raise ValueError("The maze entry and exit can't be in "
                             "the same cell")

        if (self.entry_x >= self.width or
                self.entry_y >= self.height):
            raise ValueError("The maze entry needs to be inside the maze")

        if (self.exit_x >= self.width or
                self.exit_y >= self.height):
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

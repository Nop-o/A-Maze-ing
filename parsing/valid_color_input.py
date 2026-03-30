from pydantic import BaseModel, model_validator
from coloring_text import Style, Text, Background
from typing import Any
import random


class ValidColorInput(BaseModel):
    style: Style
    tunnel: Text
    wall: Background
    entry: Background
    exit: Background
    logo: Background
    solution: Background

    @model_validator(mode='before')
    @classmethod
    def tranform_input(cls, data: dict[str, Any]) -> dict[str, Any]:
        style_settings = ["style"]
        text_settings = ["tunnel"]
        background_settings = ["wall", "entry", "exit", "logo", "solution"]

        for key, value in data.items():
            if value == "None":
                if key in style_settings:
                    data[key] = random.choice(list(Style))
                elif key in text_settings:
                    data[key] = random.choice(list(Text))
                elif key in background_settings:
                    data[key] = random.choice(list(Background))
            else:
                if key in style_settings:
                    data[key] = Style(value)
                elif key in text_settings:
                    data[key] = Text(value)
                elif key in background_settings:
                    data[key] = Background(value) 
        return data

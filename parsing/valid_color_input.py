from pydantic import BaseModel, model_validator
from coloring_text import Style, Text, Background
from typing import Any
import random


class ValidColorInput(BaseModel):
    style: Style
    wall: Text
    tunnel: Background
    entry: Background
    exit: Background
    logo: Background
    solution: Background

    @model_validator(mode='before')
    @classmethod
    def transform_input(cls, data: dict[str, Any]) -> dict[str, Any]:
        style_settings = ["style"]
        text_settings = ["wall"]
        background_settings = ["tunnel", "entry", "exit", "logo", "solution"]
        text_color = list(Text)
        background_color = list(Background)
        shared_color = list(range(len(Text)))

        for key, value in data.items():
            if value == "None":
                if key in style_settings:
                    data[key] = random.choice(list(Style))
                elif key in text_settings:
                    index = random.choice(shared_color)
                    data[key] = text_color[index]
                    shared_color.remove(index)
                elif key in background_settings:
                    index = random.choice(shared_color)
                    data[key] = background_color[index]
                    shared_color.remove(index)
            else:
                if key in style_settings:
                    data[key] = Style(value)
                elif key in text_settings:
                    data[key] = Text(value)
                elif key in background_settings:
                    data[key] = Background(value)
        return data

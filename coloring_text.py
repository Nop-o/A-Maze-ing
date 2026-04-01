from enum import Enum


class Style(Enum):
    RESET = '0'
    BOLD = '1'
    DIM = '2'
    ITALIC = '3'
    UNDERLINED = '4'
    SLOW_BLINKING = '5'
    FAST_BLINKING = '6'
    REVERSE = '7'
    HIDDEN = '8'
    STRIKETROUGH = '9'


class Text(Enum):
    BLACK = '30'
    RED = '31'
    GREEN = '32'
    YELLOW = '33'
    BLUE = '34'
    MAGENTA = '35'
    CYAN = '36'
    WHITE = '37'


class Background(Enum):
    BLACK = '40'
    RED = '41'
    GREEN = '42'
    YELLOW = '43'
    BLUE = '44'
    MAGENTA = '45'
    CYAN = '46'
    WHITE = '47'


class ColoringText:
    def __init__(self,
                 input: str,
                 style: Style,
                 text: Text,
                 background: Background) -> None:
        self.colored_text = (f"\033[{style.value};{text.value};"
                             f"{background.value}m{input}\033[0m")


if __name__ == "__main__":
    red = ColoringText("hello", Style.STRIKETROUGH, Text.BLACK, Background.RED)
    print(red.colored_text)

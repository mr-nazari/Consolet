import os
from .utils import is_windows

COLOR_SET = {
    # Standard Colors
    "black": "0",
    "blue": "1",
    "green": "2",
    "aqua": "3",
    "red": "4",
    "purple": "5",
    "yellow": "6",
    "white": "7",
    "gray": "8",
    # Light Colors
    "light_blue": "9",
    "light_green": "A",
    "light_aqua": "B",
    "light_red": "C",
    "light_purple": "D",
    "light_yellow": "E",
    "bright_white": "F",
}

class Color:
    def __init__(
        self,
        background_color="black",
        default_foreground_color="white",
        is_colorized=True,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.background_color = background_color
        self.default_foreground_color = default_foreground_color
        if is_colorized:
            self.colorize(self.background_color, self.default_foreground_color)

    def set_background_color(self, back_code):
        self.colorize(back_code, self.default_foreground_color)

    def set_foreground_color(self, fore_code):
        self.colorize(self.background_color, fore_code)

    @staticmethod
    def colorize(back_code, fore_code):
        # See : https://ss64.com/nt/color.html

        if back_code is not None:
            back_code = back_code.lower().replace(" ", "_")
            back_code = COLOR_SET.get(
                back_code, COLOR_SET.get("black")
            )
        if fore_code is not None:
            fore_code = fore_code.lower().replace(" ", "_")
            fore_code = COLOR_SET.get(
                fore_code, COLOR_SET.get("white")
            )

        if is_windows():
            os.system(f"color {back_code}{fore_code}")
        else:
            os.system(f"setterm -background {back_code} -foreground {fore_code} -store")

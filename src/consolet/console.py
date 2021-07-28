# Built-In
import os
from time import sleep
from getpass import getpass

# 3rd party
from colorama import init as colorama, Fore, Back, Style

# Local
from .terminal import Terminal
from .colors import Color
from .utils import get_console_id # Get the current console id


def init_colorama(*args, **kwargs):
    colorama(*args, **kwargs)


class Console(Terminal, Color):
    """
    # This is very basic and simple.

    This is just a console helper/manager. It's not create a new console (When you create a new instance) and something like this. JUST A HELPER AND MANAGER.
    If you want, you can do it yourself and give it to this reference class... .

    It uses to print text on the console using the built-in "print" function. It also uses the built-int "input" function to receive input.
    If you want to create some dynamic things on console you have to make this yourself.
    And it has no effect on it because it has nothing to do with it. Because you are free and you are not influenced by anything. And that can be good 🙂.

    Note: Some features do not work on Windows and some on Linux and Mac.
    """

    def __init__(
        self,
        text: str = "",
        fore_color=Fore.WHITE,
        back_color=Back.BLACK,
        text_style=Style.NORMAL,
        console_id=get_console_id(),
        *args,
        **kwargs
    ):

        kwargs["console_id"] = console_id
        super().__init__(*args, **kwargs)

        self.text = text
        self.console_id = console_id

        self.fore_color = fore_color
        self.back_color = back_color
        self.text_style = text_style

    def write(self, text=None, end="", **kwargs) -> None:
        """
        :param text: The text to be written
        :param end: Default is blank.
        :return: None | Just print in the console
        """
        fore_color = kwargs.get("fore_color", self.fore_color)
        back_color = kwargs.get("back_color", self.back_color)
        text_style = kwargs.get("text_style", self.text_style)
        start_str = fore_color + back_color + text_style
        end_str = self.fore_color + self.back_color + self.text_style
        if text is None:
            print(start_str + self.text + end_str, end=end)
        else:
            print(start_str + text + end_str, end=end)

    def new_line(self, count=1, **kwargs) -> None:
        """
        Make a new line
        :param count: Count of new lines
        :return: None
        """
        self.write(end="\n" * count, **kwargs)

    def write_line(self, text=None, count=1, **kwargs) -> None:
        """
        Write text and then make a new line
        :param count: count of new lines
        :param text: The text to be written
        :return: None
        """
        if text is None:
            self.write(self.text, **kwargs)
        else:
            self.write(text, **kwargs)
        self.new_line(count)

    def get_input(
        self,
        text: str = "",
        to_type=str,
        is_secret: bool = False,
        exit_code=None,
        stream=None,
        commands=None,
        **kwargs
    ):
        fore_color = kwargs.get("fore_color", self.fore_color)
        back_color = kwargs.get("back_color", self.back_color)
        text_style = kwargs.get("text_style", self.text_style)
        start_str = fore_color + back_color + text_style
        end_str = self.fore_color + self.back_color + self.text_style

        text = start_str + text + end_str
        user_input = getpass(text, stream) if is_secret else input(text)
        if user_input == exit_code:
            exit()
        if commands is not None:
            for command_name, command_func in commands.items():
                if user_input == command_name:
                    command_func()
                    return None
        return to_type(user_input)

    def clear_console(self, wait_time_before=0, wait_time_after=0) -> None:
        self.sleep_(wait_time_before)
        os.system("cls" if os.name == "nt" else "clear")
        self.sleep_(wait_time_after)

    @staticmethod
    def sleep_(secs: float) -> None:
        sleep(secs)

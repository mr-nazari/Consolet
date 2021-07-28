import os
import shutil
import win32api
import win32gui

from .errors import LessThanZeroException
from .utils import get_rect, is_windows


class TerminalRect:
    def __init__(self, console_id):
        self.console_id = console_id
        self.posx, self.posy, self.width, self.height = get_rect(self.console_id)

    def get_rect(self):
        return self.posx, self.posy, self.width, self.height

    def refresh(self):
        self.posx, self.posy, self.width, self.height = get_rect(self.console_id)
        return self.get_rect()

    def move_to(self, posx, posy):
        if is_windows():
            self.refresh()
            win32gui.MoveWindow(
                self.console_id, posx, posy, self.width, self.height, True
            )


class Terminal:
    def __init__(
        self, title: str = win32api.GetConsoleTitle(), console_id=0, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        if console_id != 0:
            self.rect = TerminalRect(console_id)
        self._title = title
        self._columns, self._lines = self.get_terminal_size()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if is_windows():
            win32api.SetConsoleTitle(title)
        else:
            pass
        self._title = title

    @staticmethod
    def get_terminal_size():
        return shutil.get_terminal_size()

    @staticmethod
    def validate_size(columns, lines):
        if columns < 15:
            raise LessThanZeroException("Terminal columns cannot be less than 15!")
        if lines <= 0:
            raise LessThanZeroException(
                "Terminal lines cannot be less than or equal to zero!"
            )

    def change_terminal_size(self, columns, lines):
        # TODO: Add support for linux
        self.validate_size(columns, lines)
        if is_windows():
            self._columns = columns
            self._lines = lines
            os.system(f"mode {columns},{lines}")

    @property
    def terminal_columns(self):
        return self._columns

    @property
    def terminal_lines(self):
        return self._lines

    @terminal_columns.setter
    def terminal_columns(self, value):
        # TODO: Add support for linux
        self.validate_size(value, self.terminal_lines)
        if is_windows():
            os.system(f"mode {value},{self.terminal_lines}")

    @terminal_lines.setter
    def terminal_lines(self, value):
        # TODO: Add support for linux
        self.validate_size(self.terminal_columns, value)
        if is_windows():
            os.system(f"mode {self.terminal_columns},{value}")

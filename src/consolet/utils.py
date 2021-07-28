import os
import win32api
import win32console
import win32gui

def is_windows():
    if os.name == "nt":
        return True
    return False

def get_rect(console_id):
    if is_windows():
        rect = win32gui.GetWindowRect(console_id)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        return x, y, w, h


def get_console_id():
    if is_windows():
        return win32console.GetConsoleWindow()


def get_system_metrics():
    if is_windows():
        return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

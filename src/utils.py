import os
import keyboard


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def clean_input(prompt: object = "") -> str:
    keyboard.press_and_release('esc')
    return input(prompt)


def exit_prompt(prompt):
    keyboard.press_and_release('esc')
    answer = input(f"{prompt} Y/N: ").lower().strip()

    return answer in ["y", "yes"]


def is_bool(text):
    return text in ["True", "true", "t", "T", "yes", "Yes", "y", "Y", "1"]


def coal(value, default):
    return value if value else default


def tern(value, condition, default):
    return value if condition else default


class Keys:
    KEY_ARROW_UP = 72
    KEY_ARROW_DOWN = 80
    KEY_ARROW_LEFT = 75
    KEY_ARROW_RIGHT = 77
    KEY_SPACE = 57
    KEY_SHIFT = 42

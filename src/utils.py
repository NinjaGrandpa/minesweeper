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

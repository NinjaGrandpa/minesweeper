import json
import keyboard
import colors
from utils import Keys, clear, is_bool, clean_input as input, exit_prompt
from grid import Difficulty


class Choice:
    def __init__(self, text: str, keys: list[str], on_select):
        self.text = text
        self.keys = keys
        self.on_select = on_select

    def __str__(self):
        return self.text

    def select(self):
        return self.on_select()


class Menu:
    def __init__(self, text, choices: list[Choice], default_choice: Choice | None = None, selected_choice=0):
        self.text = text
        self.choices = choices
        self.default_choice = default_choice
        self.selected_choice = selected_choice

    def __str__(self):

        return self.text + "\n" + "\n".join([
            (colors.underline + c.text + colors.reset) if self.selected_choice == i else c.text for i, c in enumerate(self.choices)])

    def select_prev(self, *args):
        if self.selected_choice > 0:
            self.selected_choice += -1
        else:
            self.selected_choice = len(self.choices) - 1
        clear()
        print(self.__str__())

    def select_next(self, *args):
        if self.selected_choice < len(self.choices) - 1:
            self.selected_choice += 1
        else:
            self.selected_choice = 0
        clear()
        print(self.__str__())

    def select_choice(self, *args):
        return self.choices[self.selected_choice].select()


class Options:
    def __init__(self, debug=False, first_run=True, input_type="keyboard"):
        self.debug = debug
        self.first_run = first_run
        self.input_type = input_type
        self.get()

    def get(self):
        try:
            with open("src/config.json", "rb") as rf:
                data = json.load(rf)

            self.debug = data["debug"]
            self.first_run = data["first_run"]
            self.input_type = data["input_type"]

        except:
            print("Cant convert json to options object")
        return self

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


DIFF_EASY = Difficulty(9, 9, 10)
DIFF_MEDIUM = Difficulty(16, 30, 40)
DIFF_HARD = Difficulty(24, 30, 160)


def option_menu():
    clear()

    while True:
        global options
        options = Options().get()

        print("\n--- Options ---")
        print(f"- Debug(d): {options.debug}")
        print(f"- First Run(f): {options.first_run}")
        print(f"- Input Type(i): {options.input_type}")
        print("---------------")
        print("Write the option and the value: 'input keyboard'\nPress 'q' to exit to menu")

        usr_input = input("Input: ").split()

        if len(usr_input) <= 0:
            print("Enter an option")
            continue

        option = usr_input[0].lower()
        value = usr_input[1].lower() if len(usr_input) > 1 else None

        def check_val():
            if (value and len(usr_input) == 2) or len(usr_input) == 1:
                return True
            else:
                print(f"Value: {value} not recognized")

        if option in ["q", "quit"]:
            if exit_prompt("Do you want to exit to the menu?"):
                break
        elif option in ["debug", "d"] and check_val():
            options.debug = is_bool(value) if value else not options.debug

        elif option in ["first", "firstrun", "first_run", "firstRun", "f"] and check_val():
            options.first_run = is_bool(
                value) if value else not options.first_run

        elif option in ["input", "type", "inputType", "input_type", "i"] and check_val():
            if value in ["keyboard", "keys" "key", "k"]:
                options.input_type = "keyboard"

            elif value in ["text", "txt" "t"]:
                options.input_type = "text"

            else:
                options.input_type = "keyboard" if options.input_type == "text" else "text"

        else:
            print(f"Option: {option} not recognized")
            continue

        with open("src/config.json", "w") as file:
            file.write(options.to_json())


def menu():
    options = Options()

    text = """
    xXx Welcome to Minesweeper! xXx
---------------------------------------
Choose the difficulty by entering one of the options below or by selecting an option with the up and down arrows and pressing enter.

You can also customize your own difficulty by entering the amount of rows, columns and mines.
An alternative to this is to write custom(c) and enter in manually.
"""

    def on_easy_select():
        print("Playing with Easy difficulty")
        return DIFF_EASY

    def on_medium_select():
        print("Playing with Medium difficulty")
        return DIFF_MEDIUM

    def on_hard_select():
        print("Playing with Hard difficulty")
        return DIFF_HARD

    def on_custom_select():
        pass

    def on_options_select():
        option_menu()

    def on_quit_select():
        if exit_prompt("Do you want to quit the game?"):
            exit()

    choices: list[Choice] = [
        Choice(
            text="- Easy(e): 9x9 grid, 10 mines",
            keys=["easy", "e"],
            on_select=on_easy_select
        ),
        Choice(
            text="- Medium(m): 16x30 grid, 40 mines",
            keys=["medium", "mid", "m"],
            on_select=on_medium_select
        ),
        Choice(
            text="- Hard(h): 24x30 grid, 160 mines",
            keys=["hard", "h"],
            on_select=on_hard_select
        ),
        Choice(
            text="- Custom(rows columns mines): Min 9x9 grid, 10 mines and Max 30x30 grid, 240 mines",
            keys=["custom", "c"],
            on_select=on_custom_select
        ),
        Choice(
            text="- Options(o): Access the options",
            keys=["options", "o"],
            on_select=on_options_select
        ),
        Choice(
            text="- Quit(q): Quit the game",
            keys=["quit", "q"],
            on_select=on_quit_select
        )
    ]

    main_menu = Menu(text, choices)

    keyboard.on_press_key(Keys.KEY_ARROW_UP, main_menu.select_prev)
    keyboard.on_press_key(Keys.KEY_ARROW_DOWN, main_menu.select_next)

    while True:
        clear()
        print(main_menu)
        menu_input = input(": ").lower().strip()

        if menu_input == "":
            result = main_menu.select_choice()
            if result != None:
                return result
            else:
                continue

        for choice in main_menu.choices:
            for key in choice.keys:
                if menu_input == key:
                    result = choice.select()
                    if result != None:
                        return result
                    else:
                        continue

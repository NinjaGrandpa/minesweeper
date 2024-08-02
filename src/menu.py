import json
from utils import clear, is_bool, clean_input as input, exit_prompt
from grid import Difficulty


DIFF_EASY = Difficulty(9, 9, 10)
DIFF_MEDIUM = Difficulty(16, 30, 40)
DIFF_HARD = Difficulty(24, 30, 160)


class Options:
    def __init__(self, debug=False, first_run=True, input_type="keyboard"):
        self.debug = debug
        self.first_run = first_run
        self.input_type = input_type

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
        print("Write the option and the value: 'input keyboard'")

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

        if option in ["debug", "d"] and check_val():
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
    clear()
    while True:
        print(
            """
            xXx Welcome to Minesweeper! xXx
        ---------------------------------------
        Choose the difficulty by entering one of the options below.

        You can also customize your own difficulty by entering the amount of rows, columns and mines.
        An alternative to this is to write custom(c) and enter in manually.

        - Easy(e): 9x9 grid, 10 mines
        - Medium(m): 16x30 grid, 40 mines
        - Hard(h): 24x30 grid, 160 mines
        - Custom(rows columns mines): Min 9x9 grid, 10 mines and Max 30x30 grid, 240 mines
        - Options(o): Access the options
        - Quit(q): Quit the game
        """
        )

        menu_input = input("")

        match menu_input.lower():
            case "easy" | "e":
                print("Playing with Easy difficulty")
                return DIFF_EASY

            case "medium" | "mid" | "m":
                print("Playing with Medium difficulty")
                return DIFF_MEDIUM

            case "hard" | "h":
                print("Playing with Hard Difficulty")
                return DIFF_HARD

            case "quit" | "q":
                if exit_prompt("Do you want to quit the game?"):
                    exit()

            case "options" | "o":
                option_menu()

            case "cls" | "clear":
                clear()

            case _:
                if menu_input.isdigit() or (menu_input in ["custom", "c"]):
                    choices = [int(i) for i in menu_input.split()]

                    if len(choices) <= 3:
                        rows = (
                            choices[0]
                            if choices[0] is not None
                            else int(input("Amount of Rows (max 30): "))
                        )
                        cols = (
                            choices[1]
                            if len(choices) > 1 is not None
                            else int(input("Amount of Columns (max 30): "))
                        )
                        mines = (
                            choices[2]
                            if len(choices) > 2 is not None
                            else int(input("Amount of Mines (max 240): "))
                        )

                        return Difficulty(rows, cols, mines)

                else:
                    print(
                        "Choose a difficulty or create a custom difficulty by entering the amount of rows, columns and mines."
                    )

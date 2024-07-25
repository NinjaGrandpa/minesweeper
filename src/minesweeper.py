import random
import keyboard
import colors
from utils import clear, exit_prompt, clean_input as input, is_bool, Keys
import json


class Difficulty:
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines = mines


class Cords:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Tile:
    def __init__(self, x: int, y: int, is_mine=False):
        self.x = x
        self.y = y
        self.is_mine = is_mine
        self.is_marked = False
        self.is_revealed = False
        self.is_selected = False
        self.mine_count = 0

    def __str__(self):
        color = colors.fg.lightgrey

        if self.is_mine and self.is_revealed:
            sym = "X"
        elif self.is_marked and self.is_revealed is False:
            sym = "P"
        elif self.is_revealed:
            sym = str(self.mine_count)
            match self.mine_count:
                case 0:
                    sym = " "
                case 1:
                    color = colors.fg.lightblue
                case 2:
                    color = colors.fg.lightgreen
                case 3:
                    color = colors.fg.lightred
                case _:
                    color = colors.fg.lightcyan
        else:
            sym = "O"

        return colors.print_color(
            sym, color, colors.reverse if self.is_selected else colors.reset
        )

    def get_neighbours(self, col_count, row_count):
        neighbours: list[Cords] = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (
                    self.x + j > -1
                    and self.x + j < col_count
                    and self.y + i > -1
                    and self.y + i < row_count
                    and not (i == 0 and j == 0)
                ):
                    neighbours.append(Cords(self.x + j, self.y + i))

        return neighbours


class Grid:
    def __init__(self, difficulty: Difficulty):
        self.difficulty = difficulty
        self.row_count = difficulty.rows
        self.col_count = difficulty.cols
        self.tile_count = difficulty.rows * difficulty.cols
        self.mine_count = difficulty.mines
        self.cleared_tiles = 0
        self.grid = self.__create_grid__()
        self.selected_tile = self.__init_select__()
        self.activated_mine = False

    def __create_grid__(self):
        grid = [
            [Tile(x=x, y=y) for x in range(self.col_count)]
            for y in range(self.row_count)
        ]
        tile_count = self.col_count * self.row_count

        for mine in random.sample(range(0, tile_count - 1), self.mine_count):
            r = mine // self.col_count
            c = mine % self.col_count
            grid[r][c].is_mine = True

        for col in grid:
            for tile in col:
                neighbours = tile.get_neighbours(
                    self.col_count, self.row_count)
                tiles = [grid[n.y][n.x] for n in neighbours]
                tile.mine_count = len(
                    list(filter(lambda t: t.is_mine == True, tiles)))

        return grid

    def __init_select__(self):
        tile: Tile

        if self.col_count % 2 == 0 and self.row_count % 2 == 0:
            tile = self.grid[0][0]

        else:
            tile = self.grid[self.row_count // 2][self.col_count // 2]

        tile.is_selected = True
        return tile

    def draw_grid(self):
        print(
            f"Current Difficulty {self.row_count}x{
                self.col_count}, {self.mine_count} mines.\n"
        )
        print(f"x ", end="")
        for i in range(self.col_count):
            print(f" {i} ", end="")
        print("")
        for row in self.grid:
            print(f"{self.grid.index(row)} ", end="")
            for col in row:
                print("{}".format(col), end="")
            print("")

    def select(self, x, y):
        self.selected_tile.is_selected = False
        self.selected_tile = self.grid[y][x]
        self.selected_tile.is_selected = True

    def reveal(self):
        if self.selected_tile.is_mine:
            print("BANG!")
            self.activated_mine = True
            self.reveal_all()

        else:
            self.reveal_neighbours(self.selected_tile)

    def reveal_neighbours(self, tile: Tile):
        tile.is_revealed = True
        neighbours = [
            self.grid[cords.y][cords.x]
            for cords in tile.get_neighbours(self.col_count, self.row_count)
        ]
        rec: list[Tile] = []

        for n in neighbours:
            if n.mine_count == 0 and not n.is_revealed and not n.is_mine:
                rec.append(n)
            if not n.is_mine:
                n.is_revealed = True

        for r in rec:
            self.reveal_neighbours(r)

    def reveal_all(self):
        for row in self.grid:
            for col in row:
                col.is_revealed = True

    def mark(self):
        if self.selected_tile.is_marked:
            self.selected_tile.is_marked = False
        else:
            self.selected_tile.is_marked = True

    def get_cleared_tiles(self):
        cleared = 0
        for col in self.grid:
            for tile in col:
                if tile.is_revealed:
                    cleared += 1

        return cleared


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

        # debug_opts = ["debug", "d"]
        # first_run_opts = ["first", "firstrun", "first_run", "firstRun", "f"]
        # input_type_opts = ["input", "type", "inputType", "input_type", "i"]
        # opts = [debug_opts, first_run_opts, input_type_opts]

        # if option  in [[o for o in l] for l in opts]:
        #     print(f"Option: {option} not recognized")
        #     continue

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


def play_game(difficulty: Difficulty):
    grid = Grid(difficulty)

    while True:
        clear()
        grid.draw_grid()
        print(grid.selected_tile.x, grid.selected_tile.y)
        print(f"Tiles: {grid.tile_count -
              grid.mine_count - grid.get_cleared_tiles()}")

        if grid.activated_mine:
            clear()
            grid.draw_grid()
            if exit_prompt("Do you want to play again?"):
                play_game(difficulty)
            else:
                break

        if grid.tile_count - grid.mine_count == grid.get_cleared_tiles():
            print("You won the game!")

            if exit_prompt("Do you want to play again?"):
                play_game(difficulty)
            else:
                break

        if options.debug:
            for col in grid.grid:
                for tile in col:
                    tile.is_revealed = not tile.is_mine

        keyboard.read_event()

        if keyboard.is_pressed(Keys.KEY_ARROW_LEFT):
            if grid.selected_tile.x - 1 != -1:
                grid.select(grid.selected_tile.x - 1, grid.selected_tile.y)

        elif keyboard.is_pressed(Keys.KEY_ARROW_RIGHT):
            if grid.selected_tile.x + 1 != difficulty.cols:
                grid.select(grid.selected_tile.x + 1, grid.selected_tile.y)

        elif keyboard.is_pressed(Keys.KEY_ARROW_UP):
            if grid.selected_tile.y - 1 != -1:
                grid.select(grid.selected_tile.x, grid.selected_tile.y - 1)

        elif keyboard.is_pressed(Keys.KEY_ARROW_DOWN):
            if grid.selected_tile.y + 1 != difficulty.rows:
                grid.select(grid.selected_tile.x, grid.selected_tile.y + 1)

        elif keyboard.is_pressed(Keys.KEY_SPACE):
            if not grid.selected_tile.is_marked:
                grid.reveal()

        elif keyboard.is_pressed(Keys.KEY_SHIFT):
            grid.mark()

        elif keyboard.is_pressed("q"):
            if exit_prompt("Do you want to exit to the menu?"):
                break


while True:
    difficulty = menu()
    play_game(difficulty)

from time import sleep
import keyboard
from utils import clear, exit_prompt, Keys
from grid import Grid, Difficulty
from menu import menu, Options


def first_run():
    options = Options()
    print(f"Welcome to Minesweeper!\nDo you want to play with a keyboard or only using text?\n- text(t)\n- keyboard(k)")
    while True:
        match input(": ").lower().strip():
            case "t" | "text":
                options.input_type = "text"
                break
            case "k" | "keyboard":
                options.input_type = "keyboard"
                break
            case _:
                print("Please enter on of the options text(t) or keyboard(k).")
    options.first_run = False
    with open("src/config.json", "w") as file:
        file.write(options.to_json())


def play_game(difficulty: Difficulty):
    keyboard.unhook_all()
    options = Options()

    grid = Grid(difficulty)

    while True:

        clear()
        grid.draw_grid()
        print(grid.selected_tile.x, grid.selected_tile.y)
        tiles_left = grid.tile_count - grid.mine_count - grid.get_cleared_tiles()
        print(f"Tiles: {tiles_left}")

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
            for c in grid.grid:
                for tile in c:
                    tile.is_revealed = not tile.is_mine

        t_input = ""
        arg = ""
        col = None
        row = None
        move = 1

        if options.input_type == "keyboard":
            keyboard.read_event()
        else:
            t_input = input(": ").lower().strip()
            args = t_input.split(" ")

            if len(args) == 0 or len(args) > 3 or sum(1 for a in args if a.isnumeric()) > 2:
                print("Enter min 1 and max 3 arguments: (action) column row")
                sleep(1.5)
                continue

            for i, a in enumerate(args):
                if a == "q":
                    arg = a
                    break
                elif a in ["s", "m", "l", "r", "u", "d"]:
                    arg = a
                elif arg in ["l", "r", "u", "d"] and len(args) == 2:
                    move = int(a)
                elif a.isnumeric():
                    if i == 0 or (i == 1 and len(args) == 3):
                        col = int(a)
                    elif i == 2 or (i == 1 and len(args) == 2):
                        row = int(a)
                    else:
                        print("Invalid syntax: (action) column row")
                        sleep(1.5)
                        continue

                elif a == "":
                    continue
                else:
                    print(f"Invalid argument: '{a}'")
                    sleep(1.5)
                    continue

        if col != None and row != None:
            grid.move(col, row)

        if keyboard.is_pressed(Keys.KEY_ARROW_LEFT) or arg == "l":
            grid.move_left(move)

        elif keyboard.is_pressed(Keys.KEY_ARROW_RIGHT) or arg == "r":
            grid.move_right(move)

        elif keyboard.is_pressed(Keys.KEY_ARROW_UP) or arg == "u":
            grid.move_up(move)

        elif keyboard.is_pressed(Keys.KEY_ARROW_DOWN) or arg == "d":
            grid.move_down(move)

        elif keyboard.is_pressed(Keys.KEY_SPACE) or arg == "s":
            grid.reveal()

        elif keyboard.is_pressed(Keys.KEY_SHIFT) or arg == "m":
            grid.mark()

        elif keyboard.is_pressed("q") or arg == "q":
            if exit_prompt("Do you want to exit to the menu?"):
                break


while True:
    options = Options()
    if options.first_run == True:
        first_run()
    difficulty = menu()
    play_game(difficulty)

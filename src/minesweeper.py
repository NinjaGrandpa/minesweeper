from time import sleep
import keyboard
from utils import clear, exit_prompt, Keys
from grid import Grid, Difficulty
from menu import menu, Options


class Minesweeper:
    def __init__(self, grid: Grid, options: Options):
        self.grid = grid
        self.options = options

    def move_left(self):
        if self.grid.selected_tile.x - 1 != -1:
            self.grid.select(self.grid.selected_tile.x -
                             1, self.grid.selected_tile.y)

    def move_right(self):
        if self.grid.selected_tile.x + 1 != difficulty.cols:
            self.grid.select(self.grid.selected_tile.x +
                             1, self.grid.selected_tile.y)

    def move_up(self):
        if self.grid.selected_tile.y - 1 != -1:
            self.grid.select(self.grid.selected_tile.x,
                             self.grid.selected_tile.y - 1)

    def move_down(self):
        if self.grid.selected_tile.y + 1 != difficulty.rows:
            self.grid.select(self.grid.selected_tile.x,
                             self.grid.selected_tile.y + 1)


options = Options().get()


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

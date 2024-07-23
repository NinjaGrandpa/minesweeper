import random
import os
import keyboard
import colors

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

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
    def __init__(self, x: int, y: int, is_mine = False):
        self.x = x
        self.y = y
        self.is_mine = is_mine
        self.is_marked = False
        self.is_revealed = False
        self.is_selected = False
        self.mine_count = 0

    def __str__(self):  
        color = colors.fg.lightgrey

        if (self.is_mine and self.is_revealed):
            sym = "X"
        elif (self.is_marked and self.is_revealed is False):
            sym = "P"
        elif (self.is_revealed):
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

        return colors.print_color(sym, color, colors.reverse if self.is_selected else colors.reset)        

    def get_neighbours(self, col_count, row_count):
        neighbours: list[Cords] = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (self.x + j > -1 and self.x + j < col_count and self.y + i > -1 and self.y + i < row_count and not (i == 0 and j == 0)):
                    neighbours.append(Cords(self.x + j, self.y + i))
     
        return neighbours

class Grid:
    def __init__(self, difficulty: Difficulty):
        self.difficulty = difficulty
        self.row_count = difficulty.rows
        self.col_count = difficulty.cols
        self.mine_count = difficulty.mines
        self.grid = self.__create_grid__()
        self.selected_tile = self.__init_select__()
        self.activated_mine = False

    def __create_grid__(self):
        grid = [[Tile(x = x, y = y) for x in range(self.col_count)] for y in range(self.row_count)]
        tile_count = self.col_count * self.row_count

        for mine in random.sample(range(0, tile_count - 1), self.mine_count):
            r  = mine // self.col_count
            c = mine % self.col_count
            grid[r][c].is_mine = True

        for col in grid:
            for tile in col:
                neighbours = tile.get_neighbours(self.col_count, self.row_count)
                tiles = [grid[n.y][n.x] for n in neighbours]
                tile.mine_count = len(list(filter(lambda t: t.is_mine == True, tiles)))

        return grid

    def __init_select__(self):
        tile: Tile

        if (self.col_count % 2 == 0 and self.row_count % 2 == 0):
            tile = self.grid[0][0]
            
        else:
            tile = self.grid[self.row_count//2][self.col_count//2]
        
        tile.is_selected = True
        return tile

    def draw_grid(self):
        clear()
        print(f"Current Difficulty {self.row_count}x{self.col_count}, {self.mine_count} mines.\n")
        print(f"x ", end = "")
        for i in range(self.col_count):
            print(f" {i} ", end = "")
        print("")
        for row in self.grid:
            print(f"{self.grid.index(row)} ", end="")
            for col in row:
                print(u"{}".format(col), end="")
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
            self.selected_tile.is_revealed = True
            neighbours = [self.grid[cords.y][cords.x] for cords in self.selected_tile.get_neighbours(self.col_count, self.row_count)]

            for n in neighbours:
                n.is_revealed = False if n.is_mine else True
                if n.mine_count == 0:
                    self.reveal_neighbours(n)


    def reveal_neighbours(self, tile: Tile):
        neighbours = [self.grid[cords.y][cords.x] for cords in tile.get_neighbours(self.col_count, self.row_count)]

        for n in neighbours:
            n.is_revealed = False if n.is_mine else True
            if n.mine_count == 0 and not n.is_revealed:
                self.reveal_neighbours(n)
            

    def reveal_all(self):
        for row in self.grid:
                for col in row:
                    col.is_revealed = True

    def mark(self):
        if self.selected_tile.is_marked:
                self.selected_tile.is_marked = False
        else:
            self.selected_tile.is_marked = True

DIFF_EASY = Difficulty(9, 9, 10)
DIFF_MEDIUM = Difficulty(16, 30, 40)
DIFF_HARD = Difficulty(24, 30, 160)

def menu(): 
    clear()
    print('''
        xXx Welcome to Minesweeper! xXx
    ---------------------------------------

    Choose the difficulty by entering one of the options below.
    You can also customize your own difficulty by entering the amount of rows, columns and mines.
    An alternative to this is to write custom(c) and enter in manually.

    - Easy(e): 9x9 grid, 10 mines
    - Medium(m): 16x30 grid, 40 mines
    - Hard(h): 24x30 grid, 160 mines
    - Custom(rows columns mines): Min 9x9 grid, 10 mines and Max 30x30 grid, 240 mines
    - Quit(q): Quit the game
    ''')

    diff_choice = input("Difficulty: ")
    difficulty = Difficulty(0, 0, 0)

    match diff_choice.lower():
        case "easy" | "e":
            print("Playing with Easy difficulty")
            difficulty = DIFF_EASY

        case "medium" | "mid" | "m":
            print("Playing with Medium difficulty")
            difficulty = DIFF_MEDIUM

        case "hard" | "h":
            print("Playing with Hard Difficulty")
            difficulty = DIFF_HARD
            
        case "quit" | "q":
            if input("Do you want to quit the game? Y/N").lower() == "y":
                exit()
                
        case _:
            if (diff_choice.isnumeric() or ("custom" or "c" in diff_choice)):
                choices = [int(i) for i in diff_choice.split()]

                if (len(choices) <= 3):
                    difficulty.rows = choices[0] if choices[0] is not None else int(input("Amount of Rows (max 30): "))
                    difficulty.cols = choices[1] if len(choices) > 1 is not None else int(input("Amount of Columns (max 30): "))
                    difficulty.mines = choices[2] if len(choices) > 2 is not None else int(input("Amount of Mines (max 240): "))

            else:
                print("Choose a difficulty or create a custom difficulty by entering the amount of rows, columns and mines.")
                menu()

    return difficulty

def play_game(difficulty: Difficulty):
    
    grid = Grid(difficulty)
    grid.draw_grid()

    while True:
        print(grid.selected_tile.x, grid.selected_tile.y)
        keyboard.read_key()
        
        if keyboard.is_pressed("vänsterpil"):
            if (grid.selected_tile.x - 1 != -1):
                grid.select(grid.selected_tile.x - 1, grid.selected_tile.y)
                       
        if keyboard.is_pressed("högerpil"):
            if (grid.selected_tile.x + 1 != difficulty.cols):
                grid.select(grid.selected_tile.x + 1, grid.selected_tile.y)
                      
        if keyboard.is_pressed('uppil'):
            if (grid.selected_tile.y - 1 != -1):
                grid.select(grid.selected_tile.x, grid.selected_tile.y - 1)
                      
        if keyboard.is_pressed('nedpil'):
            if (grid.selected_tile.y + 1 != difficulty.rows):
                grid.select(grid.selected_tile.x, grid.selected_tile.y + 1)
                      
        if keyboard.is_pressed('space'):
            grid.reveal()
            
        if keyboard.is_pressed('skift'):
            grid.mark()

        if grid.activated_mine:
            grid.draw_grid()
            play_again = input("\nDo you want to play again? Y/N: ")
            if play_again.lower() == "y":
                play_game(difficulty)

            else:
                break

        grid.draw_grid()
        
while True:
    difficulty = menu()
    play_game(difficulty)

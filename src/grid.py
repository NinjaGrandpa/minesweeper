import colors
import random


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
        print(f"""Current Difficulty {self.row_count}x{
              self.col_count}, {self.mine_count} mines.\n""")
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

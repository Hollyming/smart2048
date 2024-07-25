import itertools
import numpy as np
import tkinter as tk
from tkinter import font, simpledialog
from game import Grid, Game
from config import *

config = Base()

def get_grid(tiles, directions):
    g = Grid(config.SIZE)
    g.tiles = tiles.copy()
    for direction in directions:
        g.run(direction)
        g.add_random_tile()
    return g.tiles

def printf(tiles):
    formatted_tiles = []
    for row in tiles:
        formatted_row = []
        for i in row:
            if i == 0:
                formatted_row.append(0)
            else:
                formatted_row.append(int(np.log2(i)))
        formatted_tiles.append(formatted_row)
    
    for row in formatted_tiles:
        print("[", end='')
        for i, val in enumerate(row):
            if i < len(row) - 1:
                print(f"{val}, ", end='')
            else:
                print(f"{val}", end='')
        print("]")

def my_log2(z):
    if z == 0:
        return 0
    else:
        return z

class Ai:
    def __init__(self):
        self.g = Grid(config.SIZE)

    def get_next(self, tiles):
        score_list = []
        tn = self.get_tile_num(tiles)
        if tn >= self.g.size ** 2 / 3:
            return "RD"[np.random.randint(0, 2)], 0
        kn = min(max(tn ** 2, 20), 40)
        for directions in itertools.product("ULRD", repeat=3):
            fen = []
            for i in range(kn):
                t_g = get_grid(tiles, directions)
                fen.append(self.get_score(t_g))
            print(directions, min(fen))
            score_list.append([directions, min(fen)])
        score_list = sorted(score_list, key=(lambda x: [x[1]]))
        for d in score_list[::-1]:
            self.g.tiles = tiles.copy()
            if self.g.run(d[0][0], is_fake=False) != 0:
                return d[0][0], d[1] / kn
        self.g.tiles = tiles.copy()
        return score_list[-1][0][0], score_list[-1][1] / kn

    def get_score(self, tiles):
        a = self.get_bj2__4(tiles)
        b = self.get_bj__4(tiles)
        print(a, b)
        return a * 2.8 + b

    def debug(self, tiles):
        print('\n=======开始判断========')
        print('移动前棋盘：')
        printf(tiles)
        score_list = []
        for directions in itertools.product("ULRD", repeat=2):
            t_g = get_grid(tiles, directions)
            fen = self.get_score(t_g)
            score_list.append([directions, fen])
            print('==={}=={}=='.format(directions, fen))
            printf(t_g)
        score_list = sorted(score_list, key=(lambda x: [x[1]]))
        for d in score_list[::-1]:
            self.g.tiles = tiles.copy()
            if self.g.run(d[0][0], is_fake=True) != 0:
                self.g.run(d[0][0])
                return d[0][0]
        return score_list[-1][0][0]

    def get_tile_num(self, tiles):
        n = 0
        for row in tiles:
            for i in row:
                if i == 0:
                    n += 1
        return n

    def get_bj(self, tiles):
        gjs = [
            self.get_bj__1(tiles),
            self.get_bj__2(tiles),
            self.get_bj__3(tiles),
            self.get_bj__4(tiles)
        ]
        return gjs

    def get_bj__4(self, tiles):
        bj = 0
        l = len(tiles)
        size = self.g.size - 1
        for y in range(l):
            for x in range(l):
                z = tiles[y][x]
                if z != 0:
                    z_log = z - 2
                    bj += z_log * (x + y - (size * 2 - 1))
                else:
                    bj += (100 - 20 * (x + y - (size * 2 - 1)))
        return bj

    def get_bj__3(self, tiles):
        bj = 0
        l = len(tiles)
        size = self.g.size - 1
        for y in range(l):
            for x in range(l):
                z = tiles[y][x]
                if z != 0:
                    z_log = z - 2
                    bj += z_log * ((size - x) + y - (size * 2 - 1))
                else:
                    bj += (100 - 20 * ((size - x) + y - (size * 2 - 1)))
        return bj

    def get_bj__2(self, tiles):
        bj = 0
        l = len(tiles)
        size = self.g.size - 1
        for y in range(l):
            for x in range(l):
                z = tiles[y][x]
                if z != 0:
                    z_log = z - 2
                    bj += z_log * ((size - x) + (size - y) - (size * 2 - 1))
                else:
                    bj += (100 - 20 * ((size - x) + (size - y) - (size * 2 - 1)))
        return bj

    def get_bj__1(self, tiles):
        bj = 0
        l = len(tiles)
        size = self.g.size - 1
        for y in range(l):
            for x in range(l):
                z = tiles[y][x]
                if z != 0:
                    z_log = z - 2
                    bj += z_log * (x + (size - y) - (size * 2 - 1))
                else:
                    bj += (100 - 20 * (x + (size - y) - (size * 2 - 1)))
        return bj

    def get_bj2(self, tiles):
        gjs = [
            self.get_bj2__1(tiles),
            self.get_bj2__2(tiles),
            self.get_bj2__3(tiles),
            self.get_bj2__4(tiles)
        ]
        return gjs

    def get_bj2__1(self, tiles):
        bj = 0
        l = len(tiles)
        for y in range(0, l - 1, 1):
            for x in range(l - 1, 0, -1):
                z = tiles[y][x]
                if tiles[y][x] < tiles[y][x - 1]:
                    bj -= abs(my_log2(tiles[y][x - 1]) - z)
                if tiles[y][x] < tiles[y + 1][x]:
                    bj -= abs(my_log2(tiles[y + 1][x]) - z)
                if tiles[y][x] < tiles[y + 1][x - 1]:
                    bj -= abs(my_log2(tiles[y + 1][x - 1]) - z)
        return bj

    def get_bj2__2(self, tiles):
        bj = 0
        l = len(tiles)
        for y in range(0, l - 1):
            for x in range(0, l - 1):
                z = tiles[y][x]
                if tiles[y][x] < tiles[y][x + 1]:
                    bj -= abs(my_log2(tiles[y][x + 1]) - z)
                if tiles[y][x] < tiles[y + 1][x]:
                    bj -= abs(my_log2(tiles[y + 1][x]) - z)
                if tiles[y][x] < tiles[y + 1][x + 1]:
                    bj -= abs(my_log2(tiles[y + 1][x + 1]) - z)
        return bj

    def get_bj2__3(self, tiles):
        bj = 0
        l = len(tiles)
        for y in range(l - 1, 0, -1):
            for x in range(0, l - 1):
                z = tiles[y][x]
                if tiles[y][x] < tiles[y][x + 1]:
                    bj -= abs(my_log2(tiles[y][x + 1]) - z)
                if tiles[y][x] < tiles[y - 1][x]:
                    bj -= abs(my_log2(tiles[y - 1][x]) - z)
                if tiles[y][x] < tiles[y - 1][x + 1]:
                    bj -= abs(my_log2(tiles[y - 1][x + 1]) - z)
        return bj

    def get_bj2__4(self, tiles):
        bj = 0
        l = len(tiles)
        for y in range(l - 1, 0, -1):
            for x in range(l - 1, 0, -1):
                z = tiles[y][x]
                if z < tiles[y][x - 1]:
                    bj -= abs(my_log2(tiles[y][x - 1]) - z)
                if z < tiles[y - 1][x]:
                    bj -= abs(my_log2(tiles[y - 1][x]) - z)
                if z < tiles[y - 1][x - 1]:
                    bj -= abs(my_log2(tiles[y - 1][x - 1]) - z)
        return bj

def make_decision(tiles):
    ai = Ai()
    move, _ = ai.get_next(tiles)
    return move

class Game2048App:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game with AI")
        self.grid_size = 4
        self.tile_size = 100
        self.padding = 10

        self.tiles = np.array([
            [2, 0, 0, 0],
            [5, 2, 0, 1],
            [1, 7, 4, 3],
            [9, 8, 7, 5]
        ])
        self.tiles = np.where(self.tiles == 0, 0, 2 ** self.tiles)
        
        self.game = Game(self.grid_size)
        self.game.grid.tiles = self.tiles
        
        self.ai = Ai()
        
        self.canvas = tk.Canvas(self.root, width=self.grid_size * self.tile_size + self.padding * 2,
                                height=self.grid_size * self.tile_size + self.padding * 2)
        self.canvas.pack()
        
        self.font = font.Font(size=24, weight='bold')
        
        self.update_ui()
        
        self.canvas.bind("<Button-1>", self.modify_tile)
        self.root.bind("<Key>", self.handle_keypress)

    def update_ui(self):
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0 = j * self.tile_size + self.padding
                y0 = i * self.tile_size + self.padding
                x1 = x0 + self.tile_size
                y1 = y0 + self.tile_size
                value = self.game.grid.tiles[i][j]
                if value == 0:
                    color = "#cdc1b4"
                else:
                    color = "#f2b179"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#bbada0", width=2)
                if value != 0:
                    self.canvas.create_text(x0 + self.tile_size / 2, y0 + self.tile_size / 2,
                                            text=str(int(np.log2(value))), font=self.font, fill="#776e65")
        self.show_ai_suggestion()

    def modify_tile(self, event):
        x, y = event.x, event.y
        col = (x - self.padding) // self.tile_size
        row = (y - self.padding) // self.tile_size
        if 0 <= col < self.grid_size and 0 <= row < self.grid_size:
            new_value = simpledialog.askinteger("Input", f"Enter new value for tile ({row}, {col}) in power of 2:",
                                                minvalue=0, maxvalue=20)
            if new_value is not None:
                if new_value == 0:
                    self.game.grid.tiles[row][col] = 0
                else:
                    self.game.grid.tiles[row][col] = 2 ** new_value
                self.update_ui()
            
    def handle_keypress(self, event):
        key = event.keysym
        if key in ["Up", "Down", "Left", "Right"]:
            direction = key[0]
            if direction == "U":
                direction = "U"
            elif direction == "D":
                direction = "D"
            elif direction == "L":
                direction = "L"
            elif direction == "R":
                direction = "R"
            
            moved = self.game.run(direction)
            # if moved:
                # self.game.grid.add_random_tile()
            self.update_ui()
            
    def show_ai_suggestion(self):
        move = make_decision(self.game.grid.tiles)
        ai_suggestion_text = f"AI recommends moving: {move}"
        self.canvas.create_text(self.padding, self.grid_size * self.tile_size + self.padding / 2,
                                anchor='w', font=self.font, fill="#776e65", text=ai_suggestion_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = Game2048App(root)
    root.mainloop()

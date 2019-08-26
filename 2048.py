import tkinter as tk
import numpy as np

BG_COLORS = {0: "#CDC1B5", 2: "#EEE4DA", 4: "#ECE0CA", 8: "#EFB180",
                         16: "#F69564", 32: "#F97A63", 64: "#F25B47",
                         128: "#EECE71", 256: "#EBCE61", 512: "#EDC750",
                         1024: "#ECC440", 2048: "#F0C02E" }

FONT_COLORS = {0: "#CDC1B5", 2: "#72685E", 4: "#72685E", 8: "#FFF3E8", 16: "#FFF3E8",
                   32: "#FFFAE6", 64: "#FFF3E8", 128: "#FFF3E8",
                   256: "#FFF3E8", 512: "#FFF3E8", 1024: "#FFF3E8",
                   2048: "#FFF3E8"}

class Game():
    def __init__(self):
        self.r = tk.Tk()
        self.r.title('2048')
        self.board = np.zeros((4,4))
        self.tiles = []
        self.generate_tile()
        self.init_tiles()
        self.r.bind("<Left>", self.shift_board_left)
        self.r.bind("<Up>", self.shift_board_up)
        self.r.bind("<Down>", self.shift_board_down)
        self.r.bind("<Right>", self.shift_board_right)
        self.restart = tk.Button(self.r, text = "Restart", command=self.reset, font = ("Verdana", 15), borderwidth = 1)
        self.restart.grid(row=5, column=0, columnspan=2, rowspan=1)
        self.speed = tk.Button(self.r, text = "Speed Mode!", command=self.flag_speed_mode, font = ("Verdana", 15), borderwidth = 1)
        self.speed.grid(row=5, column=2, columnspan=2, rowspan=1)
        self.speed_flag = False
        self.r.mainloop()

    def reset(self):
        self.board = np.zeros((4,4))
        self.tiles = []
        self.generate_tile()
        self.init_tiles()
        self.update_tiles()
        self.r.bind("<Left>", self.shift_board_left)
        self.r.bind("<Up>", self.shift_board_up)
        self.r.bind("<Down>", self.shift_board_down)
        self.r.bind("<Right>", self.shift_board_right)
        self.speed_flag = False
        self.speed = tk.Button(self.r, text = "Speed Mode!", command=self.flag_speed_mode, font = ("Verdana", 15), borderwidth = 1)
        self.speed.grid(row=5, column=2, columnspan=2, rowspan=1)
        self.r.update()
        
    def init_tiles(self):
        for i in range(4):
            temp = []
            for j in range(4):
                btn = tk.Button(self.r, text = int(self.board[i][j]), font = ("Verdana Bold", 25)
                ,height=2, width = 5, borderwidth = 4)
                btn['bg'] = BG_COLORS[self.board[i][j]]
                btn['fg'] = FONT_COLORS[self.board[i][j]]
                temp.append(btn)
                btn.grid(row = i,column = j)
            self.tiles.append(temp)

    def update_tiles(self):
        for i in range(4):
            for j in range(4):
                self.tiles[i][j]["text"] = int(self.board[i][j])
                self.tiles[i][j]['bg'] = BG_COLORS[self.board[i][j]]
                self.tiles[i][j]['fg'] = FONT_COLORS[self.board[i][j]]
        self.r.update()
    
    def generate_tile_value(self):
        random = np.random.random_sample()
        tile = 0
        if (random < 0.9):
            tile = 2
        else:
            tile = 4
        return tile
    
    def generate_tile(self):
        tile = self.generate_tile_value()
        free_spaces = []
        for r in range(4):
            for c in range(4):
                if (self.board[r][c]==0):
                    free_spaces.append((r, c))
        if (len(free_spaces)!=0):
            location = free_spaces[np.random.randint(len(free_spaces))]
            self.board[location] = tile
        else:
            self.check_possible()
            
    def combine_shifted(self, tiles):
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                if (j+1 < len(tiles[i])):
                    if(tiles[i][j] == tiles[i][j+1]):
                        tiles[i][j] += tiles[i][j+1]
                        tiles[i].pop(j+1)
        return tiles

    def unbind_keys(self):
        self.r.unbind("<Left>")
        self.r.unbind("<Right>")
        self.r.unbind("<Up>")
        self.r.unbind("<Down>")
        self.r.update()
    
    def check_possible(self):
        for row in range(4):
            for col in range(4):
                if (self.board[row][col] == 0):
                    return
        for row in range(4):
            for col in range(4):
                if (self.check_adjacent_tiles(row, col)==True):
                    return
        self.restart["text"] = "You lost!"
        self.speed_flag = False
        self.unbind_keys()
        self.speed.destroy()
        self.r.update()
        
    def flag_speed_mode(self):
        self.speed_flag = True
        self.speed.destroy()
        self.speed_mode()
    
    def speed_mode(self):
        if (self.speed_flag == True):
            tile = self.generate_tile_value()
            free_spaces = []
            for r in range(4):
                for c in range(4):
                    if (self.board[r][c]==0):
                        free_spaces.append((r, c))
            if (len(free_spaces)!=0):
                location = free_spaces[np.random.randint(len(free_spaces))]
                self.board[location] = tile
                self.tiles[location[0]][location[1]]['text'] = int(self.board[location])
                self.tiles[location[0]][location[1]]['bg'] = BG_COLORS[self.board[location]]
                self.tiles[location[0]][location[1]]['fg'] = FONT_COLORS[self.board[location]]
                self.r.update()
            else:
                self.check_possible()
            self.r.after(2000, self.speed_mode)
            
    def check_adjacent_tiles(self, row, col):
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == self.board[r][c+1]:
                    return True
                elif self.board[r][c] == self.board[r+1][c]:
                    return True
            if self.board[r][3] == self.board[r+1][3]:
                return True
            if self.board[3][r] == self.board[3][r+1]:
                return True
        return False
        
    def check_win(self):
        for row in range(4):
            for col in range(4):
                if (self.board[row][col] == 2048):
                    self.restart["text"] = "You won!"
                    self.speed_flag = False
                    self.speed.destroy()
                    self.r.update()
                    self.unbind_keys()
                    
    def prep_next(self):
        self.generate_tile()
        self.update_tiles()
        self.check_possible()
        self.check_win()
        
    def shift_board_up(self, event):
        temp = np.zeros((4,4))
        cols = []
        for col in range(4):
            tiles = []
            for row in range(4):
                if(self.board[row, col] != 0):
                    tiles.append(self.board[row, col])
            cols.append(tiles)
        cols = self.combine_shifted(cols)
        for i in range(len(cols)):
            for j in range(len(cols[i])):
                temp[j,i] = cols[i][j]
        if (np.array_equal(temp, self.board) == True):
            self.board=self.board
        else:
            self.board=temp
            self.prep_next()
            
    def shift_board_down(self, event):
        temp = np.zeros((4,4))
        cols = []
        for col in range(4):
            tiles = []
            for row in range(3, -1, -1):
                if(self.board[row, col] != 0):
                    tiles.append(self.board[row, col])
            cols.append(tiles)
        cols = self.combine_shifted(cols)
        for i in range(len(cols)):
            for j in range(len(cols[i])):
                temp[3-j,i] = cols[i][j]
        if (np.array_equal(temp, self.board) == True):
            self.board=self.board
        else:
            self.board=temp
            self.prep_next()

    def shift_board_left(self, event):
        temp = np.zeros((4,4))
        rows = []
        for row in range(4):
            tiles = []
            for col in range(4):
                if(self.board[row, col] != 0):
                    tiles.append(self.board[row, col])
            rows.append(tiles)
        rows = self.combine_shifted(rows)
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                temp[i, j] = rows[i][j]
        if (np.array_equal(temp, self.board) == True):
            self.board=self.board
        else:
            self.board=temp
            self.prep_next()
            
    def shift_board_right(self, event):
        temp = np.zeros((4,4))
        rows = []
        for row in range(4):
            tiles = []
            for col in range(3, -1, -1):
                if(self.board[row, col] != 0):
                    tiles.append(self.board[row, col])
            rows.append(tiles)
        rows = self.combine_shifted(rows)
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                temp[i, 3-j] = rows[i][j]
        if (np.array_equal(temp, self.board) == True):
            self.board=self.board
        else:
            self.board=temp
            self.prep_next()


game=Game()
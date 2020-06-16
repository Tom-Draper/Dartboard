import numpy as np
import matplotlib.pyplot as plt

class Dartboard():
    
    def __init__(self, size):
        self.board = np.zeros(shape=size)
        
        # Earlier copy of the board that contains 0s along the wires
        self.wired_board = np.zeros(shape=size)
        # Boolean matrix to state whether hit the board or not
        self.board_mask = np.ones(shape=size, dtype=bool)
        
        self.centre_pt = tuple((int(size[0]/2), int(size[1]/2)))  # y, x
    
    def printBoardSection(self, centre, r):
        y_low = 0
        if centre[0]-r > 0:
            y_low = centre[0]-r
        
        y_high = len(self.board)
        if centre[0]+r < len(self.board):
            y_high = centre[0]+r
        
        x_low = 0
        if centre[1]-r > 0:
            x_low = centre[1]-r
            
        x_high = len(self.board)
        if centre[1]+r < len(self.board):
            x_high = centre[1]+r
        
        for i in range(y_low, y_high):
            for j in range(x_low, x_high):
                if i == y_low + (y_high - y_low)/2 and j == x_low + (x_high - x_low)/2:
                    print('|' + str(int(board[i][j])).ljust(2), end='')
                else:
                    print(str(int(self.board[i][j])).ljust(3), end='')
            print()
    
    def graphBoard(self, spacing=10):
        plt.figure(figsize=(12, 12), dpi=80)
        plt.xlim(right=self.board.shape[1])
        plt.ylim(top=self.board.shape[0])
        
        for x in range(0, self.board.shape[0], spacing):
            for y in range(0, self.board.shape[1], spacing):
                y_flipped = (self.board.shape[1] - 1) - y
                if self.board[x][y_flipped] != 0:
                    plt.text(x, y, str(self.board[x][y_flipped]), fontsize=6)
        
        
        # for i in range(100):
        #     print(self.board[600][100+i])
        plt.tight_layout(pad=0.07)
        plt.show()
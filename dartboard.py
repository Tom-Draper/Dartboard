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
        
    def graphCoords(self, x, y):
        # Convert x,y to graph coordinates
        # Image uses (y, x)   (0,0)--> x
        #                     |
        #                     V y
        #
        # Graph uses (x, y)  ^ y
        #                    |
        #                    (0,0)--> x
        new_x = y
        new_y = self.board.shape[1] - 1 - x
        return new_x, new_y
    
    def graphBoard(self, spacing=10, kernel=None):
        plt.figure(figsize=(12, 12), dpi=80)
        plt.xlim(right=self.board.shape[1])
        plt.ylim(top=self.board.shape[0])
        
        for i in range(0, self.board.shape[0], spacing):
            for j in range(0, self.board.shape[1], spacing):
                x, y = self.graphCoords(i, j)
                
                if self.board[i][j] != 0:
                    plt.text(x, y, str(self.board[i][j]), fontsize=6)

        plt.tight_layout(pad=0.07)
        plt.show()
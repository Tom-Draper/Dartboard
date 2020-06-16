import numpy as np

class Dartboard():
    
    def __init__(self, size):
        self.board = np.zeros(shape=self.img.shape[:2])
        # Earlier copy of the board that contains 0s along the wires
        self.wired_board = np.zeros(shape=self.img.shape[:2])
        # Boolean matrix to state whether hit the board or not
        self.board_mask = np.ones(shape=self.img.shape[:2], dtype=bool)
    
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
                print(str(int(self.board[i][j])).ljust(2), end=' ')
            print()
    
    def graphBoard(self):
        pass
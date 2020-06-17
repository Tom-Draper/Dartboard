import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Dartboard():
    
    def __init__(self, size):
        self.board = np.zeros(shape=size)
        
        # Earlier copy of the board that contains 0s along the wires
        self.wired_board = np.zeros(shape=size)
        # Boolean matrix to state whether hit the board or not
        self.board_mask = np.ones(shape=size, dtype=bool)
        
        self.centre_pt = tuple((int(size[0]/2), int(size[1]/2)))  # y, x
    
    def printBoardSection(self, centre, r):
        """Prints a square section of the dartboard to console of radius r 
           around the centre point. 

        Args:
            centre (Tuple (int, int)): point (x, y) on the dartboard to print. 
            r (int): radius of the square to print.
        """
        # Check if the square to print goes off the dartboard.
        y_low = 0
        if centre[0]-r > 0:
            y_low = centre[0]-r
        
        x_low = 0
        if centre[1]-r > 0:
            x_low = centre[1]-r
        
        y_high = len(self.board)
        if centre[0]+r < len(self.board):
            y_high = centre[0]+r
            
        x_high = len(self.board)
        if centre[1]+r < len(self.board):
            x_high = centre[1]+r
        
        # Loop through section of the board printing each value
        for i in range(y_low, y_high):
            for j in range(x_low, x_high):
                if i == y_low + (y_high - y_low)/2 and j == x_low + (x_high - x_low)/2:
                    # If printing centre value, add a pipe to identify
                    print('|' + str(int(self.board[i][j])).ljust(2), end='')
                else:
                    print(str(int(self.board[i][j])).ljust(3), end='')
            print()
        
    def graphCoords(self, point):
        """Convert image/dartboard array coordinates (x,y) to graph coordinates (x,y)
           Image uses (y, x)   (0,0)--> x
                                 |
                                 V y
        
           Graph uses (x, y)  ^ y
                              |
                            (0,0)--> x

        Args:
            point (Tuple (int, int)): Coordinate (x,y)of a image/dartboard array coordinates

        Returns:
            Tuple (int, int): Point (x, y) oresponding to graph location
        """
        
        x, y = point
        new_x = y
        new_y = self.board.shape[1] - 1 - x
        return (new_x, new_y)
    
    def graphBoard(self, spacing=10, kernel_size=None, kernel_centre=None):
        """Displays the dartboard board in the form of a graph.
           Each point in the dartboard is looped through, skipping out the values
           for the given spacing and the integer value held at that point on the 
           dartboard is added to the graph in text at the corresponding location.
           If the kernel details are given, the kernel square is displayed over
           its location on the dartboard.

        Args:
            spacing (int, optional): The values of the dartboard skipped. A 
                                     lower value shows more dartboard values and 
                                     gives a more accurate display but slows 
                                     down the responsiveness of the graph. 
                                     Defaults to 10.
            kernel_size (int, optional): Size of the square kernel (kernel_size X kernel_size)
                                         to apply during the algorithm. If 
                                         provided, the kernel will be displayed 
                                         as a scaled square over its given location 
                                         on the dartboard. Defaults to None.
            kernel_centre (Tuple (int, int), optional): The centre point (x, y)
                                                        If provided, the kernel 
                                                        will be displayed as a 
                                                        scaled square over its 
                                                        given location on the dartboard. 
                                                        Defaults to None.
        """
        
        plt.figure(figsize=(12, 12), dpi=80)
        plt.xlim(right=self.board.shape[1])
        plt.ylim(top=self.board.shape[0])
        
        # Display kernel rectangle
        if kernel_size != None and kernel_centre != None:
            centre = self.graphCoords(kernel_centre)
            # Move from centre to top left
            top_left = (centre[0] - (kernel_size/2), centre[1] - (kernel_size/2))
            square = plt.Rectangle(top_left, kernel_size, kernel_size, linewidth=2, edgecolor='r')
            plt.gca().add_patch(square)
        
        # Plot dartboard values
        for i in range(0, self.board.shape[0], spacing):
            for j in range(0, self.board.shape[1], spacing):
                x, y = self.graphCoords(i, j)
                
                if self.board[i][j] != 0:
                    plt.text(x, y, str(self.board[i][j]), fontsize=6)

        plt.tight_layout(pad=0.07)
        plt.show()
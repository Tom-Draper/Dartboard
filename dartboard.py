import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


"""Representation of a dartboard, including dartboard values. 
   A 2D numpy array holds the dartboard values at each position.
"""
class Dartboard:
    def __init__(self, size):
        self.board = np.zeros(shape=size)
        # Holds copy of the board that contains 0s along the wires
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
        
    def convertToGraphCoords(self, point):
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
    
    def graphBoard(self, spacing=5, kernel_size=None, kernel_centres=[]):
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
            kernel_centres (List [Tuple (int, int)], optional): The centre point (x, y)
                                                        If provided, the kernel 
                                                        will be displayed as a 
                                                        scaled square over its 
                                                        given location on the dartboard. 
                                                        Defaults to None.
            kernel_centres (list of tuple(int, int), optional): A list of centre points 
                                                        (x, y) that have been used 
                                                        during gradient descent 
                                                        with the final point in 
                                                        the list the maximum point.
                                                        For each centre point in
                                                        in the list, a kernel of
                                                        size kernel_size is graphed
                                                        at that position
                                                        Defaults to None.
        """
        
        plt.figure(figsize=(12, 12), dpi=80)
        
        if type(kernel_centres) != list:
            kernel_centres = [kernel_centres]
        
        # Display kernel rectangle at each kernel position in kernel_centres
        if kernel_size != None and len(kernel_centres) != 0:
            for i, centre in enumerate(kernel_centres):
                c = self.convertToGraphCoords(centre)
                # Move from centre to top left
                top_left = (c[0] - (kernel_size/2), c[1] - (kernel_size/2))
                # If displaying last kernel position (the maxima) use a green colour
                if i == len(kernel_centres) - 1:
                    edge_colour = 'g'
                else:
                    edge_colour = 'r'
                # square = plt.Rectangle(top_left, kernel_size, kernel_size, linewidth=2, edgecolor=edge_colour)
                # plt.gca().add_patch(square)
                circle = plt.Circle(xy=c, radius=kernel_size/2, linewidth=2, edgecolor=edge_colour)
                plt.gca().add_patch(circle)
        
        if kernel_size > 20:
            # Display small green dot at exact point of maxima 
            # plt.plot(1200 - kernel_centres[-1][1], 1200 - kernel_centres[-1][0], 'go')
            circle = plt.Circle(xy=(kernel_centres[-1][1], 1200 - kernel_centres[-1][0]), radius=4, linewidth=2, edgecolor='w')
            plt.gca().add_patch(circle)
        
        # Plot dartboard values
        for i in range(0, self.board.shape[0], spacing):
            for j in range(0, self.board.shape[1], spacing):
                x, y = self.convertToGraphCoords((i, j))
                
                if self.board[i][j] != 0:
                    plt.text(x, y, str(self.board[i][j]), fontsize=6)

        plt.xlim([100, 1100])
        plt.ylim([100, 1100])
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.annotate(f'Kernel size= {kernel_size}', xy=(150, 1050), size=20)
        plt.savefig("maxima.png", bbox_inches='tight')
        plt.show()



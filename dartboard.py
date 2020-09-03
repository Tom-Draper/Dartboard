import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import queue
import random
from collections import namedtuple


"""Represents a dartboard. 2D board array holds the dartboard values at each point.
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
    
    def graphBoard(self, spacing=10, kernel_size=None, kernel_centres=[]):
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
                square = plt.Rectangle(top_left, kernel_size, kernel_size, linewidth=2, edgecolor=edge_colour)
                plt.gca().add_patch(square)
        
        # Display green dot at exact point of maxima 
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


"""This class contains the functions to convert the dartboard image (H x W x RGBA) 
   found in the dartboard_img folder to a 2D numpy array (H x W) representation 
   of a dartboard that holds integer dartboard values (up to 60).
   The array is created based on image pixel colours and positions. Zeros are
   added to the array at positions in the image where the pixel is outside of the
   dartboard. 
"""
class GenerateDartboard:
    def __init__(self, url):
        self.img = mpimg.imread(url)
        
        # Create db object
        # First two dimensions (no RGB)
        self.db = Dartboard(self.img.shape[:2])

        # Red [1. 0. 0. 1.]
        # Green [0. 0.627451 0. 1.]
        # Black [0. 0. 0. 1.]
        # White [0.90588236 0.89411765 0.78039217 1.]
        # Wire [0.9647059 0.18431373 0.2 1.] [0.8156863 0.92941177 0.99215686 1.] [0.8156863 0.92941177 0.99215686 1.] [0.5803922 0.8392157 0.7058824 1.]
        self.colours = {}
        

    def setColours(self):
        """Finds each unique colour on the dartboard (red, green, black, white)
           and saves each RGB colour value to a class colour dictionary."""
        # Add value of the border colour around the db
        for pixel in self.img[0]:
            if pixel[0] != 0:
                self.colours['outside_border'] = pixel
                break

        # Add bullseye colour
        red_col = self.img[self.db.centre_pt[0]][self.db.centre_pt[1]]
        self.colours['red'] = red_col

        # Add the colour of outer bullseye
        green_col = 0
        for i in range(self.db.centre_pt[0]):
            pixel = self.img[self.db.centre_pt[0]][self.db.centre_pt[1] + i]
            if pixel[0] == 0:
                green_col = pixel
                break
        self.colours['green'] = green_col

        self.colours['white'] = self.img[self.db.centre_pt[0]][self.db.centre_pt[1] + 50]
        self.colours['black'] = self.img[self.db.centre_pt[0] + 50][self.db.centre_pt[1]]

    def createBoard(self):
        """Creates a queue of unique sections of the dartboard using hardcoded 
           points (x, y). Run a flood filling algorithm on each of the points
           in the queue and insert the dartboard value at that same point in the 
           dartboard array.
           Finishes with a 2D dartboard array filled with dartboard values at the 
           correct locations, with 0s along the wires and outside the board."""
        Point = namedtuple('Point', 'point colour board_value')

        bullseye = Point(point=(self.db.centre_pt[0], self.db.centre_pt[1]), 
                         colour=self.colours['red'], board_value=50)
        outer_bullseye = Point(point=(self.db.centre_pt[0] + 25, self.db.centre_pt[1]), 
                               colour=self.colours['green'], board_value=25)

        # Each number on the dart board:
        # [lower value, triple, higher value, double]
        twenty = [Point(point=(self.db.centre_pt[0] - 50, self.db.centre_pt[1]),
                        colour=self.colours['black'], board_value=20),
                  Point(point=(self.db.centre_pt[0] - 270, self.db.centre_pt[1]),
                        colour=self.colours['red'], board_value=60),
                  Point(point=(self.db.centre_pt[0] - 290, self.db.centre_pt[1]),
                        colour=self.colours['black'], board_value=20),
                  Point(point=(self.db.centre_pt[0] - 440, self.db.centre_pt[1]),
                        colour=self.colours['red'], board_value=40)]

        three = [Point(point=(self.db.centre_pt[0] + 50, self.db.centre_pt[1]),
                       colour=self.colours['black'], board_value=3),
                 Point(point=(self.db.centre_pt[0] + 270, self.db.centre_pt[1]),
                       colour=self.colours['red'], board_value=9),
                 Point(point=(self.db.centre_pt[0] + 290, self.db.centre_pt[1]),
                       colour=self.colours['black'], board_value=3),
                 Point(point=(self.db.centre_pt[0] + 440, self.db.centre_pt[1]), 
                       colour=self.colours['red'], board_value=6)]

        six = [Point(point=(self.db.centre_pt[0], self.db.centre_pt[1] + 50), 
                     colour=self.colours['white'], board_value=6),
               Point(point=(self.db.centre_pt[0], self.db.centre_pt[1] + 270),
                     colour=self.colours['green'], board_value=18),
               Point(point=(self.db.centre_pt[0], self.db.centre_pt[1] + 290),
                     colour=self.colours['white'], board_value=6),
               Point(point=(self.db.centre_pt[0], self.db.centre_pt[1] + 440), 
                     colour=self.colours['green'], board_value=12)]

        eleven = [Point(point=(self.db.centre_pt[0], self.db.centre_pt[1] - 50), 
                        colour=self.colours['white'], board_value=11),
                  Point(point=(self.db.centre_pt[0], self.db.centre_pt[1] - 270),
                        colour=self.colours['green'], board_value=33),
                  Point(point=(self.db.centre_pt[0], self.db.centre_pt[1] - 290),
                        colour=self.colours['white'], board_value=11),
                  Point(point=(self.db.centre_pt[0], self.db.centre_pt[1] - 440), 
                        colour=self.colours['green'], board_value=22)]

        one = [Point(point=(self.db.centre_pt[0] - 50, self.db.centre_pt[1] + 20), 
                     colour=self.colours['white'], board_value=1),
               Point(point=(self.db.centre_pt[0] - 270, self.db.centre_pt[1] + 50),
                     colour=self.colours['green'], board_value=3),
               Point(point=(self.db.centre_pt[0] - 290, self.db.centre_pt[1] + 60),
                     colour=self.colours['white'], board_value=1),
               Point(point=(self.db.centre_pt[0] - 440, self.db.centre_pt[1] + 90), 
                     colour=self.colours['green'], board_value=2)]

        five = [Point(point=(self.db.centre_pt[0] - 50, self.db.centre_pt[1] - 20), 
                      colour=self.colours['white'], board_value=5),
                Point(point=(self.db.centre_pt[0] - 270, self.db.centre_pt[1] - 50),
                      colour=self.colours['green'], board_value=15),
                Point(point=(self.db.centre_pt[0] - 290, self.db.centre_pt[1] - 60),
                      colour=self.colours['white'], board_value=5),
                Point(point=(self.db.centre_pt[0] - 440, self.db.centre_pt[1] - 90), 
                      colour=self.colours['green'], board_value=10)]

        seventeen = [Point(point=(self.db.centre_pt[0] + 50, self.db.centre_pt[1] + 20), 
                           colour=self.colours['white'], board_value=17),
                     Point(point=(self.db.centre_pt[0] + 270, self.db.centre_pt[1] + 50),
                           colour=self.colours['green'], board_value=51),
                     Point(point=(self.db.centre_pt[0] + 290, self.db.centre_pt[1] + 60),
                           colour=self.colours['white'], board_value=17),
                     Point(point=(self.db.centre_pt[0] + 440, self.db.centre_pt[1] + 90), 
                           colour=self.colours['green'], board_value=34)]

        nineteen = [Point(point=(self.db.centre_pt[0] + 50, self.db.centre_pt[1] - 20), 
                          colour=self.colours['white'], board_value=19),
                    Point(point=(self.db.centre_pt[0] + 270, self.db.centre_pt[1] - 50),
                          colour=self.colours['green'], board_value=57),
                    Point(point=(self.db.centre_pt[0] + 290, self.db.centre_pt[1] - 60),
                          colour=self.colours['white'], board_value=19),
                    Point(point=(self.db.centre_pt[0] + 440, self.db.centre_pt[1] - 90), 
                          colour=self.colours['green'], board_value=38)]

        thirteen = [Point(point=(self.db.centre_pt[0] - 20, self.db.centre_pt[1] + 50), 
                          colour=self.colours['black'], board_value=13),
                    Point(point=(self.db.centre_pt[0] - 50, self.db.centre_pt[1] + 270), 
                          colour=self.colours['red'], board_value=39),
                    Point(point=(self.db.centre_pt[0] - 60, self.db.centre_pt[1] + 290), 
                          colour=self.colours['black'], board_value=13),
                    Point(point=(self.db.centre_pt[0] - 90, self.db.centre_pt[1] + 440), 
                          colour=self.colours['red'], board_value=26)]

        ten = [Point(point=(self.db.centre_pt[0] + 20, self.db.centre_pt[1] + 50), 
                     colour=self.colours['black'], board_value=10),
               Point(point=(self.db.centre_pt[0] + 50, self.db.centre_pt[1] + 270), 
                     colour=self.colours['red'], board_value=30),
               Point(point=(self.db.centre_pt[0] + 60, self.db.centre_pt[1] + 290), 
                     colour=self.colours['black'], board_value=10),
               Point(point=(self.db.centre_pt[0] + 90, self.db.centre_pt[1] + 440), 
                     colour=self.colours['red'], board_value=20)]

        fourteen = [Point(point=(self.db.centre_pt[0] - 20, self.db.centre_pt[1] - 50), 
                          colour=self.colours['black'], board_value=14),
                    Point(point=(self.db.centre_pt[0] - 50, self.db.centre_pt[1] - 270),
                          colour=self.colours['red'], board_value=42),
                    Point(point=(self.db.centre_pt[0] - 60, self.db.centre_pt[1] - 290), 
                          colour=self.colours['black'], board_value=14),
                    Point(point=(self.db.centre_pt[0] - 90, self.db.centre_pt[1] - 440), 
                          colour=self.colours['red'], board_value=28)]

        eight = [Point(point=(self.db.centre_pt[0] + 20, self.db.centre_pt[1] - 50), 
                       colour=self.colours['black'], board_value=8),
                 Point(point=(self.db.centre_pt[0] + 50, self.db.centre_pt[1] - 270), 
                       colour=self.colours['red'], board_value=32),
                 Point(point=(self.db.centre_pt[0] + 60, self.db.centre_pt[1] - 290), 
                       colour=self.colours['black'], board_value=8),
                 Point(point=(self.db.centre_pt[0] + 90, self.db.centre_pt[1] - 440), 
                       colour=self.colours['red'], board_value=16)]

        eighteen = [Point(point=(self.db.centre_pt[0] - 50, self.db.centre_pt[1] + 40), 
                          colour=self.colours['black'], board_value=18),
                    Point(point=(self.db.centre_pt[0] - 240, self.db.centre_pt[1] + 140), 
                          colour=self.colours['red'], board_value=54),
                    Point(point=(self.db.centre_pt[0] - 290, self.db.centre_pt[1] + 160), 
                          colour=self.colours['black'], board_value=18),
                    Point(point=(self.db.centre_pt[0] - 380, self.db.centre_pt[1] + 220), 
                          colour=self.colours['red'], board_value=36)]

        twelve = [Point(point=(self.db.centre_pt[0] - 50, self.db.centre_pt[1] - 40), 
                        colour=self.colours['black'], board_value=12),
                  Point(point=(self.db.centre_pt[0] - 240, self.db.centre_pt[1] - 140), 
                        colour=self.colours['red'], board_value=36),
                  Point(point=(self.db.centre_pt[0] - 290, self.db.centre_pt[1] - 160), 
                        colour=self.colours['black'], board_value=12),
                  Point(point=(self.db.centre_pt[0] - 380, self.db.centre_pt[1] - 220), 
                        colour=self.colours['red'], board_value=24)]

        two = [Point(point=(self.db.centre_pt[0] + 50, self.db.centre_pt[1] + 40), 
                     colour=self.colours['black'], board_value=2),
               Point(point=(self.db.centre_pt[0] + 240, self.db.centre_pt[1] + 140), 
                     colour=self.colours['red'], board_value=6),
               Point(point=(self.db.centre_pt[0] + 290, self.db.centre_pt[1] + 160), 
                     colour=self.colours['black'], board_value=2),
               Point(point=(self.db.centre_pt[0] + 380, self.db.centre_pt[1] + 220), 
                     colour=self.colours['red'], board_value=4)]

        seven = [Point(point=(self.db.centre_pt[0] + 50, self.db.centre_pt[1] - 40), 
                       colour=self.colours['black'], board_value=7),
                 Point(point=(self.db.centre_pt[0] + 240, self.db.centre_pt[1] -
                              140), colour=self.colours['red'], board_value=21),
                 Point(point=(self.db.centre_pt[0] + 290, self.db.centre_pt[1] -
                              160), colour=self.colours['black'], board_value=7),
                 Point(point=(self.db.centre_pt[0] + 380, self.db.centre_pt[1] - 220), 
                       colour=self.colours['red'], board_value=14)]

        four = [Point(point=(self.db.centre_pt[0] - 40, self.db.centre_pt[1] + 50), 
                      colour=self.colours['white'], board_value=4),
                Point(point=(self.db.centre_pt[0] - 140, self.db.centre_pt[1] + 240), 
                      colour=self.colours['green'], board_value=12),
                Point(point=(self.db.centre_pt[0] - 160, self.db.centre_pt[1] + 290), 
                      colour=self.colours['white'], board_value=4),
                Point(point=(self.db.centre_pt[0] - 220, self.db.centre_pt[1] + 380), 
                      colour=self.colours['green'], board_value=8)]

        fifteen = [Point(point=(self.db.centre_pt[0] + 40, self.db.centre_pt[1] + 50), 
                         colour=self.colours['white'], board_value=15),
                   Point(point=(self.db.centre_pt[0] + 140, self.db.centre_pt[1] + 240), 
                         colour=self.colours['green'], board_value=45),
                   Point(point=(self.db.centre_pt[0] + 160, self.db.centre_pt[1] + 290), 
                         colour=self.colours['white'], board_value=15),
                   Point(point=(self.db.centre_pt[0] + 220, self.db.centre_pt[1] + 380), 
                         colour=self.colours['green'], board_value=30)]

        nine = [Point(point=(self.db.centre_pt[0] - 40, self.db.centre_pt[1] - 50), 
                      colour=self.colours['white'], board_value=9),
                Point(point=(self.db.centre_pt[0] - 140, self.db.centre_pt[1] - 240), 
                      colour=self.colours['green'], board_value=27),
                Point(point=(self.db.centre_pt[0] - 160, self.db.centre_pt[1] - 290), 
                      colour=self.colours['white'], board_value=9),
                Point(point=(self.db.centre_pt[0] - 220, self.db.centre_pt[1] - 380), 
                      colour=self.colours['green'], board_value=18)]

        sixteen = [Point(point=(self.db.centre_pt[0] + 40, self.db.centre_pt[1] - 50), 
                         colour=self.colours['white'], board_value=16),
                   Point(point=(self.db.centre_pt[0] + 140, self.db.centre_pt[1] - 240), 
                         colour=self.colours['green'], board_value=48),
                   Point(point=(self.db.centre_pt[0] + 160, self.db.centre_pt[1] - 290), 
                         colour=self.colours['white'], board_value=16),
                   Point(point=(self.db.centre_pt[0] + 220, self.db.centre_pt[1] - 380), 
                         colour=self.colours['green'], board_value=32)]

        numbers = one + two + three + four + five + six + seven + eight + nine + \
            ten + eleven + twelve + thirteen + fourteen + fifteen + sixteen + \
            seventeen + eighteen + nineteen + twenty

        q = queue.Queue()
        q.put(bullseye)
        q.put(outer_bullseye)
        [q.put(i) for i in numbers]

        while not q.empty():
            p = q.get()
            self.floodFill(p.point, p.colour, p.board_value)

        # Save current progress as a wired board (before wires are allocated)
        self.db.wired_board = copy.deepcopy(self.db.board)

    def floodFillRecursion(self, point, colour, board_value):
        """Recursively takes a point checks whether the point on the image is 
           the target colour "to fill". If so, the board value is inserted into 
           the identical location in the dartboard. If not, no action is taken.
           It then applys this algorithm to all neighbouring points.

        Args:
            point (Tuple (int, int)): point (x, y) on the dartboard to apply the 
                                      algorithm.
            colour (Array [float, float, float, float]): RBGA colour value of 
                                                         the area you want to 
                                                         flood
            board_value (int): the board value to add to the dartboard at the 
                               corresponding place (e.g. 50 for the bullseye)
        """
        # Return if this point on image is not the target colour
        # OR if this position on dartboard has already been filled
        if not (self.img[point[0]][point[1]] == colour).all() or self.db.board[point[0]][point[1]] == board_value:
            return
        else:
            self.db.board[point[0]][point[1]] = board_value
            self.floodFill((point[0] + 1, point[1]), colour, board_value)
            self.floodFill((point[0], point[1] + 1), colour, board_value)
            self.floodFill((point[0] - 1, point[1]), colour, board_value)
            self.floodFill((point[0], point[1] - 1), colour, board_value)

    def floodFill(self, point, colour, board_value):
        """Takes a point checks whether the point on the image is the target colour 
           "to fill". If so, the board value is inserted into the identical
           location in the dartboard. This points neighbours is added to a queue
           to repeat the process on them. Finished once the queue is empty.

        Args:
            point (Tuple (int, int)): point (x, y) on the dartboard to apply the 
                                      algorithm.
            colour (1D float array (length 4)): RBGA colour value of 
                                                         the area you want to 
                                                         flood
            board_value (int): the board value to add to the dartboard at the 
                               corresponding place (e.g. 50 for the bullseye)
        """
        # Return if this point on image is not the target colour
        # OR if this position on dartboard has already been filled
        if not (self.img[point[0]][point[1]] == colour).all() or self.db.board[point[0]][point[1]] == board_value:
            return
        else:
            # Add the board value to input point
            self.db.board[point[0]][point[1]] = board_value
            
            # Create a queue to hold points that its neighbours need to be checked
            q = queue.Queue()
            q.put(point)
            while not q.empty():
                # Take point from the queue, add neighbouring points around current
                # point to the queue IF they have the target colour and have not 
                # yet been filled in the dartboard
                n = q.get()
                for pt in [(n[0] + 1, n[1]), (n[0], n[1] + 1), (n[0] - 1, n[1]), (n[0], n[1] - 1)]:
                    # If this point in the image contains target colour
                    # AND this point in the dartboard has not yet been filled
                    # AND this point is not already in the queue
                    if (self.img[pt[0]][pt[1]] == colour).all() and self.db.board[pt[0]][pt[1]] != board_value and (pt[0], pt[1]) not in q.queue:
                        self.db.board[pt[0]][pt[1]] = board_value
                        # Add point to the queue to check neighbours
                        q.put((pt[0], pt[1]))

    def calculateMask(self):
        """Calculates the 2D array mask containing 1s where the dartboard is 
           present and 0s where it is not. Searches for the outside board colour
           in the image to find the radius of the dartboard and uses distance to
           centre to determine if point is inside or outside board."""
        r = 0
        # Calculate radius to
        for i in range(self.db.centre_pt[0]):
            if (self.img[self.db.centre_pt[0] + i][self.db.centre_pt[1]] == self.colours['outside_border']).all():
                r = i
                break

        for i in range(self.db.board_mask.shape[0]):
            for j in range(self.db.board_mask.shape[1]):
                d = np.sqrt((self.db.centre_pt[0]-i) **2 + (self.db.centre_pt[1]-j)**2)
                if d > r:
                    self.db.board_mask[i][j] = False

    def allocateWire(self, point):
        """Searches through a 2D dartboard array with dartboard values filled in
           and for each blank zero value on the dartboard (areas containing wire)
           it searches for the nearest dartboard value to take the value of.
           Results in a 2D dartboard with all elements within the dartboard radius
           contining a dartboard value (no zeros). The only zeros in the 2D dartboard
           array are locations outside the perimeter of the dartboard.

        Args:
            point (Tuple (int, int)): point (x, y) on the 2D dartboard where a 
                                      wire is located wire and initially containing 
                                      zero.
        """
        # Copy of board to find nearest values for each point
        r = 0
        while True:
            r += 1
            local = []

            points = [(point[0], point[1] + r), (point[0], point[1] - r),
                      (point[0] + r, point[1] + r), (point[0] - r, point[1] - r),
                      (point[0] + r, point[1]), (point[0] - r, point[1]),
                      (point[0] - r, point[1] + r), (point[0] + r, point[1] - r)]

            for pt in points:
                if self.db.board_mask[pt[0]][pt[1]]:  # If on the board
                    if self.db.wired_board[pt[0]][pt[1]] != 0:  # If point not another wire
                        local.append(self.db.wired_board[pt[0]][pt[1]])  # Take value
                else:
                    local.append(0)  # If reach off the board, take zero

            if any(local):
                self.db.board[point[0]][point[1]] = local[0]
                break

    def removeWires(self):
        """Searches through all points in the 2D dartboard array that are within
           the perimeter of the dartboard. If a point contains a zero, it is 
           interpreted as a wire and it takes the nearest board value."""
        cur = 0
        for i in range(self.db.board.shape[0]):
            for j in range(self.db.board.shape[1]):
                if self.db.board[i][j] == 0 and self.db.board_mask[i][j]:
                    self.allocateWire((i, j))
    
    def load(self, filename):
        """Loads a dartboard numpy array.
           Creates and populates dartboard object with loaded array.

        Args:
            file (string): name of the file to load

        Returns:
            2D int array: 2D numpy dartboard array
        """
        board = np.load(filename)
        self.db = Dartboard(self.img.shape[:2])  # Create fresh object
        self.db.board = board
        
        return self.db  # Return dartboard object

    def generate(self):
        self.setColours()
        self.createBoard()
        self.calculateMask()
        self.removeWires()
        #self.printBoardSection((535,176), 55)
        #self.printBoardSection((535,1024), 55)
        #self.printBoardSection((176,535), 55)
        #self.printBoardSection((1024,535), 55)
        np.save('dartboard.npy', self.db.board)
        return self.db  # Return dartboard object 
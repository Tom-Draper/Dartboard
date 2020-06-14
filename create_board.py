import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import queue
import random
from collections import namedtuple


class CreateDartboard():
    
    def __init__(self, url):
        self.img = mpimg.imread(url)
        self.dartboard = np.zeros(shape=self.img.shape[:2])
        self.wired_board = np.zeros(shape=self.img.shape[:2])
        # Matrix to state whether hit the board or not
        self.board_mask = np.ones(shape=self.img.shape[:2], dtype=bool)
        
        self.colours = {}
        # Red [1. 0. 0. 1.]
        # Green [0. 0.627451 0. 1.]
        # Black [0. 0. 0. 1.]
        # White [0.90588236 0.89411765 0.78039217 1.]
        # Wire [0.9647059 0.18431373 0.2 1.] [0.8156863 0.92941177 0.99215686 1.] [0.8156863 0.92941177 0.99215686 1.] [0.5803922 0.8392157 0.7058824 1.]
    
        self.centre_pt = tuple((int(self.img.shape[0]/2), int(self.img.shape[1]/2)))  # y, x
    
    def setColours(self):
        # Add value of the border colour around the dartboard
        for pixel in self.img[0]:
            if pixel[0] != 0:
                self.colours['outside_border'] = pixel
                break
        
        # Add bullseye colour
        red_col = self.img[self.centre_pt[0]][self.centre_pt[1]]
        self.colours['red'] = red_col

        # Add the colour of outer bullseye
        green_col = 0
        for i in range(self.centre_pt[0]):
            pixel = self.img[self.centre_pt[0]][self.centre_pt[1] + i]
            if pixel[0] == 0:
                green_col = pixel
                break
        self.colours['green'] = green_col
        
        self.colours['white'] = self.img[self.centre_pt[0]][self.centre_pt[1] + 50]
        self.colours['black'] = self.img[self.centre_pt[0] + 50][self.centre_pt[1]]
    
    def printBoardSection(self, centre, r):
        y_low = 0
        if centre[0]-r > 0:
            y_low = centre[0]-r
        
        y_high = len(self.dartboard)
        if centre[0]+r < len(self.dartboard):
            y_high = centre[0]+r
        
        x_low = 0
        if centre[1]-r > 0:
            x_low = centre[1]-r
            
        x_high = len(self.dartboard)
        if centre[1]+r < len(self.dartboard):
            x_high = centre[1]+r
        
        for i in range(y_low, y_high):
            for j in range(x_low, x_high):
                print(str(int(self.dartboard[i][j])).ljust(2), end=' ')
            print()
    
    def createBoard(self):
        # Create queue of points inside each unique value dart section
        Point = namedtuple('Point', 'point colour board_value')
        
        bullseye = Point(point=(self.centre_pt[0], self.centre_pt[1]), colour=self.colours['red'], board_value=50)
        outer_bullseye = Point(point=(self.centre_pt[0] + 25, self.centre_pt[1]), colour=self.colours['green'], board_value=25)

        # Each number on the dart board:
        # [lower value, triple, higher value, double]
        twenty = [Point(point=(self.centre_pt[0] - 50, self.centre_pt[1]), colour=self.colours['black'], board_value=20),
                  Point(point=(self.centre_pt[0] - 270, self.centre_pt[1]), colour=self.colours['red'], board_value=60),
                  Point(point=(self.centre_pt[0] - 290, self.centre_pt[1]), colour=self.colours['black'], board_value=20),
                  Point(point=(self.centre_pt[0] - 440, self.centre_pt[1]), colour=self.colours['red'], board_value=40)]
        
        three = [Point(point=(self.centre_pt[0] + 50, self.centre_pt[1]), colour=self.colours['black'], board_value=3), 
                 Point(point=(self.centre_pt[0] + 270, self.centre_pt[1]), colour=self.colours['red'], board_value=9),
                 Point(point=(self.centre_pt[0] + 290, self.centre_pt[1]), colour=self.colours['black'], board_value=3),
                 Point(point=(self.centre_pt[0] + 440, self.centre_pt[1]), colour=self.colours['red'], board_value=6)]
        
        six = [Point(point=(self.centre_pt[0], self.centre_pt[1] + 50), colour=self.colours['white'], board_value=6),
               Point(point=(self.centre_pt[0], self.centre_pt[1] + 270), colour=self.colours['green'], board_value=18),
               Point(point=(self.centre_pt[0], self.centre_pt[1] + 290), colour=self.colours['white'], board_value=6),
               Point(point=(self.centre_pt[0], self.centre_pt[1] + 440), colour=self.colours['green'], board_value=12)]
        
        eleven = [Point(point=(self.centre_pt[0], self.centre_pt[1] - 50), colour=self.colours['white'], board_value=11),
                  Point(point=(self.centre_pt[0], self.centre_pt[1] - 270), colour=self.colours['green'], board_value=33),
                  Point(point=(self.centre_pt[0], self.centre_pt[1] - 290), colour=self.colours['white'], board_value=11),
                  Point(point=(self.centre_pt[0], self.centre_pt[1] - 440), colour=self.colours['green'], board_value=22)]
        
        one = [Point(point=(self.centre_pt[0] - 50, self.centre_pt[1] + 20), colour=self.colours['white'], board_value=1),
               Point(point=(self.centre_pt[0] - 270, self.centre_pt[1] + 50), colour=self.colours['green'], board_value=3),
               Point(point=(self.centre_pt[0] - 290, self.centre_pt[1] + 60), colour=self.colours['white'], board_value=1),
               Point(point=(self.centre_pt[0] - 440, self.centre_pt[1] + 90), colour=self.colours['green'], board_value=2)]
        
        five = [Point(point=(self.centre_pt[0] - 50, self.centre_pt[1] - 20), colour=self.colours['white'], board_value=5),
               Point(point=(self.centre_pt[0] - 270, self.centre_pt[1] - 50), colour=self.colours['green'], board_value=15),
               Point(point=(self.centre_pt[0] - 290, self.centre_pt[1] - 60), colour=self.colours['white'], board_value=5),
               Point(point=(self.centre_pt[0] - 440, self.centre_pt[1] - 90), colour=self.colours['green'], board_value=10)]
        
        seventeen = [Point(point=(self.centre_pt[0] + 50, self.centre_pt[1] + 20), colour=self.colours['white'], board_value=17),
                     Point(point=(self.centre_pt[0] + 270, self.centre_pt[1] + 50), colour=self.colours['green'], board_value=51),
                     Point(point=(self.centre_pt[0] + 290, self.centre_pt[1] + 60), colour=self.colours['white'], board_value=17),
                     Point(point=(self.centre_pt[0] + 440, self.centre_pt[1] + 90), colour=self.colours['green'], board_value=34)]
        
        nineteen = [Point(point=(self.centre_pt[0] + 50, self.centre_pt[1] - 20), colour=self.colours['white'], board_value=19),
                    Point(point=(self.centre_pt[0] + 270, self.centre_pt[1] - 50), colour=self.colours['green'], board_value=57),
                    Point(point=(self.centre_pt[0] + 290, self.centre_pt[1] - 60), colour=self.colours['white'], board_value=19),
                    Point(point=(self.centre_pt[0] + 440, self.centre_pt[1] - 90), colour=self.colours['green'], board_value=38)]
        
        thirteen = [Point(point=(self.centre_pt[0] - 20, self.centre_pt[1] + 50), colour=self.colours['black'], board_value=13),
                    Point(point=(self.centre_pt[0] - 50, self.centre_pt[1] + 270), colour=self.colours['red'], board_value=39),
                    Point(point=(self.centre_pt[0] - 60, self.centre_pt[1] + 290), colour=self.colours['black'], board_value=13),
                    Point(point=(self.centre_pt[0] - 90, self.centre_pt[1] + 440), colour=self.colours['red'], board_value=26)]
        
        ten = [Point(point=(self.centre_pt[0] + 20, self.centre_pt[1] + 50), colour=self.colours['black'], board_value=10),
               Point(point=(self.centre_pt[0] + 50, self.centre_pt[1] + 270), colour=self.colours['red'], board_value=30),
               Point(point=(self.centre_pt[0] + 60, self.centre_pt[1] + 290), colour=self.colours['black'], board_value=10),
               Point(point=(self.centre_pt[0] + 90, self.centre_pt[1] + 440), colour=self.colours['red'], board_value=20)]
        
        fourteen = [Point(point=(self.centre_pt[0] - 20, self.centre_pt[1] - 50), colour=self.colours['black'], board_value=14),
                    Point(point=(self.centre_pt[0] - 50, self.centre_pt[1] - 270), colour=self.colours['red'], board_value=42),
                    Point(point=(self.centre_pt[0] - 60, self.centre_pt[1] - 290), colour=self.colours['black'], board_value=14),
                    Point(point=(self.centre_pt[0] - 90, self.centre_pt[1] - 440), colour=self.colours['red'], board_value=28)]
        
        eight = [Point(point=(self.centre_pt[0] + 20, self.centre_pt[1] - 50), colour=self.colours['black'], board_value=8),
                 Point(point=(self.centre_pt[0] + 50, self.centre_pt[1] - 270), colour=self.colours['red'], board_value=32),
                 Point(point=(self.centre_pt[0] + 60, self.centre_pt[1] - 290), colour=self.colours['black'], board_value=8),
                 Point(point=(self.centre_pt[0] + 90, self.centre_pt[1] - 440), colour=self.colours['red'], board_value=16)]
        
        eighteen = [Point(point=(self.centre_pt[0] - 50, self.centre_pt[1] + 40), colour=self.colours['black'], board_value=18),
                    Point(point=(self.centre_pt[0] - 240, self.centre_pt[1] + 140), colour=self.colours['red'], board_value=54),
                    Point(point=(self.centre_pt[0] - 290, self.centre_pt[1] + 160), colour=self.colours['black'], board_value=18),
                    Point(point=(self.centre_pt[0] - 380, self.centre_pt[1] + 220), colour=self.colours['red'], board_value=36)]
        
        twelve = [Point(point=(self.centre_pt[0] - 50, self.centre_pt[1] - 40), colour=self.colours['black'], board_value=12),
                  Point(point=(self.centre_pt[0] - 240, self.centre_pt[1] - 140), colour=self.colours['red'], board_value=36),
                  Point(point=(self.centre_pt[0] - 290, self.centre_pt[1] - 160), colour=self.colours['black'], board_value=12),
                  Point(point=(self.centre_pt[0] - 380, self.centre_pt[1] - 220), colour=self.colours['red'], board_value=24)]
        
        two = [Point(point=(self.centre_pt[0] + 50, self.centre_pt[1] + 40), colour=self.colours['black'], board_value=2),
               Point(point=(self.centre_pt[0] + 240, self.centre_pt[1] + 140), colour=self.colours['red'], board_value=6),
               Point(point=(self.centre_pt[0] + 290, self.centre_pt[1] + 160), colour=self.colours['black'], board_value=2),
               Point(point=(self.centre_pt[0] + 380, self.centre_pt[1] + 220), colour=self.colours['red'], board_value=4)]
        
        seven = [Point(point=(self.centre_pt[0] + 50, self.centre_pt[1] - 40), colour=self.colours['black'], board_value=7),
                 Point(point=(self.centre_pt[0] + 240, self.centre_pt[1] - 140), colour=self.colours['red'], board_value=21),
                 Point(point=(self.centre_pt[0] + 290, self.centre_pt[1] - 160), colour=self.colours['black'], board_value=7),
                 Point(point=(self.centre_pt[0] + 380, self.centre_pt[1] - 220), colour=self.colours['red'], board_value=14)]
        
        four = [Point(point=(self.centre_pt[0] - 40, self.centre_pt[1] + 50), colour=self.colours['white'], board_value=4),
                Point(point=(self.centre_pt[0] - 140, self.centre_pt[1] + 240), colour=self.colours['green'], board_value=12),
                Point(point=(self.centre_pt[0] - 160, self.centre_pt[1] + 290), colour=self.colours['white'], board_value=4),
                Point(point=(self.centre_pt[0] - 220, self.centre_pt[1] + 380), colour=self.colours['green'], board_value=8)]
        
        fifteen = [Point(point=(self.centre_pt[0] + 40, self.centre_pt[1] + 50), colour=self.colours['white'], board_value=15),
                   Point(point=(self.centre_pt[0] + 140, self.centre_pt[1] + 240), colour=self.colours['green'], board_value=45),
                   Point(point=(self.centre_pt[0] + 160, self.centre_pt[1] + 290), colour=self.colours['white'], board_value=15),
                   Point(point=(self.centre_pt[0] + 220, self.centre_pt[1] + 380), colour=self.colours['green'], board_value=30)]
        
        nine = [Point(point=(self.centre_pt[0] - 40, self.centre_pt[1] - 50), colour=self.colours['white'], board_value=9),
                Point(point=(self.centre_pt[0] - 140, self.centre_pt[1] - 240), colour=self.colours['green'], board_value=27),
                Point(point=(self.centre_pt[0] - 160, self.centre_pt[1] - 290), colour=self.colours['white'], board_value=9),
                Point(point=(self.centre_pt[0] - 220, self.centre_pt[1] - 380), colour=self.colours['green'], board_value=18)]
        
        sixteen = [Point(point=(self.centre_pt[0] + 40, self.centre_pt[1] - 50), colour=self.colours['white'], board_value=16),
                   Point(point=(self.centre_pt[0] + 140, self.centre_pt[1] - 240), colour=self.colours['green'], board_value=48),
                   Point(point=(self.centre_pt[0] + 160, self.centre_pt[1] - 290), colour=self.colours['white'], board_value=16),
                   Point(point=(self.centre_pt[0] + 220, self.centre_pt[1] - 380), colour=self.colours['green'], board_value=32)]
        
        numbers = one + two + three + four + five + six + seven + eight + nine + ten + eleven + twelve + thirteen + fourteen + fifteen + sixteen + seventeen + eighteen + nineteen + twenty
        
        q = queue.Queue()
        q.put(bullseye)
        q.put(outer_bullseye)
        [q.put(i) for i in numbers]
        
        while not q.empty():
            p = q.get()
            self.floodFill(p.point, p.colour, p.board_value)
        
        self.wired_board = copy.deepcopy(self.dartboard)
    
    def floodFillRecursion(self, point, colour, board_value):
        # Return if this point on image is not the target colour 
        # OR if this position on dartboard has already been filled
        if not (self.img[point[0]][point[1]] == colour).all() or self.dartboard[point[0]][point[1]] == board_value:
            return
        else:
            self.dartboard[point[0]][point[1]] = board_value
            self.floodFill((point[0] + 1, point[1]), colour, board_value)
            self.floodFill((point[0], point[1] + 1), colour, board_value)
            self.floodFill((point[0] - 1, point[1]), colour, board_value)
            self.floodFill((point[0], point[1] - 1), colour, board_value)
    
    def floodFill(self, point, colour, board_value):
        if not (self.img[point[0]][point[1]] == colour).all() or self.dartboard[point[0]][point[1]] == board_value:
            return
        else:
            self.dartboard[point[0]][point[1]] = board_value
            q = queue.Queue()
            q.put(point)
            while not q.empty():
                n = q.get()
                
                for pt in [(n[0] + 1, n[1]), (n[0], n[1] + 1), (n[0] - 1, n[1]), (n[0], n[1] - 1)]:
                    if (self.img[pt[0]][pt[1]] == colour).all() and self.dartboard[pt[0]][pt[1]] != board_value and (pt[0], pt[1]) not in q.queue:
                        self.dartboard[pt[0]][pt[1]] = board_value
                        q.put((pt[0], pt[1]))
    
    def calculateMask(self):
        r = 0
        for i in range(self.centre_pt[0]):
            if (self.img[self.centre_pt[0] + i][self.centre_pt[1]] == self.colours['outside_border']).all():
                r = i
                break
        
        for i in range(self.board_mask.shape[0]):
            for j in range(self.board_mask.shape[1]):
                d = np.sqrt((self.centre_pt[0]-i)**2 + (self.centre_pt[1]-j)**2)
                if d > r:
                    self.board_mask[i][j] = False
    
    def allocateWire(self, point):
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
                if self.board_mask[pt[0]][pt[1]]:  # If on the board
                    if self.wired_board[pt[0]][pt[1]] != 0:  # If not another wire
                        local.append(self.wired_board[pt[0]][pt[1]])  #T Take value
                else:
                    local.append(0)  # If reach off the board, take zero
            
            if any(local):
                self.dartboard[point[0]][point[1]] = local[0]
                break
    
    def removeWires(self):
        cur = 0
        for i in range(self.dartboard.shape[0]):
            for j in range(self.dartboard.shape[1]):
                if self.dartboard[i][j] == 0 and self.board_mask[i][j]:
                    self.allocateWire((i,j))
    
    def run(self):
        self.setColours()
        self.createBoard()
        self.calculateMask()
        self.removeWires()
        #self.printBoardSection((535,176), 55)
        #self.printBoardSection((535,1024), 55)
        #self.printBoardSection((176,535), 55)
        #self.printBoardSection((1024,535), 55)
        np.save('dartboard.npy', self.dartboard)



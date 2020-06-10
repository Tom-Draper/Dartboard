import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import queue
from collections import namedtuple


class CreateDartboard():
    
    def __init__(self, url):
        self.img = mpimg.imread(url)
        self.dartboard = np.zeros(shape=self.img.shape[:2])
        
        self.colours = {}
        # Red [1. 0. 0. 1.]
        # Green [0. 0.627451 0.  1.]
        # Black [0. 0. 0. 1.]
        # White [0.90588236 0.89411765 0.78039217 1.]
        # Wire [0.9647059  0.18431373 0.2  1.] [0.8156863  0.92941177 0.99215686 1.] [0.8156863  0.92941177 0.99215686 1.] [0.5803922 0.8392157 0.7058824 1.]

        self.centre_pt = tuple((int(self.img.shape[0]/2), int(self.img.shape[1]/2)))  # y, x
    
    def setColours(self):
        # Add value of the border colour around the dartboard
        for pixel in self.img[0]:
            if pixel[0] != 0:
                self.colours['outside_border'] = pixel[0]
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
        for i in range(centre[0]-r, centre[0]+r):
            for j in range(centre[1]-r, centre[1]+r):
                print(str(int(self.dartboard[i][j])).ljust(1), end=' ')
            print()

    # Scans the radius around the centre_pt and adds the updates dartboard with the 
    # board value at equivalent position where the input colour is found 
    def addValue(self, r, colour, board_value):
        for i in range(self.centre_pt[0] - r, self.centre_pt[0] + r):
            for j in range(self.centre_pt[1] - r, self.centre_pt[1] + r):
                if (self.img[i][j] == colour).all():
                    self.dartboard[i][j] = board_value

    def createInnerBullseye(self):
        # Fill the areas on the dartboard where the image is red centre with value 50 
        self.floodFill(self.centre_pt, self.colours['red'], 50)
    
    def distanceCentreToColour(self, colour):
        r = 0
        # Add distance from centre to first green pixel 
        while True:
            if not (self.img[self.centre_pt[0]][self.centre_pt[1] + r] == colour).all():
                r += 1
            else:
                r += 1  # Include centre
                break
        return r
    
    def createOuterBullseye(self):
        r = 1 + self.distanceCentreToColour(self.colours['green'])
        self.floodFill((self.centre_pt[0] + r, self.centre_pt[1]), self.colours['green'], 25)

    def allocateWire(self, point):
        # Copy of board to find nearest values for each point
        board = self.dartboard.copy()
        
        for r in range(100):
            local = [board[point[0] + r][point[1]],
                    board[point[0] - r][point[1]],
                    board[point[0]][point[1] + r],
                    board[point[0]][point[1] - r],
                    board[point[0] + r][point[1] + r],
                    board[point[0] + r][point[1] - r],
                    board[point[0] - r][point[1] + r],
                    board[point[0] - r][point[1] - r]]
            
            if any(local):
                local = list(filter(lambda v : v != 0, local))  # Remove zeros
                if len(local) == 1:
                    self.dartboard[point[0]][point[1]] = local[0]
                    self.dartboard[point[0]][point[1]] = np.random.choice(local)

    def bullseyeWire(self):
        r = self.distanceCentreToColour(self.colours['green'])
        
        for i in range(self.centre_pt[0] - r, self.centre_pt[0] + r):
            for j in range(self.centre_pt[1] - r, self.centre_pt[1] + r):
                if self.dartboard[i][j] == 0:
                    self.allocateWire((i, j))
    
    def createNumbers(self):
        Point = namedtuple('Point', 'point colour board_value')

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
        
        numbers = twenty + three + six + eleven + one + five + nineteen + seventeen
        
        q = queue.Queue()
        [q.put(i) for i in numbers]
        
        while not q.empty():
            p = q.get()
            self.floodFill(p.point, p.colour, p.board_value)
    
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
    
    def run(self):
        self.setColours()
        self.createInnerBullseye()
        self.createOuterBullseye()
        #self.bullseyeWire()
        self.createNumbers()
        self.printBoardSection((self.centre_pt[0]+420, self.centre_pt[1] - 80), 25)


create = CreateDartboard('dartboard_img/dartboard.png')
create.run()
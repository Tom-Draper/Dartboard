import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class CreateDartboard():
    
    def __init__(self, url):
        self.img = mpimg.imread(url)
        self.dartboard = np.zeros(shape=self.img.shape[:2])
        
        self.colours = {}
        # Get value of the border colour around the dartboard
        for pixel in self.img[0]:
            if pixel[0] != 0:
                self.colours['outside_border'] = pixel[0]
                break

        # Bullseye
        self.centre_pt = tuple((int(self.img.shape[0]/2), int(self.img.shape[1]/2)))  # x, y

    # Scans the radius around the centre_pt and adds the updates dartboard with the 
    # board value at equivalent position where the input colour is found 
    def addValue(self, r, colour, board_value):
        for i in range(self.centre_pt[0] - r, self.centre_pt[0] + r):
            for j in range(self.centre_pt[1] - r, self.centre_pt[1] + r):
                if (self.img[i][j] == colour).all():
                    self.dartboard[i][j] = board_value

    def createInnerBullseye(self):
        # Get the colour of inner bullseye
        red_col = self.img[self.centre_pt[0]][self.centre_pt[1]]
        self.colours['red'] = red_col
        
        # Calculate inner bullseye radius
        r = 1
        while True:
            if (self.img[self.centre_pt[0]][self.centre_pt[1] + r] == red_col).all():
                r += 1
            else:
                r += 1  # Include centre
                break
        
        self.addValue(r, self.colours['red'], 50)
        
    
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

    def outerBullseyeRadius(self):
        green_col = self.colours['green']
        r = 1 + self.distanceCentreToColour(green_col)
        # Add distance from first green pixel to last green pixel
        while True:
            if (self.img[self.centre_pt[0]][self.centre_pt[1] + r] == green_col).all():
                r += 1
            else:
                break
        return r

    def createOuterBullseye(self):
        # Get the colour of outer bullseye
        green_col = 0
        for i in range(self.centre_pt[0]):
            pixel = self.img[self.centre_pt[0]][self.centre_pt[1] + i]
            if pixel[0] == 0:
                green_col = pixel
                break
        self.colours['green'] = green_col
        
        # Calculute outer bullseyeself. radius
        r = self.outerBullseyeRadius()
        
        self.addValue(r, self.colours['green'], 25)

    def allocateWire(self, point):
        for r in range(100):
            local = [self.dartboard[point[0] + r][point[1]],
                    self.dartboard[point[0] - r][point[1]],
                    self.dartboard[point[0]][point[1] + r],
                    self.dartboard[point[0]][point[1] - r],
                    self.dartboard[point[0] + r][point[1] + r],
                    self.dartboard[point[0] + r][point[1] - r],
                    self.dartboard[point[0] - r][point[1] + r],
                    self.dartboard[point[0] - r][point[1] - r]]
            
            if any(local):
                local = list(filter(lambda v : v != 0, local))  # Remove zeros
                if len(local) == 1:
                    self.dartboard[point[0]][point[1]] = local[0]
                else:
                    self.dartboard[point[0]][point[1]] = np.random.choice(local)

    def bullseyeWire(self):
        r = self.distanceCentreToColour(self.colours['green'])
        
        for i in range(self.centre_pt[0] - r, self.centre_pt[0] + r):
            for j in range(self.centre_pt[1] - r, self.centre_pt[1] + r):
                if self.dartboard[i][j] == 0:
                    self.allocateWire(tuple((i, j)))

    def run(self):
        self.createInnerBullseye()
        self.createOuterBullseye()
        self.bullseyeWire()


create = CreateDartboard('dartboard_img/dartboard.png')
create.run()
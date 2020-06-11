import numpy as np

class Gaussian():
    
    def __init__(self):
        self.gaussian = 0
        print("2D Gaussian-like array:")

    def calculateGaussian(self, sigma, mu, size):
        x, y = np.meshgrid(np.linspace(-1,1,size), np.linspace(-1,1,size))
        d = np.sqrt(x*x + y*y)
        self.gaussian = np.exp(-((d-mu)**2 / (2.0 * sigma**2)))

    def printGaussian(self):
        print(self.gaussian)
    
    def applyGaussian(self, dartboard, point):
        if (self.gaussian is int):
            print("Set gaussian")
            return
        
        # If gaussian even length, take top left of the central four as mid point
        if len(self.gaussian) % 2 == 0:
            y_start = int(point[0] - len(self.gaussian)/2)
            x_start = int(point[1] - len(self.gaussian[0])/2)
            
            p = 0
            for y in range(y_start, y_start + len(self.gaussian)):
                for x in range(x_start, x_start + len(self.gaussian[0])):
                    if y < dartboard.shape[0] and x < dartboard.shape[1] and y > 0 and x > 0:
                        p += self.gaussian[y - y_start][x - x_start] * dartboard[y][x]
            print(p)
            
            return p
        


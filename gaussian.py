import numpy as np

class Gaussian():
    
    def __init__(self):
        self.gaussian = 0
        print("2D Gaussian-like array:")

    def calculateGaussian(self, sigma, mu, size):
        x, y = np.meshgrid(np.linspace(-1,1,size), np.linspace(-1,1,size))
        d = np.sqrt(x*x + y*y)
        self.gaussian = np.exp(-((d-mu)**2 / (2.0 * sigma**2)))
    
    def applyGaussian(self, dartboard, point):
        if (self.gaussian == 0):
            print("Set gaussian")
            return
            
        


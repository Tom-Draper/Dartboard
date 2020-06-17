import numpy as np

class Gaussian():
    
    def __init__(self):
        self.gaussian = None

    def calculateGaussian(self, sigma, mu, size):
        """Calculates and returns the Gaussian kernel.

        Args:
            sigma (int): the standard deviation of the Gaussian distribution.
            mu (int): the mean of the Gaussian distribution.
            size (int): the size of one side of the kernel (size X size).
        """
        x, y = np.meshgrid(np.linspace(-1,1,size), np.linspace(-1,1,size))
        d = np.sqrt(x*x + y*y)
        self.gaussian = np.exp(-((d-mu)**2 / (2.0 * sigma**2)))
        self.gaussian = self.gaussian / np.sum(self.gaussian)

    def printGaussian(self):
        """Prints the values in the gaussian kernel to 2d.p."""
        
        for i in range(len(self.gaussian)):
            for j in range(len(self.gaussian)):
                print('{:4.2f}'.format(self.gaussian[i][j]), end='')
            print()
                
    
    def applyGaussian(self, dartboard, point):
        """Applies the Gaussian kernel to the point on the dartboard and returns
           the result.

        Args:
            dartboard (2D int array): Same dimensions as the dartboard image
                                      to represent the dartboard. Each element 
                                      holds the board value found on a dartboard 
                                      at that location.
            point (Tuple (int, int)): The point on the dartboard to apply the
                                      Gaussian kernel at.

        Returns:
            float: the value returned from applying the Gaussian kernel to the
                   point on the dartboard.
        """
        if (self.gaussian is int):
            print("Set gaussian")
            return
        
        # If gaussian even length, take top left of the central four as mid point
        y_start = int(point[0] - len(self.gaussian)/2)
        x_start = int(point[1] - len(self.gaussian[0])/2)
        
        # Take slice of dartboard of size of gaussian kernel, around the centre point
        db = dartboard[y_start:y_start + len(self.gaussian), x_start:x_start + len(self.gaussian)]
        # Multiply each point in dartboard by its corresponding gaussian value and sum all results
        # p value gives relative score of how good the current aim point is
        p = np.sum(db * self.gaussian)
        
        return p
        


import numpy as np
import random
from create_board import CreateDartboard
from gaussian import Gaussian


def createBoard(board):
    board.run()
    board.printBoardSection((600,600), 100)         

def printBoardSection(dartboard, centre, r):
    y_low = 0
    if centre[0]-r > 0:
        y_low = centre[0]-r
    
    y_high = len(dartboard)
    if centre[0]+r < len(dartboard):
        y_high = centre[0]+r
    
    x_low = 0
    if centre[1]-r > 0:
        x_low = centre[1]-r
        
    x_high = len(dartboard)
    if centre[1]+r < len(dartboard):
        x_high = centre[1]+r
    
    for i in range(y_low, y_high):
        for j in range(x_low, x_high):
            print(str(int(dartboard[i][j])).ljust(2), end=' ')
        print()

board = CreateDartboard('dartboard_img/dartboard.png')
# createBoard(board)

dartboard = np.load('dartboard.npy')

gaussian = Gaussian()
gaussian.calculateGaussian(1, 0, 150)
gaussian.printGaussian()

final = tuple(((len(dartboard), len(dartboard[1])), 0))  # (point, value)
for _ in range(100):
    complete = False
    point = (np.random.randint(200, 1000), np.random.randint(200, 1000))
    d = 10
    while not complete:
        value = gaussian.applyGaussian(dartboard, point)
        #print(point, value)
        
        up = (point[0] - d, point[1])
        down = (point[0] + d, point[1])
        right = (point[0], point[1] + d)
        left = (point[0], point[1] - d)
        up_right = (point[0] - d, point[1] + d)
        up_left = (point[0] - d, point[1] - d)
        down_right = (point[0] + d, point[1] + d)
        down_left = (point[0] + d, point[1] - d)
        
        up_value = gaussian.applyGaussian(dartboard, up)
        down_value = gaussian.applyGaussian(dartboard, down)
        right_value = gaussian.applyGaussian(dartboard, right)
        left_value = gaussian.applyGaussian(dartboard, left)
        up_right_value = gaussian.applyGaussian(dartboard, up_right)
        up_left_value = gaussian.applyGaussian(dartboard, up_left)
        down_right_value = gaussian.applyGaussian(dartboard, down_right)
        down_left_value = gaussian.applyGaussian(dartboard, down_left)
        
        value_to_point = {up_value : up, down_value : down, 
                          right_value : right, left_value : left, 
                          up_right_value : up_right, up_left_value : up_left, 
                          down_right_value : down_right, down_left_value : down_left}
        
        max_value = max([up_value, down_value, right_value, left_value, 
                         up_right_value, up_left_value, down_right_value, down_left_value])
        
        if value > max_value:  # Found max point
            optimum = value
            if (optimum > final[1]):  # Record max value found this time
                final = (point, optimum)
            complete = True
        else:
            point = value_to_point[max_value]  # Take the point with the maximum value

print(final)

printBoardSection(dartboard, final[0], 40)
print()
printBoardSection(dartboard, final[0], 20)
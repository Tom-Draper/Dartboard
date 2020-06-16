import numpy as np
from collections import namedtuple
from generate_dartboard import GenerateDartboard
from gaussian import Gaussian

def algorithm(dartboard, kernel_size):
    gaussian = Gaussian()
    # 127 and below for 20
    # 128 and above for 19
    # 128 -> drops a couple cm vertically down the board -> 173
    # 173 and above for top of 20
    
    gaussian.calculateGaussian(1, 0, kernel_size)
    
    Final = namedtuple('Final', 'point expected_value')
    final = Final(point=(len(dartboard), len(dartboard[1])), expected_value=0)
    for _ in range(200):
        complete = False
        point = (np.random.randint(200, 1000), np.random.randint(200, 1000))
        d = 2
        # Search for local maximum at this starting point
        while not complete:
            value = gaussian.applyGaussian(dartboard, point)
            
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
            

            if value >= max_value:  # If current point is highest in the local area
                if (value > final[1]):
                    final = Final(point=point, expected_value=value)  # Update the final value with improvement
                complete = True
            else:
                point = value_to_point[max_value]  # Take the point with the maximum value
    print(final)
    return final

def algorithmRange(dartboard, lower, higher, step=0):
    # Build list of tuples (kernel size, point (x,y), max value) for each kernel size in range
    results = [] 
    Result = namedtuple('Result', 'kernel_size  board_value final')
    for kernel_size in range(lower, higher, step):
        final = algorithm(dartboard, kernel_size)
        results.append(Result(kernel_size=kernel_size, board_value=db.board[final[0][0]][final[0][1]], final=final))
    
    for result in results:
        print(result)
    return results


board = GenerateDartboard('dartboard_img/dartboard.png')

#db = board.generate()
db = board.load('dartboard.npy')

algorithm(db.board, 5)
#algorithmRange(10, 20, 2)

#db.graphBoard(spacing=10)
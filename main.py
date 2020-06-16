import numpy as np
from generate_dartboard import GenerateDartboard
from gaussian import Gaussian


board = GenerateDartboard('dartboard_img/dartboard.png')
#dartboard = board.generate()

dartboard = board.load('dartboard.npy')

gaussian = Gaussian()
# 127 and below for 20
# 128 and above for 19
# 128 -> drops a couple cm vertically down the board -> 173
# 173 and above for top of 20
#kernel_size = 173
results = []
for kernel_size in range(2, 120, 2):
    print(kernel_size)
    gaussian.calculateGaussian(1, 0, kernel_size)

    final = tuple(((len(dartboard), len(dartboard[1])), 0))  # (point, value)
    for _ in range(200):
        complete = False
        point = (np.random.randint(200, 1000), np.random.randint(200, 1000))
        d = 2
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
            
            if value >= max_value:  # Found max point
                optimum = value
                if (optimum > final[1]):  # Record max value found this time
                    final = (point, optimum)
                complete = True
            else:
                point = value_to_point[max_value]  # Take the point with the maximum value
    results.append(tuple((kernel_size, dartboard[final[0][0]][final[0][1]], final)))

# print(final)
# print()
# board.printBoardSection(dartboard, final[0], 40)
for result in results:
    print(result)

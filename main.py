import numpy as np
from collections import namedtuple
from generate_dartboard import GenerateDartboard
from gaussian import Gaussian

def algorithm(dartboard, kernel_size, loops):
    """Takes a dartboard to search, the size of the kernel (K x K) to use and
       the number of loops to repeat the search. The algorithm selects a random 
       point on the dartboard. The gaussian distribution kernel is applied to 
       the area around the point to give a value of how optimal that point is to 
       aim for. The algorithm uses gradient descent and tests the nearby points, 
       taking the maximum. This is continued until a local maximum is found.
       This process is repeated by the input number of loops and the maximum
       value found is saved and returned.

    Args:
        dartboard (2D int array): Same dimensions as the dartboard image
                                  to represent the dartboard. Each element holds
                                  the board value found on a dartboard at that location.
        kernel_size (int): Size of the square kernel (kernel_size X kernel_size)
                           to apply during the algorithm.
        loops (int): The number of times to repeat a gradient descent process
                     and find the local maximum of a point. The more loops,
                     the higher the accuracy.

    Returns:
        Named tuple: (point, board_value, expected_value) 
                    - point: (int, int) Tuple of a board position (x, y)
                    - board_value: The value of the element in dartboard at 
                      that point
                    - expected_value: The value the returned from applying the 
                      kernel to that point
    """
    
    # 127 and below for 20
    # 128 and above for 19
    # 128 -> drops a couple cm vertically down the board -> 173
    # 173 and above for top of 20
    gaussian = Gaussian()
    gaussian.calculateGaussian(sigma=1, mu=0, size=kernel_size)
    
    print("Kernel size:", kernel_size)
    
    Final = namedtuple('Final', 'point board_value expected_value')
    final = Final(point=(len(dartboard), len(dartboard[1])), board_value=0, expected_value=0)
    for _ in range(loops):
        complete = False
        point = (np.random.randint(200, 1000), np.random.randint(200, 1000))
        d = 2
        # Search for local maximum at this starting point
        while not complete:
            value = gaussian.applyGaussian(dartboard, point)
            
            # Local points (x, y)
            up = (point[0] - d, point[1])
            down = (point[0] + d, point[1])
            right = (point[0], point[1] + d)
            left = (point[0], point[1] - d)
            up_right = (point[0] - d, point[1] + d)
            up_left = (point[0] - d, point[1] - d)
            down_right = (point[0] + d, point[1] + d)
            down_left = (point[0] + d, point[1] - d)
            
            # Expected values for each point
            up_value = gaussian.applyGaussian(dartboard, up)
            down_value = gaussian.applyGaussian(dartboard, down)
            right_value = gaussian.applyGaussian(dartboard, right)
            left_value = gaussian.applyGaussian(dartboard, left)
            up_right_value = gaussian.applyGaussian(dartboard, up_right)
            up_left_value = gaussian.applyGaussian(dartboard, up_left)
            down_right_value = gaussian.applyGaussian(dartboard, down_right)
            down_left_value = gaussian.applyGaussian(dartboard, down_left)
            
            # Mappings of expected value to the point that has that expected value
            value_to_point = {up_value : up, down_value : down, 
                            right_value : right, left_value : left, 
                            up_right_value : up_right, up_left_value : up_left, 
                            down_right_value : down_right, down_left_value : down_left}
            
            # Get max expected values from all local points
            max_value = max([up_value, down_value, right_value, left_value, 
                            up_right_value, up_left_value, down_right_value, down_left_value])
            
            if value >= max_value:  # If current point is highest in the local area
                if (value > final.expected_value):
                    # Update the final value with improvement
                    final = Final(point=point, board_value=dartboard[point[0]][point[1]], expected_value=value)
                    print(final)
                complete = True
            else:
                point = value_to_point[max_value]  # Take the point with the maximum value
    
    print(final)
    print("Displaying...")
    db.printBoardSection(centre=final[0], r=kernel_size)
    db.graphBoard(spacing=10, kernel_size=kernel_size, kernel_centre=final[0])

    return final

def algorithmRange(dartboard, lower, higher, step=1):
    """Applies the gradient descent algorithm for a range of different kernel sizes.

    Args:
        dartboard (2D int array): Same dimensions as the dartboard image
                                  to represent the dartboard. Each element holds
                                  the board value found on a dartboard at that location.
        lower (int): The lower bound of the kernel size to use.
        higher (int): The upper bound of the kernel size to use.
        step (int, optional): The step size between lower and higher. Defaults to 1.

    Returns:
        Dict (key = int, value = named tuple): kernel_size maps to a named tuple 
                                               (point, board_value, expected_value) 
    """
    # Build list of tuples (kernel size, point (x,y), max value) for each kernel size in range
    results = {}
    for kernel_size in range(lower, higher, step):
        final = algorithm(dartboard, kernel_size)
        results[kernel_size] = final
    
    print(results)
    return results


board = GenerateDartboard('dartboard_img/dartboard.png')

#db = board.generate()
db = board.load('dartboard.npy')

algorithm(db.board, 20)
#algorithmRange(db.board, 10, 20, 2)

#db.graphBoard(spacing=10)
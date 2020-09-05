import numpy as np
from collections import namedtuple
from generate_dartboard import GenerateDartboard
from gaussian import Gaussian


class FinalPoint(namedtuple('FinalPoint', ['point', 'point_value', 'expected_value', 'surrounding_values'])):
    __slots__ = ()
    
    def __str__(self):
        return f"Final Point: (x={self.point[0]}, y={self.point[1]}), point value={self.point_value}, expected value={round(self.expected_value, 2)}, surrounding values {list(map(lambda x : round(x, 2), self.surrounding_values))}"


class GradientDescent:
    def run(self, dartboard, kernel_size, loops, d=1, display="default", print_kernel=False, debug=False):
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
            loops (int): The number of times to repeat the entire gradient descent process
                        and find the local maximum of a point. The more loops,
                        the higher the accuracy.
            d (int): the distance away from a point to apply the kernel and 
                    test the values of surrounding points 

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
        gaussian.calcCircularGaussian(sigma=0.3, mu=0, size=kernel_size)
        
        print(f"Kernel: ({kernel_size}x{kernel_size})")
        if print_kernel:
            gaussian.printGaussian()
        
        # Final = namedtuple('Final', 'point point_value expected_value surrounding_values')
        # Default starting final (expected value at minimum)
        final_point = FinalPoint(point=(len(dartboard), len(dartboard[1])), point_value=0, expected_value=0, surrounding_values=[])
        # Stores the path of points taken to reach the current highest peak we've found so far
        final_gradient_descent_path = []

        # For each loop, a point is taken and it's local maxima is found
        # If it's local maxima is the largest we've seen so far, we store it in final
        for i in range(loops):
            # BEGIN A GRADIENT DESCENT
            
            # Chose random starting point inside dartboard
            point = (np.random.randint(200, 1000), np.random.randint(200, 1000))        
            # To build a list of points (x, y) that we have taken during this current 
            # gradient descent
            gradient_descent_path = []
            
            # Search for local maximum at this starting point
            while True:

                # Add 
                gradient_descent_path.append(point)
                
                # Get expected value of this point
                exp_value = gaussian.applyGaussian(dartboard, point)
                
                # Surrouding points (x, y), d spaces away
                up = (point[0] - d, point[1])
                down = (point[0] + d, point[1])
                right = (point[0], point[1] + d)
                left = (point[0], point[1] - d)
                up_right = (point[0] - d, point[1] + d)
                up_left = (point[0] - d, point[1] - d)
                down_right = (point[0] + d, point[1] + d)
                down_left = (point[0] + d, point[1] - d)
                
                # Expected values for each point
                up_exp_value = gaussian.applyGaussian(dartboard, up)
                down_exp_value = gaussian.applyGaussian(dartboard, down)
                right_exp_value = gaussian.applyGaussian(dartboard, right)
                left_exp_value = gaussian.applyGaussian(dartboard, left)
                up_right_exp_value = gaussian.applyGaussian(dartboard, up_right)
                up_left_exp_value = gaussian.applyGaussian(dartboard, up_left)
                down_right_exp_value = gaussian.applyGaussian(dartboard, down_right)
                down_left_exp_value = gaussian.applyGaussian(dartboard, down_left)
                
                # Mappings of expected value (int) to the point (x, y) that has that expected value
                value_to_point = {up_exp_value : up, down_exp_value : down, 
                                right_exp_value : right, left_exp_value : left, 
                                up_right_exp_value : up_right, up_left_exp_value : up_left, 
                                down_right_exp_value : down_right, down_left_exp_value : down_left}
                
                # Get the maximum expected value our of all the surrouding points
                max_exp_value = max([up_exp_value, down_exp_value, right_exp_value, left_exp_value, 
                                up_right_exp_value, up_left_exp_value, down_right_exp_value, down_left_exp_value])
                
                if exp_value >= max_exp_value: # If current point is a local maximum (reached a peak)
                    if (exp_value > final_point.expected_value):  # If peak we've landed on is higher than any peak we've reached before
                        # Update the final value with the improvement
                        final_point = FinalPoint(point=point, point_value=dartboard[point[0]][point[1]], expected_value=exp_value, surrounding_values=list(value_to_point.keys()))
                        final_gradient_descent_path = gradient_descent_path
                        if debug:
                            print("LOOP", i, "--> NEW IMPROVED MAXIMA:", final_point)
                            print("PATH TAKEN:", final_gradient_descent_path, "\n")
                    break
                else:
                    # Take the point with the maximum value to use next loop
                    point = value_to_point[max_exp_value]
                    gradient_descent_path.append(point)
        
        print("-"*40, "\n")
        print("GLOBAL MAXIMA FOUND:", final_point, "\nPATH TAKEN:", final_gradient_descent_path, "\n")
        
        if display == "default":
            # Display a kernel-sized section of the dartboard where the final point 
            # where the global maxima has been found
            if kernel_size < 50:
                print("Displaying to command line...")
                db.printBoardSection(centre=final_point.point, r=int(kernel_size/2))
            print("Displaying graph...")
            db.graphBoard(spacing=10, kernel_size=kernel_size, kernel_centres=final_gradient_descent_path)
        elif display == "graph":
            # Display the matplotlib graphed dartboard with kernel overlaying the 
            # position of the global maxima
            print("Displaying graph...")
            db.graphBoard(spacing=10, kernel_size=kernel_size, kernel_centres=final_gradient_descent_path)
        elif display == "cmdline":
            print("Displaying to command line...")
            db.printBoardSection(centre=final_point.point, r=int(kernel_size/2))

        return final_point

    def runOverRange(self, dartboard, k_lower, k_higher, loops, step=1, d=1, display="default"):
        """Applies the gradient descent algorithm for an inclusive range of different
        kernel sizes.

        Args:
            dartboard (2D int array): same dimensions as the dartboard image
                                    to represent the dartboard. Each element holds
                                    the board value found on a dartboard at that location.
            lower (int): the lower bound of the kernel size to use.
            higher (int): the upper bound of the kernel size to use (inclusive).
            step (int, optional): the step size between lower and higher. Defaults to 1.

        Returns:
            Dict (key = int, value = named tuple): kernel_size maps to a named tuple 
                                                (point, board_value, expected_value) 
        """
        # Build list of tuples (kernel size, point (x,y), max value) for each kernel size in range
        results = {}
        for kernel_size in range(k_lower, k_higher+1, step):
            final = self.run(dartboard, kernel_size, loops, d=d, display=display)
            results[kernel_size] = final
        
        print("\nRESULTS:")
        for kernel_size, result in results.items():
            print(f"Kernel size={kernel_size} --> {result}")
        return results


if __name__ == "__main__":
    board = GenerateDartboard('dartboard_img/dartboard.png')

    # Get board
    #db = board.generate()
    db = board.load('dartboard.npy')

    algorithm = GradientDescent()
    # Perform Gradient Descent
    # Triple 20
    # algorithm.run(db.board, kernel_size=126, loops=1000, d=5)
    # Triple 19
    # algorithm.run(db.board, kernel_size=127, loops=1000, d=5)
    algorithm.run(db.board, kernel_size=297, loops=1000, d=5)
    # algorithm.runOverRange(db.board, k_lower=150, k_higher=160, loops=500, step=1, display="none")
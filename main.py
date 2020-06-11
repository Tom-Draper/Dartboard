import numpy as np
from create_board import CreateDartboard
from gaussian import Gaussian


board = CreateDartboard('dartboard_img/dartboard.png')
board.run()
board.printBoardSection((600,600), 100)

dartboard = np.load('dartboard.npy')

gaussian = Gaussian()
gaussian.calculateGaussian(1, 0, 100)
gaussian.printGaussian()
gaussian.applyGaussian(dartboard, (600,600))

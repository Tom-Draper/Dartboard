import numpy as np
from create_board import CreateDartboard
from gaussian import Gaussian
from printer import Printer


create = CreateDartboard('dartboard_img/dartboard.png')
create.run()
dartboard = np.load('dartboard.npy')
p = Printer()
p.printBoardSection(dartboard, 600,600)
gaussian = Gaussian()
gaussian.calculateGaussian(1, 0, 10)
gaussian.applyGaussian(dartboard, (600,600))

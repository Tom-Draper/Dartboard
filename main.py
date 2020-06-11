import numpy as np
from create_board import CreateDartboard
from gaussian import Gaussian


create = CreateDartboard('dartboard_img/dartboard.png')
create.run()
dartboard = np.load('dartboard.npy')
gaussian = Gaussian()
gaussian.calculateGaussian(1, 0, 100)
gaussian.applyGaussian(dartboard, (600,600))

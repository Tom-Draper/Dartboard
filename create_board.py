import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread('dartboard_img/dartboard.png')

dartboard = np.zeros(shape=img.shape[:2])
print(img.shape)
print(dartboard.shape)

for img_row in img:
    for pixel in img_row:
        if pixel[0] != 0:
            print()

#imgplot = plt.imshow(img)
#plt.show()
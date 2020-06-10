import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread('dartboard_img/dartboard.png')

dartboard = np.zeros(shape=img.shape[:2])

# Get value of the border colour around the dartboard
outside_border_col = 0
for pixel in img[0]:
    if pixel[0] != 0:
        outside_border_col = pixel[0]
        break

# Bullseye
centre_pt = tuple((int(img.shape[0]/2), int(img.shape[1]/2)))  # x, y

# Scans the radius around the centre_pt and adds the updates dartboard with the 
# board value at equivalent position where the input colour is found 
def addValue(img, centre_pt, radius, colour, board_value, dartboard):
    for i in range(centre_pt[0] - radius, centre_pt[0] + radius):
        for j in range(centre_pt[1] - radius, centre_pt[1] + radius):
            if (img[i][j] == colour).all():
                dartboard[i][j] = board_value

def createInnerBullseye(img, centre_pt, dartboard):
    # Get the colour of inner bullseye
    red_col = img[centre_pt[0]][centre_pt[1]]
    print(red_col)
    
    # Calculate inner bullseye radius
    r = 1
    while True:
        if (img[centre_pt[0]][centre_pt[1] + r] == red_col).all():
            r += 1
        else:
            r += 1  # Include centre
            break
    
    addValue(img, centre_pt, r, red_col, 50, dartboard)


def outerBullseyeRadius(img, centre_pt, green_col):
    r = 1
    # Add distance from centre to first green pixel 
    while True:
        if (img[centre_pt[0]][centre_pt[1] + r] != green_col).all():
            r += 1
    
    # Add distance from first green pixel to last green pixel
    while True:
        if (img[centre_pt[0]][centre_pt[1] + r] == green_col).all():
            r += 1
        else:
            r += 1  # Include centre
            break
    return r

def createOuterBullseye(img, centre_pt, dartboard):
    # Get the colour of outer bullseye
    green_col = 0
    for i in range(centre_pt[0]):
        pixel = img[centre_pt[0]][centre_pt[1] + i]
        print(pixel)
        if pixel[0] == 0:
            green_col = pixel
            break
    
    # Calculute outer bullseye radius
    r = outerBullseyeRadius()
    
    addValue(img, centre_pt, r, green_col, 25, dartboard)


def allocateWire(dartboard, point):
    for r in range(100):
        local = [dartboard[point[0] + r][point[1]],
                 dartboard[point[0] - r][point[1]],
                 dartboard[point[0]][point[1] + r],
                 dartboard[point[0]][point[1] - r],
                 dartboard[point[0] + r][point[1] + r],
                 dartboard[point[0] + r][point[1] - r],
                 dartboard[point[0] - r][point[1] + r],
                 dartboard[point[0] - r][point[1] - r]]
        
        if any(local):
            local = local(filter(lambda v : v != 0, local))  # Remove zeros
            if len(local) == 1:
                dartboard[point[0][point[1]]] = local[0]
            else:
                dartboard[point[0][point[1]]] = np.random.choice(local)


def bullseyeWire(dartboard):
    r = outerBullseyeRadius(img, centre_pt, green_col)
    
    for i in range(centre_pt[0] - radius, centre_pt[0] + radius):
        for j in range(centre_pt[1] - radius, centre_pt[1] + radius):
            if dartboard[i][j] == 0:
                allocateWire(dartboard, tuple((i, j)))

def createDartboard():
    createInnerBullseye(img, centre_pt, dartboard)
    createOuterBullseye(img, centre_pt, dartboard)
    allocateInnerOuterWire(dartboard, point)

#imgplot = plt.imshow(img)
#plt.show()
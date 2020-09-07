# Dartboard

## Hypothesis
There exists a standard deviation of dart throwing accuracy that, once exceeded, no longer makes aiming directly for the triple 20 position optimal.

## Experiment
The idea behind this experiment is to locate the global maxima on the dartboard (i.e. the optimal position to aim) given a standard distribution of a dart throw. To do this I needed a large 2D array filled with dartboard values (e.g. 50 in the centre for bullseye, 60 at the triple 60 position etc.) which I could apply a 2D Guassian kernel of a given standard deviation to give an indication of the expected value at that position on the dartboard. I could then use gradient descent to find a local maxima, and repeat this, recording the highest expected value found, until I was confident I had found the global maxima on the dartboard.   

The 2D array of dartboard values that would represent the dartboard needed to be very large, as a real dartboard has a continuous number of available positions to hit. Representing a dartboard as an array would be quantising the dartboard into discrete slots to hit, therefore the larger the dartboard, the more accurate my experiment could be. As it would be tedious to manually enter dartboard values in the correct position, I took an image of a dartboard and replaced the pixel values with the correct dartboard value using the GenerateDartboard class. This class uses the image pixel colours and positions to insert the values. The positions on the image that are occupied by a dartboard wire (the separation between two segments on the dartboard), were given the same value as the nearest available value to that point. The result gave me a 1200 x 1200 array with a circle of dartboard values, and zeros filling the areas outside of the dartboard.

I then built the circular, normalised 2D kernel array to apply to the dartboard at a given position. Each element in the kernel holds a value less than 1. The elements in the centre of the kernel have the largest values, as the single most frequent place a player will hit is the exact location they are aiming at. The values get smaller as you get further away from the centre point. Applying the kernel to a point on the dartboard array multiplies each value in the kernel with its corresponding value on the dartboard and sums up all the results to give a single value that represents how good that dartboard position is to aim for. As the kernel is normalised, it represents the average value a player (with the throwing accuracy standard deviation equal to that of the kernel) should expect to get from aiming at that point on the dartboard. Due to the size of the image, the kernel size cannot have a size exceeding 295 as the radius of the kernel would exceed the width of the border of zeros around the circle of dartboard values, meaning the kernel does not have enough room to be applied to the edge value of the dartboard.

| ![kernel example](https://user-images.githubusercontent.com/41476809/92311923-93700d00-efb3-11ea-9ea3-014df586cfad.png) | 
|:--:| 
| Kernel example (250x250) |

Now I had the dartboard and can apply the kernel to any point to get its expected value, I used a gradient descent algorithm to find a global maxima. The algorithm applies the kernel to a random point to get the expected value of that point, and then again to each nearby point around it. The nearby point with the highest expected value is taken and the nearby points are tested again. This continues until the algorithm reaches a point where no points nearby have a higher expected value than the current point. This point is a local maxima. Each point on the dartboard has its own local maxima that it travels to. The program repeats running gradient descent on different points within the dartboard and records the best local maxima value found so far until it is confident it has found the global maxima on the dartboard. This is the optimal point to aim for on the dartboard given the standard deviation of the kernel.

Throughout this program, I have make the assumption that distribution of darts thrown follows a perfect 2D Gaussian distribution with the centre the point the player was aiming for. In reality, the distribution would most likely be eliptical running either vertically or horizontally, depending on the player's throw style. The accuracy/experience of a player would therefore increase or decrease the standard deviation of this distribution.

## Results

The following results show the highest expected value (global maxima) found given a kernel size. It shows the path taken by the gradient descent to reach that maxima. For each of these results, d (the distance away from current point to test the expected value of nearby points) is 5.   
As shown down below, kernel sizes up to 296 give a maxima centered on or near the triple 20 position. Kernel sizes of 297 and above moved the optimal position to aim to near the triple 19.

### Converting kernel size in pixels --> standard deviation of a player's throw in mm

For these results to be useful, we need to be able to convert a particular kernel size to a players accuracy and vice versa. Doing this will allow a player to record the standard deviation of x amount of throws, and select the equivalent kernel size. Running the algorithm with the given kernel size will give them the optimum location for that specific player to aim for.    
Kernel sizes are described in the form of the the number of elements (dartboard values) they cover (e.g. 50x50). When creating the gaussian kernel, I experimented with different values of sigma (standard deviation) until the entire Gaussian distribution could fit on the kernel whilst being as large as possible (as shown in the above image). The standard deviation value I used was 0.3. This means a central ring (of radius 0.3 * the kernel size) contains all points within 1 standard deviation of the mean.   
Now to find the length of one pixel in mm. I measured the width of the inner dartboard ring that contains dartboard values to be 338mm +- 1mm. The dartboard image used was 1200x1200 pixels, but the width of the area that contains dartboard values is 904 pixels. Therefore each pixel must be 338/904 = 0.373894mm in length (6 d.p.).    
This means for a 50x50 kernel, 1 standard deviation would have a width of 0.3 * 50 * 2 = 30 pixels, which is equivalent to 30 * 0.373894 = 11.22mm (2 d.p.).

Formula: s.d. used for kernel (0.3 hard-coded) * kernel size in pixels * 2 (to give diameter) * length of one pixel in mm (found to be 0.373894)

68% of darts should land within one standard deviation of the mean. To find the standard deviation of your throw:
- Choose a position on the dartboard to aim at (this will be the mean position)
- Create a sheet of paper that is large enough to stick to the front of the dartboard, with a layer of strong tape (e.g. electrical tape) covering the paper
- Stick this material to the front of the dartboard and create a recognisable hole for the mean position you're going to aim for
- Throw 100 darts at that position
- Count the outer most 32 dart holes and measure the distance in mm from the mean position (point you were aiming at) to the 32nd outermost dart hole. This is your standard deviation.

### Kernel = (50x50)
Player's dart throw has 11.2mm standard deviation.
![50-kernel](https://user-images.githubusercontent.com/41476809/92312059-35442980-efb5-11ea-9a15-bb23715bfb27.png)

### Kernel = (75x75)
Player dart throw has 16.83mm standard deviation. 
![75-kernel](https://user-images.githubusercontent.com/41476809/92312093-8f44ef00-efb5-11ea-838f-0c870ff4d293.png)

### Kernel = (100x100)
Player dart throw has 22.43mm standard deviation. 
![100-kernel](https://user-images.githubusercontent.com/41476809/92312130-d59a4e00-efb5-11ea-8fa3-d04b5de215f0.png)

### Kernel = (150x150)
Player dart throw has 33.65mm standard deviation. 
![150-kernel](https://user-images.githubusercontent.com/41476809/92312155-11cdae80-efb6-11ea-89b1-10066f0f8d1e.png)

### Kernel = (200x200)
Player dart throw has 44.87mm standard deviation. 
![200-kernel](https://user-images.githubusercontent.com/41476809/92312198-7db01700-efb6-11ea-892e-8fd199ad2c2b.png)

### Kernel = (250x250)
Player dart throw has 56.08mm standard deviation. 
![250-kernel](https://user-images.githubusercontent.com/41476809/92312255-ea2b1600-efb6-11ea-87ed-3566933d23fc.png)

### Kernel = (290x290)
Player dart throw has 65.06mm standard deviation. 
![290-kernel](https://user-images.githubusercontent.com/41476809/92312394-ffed0b00-efb7-11ea-917e-0d0f4a5e90c7.png)

### Kernel = (296x296)
Player dart throw has 66.40mm standard deviation. 
![296-kernel](https://user-images.githubusercontent.com/41476809/92312493-f021f680-efb8-11ea-9526-89e8fa7c4ec5.png)

### Kernel = (297x297)
Player dart throw has 66.63mm standard deviation. 
![297-kernel](https://user-images.githubusercontent.com/41476809/92312528-6292d680-efb9-11ea-8378-6459e96be82d.png)

# Dartboard

## Hypothesis
There exists a standard deviation of dart throwing accuracy that, once exceeded, no longer makes aiming directly for the triple 20 position optimal.

## Experiment
The idea behind this experiment is to locate the global maxima on the dartboard (i.e. the optimal position to aim) given a standard distribution of a dart throw. To do this I needed a large 2D array filled with dartboard values (e.g. 50 in the centre for bullseye, 60 at the triple 60 position etc.) which I could apply a 2D Guassian kernel of a given standard deviation to give an indication of the expected value at that position on the dartboard. I could then use gradient descent to find a local maxima, and repeat this, recording the highest expected value found, until I was confident I had found the global maxima on the dartboard.   

The 2D array of dartboard values that would represent the dartboard needed to be very large, as a real dartboard has a continuous number of available positions to hit. Representing a dartboard as an array would be quantising the dartboard into discrete slots to hit, therefore the larger the dartboard, the more accurate my experiment could be. As it would be tedious to manually enter dartboard values in the correct position, I took an image of a dartboard and replaced the pixel values with the correct dartboard value using the GenerateDartboard class. This class uses the image pixel colours and positions to insert the values. The positions on the image that are occupied by a dartboard wire (the separation between two segments on the dartboard), were given the same value as the nearest available value to that point. The result gave me a 1200 x 1200 array with a circle of dartboard values, and zeros filling the areas outside of the dartboard.

I then built the circular, normalised 2D kernel array to apply to the dartboard at a given position. Each element in the kernel holds a value less than 1. The elements in the centre of the kernel have the largest values, as the single most frequent place a player will hit is the exact location they are aiming at. The values get smaller as you get further away from the centre point. Applying the kernel to a point on the dartboard array multiplies each value in the kernel with its corresponding value on the dartboard and sums up all the results to give a single value that represents how good that dartboard position is to aim for. As the kernel is normalised, it represents the average value a player (with the throwing accuracy standard deviation equal to that of the kernel) should expect to get from aiming at that point on the dartboard. Due to the size of the image, the kernel size cannot have a size exceeding 295 as the radius of the kernel would exceed the width of the border of zeros around the circle of dartboard values, meaning the kernel does not have enough room to be applied to the edge value of the dartboard.

![kernel](https://user-images.githubusercontent.com/41476809/92282774-3b270580-eef6-11ea-8561-531faa88036e.png)

Now I had the dartboard and can apply the kernel to any point to get its expected value, I used a gradient descent algorithm to find a global maxima. The algorithm applies the kernel to a random point to get the expected value of that point, and then again to each nearby point around it. The nearby point with the highest expected value is taken and the nearby points are tested again. This continues until the algorithm reaches a point where no points nearby have a higher expected value than the current point. This point is a local maxima. Each point on the dartboard has its own local maxima that it travels to. The program repeats running gradient descent on different points within the dartboard and records the best local maxima value found so far until it is confident it has found the global maxima on the dartboard. This is the optimal point to aim for on the dartboard given the standard deviation of the kernel.

Throughout this program, I have make the assumption that distribution of darts thrown follows a perfect 2D Gaussian distribution with the centre the point the player was aiming for. In reality, the distribution would most likely be eliptical running either vertically or horizontally, depending on the player's throw style. The accuracy/experience of a player would therefore increase or decrease the standard deviation of this distribution.

## Results

The following results show the highest expected value (global maxima) found given a kernel size. It shows the path taken by the gradient descent to reach that maxima. For each of these results, d (the distance away from current point to test the expected value of nearby points) is 5.   
As shown down below, kernel sizes of 217 and above moved the optimal position from around the triple 20 to near the triple 19. 

### Kernel = (50x50)
![50-kernel](https://user-images.githubusercontent.com/41476809/92283084-01a2ca00-eef7-11ea-9e5b-a5abdedc3af7.png)

### Kernel = (75x75)
![75-kernel](https://user-images.githubusercontent.com/41476809/92283296-82fa5c80-eef7-11ea-9e5c-22810f526c00.png)

### Kernel = (100x100)
![100-kernel](https://user-images.githubusercontent.com/41476809/92283425-c2c14400-eef7-11ea-88c8-db46293c7839.png)

### Kernel = (150x150)
![150-kernel](https://user-images.githubusercontent.com/41476809/92283594-1e8bcd00-eef8-11ea-89db-5f0660b090c3.png)

### Kernel = (200x200)
![200-kernel](https://user-images.githubusercontent.com/41476809/92284640-4ed46b00-eefa-11ea-9e7a-4fa2518f48b2.png)

### Kernel = (210x210)
![210-kernel](https://user-images.githubusercontent.com/41476809/92284743-9b1fab00-eefa-11ea-8820-a8ad91fd0e7c.png)

### Kernel = (215x215)
![215-kernel](https://user-images.githubusercontent.com/41476809/92284848-dd48ec80-eefa-11ea-8f08-98cde4a6ec79.png)

### Kernel = (216x216)
![216-kernel](https://user-images.githubusercontent.com/41476809/92285074-52b4bd00-eefb-11ea-8f4f-99cb77a7188b.png)

### Kernel = (217x217)
![217-kernel](https://user-images.githubusercontent.com/41476809/92285351-fb631c80-eefb-11ea-80bb-b755bc8bc7cf.png)

### Kernel = (218x218)
![218-kernel](https://user-images.githubusercontent.com/41476809/92285533-7593a100-eefc-11ea-87fc-79108da919ce.png)

### Kernel = (250x250)
![250-kernel](https://user-images.githubusercontent.com/41476809/92285677-cf946680-eefc-11ea-9d50-a46b4ed432e0.png)

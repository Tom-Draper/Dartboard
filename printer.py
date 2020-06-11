import numpy as np

class Printer:
    def printBoardSection(self, dartboard, centre, r):
        for i in range(centre[0]-r, centre[0]+r):
            for j in range(centre[1]-r, centre[1]+r):
                print(str(int(dartboard[i][j])).ljust(2), end=' ')
            print()


dartboard = np.load('dartboard.npy')
dartboard2 = np.load('dartboard2.npy')

p = Printer()
p.printBoardSection(dartboard, (600,600), 30)
#printBoardSection(dartboard, (200,600), 55)
# printBoardSection(dartboard, (500,200), 55)

printBoardSection(dartboard, (530,180), 30)
#printBoardSection(dartboard, (1000,600), 55)
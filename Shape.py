from Tetrominoe import Tetrominoe
import random

class Shape(object):

    def __init__(self):

        # self.coords = [[0, 0] for i in range(4)]
        # self.coords = [[0, 0] for i in range(5)]
        self.coords = [[]]
        self.pieceShape = Tetrominoe.NoShape
        self.setShape(Tetrominoe.NoShape)
        self.shapeSize = 0


    def shape(self):
        '''returns shape'''
        return self.pieceShape

    # create shape
    def setShape(self, shape):
        '''sets a shape'''

        table = Tetrominoe.coordsTable[shape]
        self.coords.clear()
        for i in range(len(table)):
            # for j in range(2):
            #     self.coords[i][j] = table[i][j]
            tempCoord = []
            for j in range(len(table[i])):
                tempCoord.append(table[i][j])
            self.coords.append(tempCoord)

        self.pieceShape = shape
        self.shapeSize = len(table)


    def setRandomShape(self):
        '''chooses a random shape'''
        # self.setShape(random.randint(1, 7))
        self.setShape(random.randint(1, len(Tetrominoe.coordsTable) -1 ))
        # self.setShape(8)


    def x(self, index):
        '''returns x coordinate'''
        return self.coords[index][0]


    def y(self, index):
        '''returns y coordinate'''
        return self.coords[index][1]


    def setX(self, index, x):
        '''sets x coordinate'''
        self.coords[index][0] = x


    def setY(self, index, y):
        '''sets y coordinate'''
        self.coords[index][1] = y


    def minX(self):
        '''returns min x value'''
        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])
        return m


    def maxX(self):
        '''returns max x value'''
        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])
        return m


    def minY(self):
        '''returns min y value'''
        # m = self.coords[0][1]
        m = 0
        for i in range(self.shapeSize):
            m = min(m, self.coords[i][1])
        return m


    def maxY(self):
        '''returns max y value'''
        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])
        return m


    def rotateLeft(self):
        '''rotates shape to the left'''

        result = Shape()
        result.pieceShape = self.pieceShape
        result.shapeSize = self.shapeSize
        result.coords = [[0, 0] for i in range(len(self.coords))]

        for i in range(self.shapeSize):
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))
        return result


    def rotateRight(self):
        '''rotates shape to the right'''

        result = Shape()
        result.pieceShape = self.pieceShape
        result.shapeSize = self.shapeSize
        result.coords = [[0, 0] for i in range(len(self.coords))]

        for i in range(self.shapeSize):
            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))
        return result
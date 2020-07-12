import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QColor


class Example(QMainWindow):

    coordsTable = (
        ((0, 0),     (0, 0),     (0, 0),     (0, 0)),
        ((0, -1),    (0, 0),     (-1, 0),    (-1, 1)),  # z-shape
        ((0, -1),    (0, 0),     (1, 0),     (1, 1)),
        ((0, -1),    (0, 0),     (0, 1),     (0, 2)),
        ((-1, 0),    (0, 0),     (1, 0),     (0, 1)),
        ((0, 0),     (1, 0),     (0, 1),     (1, 1)),   # SquareShape
        ((-1, -1),   (0, -1),    (0, 0),     (0, 1)),
        ((1, -1),    (0, -1),    (0, 0),     (0, 1)),
        ((-1, -1),   (1, -1),    (-1, 1),     (1, 1), (0,0))   # customer shape
    )

    BoardWidth = 20
    BoardHeight = 20


    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):               
        self.statusBar().showMessage('Ready')
        self.setGeometry(1000, 200, 500, 500)
        self.setWindowTitle('Statusbar')
        self.show()

    def paintEvent(self, event):
        '''paints all shapes of the game'''

        painter = QPainter(self)
        rect = self.contentsRect()
        boardTop = rect.bottom() - self.BoardHeight * self.squareHeight()

        # for i in range(len(coordsTable[8])):
        self.drawSquare(painter, 1, 1, 3)
    
    def drawSquare(self, painter, x, y, shape):
        '''draws a square of a shape'''

        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00, 0xCCFF66]

        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2, 
            self.squareHeight() - 2, color)

        # painter.setPen(color.lighter())
        # painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        # painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        # painter.setPen(color.darker())
        # painter.drawLine(x + 1, y + self.squareHeight() - 1,
        #     x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        # painter.drawLine(x + self.squareWidth() - 1, 
        #     y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)
    
    
    def squareWidth(self):
        '''returns the width of one square'''
        # return 200
        sw = self.contentsRect().width() // self.BoardWidth
        print (self.contentsRect().width(), self.BoardWidth)
        return self.contentsRect().width() // self.BoardWidth


    def squareHeight(self):
        '''returns the height of one square'''
        # return 200
        return self.contentsRect().height() // self.BoardHeight


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
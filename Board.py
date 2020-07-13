from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from Tetrominoe import Tetrominoe
from Shape import Shape

class Board(QFrame):
    # 创建了一个自定义信号msg2Statusbar，当我们想往statusbar里显示信息的时候，发出这个信号就行了
    msg2Statusbar = pyqtSignal(str)
    # 这些是Board类的变量。BoardWidth和BoardHeight分别是board的宽度和高度。Speed是游戏的速度，每300ms出现一个新的方块
    BoardWidth = 10
    BoardHeight = 25
    # BoardWidth = 20
    # BoardHeight = 50
    Speed = 300

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()


    def initBoard(self):     
        '''initiates board'''

        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False

        #在initBoard()里初始化了一些重要的变量。self.board定义了方块的形状和位置，取值范围是0-7
        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()

    #shapeAt()决定了board里方块的的种类
    def shapeAt(self, x, y):
        '''determines shape at the board position'''

        return self.board[(y * Board.BoardWidth) + x]


    def setShapeAt(self, x, y, shape):
        '''sets a shape at the board'''

        self.board[(y * Board.BoardWidth) + x] = shape
    

    # board的大小可以动态的改变。所以方格的大小也应该随之变化。
    # squareWidth()计算并返回每个块应该占用多少像素--也
    # 即Board.BoardWidth
    def squareWidth(self):
        '''returns the width of one square'''

        return self.contentsRect().width() // Board.BoardWidth


    def squareHeight(self):
        '''returns the height of one square'''

        return self.contentsRect().height() // Board.BoardHeight
    

    def start(self):
        '''starts game'''

        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clearBoard()

        self.msg2Statusbar.emit(str(self.numLinesRemoved))

        self.newPiece()
        self.timer.start(Board.Speed, self)


    # pause()方法用来暂停游戏，停止计时并在statusbar上显示一条信息
    def pause(self):
        '''pauses game'''

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.msg2Statusbar.emit("paused")

        else:
            self.timer.start(Board.Speed, self)
            self.msg2Statusbar.emit(str(self.numLinesRemoved))

        self.update()


    # 渲染是在paintEvent()方法里发生的QPainter负责PyQt5里所有低级绘画操作
    def paintEvent(self, event):
        '''paints all shapes of the game'''

        painter = QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()

        # 渲染游戏分为两步。第一步是先画出所有已经落在最下面的的图，这些保存在self.board里。可以使用shapeAt()查看这个这个变量
        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.shapeAt(j, Board.BoardHeight - i - 1)

                if shape != Tetrominoe.NoShape:
                    self.drawSquare(painter,
                        rect.left() + j * self.squareWidth(),
                        boardTop + i * self.squareHeight(), shape)

        # 第二步是画出正在下落的方块
        if self.curPiece.shape() != Tetrominoe.NoShape:

            for i in range(self.curPiece.shapeSize):

                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                    boardTop + (Board.BoardHeight - y - 1) * self.squareHeight(),
                    self.curPiece.shape())


    def keyPressEvent(self, event):
        '''processes key press events'''

        if not self.isStarted or self.curPiece.shape() == Tetrominoe.NoShape:
            super(Board, self).keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return

        # # 在keyPressEvent()方法获得用户按下的按键。如果按下的是右方向键，就尝试把方块向右移动，说尝试是因为有可能到边界不能移动了
        elif key == Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)

        elif key == Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)

        elif key == Qt.Key_Down:
            # self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)
            self.oneLineDown()

        # 上方向键是把方块向左旋转一下
        elif key == Qt.Key_Up:
            self.tryMove(self.curPiece.rotateLeft(), self.curX, self.curY)

        # 空格键会直接把方块放到底部 Key_Space
        elif key == Qt.Key_Space:
            self.dropDown()

        # D键是加速一次下落速度
        elif key == Qt.Key_D:
            self.oneLineDown()

        else:
            super(Board, self).keyPressEvent(event)


    # 在计时器事件里，要么是等一个方块下落完之后创建一个新的方块，要么是让一个方块直接落到底（move a falling piece one line down）
    def timerEvent(self, event):
        '''handles timer event'''

        if event.timerId() == self.timer.timerId():

            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()
            else:
                self.oneLineDown()

        else:
            super(Board, self).timerEvent(event)


    # clearBoard()方法通过Tetrominoe.NoShape清空broad
    def clearBoard(self):
        '''clears shapes from the board'''

        for i in range(Board.BoardHeight * Board.BoardWidth):
            self.board.append(Tetrominoe.NoShape)
    
    def dropDown(self):
        '''drops down a shape'''

        newY = self.curY

        while newY > 0:

            if not self.tryMove(self.curPiece, self.curX, newY - 1):
                break

            newY -= 1

        self.pieceDropped()


    def oneLineDown(self):
        '''goes one line down with a shape'''

        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped()


    def pieceDropped(self):
        '''after dropping shape, remove full lines and create new shape'''

        # for i in range(self.curPiece.shapeSize):
        for i in range(self.curPiece.shapeSize):
            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.removeFullLines()

        if not self.isWaitingAfterLine:
            self.newPiece()


    # 如果方块碰到了底部，就调用removeFullLines()方法，找到所有能
    # 消除的行消除它们。消除的具体动作就是把符合条件的行消除掉之后，
    # 再把它上面的行下降一行。注意移除满行的动作是倒着来的，因为我
    # 们是按照重力来表现游戏的，如果不这样就有可能出现有些方块浮在
    # 空中的现象
    def removeFullLines(self):
        '''removes all full lines from the board'''

        numFullLines = 0
        rowsToRemove = []

        for i in range(Board.BoardHeight):

            n = 0
            for j in range(Board.BoardWidth):
                if not self.shapeAt(j, i) == Tetrominoe.NoShape:
                    n = n + 1

            if n == 10:
                rowsToRemove.append(i)

        rowsToRemove.reverse()


        for m in rowsToRemove:

            for k in range(m, Board.BoardHeight):
                for l in range(Board.BoardWidth):
                        self.setShapeAt(l, k, self.shapeAt(l, k + 1))

        numFullLines = numFullLines + len(rowsToRemove)

        if numFullLines > 0:

            self.numLinesRemoved = self.numLinesRemoved + numFullLines
            self.msg2Statusbar.emit(str(self.numLinesRemoved))

            self.isWaitingAfterLine = True
            self.curPiece.setShape(Tetrominoe.NoShape)
            self.update()


    # newPiece()方法是用来创建形状随机的方块。如果随机的方块
    # 不能正确的出现在预设的位置，游戏结束
    def newPiece(self):
        '''creates a new shape'''

        self.curPiece = Shape()
        self.curPiece.setRandomShape()
        self.curX = Board.BoardWidth // 2 + 1
        self.curY = Board.BoardHeight - 1 + self.curPiece.minY()

        if not self.tryMove(self.curPiece, self.curX, self.curY):

            self.curPiece.setShape(Tetrominoe.NoShape)
            self.timer.stop()
            self.isStarted = False
            self.msg2Statusbar.emit("Game over")


    # tryMove()是尝试移动方块的方法。如果方块已经到达board的边缘或者遇到了其他方块，就返回False。否则就把方块下落到想要
    def tryMove(self, newPiece, newX, newY):
        '''tries to move a shape'''

        for i in range(self.curPiece.shapeSize):

            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)

            if x < 0 or x >= Board.BoardWidth or y < 0 or y >= Board.BoardHeight:
                return False

            if self.shapeAt(x, y) != Tetrominoe.NoShape:
                return False

        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.update()

        return True


    def drawSquare(self, painter, x, y, shape):
        '''draws a square of a shape'''        

        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00,
                      0xCCFF66, 0x66CCFF]

        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2, 
            self.squareHeight() - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
            x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1, 
            y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)
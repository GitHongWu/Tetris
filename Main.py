from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget
import sys
from Board import Board


class Tetris(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):    
        '''initiates application UI'''

        #创建了一个Board类的实例，并设置为应用的中心组件
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)

        # 创建一个statusbar来显示三种信息：消除的行数，游戏暂停状
        # 态或者游戏结束状态。msg2Statusbar是一个自定义的信号，用
        # 用在（和）Board类（交互）
        # showMessage()方法是一个内建的，用来在statusbar上显示信息的方法
        self.statusbar = self.statusBar()        
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        self.tboard.start()

        self.resize(180, 380)
        self.center()
        self.setWindowTitle('Tetris')        
        self.show()

    '''centers the window on the screen'''
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)




if __name__ == '__main__':

    app = QApplication([])
    tetris = Tetris()    
    sys.exit(app.exec_())
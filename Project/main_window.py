from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPixmap
import sys

from sim_move_demo import SimMoveDemo


class MainWindow(QWidget):
    MainWindowHeight = 1080
    MainWindowWidth = 1920

    def __init__(self):
        super().__init__()
        self.initUI()

    def run(self):
        self.smd = SimMoveDemo()

    def quit(self):
        self.close();

    def initUI(self):
        self.resize(self.MainWindowHeight, self.MainWindowWidth)
        self.center()

        self.setWindowTitle('Donkey Kong')

        self.setMinimumHeight(self.MainWindowHeight)
        self.setMinimumWidth(self.MainWindowWidth)
        self.setMaximumHeight(self.MainWindowHeight)
        self.setMaximumWidth(self.MainWindowWidth)
        self.setStyleSheet("background-color: black;")

        b1 = QtWidgets.QPushButton(self)
        b1.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red;font-size: 26px; font-family: Segoe Script;");
        b1.setText("START GAME")
        b1.setGeometry(200, 400, 350, 50)
        b1.clicked.connect(self.run)

        b2 = QtWidgets.QPushButton(self)
        b2.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red;font-size: 26px; font-family: Segoe Script;");
        b2.setText("QUIT")
        b2.setGeometry(200, 500, 350, 50)
        b2.clicked.connect(self.quit)

        self.logoPic = QPixmap('donkey_logo.png')
        self.logoLabel = QtWidgets.QLabel(self)
        self.logoLabel.setPixmap(self.logoPic)
        self.logoLabel.move(880, 120)

        self.monkeyPic = QPixmap('donkey_monkey.png')
        self.monkeyLabel = QtWidgets.QLabel(self)
        self.monkeyLabel.setPixmap(self.monkeyPic)
        self.monkeyLabel.move(970, 300)

        self.showMaximized()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)







if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

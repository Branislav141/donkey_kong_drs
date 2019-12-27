from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPixmap, QMovie
import sys


class Barrel(QFrame):

    barrelPositionX = 0
    barrelPositionY = 0
    barrelIdlePicture = 0
    barrelLabel = 0
    isCreated = 0
    setImage = 1


    def __init__(self, parent, x, y):
        super().__init__(parent)

        self.initBarrel(parent, x, y)


    def initBarrel(self, parent, x, y):
        self.barrelIdlePicture = QPixmap("images\items\\barrel.png")
        self.barrelLabel = QLabel(parent)
        self.barrelLabel.setGeometry(x, y, 50, 50)


    def updatePosition(self, x, y):
        if self.setImage == 1:
            self.barrelLabel.setPixmap(self.barrelIdlePicture)
        self.barrelPositionX = x
        self.barrelPositionY = y
        self.barrelLabel.move(x, y)

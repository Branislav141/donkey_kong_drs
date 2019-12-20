from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPixmap, QMovie
import sys, random
import time

class Gorilla(QFrame):
    gorillaPositionX = 0
    gorillaPositionY = 0
    gorillaIdle = 0
    gorillaRunRight = 0
    gorillaRunLeft = 0
    gorillaRunningDirection = "right"

    gorillaLabel = 0



    def __init__(self, parent):
        super().__init__(parent)

        self.initGorilla(parent)


    def initGorilla(self, parent):

        self.gorillaPositionX = 700
        self.gorillaPositionY = 150

        self.gorillaIdle = QMovie("images\\npc\\npc_gorilla\standing2.gif")
        self.gorillaRunRight = QMovie("images\\npc\\npc_gorilla\\right.gif")
        self.gorillaRunLeft = QMovie("images\\npc\\npc_gorilla\left.gif")

        self.gorillaLabel = QLabel(parent)
        self.gorillaLabel.setGeometry(self.gorillaPositionX, self.gorillaPositionY, 100, 100)


    def updatePosition(self, x, y):

        self.gorillaPositionX = x
        self.gorillaPositionY = y

        self.gorillaLabel.move(x, y)

    def startRunning(self):
        while 1:
            if self.gorillaRunningDirection == "right":
                if self.gorillaPositionX >= 950:
                    self.gorillaRunningDirection = "left"
                else:
                    self.updatePosition(self.gorillaPositionX + 5, self.gorillaPositionY)
            else:
                if self.gorillaPositionX == 0:
                    self.gorillaRunningDirection = "right"
                else:
                    self.updatePosition(self.gorillaPositionX - 5, self.gorillaPositionY)

            time.sleep(0.1)
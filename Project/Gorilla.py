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

    leftDirectionSignal = pyqtSignal()
    rightDirectionSignal = pyqtSignal()



    def __init__(self, parent):
        super().__init__(parent)

        self.initGorilla(parent)


    def initGorilla(self, parent):

        self.gorillaPositionX = 900
        self.gorillaPositionY = 150

        self.gorillaIdle = QPixmap("images\\npc\\npc_gorilla\standing2.png")
        self.gorillaRunRight = QMovie("images\\npc\\npc_gorilla\\right.gif")
        self.gorillaRunLeft = QMovie("images\\npc\\npc_gorilla\left.gif")

        self.gorillaLabel = QLabel(parent)
        #self.gorillaLabel.setStyleSheet("background-color: lime;")  # For test purposes
        self.gorillaLabel.setGeometry(self.gorillaPositionX, self.gorillaPositionY, 100, 100)

        self.gorillaLabel.setPixmap(self.gorillaIdle)

        self.leftDirectionSignal.connect(self.leftDirectionGifSetup)
        self.rightDirectionSignal.connect(self.rightDirectionGifSetup)

    def updatePosition(self, x, y):

        self.gorillaPositionX = x
        self.gorillaPositionY = y

        self.gorillaLabel.move(x, y)

    def startRunning(self):
        time.sleep(7)
        self.rightDirectionSignal.emit()
        while 1:
            if self.gorillaRunningDirection == "right":
                if self.gorillaPositionX >= 1820:
                    self.gorillaRunningDirection = "left"
                    self.leftDirectionSignal.emit()
                else:
                    self.updatePosition(self.gorillaPositionX + 15, self.gorillaPositionY)
            else:
                if self.gorillaPositionX == 0:
                    self.gorillaRunningDirection = "right"
                    self.rightDirectionSignal.emit()
                else:
                    self.updatePosition(self.gorillaPositionX - 15, self.gorillaPositionY)

            time.sleep(0.1)

    def leftDirectionGifSetup(self):
         self.gorillaLabel.setMovie(self.gorillaRunLeft)
         self.gorillaRunLeft.start()

    def rightDirectionGifSetup(self):
         self.gorillaLabel.setMovie(self.gorillaRunRight)
         self.gorillaRunRight.start()
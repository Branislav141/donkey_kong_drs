from threading import Thread

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
    gorillaRunningDirection = 0
    gorillaRunningDirections = ['left', 'right']

    gorillaLabel = 0


    leftDirectionSignal = pyqtSignal()
    rightDirectionSignal = pyqtSignal()
    updatePositionSignal = pyqtSignal(int, int)
    createBarrelSignal = pyqtSignal()
    moveBarrelsSignal = pyqtSignal()


    barrelMoveSpeed = 3
    gorillaMoveSpeed = 3
    closeGorillaThread = 0



    def __init__(self, parent):
        super().__init__(parent)

        self.initGorilla(parent)


    def initGorilla(self, parent):

        self.gorillaPositionX = 900
        self.gorillaPositionY = 150
        self.gorillaRunningDirection = random.choice(self.gorillaRunningDirections)

        self.gorillaIdle = QPixmap("images\\npc\\npc_gorilla\standing2.png")
        self.gorillaRunRight = QMovie("images\\npc\\npc_gorilla\\right.gif")
        self.gorillaRunLeft = QMovie("images\\npc\\npc_gorilla\left.gif")

        self.gorillaLabel = QLabel(parent)
        #self.gorillaLabel.setStyleSheet("background-color: lime;")  # For test purposes
        self.gorillaLabel.setGeometry(self.gorillaPositionX, self.gorillaPositionY, 100, 100)

        self.gorillaLabel.setPixmap(self.gorillaIdle)



        self.barrel1Label = QLabel(parent)
        self.barrel1Label.setPixmap(QPixmap("images\items\\barrel.png"))
        self.barrel1Label.hide()
        self.barrel1LabelCreated = 0
        self.barrel2Label = QLabel(parent)
        self.barrel2Label.setPixmap(QPixmap("images\items\\barrel.png"))
        self.barrel2Label.hide()
        self.barrel2LabelCreated = 0
        self.barrel3Label = QLabel(parent)
        self.barrel3Label.setPixmap(QPixmap("images\items\\barrel.png"))
        self.barrel3Label.hide()
        self.barrel3LabelCreated = 0
        self.barrel4Label = QLabel(parent)
        self.barrel4Label.setPixmap(QPixmap("images\items\\barrel.png"))
        self.barrel4Label.hide()
        self.barrel4LabelCreated = 0
        self.barrel5Label = QLabel(parent)
        self.barrel5Label.setPixmap(QPixmap("images\items\\barrel.png"))
        self.barrel5Label.hide()
        self.barrel5LabelCreated = 0



    def updatePosition(self, x, y):

        self.gorillaPositionX = x
        self.gorillaPositionY = y

        self.gorillaLabel.move(x, y)

    def startRunning(self):
        time.sleep(7)
        i = 0
        if self.gorillaRunningDirection == 'right':
            self.rightDirectionSignal.emit()
        else:
            self.leftDirectionSignal.emit()
        while 1:
            i += 1
            if i % 60 == 0:
                self.createBarrelSignal.emit()

            self.moveBarrelsSignal.emit()

            if self.gorillaRunningDirection == 'right':
                if self.gorillaPositionX >= 1820:
                    self.gorillaRunningDirection = 'left'
                    self.leftDirectionSignal.emit()
                else:
                    self.updatePositionSignal.emit(self.gorillaPositionX + self.gorillaMoveSpeed, self.gorillaPositionY)
                    #self.updatePosition(self.gorillaPositionX + 5, self.gorillaPositionY)
            else:
                if self.gorillaPositionX <= 0:
                    self.gorillaRunningDirection = 'right'
                    self.rightDirectionSignal.emit()
                else:
                    self.updatePositionSignal.emit(self.gorillaPositionX - self.gorillaMoveSpeed, self.gorillaPositionY)
                    #self.updatePosition(self.gorillaPositionX - 5, self.gorillaPositionY)

            if self.closeGorillaThread == 1:
                break
            time.sleep(0.05)


    def leftDirectionGifSetup(self):
         self.gorillaLabel.setMovie(self.gorillaRunLeft)
         self.gorillaRunLeft.start()

    def rightDirectionGifSetup(self):
         self.gorillaLabel.setMovie(self.gorillaRunRight)
         self.gorillaRunRight.start()



    def moveBarrels(self):
        if self.barrel1LabelCreated == 1:
            self.barrel1Label.move(self.barrel1Label.x(), self.barrel1Label.y() + self.barrelMoveSpeed)
            if self.barrel1Label.y() >= 1070:
                self.barrel1LabelCreated = 0

        if self.barrel2LabelCreated == 1:
            self.barrel2Label.move(self.barrel2Label.x(), self.barrel2Label.y() + self.barrelMoveSpeed)
            if self.barrel2Label.y() >= 1070:
                self.barrel2LabelCreated = 0

        if self.barrel3LabelCreated == 1:
            self.barrel3Label.move(self.barrel3Label.x(), self.barrel3Label.y() + self.barrelMoveSpeed)
            if self.barrel3Label.y() >= 1070:
                self.barrel3LabelCreated = 0

        if self.barrel4LabelCreated == 1:
            self.barrel4Label.move(self.barrel4Label.x(), self.barrel4Label.y() + self.barrelMoveSpeed)
            if self.barrel4Label.y() >= 1070:
                self.barrel4LabelCreated = 0

        if self.barrel5LabelCreated == 1:
            self.barrel5Label.move(self.barrel5Label.x(), self.barrel5Label.y() + self.barrelMoveSpeed)
            if self.barrel5Label.y() >= 1070:
                self.barrel5LabelCreated = 0

    def createBarrel(self):
        if self.barrel1LabelCreated == 0:
            self.barrel1Label.setGeometry(self.gorillaPositionX, self.gorillaPositionY+100, 100, 100)
            self.barrel1Label.show()
            self.barrel1LabelCreated = 1
        elif self.barrel2LabelCreated == 0:
            self.barrel2Label.setGeometry(self.gorillaPositionX, self.gorillaPositionY + 100, 100, 100)
            self.barrel2Label.show()
            self.barrel2LabelCreated = 1
        elif self.barrel3LabelCreated == 0:
            self.barrel3Label.setGeometry(self.gorillaPositionX, self.gorillaPositionY + 100, 100, 100)
            self.barrel3Label.show()
            self.barrel3LabelCreated = 1
        elif self.barrel4LabelCreated == 0:
            self.barrel4Label.setGeometry(self.gorillaPositionX, self.gorillaPositionY + 100, 100, 100)
            self.barrel4Label.show()
            self.barrel4LabelCreated = 1
        elif self.barrel3LabelCreated == 0:
            self.barrel5Label.setGeometry(self.gorillaPositionX, self.gorillaPositionY + 100, 100, 100)
            self.barrel5Label.show()
            self.barrel5LabelCreated = 1

    def stopGorillaThread(self):
        self.gorillaLabel.setPixmap(self.gorillaIdle)
        self.closeGorillaThread = 1
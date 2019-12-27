from threading import Thread

from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPixmap, QMovie
from Barrel import Barrel

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

        self.threads = []
        self.barrelList = []
        self.barrel1 = Barrel(parent, self.gorillaPositionX, self.gorillaPositionY + 100)
        self.barrel2 = Barrel(parent, self.gorillaPositionX, self.gorillaPositionY + 100)
        self.barrel3 = Barrel(parent, self.gorillaPositionX, self.gorillaPositionY + 100)
        self.barrel4 = Barrel(parent, self.gorillaPositionX, self.gorillaPositionY + 100)
        self.barrel5 = Barrel(parent, self.gorillaPositionX, self.gorillaPositionY + 100)
        self.barrel6 = Barrel(parent, self.gorillaPositionX, self.gorillaPositionY + 100)
        self.barrel7 = Barrel(parent, self.gorillaPositionX, self.gorillaPositionY + 100)
        self.barrel8 = Barrel(parent, self.gorillaPositionX, self.gorillaPositionY + 100)
        self.barrel9 = Barrel(parent, self.gorillaPositionX, self.gorillaPositionY + 100)
        self.barrel10 = Barrel(parent, self.gorillaPositionX, self.gorillaPositionY + 100)

        self.barrelList.append(self.barrel1)
        self.barrelList.append(self.barrel2)
        self.barrelList.append(self.barrel3)


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



    def moveBarrels(self):
        i = 0
        time.sleep(7)
        while 1:
            time.sleep(0.3)
            i += 1
            if i % 15 == 0:
                self.createBarrel()

            if self.barrel1.isCreated == 1:
                self.barrel1.updatePosition(self.barrel1.barrelPositionX, self.barrel1.barrelPositionY + 5)
            if self.barrel2.isCreated == 1:
                self.barrel2.updatePosition(self.barrel2.barrelPositionX, self.barrel2.barrelPositionY + 5)
            if self.barrel3.isCreated == 1:
                self.barrel3.updatePosition(self.barrel3.barrelPositionX, self.barrel3.barrelPositionY + 5)
            if self.barrel4.isCreated == 1:
                self.barrel4.updatePosition(self.barrel4.barrelPositionX, self.barrel4.barrelPositionY + 5)
            if self.barrel5.isCreated == 1:
                self.barrel5.updatePosition(self.barrel5.barrelPositionX, self.barrel5.barrelPositionY + 5)
            if self.barrel6.isCreated == 1:
                self.barrel6.updatePosition(self.barrel6.barrelPositionX, self.barrel6.barrelPositionY + 5)
            if self.barrel7.isCreated == 1:
                self.barrel7.updatePosition(self.barrel7.barrelPositionX, self.barrel7.barrelPositionY + 5)
            if self.barrel8.isCreated == 1:
                self.barrel8.updatePosition(self.barrel8.barrelPositionX, self.barrel8.barrelPositionY + 5)
            if self.barrel9.isCreated == 1:
                self.barrel9.updatePosition(self.barrel9.barrelPositionX, self.barrel9.barrelPositionY + 5)
            if self.barrel10.isCreated == 1:
                self.barrel10.updatePosition(self.barrel10.barrelPositionX, self.barrel10.barrelPositionY + 5)


    def createBarrel(self):
        if self.barrel1.isCreated == 0:
            self.barrel1.isCreated = 1
            self.barrel1.updatePosition(self.gorillaPositionX, self.gorillaPositionY + 100)
        elif self.barrel2.isCreated == 0:
            self.barrel2.isCreated = 1
            self.barrel2.updatePosition(self.gorillaPositionX, self.gorillaPositionY + 100)
        elif self.barrel3.isCreated == 0:
            self.barrel3.isCreated = 1
            self.barrel3.updatePosition(self.gorillaPositionX, self.gorillaPositionY + 100)


    def createBarrelThread(self):
        time.sleep(7)
        while 1:
            time.sleep(2)
            if self.barrel1.isCreated == 0:
                self.barrel1.isCreated = 1
                self.barrel1.updatePosition(self.gorillaPositionX, self.gorillaPositionY + 100)
                thread = Thread(target=self.barrelHandle, args=[self.barrel1])
                self.threads.append(thread)
                thread.setDaemon(True)
                thread.start()
            elif self.barrel2.isCreated == 0:
                self.barrel2.isCreated = 1
                self.barrel2.updatePosition(self.gorillaPositionX, self.gorillaPositionY + 100)
                thread = Thread(target=self.barrelHandle, args=[self.barrel2])
                self.threads.append(thread)
                thread.setDaemon(True)
                thread.start()
            elif self.barrel3.isCreated == 0:
                self.barrel3.isCreated = 1
                self.barrel3.updatePosition(self.gorillaPositionX, self.gorillaPositionY + 100)
                thread = Thread(target=self.barrelHandle, args=[self.barrel3])
                self.threads.append(thread)
                thread.setDaemon(True)
                thread.start()
            elif self.barrel4.isCreated == 0:
                self.barrel4.isCreated = 1
                self.barrel4.updatePosition(self.gorillaPositionX, self.gorillaPositionY + 100)
                thread = Thread(target=self.barrelHandle, args=[self.barrel4])
                self.threads.append(thread)
                thread.setDaemon(True)
                thread.start()
            elif self.barrel5.isCreated == 0:
                self.barrel5.isCreated = 1
                self.barrel5.updatePosition(self.gorillaPositionX, self.gorillaPositionY + 100)
                thread = Thread(target=self.barrelHandle, args=[self.barrel5])
                self.threads.append(thread)
                thread.setDaemon(True)
                thread.start()
            elif self.barrel6.isCreated == 0:
                self.barrel6.isCreated = 1
                self.barrel6.updatePosition(self.gorillaPositionX, self.gorillaPositionY + 100)
                thread = Thread(target=self.barrelHandle, args=[self.barrel6])
                self.threads.append(thread)
                thread.setDaemon(True)
                thread.start()
            elif self.barrel7.isCreated == 0:
                self.barrel7.isCreated = 1
                self.barrel7.updatePosition(self.gorillaPositionX, self.gorillaPositionY + 100)
                thread = Thread(target=self.barrelHandle, args=[self.barrel7])
                self.threads.append(thread)
                thread.setDaemon(True)
                thread.start()
            elif self.barrel8.isCreated == 0:
                self.barrel8.isCreated = 1
                self.barrel8.updatePosition(self.gorillaPositionX, self.gorillaPositionY + 100)
                thread = Thread(target=self.barrelHandle, args=[self.barrel8])
                self.threads.append(thread)
                thread.setDaemon(True)
                thread.start()
            elif self.barrel9.isCreated == 0:
                self.barrel9.isCreated = 1
                self.barrel9.updatePosition(self.gorillaPositionX, self.gorillaPositionY + 100)
                thread = Thread(target=self.barrelHandle, args=[self.barrel9])
                self.threads.append(thread)
                thread.setDaemon(True)
                thread.start()
            elif self.barrel10.isCreated == 0:
                self.barrel10.isCreated = 1
                self.barrel10.updatePosition(self.gorillaPositionX, self.gorillaPositionY + 100)
                thread = Thread(target=self.barrelHandle, args=[self.barrel10])
                self.threads.append(thread)
                thread.setDaemon(True)
                thread.start()

    def barrelHandle(self, barrel):
        while 1:
            time.sleep(0.1)
            if barrel.barrelPositionY >= 1050:
                break
            barrel.updatePosition(barrel.barrelPositionX, barrel.barrelPositionY + 1)
import sys
import time
from threading import Thread

from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton


from key_notifier import KeyNotifier
from Character import Character

import datetime
import random


# list of values of Y axis where characters can move
listOfValidYAxisValues = [950, 951, 952, 750, 751, 752, 550, 551, 552, 350, 351, 352, 150, 151, 152, 0, 1, 2]
listOfSoundtracks = ["song_hyouhaku", "song_kokuten", "song_raising_fighting_spirit", "song_saika", "song_senya", "song_madara_theme"]

class LevelGenerator(QWidget):

    def __init__(self, gameMode, player1, player2, player3, player4):
        super().__init__()

        self.newLevel(gameMode, player1, player2, player3, player4)
        self.levelIntroHandle();

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

        self.player1.winnerSignal.connect(self.winner1Trigger__)
        self.player2.winnerSignal.connect(self.winner2Trigger__)

    def levelIntroHandle(self):
        countdownThread = Thread(target=self.countdown__)
        countdownThread.setDaemon(True)
        countdownThread.start()

        self.player1.playerIntroRight.finished.connect(self.char1Intro)
        self.player2.playerIntroLeft.finished.connect(self.char2Intro)


    def winner1Trigger__(self):
        self.player1.winnerLabel.show()
        self.key_notifier.die()

    def winner2Trigger__(self):
        self.player2.winnerLabel.show()
        self.key_notifier.die()
        
    def char1Intro(self):
        self.player1.playerLabel.setMovie(self.player1.playerIdleRight)
        self.player1.playerIdleRight.start()

    def char2Intro(self):
        self.player2.playerLabel.setMovie(self.player2.playerIdleLeft)
        self.player2.playerIdleLeft.start()


    def countdown__(self):
        time.sleep(2)
        self.countdownLabel.show()
        time.sleep(1)
        self.countdownLabel.setPixmap(self.cdnTwo)
        time.sleep(1)
        self.countdownLabel.setPixmap(self.cdnOne)
        time.sleep(1)
        self.countdownLabel.hide()
        self.startLabel.show()
        time.sleep(2)
        self.startLabel.hide()

    def newLevel(self, mode, character1, character2, character3, character4):

        self.setLevelDesign()
        self.setLevelSoundtrack()
        self.initPlayers(character1, character2)
        self.showFullScreen()

    def setLevelDesign(self):

        self.reset = QPixmap('images\characters\\reset.png')

        # background image
        self.backgroundPicture = QPixmap('images\level\\background.png')
        self.backgroundLabel = QLabel(self)
        self.backgroundLabel.setPixmap(self.backgroundPicture)
        self.backgroundLabel.move(0, 0)

        # countdown
        self.cdnOne = QPixmap('images\level\one.png')
        self.cdnTwo = QPixmap('images\level\\two.png')
        self.cdnThree = QPixmap('images\level\\three.png')
        self.countdownLabel = QLabel(self)
        self.countdownLabel.hide()
        self.countdownLabel.setPixmap(self.cdnThree)
        self.countdownLabel.move(755, 300)

        # begin
        self.startPicture = QPixmap('images\level\\begin.png')
        self.startLabel = QLabel(self)
        self.startLabel.hide()
        self.startLabel.setPixmap(self.startPicture)
        self.startLabel.move(585, 300)

        #  princess
        self.princessIdle = QMovie('images\\npc\\npc_flame_princess\\npc_flame_princess_idle.gif')
        self.princessLabel = QLabel(self)
        self.princessLabel.setStyleSheet("background-color: lime;")
        self.princessLabel.setMovie(self.princessIdle)
        self.princessIdle.start()
        self.princessLabel.move(1150, 0)

        self.setWindowState(Qt.WindowMaximized)

        #self.exitButton = QPushButton(self)
        #self.exitButton.setGeometry(1400, 0, 90, 25)
        #self.exitButton.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red;font-size: 18px; font-family: Segoe Script;");
        #self.exitButton.setText("QUIT")
        #self.exitButton.clicked.connect(self.exitLevel)


    def setLevelSoundtrack(self):
        self.song = random.choice(listOfSoundtracks)
        self.levelMusic = QSound("sounds\level\\" + self.song + ".wav")
        self.levelMusic.setLoops(-1)
        self.levelMusic.play()

    def initPlayers(self, chr1, chr2):
        self.player1 = Character(self, 100, 150, chr1)
        self.player2 = Character(self, 1720, 150, chr2)

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        self.key_notifier.add_key(event.key())

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
        self.key_notifier.rem_key(event.key())

        rec1 = self.player1.playerLabel.geometry()
        rec2 = self.player2.playerLabel.geometry()

        if not self.checkLeftRight(rec1.y()):
            self.player1.playerLabel.setPixmap(self.player1.playerClimbPicture)
        else:
            if rec1.x() >= rec2.x():
                self.player1.playerLabel.setMovie(self.player1.playerIdleLeft)
                self.player1.playerIdleLeft.start()
            else:
                self.player1.playerLabel.setMovie(self.player1.playerIdleRight)
                self.player1.playerIdleRight.start()

        if not self.checkLeftRight(rec2.y()):
            self.player2.playerLabel.setPixmap(self.player2.playerClimbPicture)
        else:
            if rec1.x() >= rec2.x():
                self.player2.playerLabel.setMovie(self.player2.playerIdleRight)
                self.player2.playerIdleRight.start()
            else:
                self.player2.playerLabel.setMovie(self.player2.playerIdleLeft)
                self.player2.playerIdleLeft.start()

    # check if character can move up
    def checkLadderUp(self, x, y):
        if 900 <= x <= (900 + 20) and y >= 751:
            return True
        elif 115 <= x <= (115 + 20) and 551 <= y <= 751:
            return True
        elif 1732 <= x <= (1732 + 20) and 351 <= y <= 551:
            return True
        elif 323 <= x <= (323 + 20) and 151 <= y <= 351:
            return True
        elif 900 <= x <= (900 + 20) and 10 <= y <= 151:
            return True
        else:
            return False

    # check if character can move down
    def checkLadderDown(self, x, y):
        if 900 <= x <= (900 + 20) and y >= 749:
            return True
        elif 115 <= x <= (115 + 20) and 549 <= y <= 749:
            return True
        elif 1732 <= x <= (1732 + 20) and 349 <= y <= 549:
            return True
        elif 323 <= x <= (323 + 20) and 149 <= y <= 349:
            return True
        elif 900 <= x <= (900 + 20) and -1 <= y <= 149:
            return True
        else:
            return False

    # check if character can move left or right (if on bricks)
    def checkLeftRight(self, y):
        if y in listOfValidYAxisValues:
            return True
        else:
            return False

    # check if character is on top ladder
    def isTopLadder(self, y):
        if y == 2 or y == 1 or y == 0:
            return True
        else:
            return False

    # updates position of character
    def __update_position__(self, key):
        rec1 = self.player1.playerLabel.geometry()
        rec2 = self.player2.playerLabel.geometry()

        if key == Qt.Key_Escape:
            self.levelMusic.stop()
            from Project.main_window import MainWindow
            self.mainMenu = MainWindow()
            self.close()

        if key == Qt.Key_D:
            if self.checkLeftRight(rec1.y()):
                if self.isTopLadder(rec1.y()):
                    if rec1.x() < 1160:
                        self.player1.playerLabel.setMovie(self.player1.playerRunRight)
                        self.player1.playerRunRight.start()
                        self.player1.updatePosition(rec1.x() + 10, rec1.y())
                else:
                    if rec1.x() < 1825:
                        self.player1.playerLabel.setMovie(self.player1.playerRunRight)
                        self.player1.playerRunRight.start()
                        self.player1.updatePosition(rec1.x() + 10, rec1.y())
        elif key == Qt.Key_S:
            if rec1.y() < 950:
                if self.checkLadderDown(rec1.x(), rec1.y()):
                    self.player1.playerLabel.setMovie(self.player1.playerClimb)
                    self.player1.playerClimb.start()
                    self.player1.updatePosition(rec1.x(), rec1.y() + 10)
        elif key == Qt.Key_W:
            if self.checkLadderUp(rec1.x(), rec1.y()):
                self.player1.playerLabel.setMovie(self.player1.playerClimb)
                self.player1.playerClimb.start()
                self.player1.updatePosition(rec1.x(), rec1.y() - 10)
        elif key == Qt.Key_A:
            if self.checkLeftRight(rec1.y()):
                if self.isTopLadder(rec1.y()):
                    if rec1.x() > 645:
                        self.player1.playerLabel.setMovie(self.player1.playerRunLeft)
                        self.player1.playerRunLeft.start()
                        self.player1.updatePosition(rec1.x() - 10, rec1.y())
                else:
                    if rec1.x() > -5:
                        self.player1.playerLabel.setMovie(self.player1.playerRunLeft)
                        self.player1.playerRunLeft.start()
                        self.player1.updatePosition(rec1.x() - 10, rec1.y())

        if key == Qt.Key_Right:
            if self.checkLeftRight(rec2.y()):
                if self.isTopLadder(rec2.y()):
                    if rec2.x() < 1160:
                        self.player2.playerLabel.setMovie(self.player2.playerRunRight)
                        self.player2.playerRunRight.start()
                        self.player2.updatePosition(rec2.x() + 10, rec2.y())
                else:
                    if rec2.x() < 1825:
                        self.player2.playerLabel.setMovie(self.player2.playerRunRight)
                        self.player2.playerRunRight.start()
                        self.player2.updatePosition(rec2.x() + 10, rec2.y())
        elif key == Qt.Key_Down:
            if rec2.y() < 950:
                if self.checkLadderDown(rec2.x(), rec2.y()):
                    self.player2.playerLabel.setMovie(self.player2.playerClimb)
                    self.player2.playerClimb.start()
                    self.player2.updatePosition(rec2.x(), rec2.y() + 10)
        elif key == Qt.Key_Up:
            if self.checkLadderUp(rec2.x(), rec2.y()):
                self.player2.playerLabel.setMovie(self.player2.playerClimb)
                self.player2.playerClimb.start()
                self.player2.updatePosition(rec2.x(), rec2.y() - 10)
        elif key == Qt.Key_Left:
            if self.checkLeftRight(rec2.y()):
                if self.isTopLadder(rec2.y()):
                    if rec2.x() > 645:
                        self.player2.playerLabel.setMovie(self.player2.playerRunLeft)
                        self.player2.playerRunLeft.start()
                        self.player2.updatePosition(rec2.x() - 10, rec2.y())
                else:
                    if rec2.x() > -5:
                        self.player2.playerLabel.setMovie(self.player2.playerRunLeft)
                        self.player2.playerRunLeft.start()
                        self.player2.updatePosition(rec2.x() - 10, rec2.y())

    def closeEvent(self, event):
        self.key_notifier.die()

    def exitLevel(self):
        self.levelMusic.stop()
        self.close()

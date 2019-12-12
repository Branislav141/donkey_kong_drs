import sys

from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QWidget, QLabel, QApplication

from key_notifier import KeyNotifier
import datetime

from Character import Character

# list of values of Y axis where characters can move
listOfValidYAxisValues = [940, 941, 942, 740, 741, 742, 540, 541, 542, 340, 341, 342, 140, 141, 142, -10, -9, -8]


class LevelGenerator(QWidget):

    def __init__(self):
        super().__init__()

        # background image
        self.backgroundPicture = QPixmap('images\level\\background.png')
        self.backgroundLabel = QLabel(self)

        self.setWindowState(Qt.WindowMaximized)
        self.newLevel()

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

    def newLevel(self):

        self.backgroundLabel.setPixmap(self.backgroundPicture)
        self.backgroundLabel.move(0, 0)

        self.levelMusic = QSound("sounds\level\hyouhaku.wav")
        self.levelMusic.setLoops(-1)
        self.levelMusic.play()

        #self.player1 = Character(self, 100, 940, "\\naruto")
        self.player1 = Character(self, 100, 940, "\itachi")
        self.player2 = Character(self, 1720, 940, "\sasuke")

        self.setWindowTitle('Donkey Kong The Game')
        self.showFullScreen()

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
        if 900 <= x <= (900 + 20) and y >= 741:
            return True
        elif 115 <= x <= (115 + 20) and 541 <= y <= 741:
            return True
        elif 1732 <= x <= (1732 + 20) and 341 <= y <= 541:
            return True
        elif 323 <= x <= (323 + 20) and 141 <= y <= 341:
            return True
        elif 900 <= x <= (900 + 20) and 0 <= y <= 141:
            return True
        else:
            return False

    # check if character can move down
    def checkLadderDown(self, x, y):
        if 900 <= x <= (900 + 20) and y >= 739:
            return True
        elif 115 <= x <= (115 + 20) and 539 <= y <= 739:
            return True
        elif 1732 <= x <= (1732 + 20) and 339 <= y <= 539:
            return True
        elif 323 <= x <= (323 + 20) and 139 <= y <= 339:
            return True
        elif 900 <= x <= (900 + 20) and -11 <= y <= 139:
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
        if y == -8 or y == -9 or y == -10:
            return True
        else:
            return False

    # updates position of character
    def __update_position__(self, key):
        rec1 = self.player1.playerLabel.geometry()
        rec2 = self.player2.playerLabel.geometry()

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
            if rec1.y() < 940:
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
                    if rec1.x() > -25:
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
            if rec2.y() < 940:
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
                    if rec2.x() > -25:
                        self.player2.playerLabel.setMovie(self.player2.playerRunLeft)
                        self.player2.playerRunLeft.start()
                        self.player2.updatePosition(rec2.x() - 10, rec2.y())

    def closeEvent(self, event):
        self.key_notifier.die()
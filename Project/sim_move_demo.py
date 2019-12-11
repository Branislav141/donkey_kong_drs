import sys

from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QWidget, QLabel, QApplication

from key_notifier import KeyNotifier
import datetime

# list of values of Y axis where characters can move
listOfValidYAxisValues = [940, 941, 942, 740, 741, 742, 540, 541, 542, 340, 341, 342, 140, 141, 142, -10, -9, -8]


class SimMoveDemo(QWidget):

    def __init__(self):
        super().__init__()

        # background image
        self.backgroundPicture = QPixmap('images\level\\background.png')
        self.backgroundLabel = QLabel(self)

        self.pix2 = QPixmap('skull_green.png')

        # player labels
        self.player1Label = QLabel(self)
        self.player2Label = QLabel(self)

        # player 1 gif animations
        self.player1Idle = QMovie("images\characters\\naruto\\naruto_idle_right.gif");
        self.player1RunRight = QMovie("images\characters\\naruto\\naruto_run_right.gif");
        self.player1RunLeft = QMovie("images\characters\\naruto\\naruto_run_left.gif");
        self.player1Climb = QMovie("images\characters\\naruto\\naruto_climb.gif");

        self.player2Idle = QMovie("images\characters\sasuke\sasuke_idle_left.gif");
        self.player2RunRight = QMovie("images\characters\sasuke\sasuke_run_right.gif");
        self.player2RunLeft = QMovie("images\characters\sasuke\sasuke_run_left.gif");
        self.player2Climb = QMovie("images\characters\sasuke\sasuke_climb.gif");

        self.setWindowState(Qt.WindowMaximized)
        self.__init_ui__()

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

    def __init_ui__(self):
        self.backgroundLabel.setPixmap(self.backgroundPicture)
        self.backgroundLabel.move(0, 0)

        # initial state of player 1
        self.player1Label.setGeometry(100, 940, 120, 120)
        self.player1Label.setMovie(self.player1Idle);
        self.player1Idle.start();

        # initial state of player 2
        self.player2Label.setGeometry(1720, 940, 120, 120)
        self.player2Label.setMovie(self.player2Idle);
        self.player2Idle.start();

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

        self.player1Label.setMovie(self.player1Idle);
        self.player1Idle.start();

        self.player2Label.setMovie(self.player2Idle);
        self.player2Idle.start();

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
        rec1 = self.player1Label.geometry()
        rec2 = self.player2Label.geometry()

        if key == Qt.Key_Right:
            if self.checkLeftRight(rec1.y()):
                if self.isTopLadder(rec1.y()):
                    if rec1.x() < 1160:
                        self.player1Label.setMovie(self.player1RunRight);
                        self.player1RunRight.start();
                        self.player1Label.setGeometry(rec1.x() + 10, rec1.y(), rec1.width(), rec1.height())
                else:
                    if rec1.x() < 1825:
                        self.player1Label.setMovie(self.player1RunRight);
                        self.player1RunRight.start();
                        self.player1Label.setGeometry(rec1.x() + 10, rec1.y(), rec1.width(), rec1.height())
        elif key == Qt.Key_Down:
            if rec1.y() < 940:
                if self.checkLadderDown(rec1.x(), rec1.y()):
                    self.player1Label.setMovie(self.player1Climb);
                    self.player1Climb.start();
                    self.player1Label.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
        elif key == Qt.Key_Up:
            if self.checkLadderUp(rec1.x(), rec1.y()):
                self.player1Label.setMovie(self.player1Climb);
                self.player1Climb.start();
                self.player1Label.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
        elif key == Qt.Key_Left:
            if self.checkLeftRight(rec1.y()):
                if self.isTopLadder(rec1.y()):
                    if rec1.x() > 645:
                        self.player1Label.setMovie(self.player1RunLeft);
                        self.player1RunLeft.start();
                        self.player1Label.setGeometry(rec1.x() - 10, rec1.y(), rec1.width(), rec1.height())
                else:
                    if rec1.x() > -25:
                        self.player1Label.setMovie(self.player1RunLeft);
                        self.player1RunLeft.start();
                        self.player1Label.setGeometry(rec1.x() - 10, rec1.y(), rec1.width(), rec1.height())

        if key == Qt.Key_D:
            if self.checkLeftRight(rec2.y()):
                if self.isTopLadder(rec2.y()):
                    if rec2.x() < 1160:
                        self.player2Label.setMovie(self.player2RunRight);
                        self.player2RunRight.start();
                        self.player2Label.setGeometry(rec2.x() + 10, rec2.y(), rec2.width(), rec2.height())
                else:
                    if rec2.x() < 1825:
                        self.player2Label.setMovie(self.player2RunRight);
                        self.player2RunRight.start();
                        self.player2Label.setGeometry(rec2.x() + 10, rec2.y(), rec2.width(), rec2.height())
        elif key == Qt.Key_S:
            if rec2.y() < 940:
                if self.checkLadderDown(rec2.x(), rec2.y()):
                    self.player2Label.setMovie(self.player2Climb);
                    self.player2Climb.start();
                    self.player2Label.setGeometry(rec2.x(), rec2.y() + 10, rec2.width(), rec2.height())
        elif key == Qt.Key_W:
            if self.checkLadderUp(rec2.x(), rec2.y()):
                self.player2Label.setMovie(self.player2Climb);
                self.player2Climb.start();
                self.player2Label.setGeometry(rec2.x(), rec2.y() - 10, rec2.width(), rec2.height())
        elif key == Qt.Key_A:
            if self.checkLeftRight(rec2.y()):
                if self.isTopLadder(rec2.y()):
                    if rec2.x() > 645:
                        self.player2Label.setMovie(self.player2RunLeft);
                        self.player2RunLeft.start();
                        self.player2Label.setGeometry(rec2.x() - 10, rec2.y(), rec2.width(), rec2.height())
                else:
                    if rec2.x() > -25:
                        self.player2Label.setMovie(self.player2RunLeft);
                        self.player2RunLeft.start();
                        self.player2Label.setGeometry(rec2.x() - 10, rec2.y(), rec2.width(), rec2.height())

    def closeEvent(self, event):
        self.key_notifier.die()

from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPixmap, QMovie
import sys, random


class Character(QFrame):

    playerLabel = 0
    playerIdle = 0
    playerRunRight = 0
    playerRunLeft = 0
    playerClimb = 0
    playerClimbPicture = 0

    def __init__(self, parent, x, y, player):
        super().__init__(parent)

        self.initCharacter(parent, x, y, player)


    def initCharacter(self, parent,  x, y, player):

        if player == 1:
            self.playerIdle = QMovie("images\characters\\naruto\\naruto_idle_right.gif");
            self.playerRunRight = QMovie("images\characters\\naruto\\naruto_run_right.gif");
            self.playerRunLeft = QMovie("images\characters\\naruto\\naruto_run_left.gif");
            self.playerClimb = QMovie("images\characters\\naruto\\naruto_climb.gif");
            self.playerClimbPicture = QPixmap("images\characters\\naruto\\naruto_climb.gif");
        elif player == 2:
            self.playerIdle = QMovie("images\characters\sasuke\sasuke_idle_left.gif");
            self.playerRunRight = QMovie("images\characters\sasuke\sasuke_run_right.gif");
            self.playerRunLeft = QMovie("images\characters\sasuke\sasuke_run_left.gif");
            self.playerClimb = QMovie("images\characters\sasuke\sasuke_climb.gif");
            self.playerClimbPicture = QPixmap("images\characters\sasuke\sasuke_climb.gif");

        self.playerLabel = QLabel(parent)
        self.playerLabel.setGeometry(x, y, 120, 120)
        self.playerLabel.setMovie(self.playerIdle)
        self.playerIdle.start()


    def updatePosition(self, x, y):
        self.playerLabel.setGeometry(x, y, 120, 120)



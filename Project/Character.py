from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPixmap, QMovie
import sys, random


class Character(QFrame):

    playerLabel = 0
    playerIdleRight = 0
    playerIdleLeft = 0
    playerRunRight = 0
    playerRunLeft = 0
    playerClimb = 0
    playerClimbPicture = 0

    def __init__(self, parent, x, y, player):
        super().__init__(parent)

        self.initCharacter(parent, x, y, player)


    def initCharacter(self, parent,  x, y, player):

        characterName = player + player;

        self.playerIdleRight = QMovie("images\characters" + characterName + "_idle_right.gif");
        self.playerIdleLeft = QMovie("images\characters" + characterName + "_idle_left.gif");
        self.playerRunRight = QMovie("images\characters" + characterName + "_run_right.gif");
        self.playerRunLeft = QMovie("images\characters" + characterName + "_run_left.gif");
        self.playerClimb = QMovie("images\characters" + characterName + "_climb.gif");
        self.playerClimbPicture = QPixmap("images\characters" + characterName + "_climb.gif");


        self.playerLabel = QLabel(parent)
        self.playerLabel.setGeometry(x, y, 120, 120)
        if x < 900:
            self.playerLabel.setMovie(self.playerIdleRight)
            self.playerIdleRight.start()
        else:
            self.playerLabel.setMovie(self.playerIdleLeft)
            self.playerIdleLeft.start()


    def updatePosition(self, x, y):
        self.playerLabel.setGeometry(x, y, 120, 120)



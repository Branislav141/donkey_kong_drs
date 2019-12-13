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
    playerProfilePicture = 0
    playerProfilePictureLabel = 0
    playerNameLabel = 0

    def __init__(self, parent, x, y, player):
        super().__init__(parent)

        self.initCharacter(parent, x, y, player)


    def initCharacter(self, parent,  x, y, characterName):

        parsedName = characterName.lower()
        parsedName = r"\ch_" + parsedName + r"\ch_" + parsedName

        self.playerIdleRight = QMovie("images\characters" + parsedName + "_idle_right.gif");
        self.playerIdleLeft = QMovie("images\characters" + parsedName + "_idle_left.gif");
        self.playerRunRight = QMovie("images\characters" + parsedName + "_run_right.gif");
        self.playerRunLeft = QMovie("images\characters" + parsedName + "_run_left.gif");
        self.playerClimb = QMovie("images\characters" + parsedName + "_climb.gif");
        self.playerClimbPicture = QPixmap("images\characters" + parsedName + "_climb.gif");
        self.playerProfilePicture = QPixmap("images\characters" + parsedName + "_profile.png");

        self.playerProfilePictureLabel = QLabel(parent)
        self.playerProfilePictureLabel.setPixmap(self.playerProfilePicture)

        self.playerNameLabel = QLabel(parent)
        self.playerNameLabel.setText(str(characterName))
        self.playerNameLabel.setStyleSheet("color: red;font-size: 21px; font-family: Segoe Script;");

        self.playerLabel = QLabel(parent)
        self.playerLabel.setGeometry(x, y, 120, 120)
        if x < 900:
            self.playerProfilePictureLabel.move(0,0)
            self.playerNameLabel.move(0, 80)
            self.playerLabel.setMovie(self.playerIdleRight)
            self.playerIdleRight.start()
        else:
            self.playerProfilePictureLabel.move(1830, 0)
            self.playerNameLabel.move(1830, 80)
            self.playerLabel.setMovie(self.playerIdleLeft)
            self.playerIdleLeft.start()


    def updatePosition(self, x, y):
        self.playerLabel.setGeometry(x, y, 120, 120)



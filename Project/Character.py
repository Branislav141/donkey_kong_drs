from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPixmap, QMovie
import sys, random


class Character(QFrame):

    playerLabel = 0
    playerIdleRight = 0
    playerIdleLeft = 0
    playerIntroRight = 0
    playerIntroLeft = 0
    playerRunRight = 0
    playerRunLeft = 0
    playerClimb = 0
    playerClimbPicture = 0
    playerProfilePicture = 0
    playerProfilePictureLabel = 0
    playerNameLabel = 0
    winnerLabel = 0
    pointsLabel = 0
    playerPoints = 0
    playerName = 0
    korak = 10
    playerWin = 0
    playerWinQuote = 0

    winnerSignal = pyqtSignal()

    def __init__(self, parent, x, y, player):
        super().__init__(parent)

        self.initCharacter(parent, x, y, player)


    def initCharacter(self, parent,  x, y, characterName):
        parsedName = characterName.lower()
        parsedName = r"\ch_" + parsedName + r"\ch_" + parsedName

        self.playerName = characterName
        self.playerPoints = 0

        # gif animations and images
        self.playerIdleRight = QMovie("images\characters" + parsedName + "_idle_right.gif")
        self.playerIdleLeft = QMovie("images\characters" + parsedName + "_idle_left.gif")
        self.playerRunRight = QMovie("images\characters" + parsedName + "_run_right.gif")
        self.playerRunLeft = QMovie("images\characters" + parsedName + "_run_left.gif")
        self.playerClimb = QMovie("images\characters" + parsedName + "_climb.gif")
        self.playerClimbPicture = QPixmap("images\characters" + parsedName + "_climb.gif")
        self.playerProfilePicture = QPixmap("images\characters" + parsedName + "_profile.png")
        self.playerIntroRight = QMovie("images\characters" + parsedName + "_intro_right.gif")
        self.playerIntroLeft = QMovie("images\characters" + parsedName + "_intro_left.gif")

        self.playerWin = QMovie("images\characters" + parsedName + "_win.gif");
        self.playerWinQuote = QSound("sounds\characters" + parsedName + "_win.wav")
        self.playerWinQuote.setLoops(1)

        self.pointsLabel = QLabel(parent)
        self.pointsLabel.setStyleSheet("color: red;font-size: 30px; font-family: Segoe Script;")
        self.pointsLabel.setText(str(self.playerPoints))

        self.playerProfilePictureLabel = QLabel(parent)
        self.playerProfilePictureLabel.setPixmap(self.playerProfilePicture)

        self.playerNameLabel = QLabel(parent)
        self.playerNameLabel.setText(str(characterName))
        self.playerNameLabel.setStyleSheet("color: red;font-size: 21px; font-family: Segoe Script;")

        self.winnerLabel = QLabel(parent)
        self.winnerLabel.setText("Winner!")
        self.winnerLabel.setStyleSheet("color: red;font-size: 21px; font-family: Segoe Script;")
        self.winnerLabel.hide()

        self.playerLabel = QLabel(parent)
        #self.playerLabel.setStyleSheet("background-color: lime;")  # For test purposes
        self.playerLabel.setGeometry(x, y, 100, 100)

        if x < 900:
            self.pointsLabel.move(100, 0)
            self.playerProfilePictureLabel.move(0,0)
            self.playerNameLabel.move(0, 80)
            self.winnerLabel.move(0, 110)
            self.playerLabel.setMovie(self.playerIntroRight)
            self.playerIntroRight.start()
        else:
            self.pointsLabel.move(1790, 0)
            self.playerProfilePictureLabel.move(1830, 0)
            self.playerNameLabel.move(1830, 80)
            self.winnerLabel.move(1830, 110)
            self.playerLabel.setMovie(self.playerIntroLeft)
            self.playerIntroLeft.start()


    def updatePosition(self, x, y):
        self.playerLabel.setGeometry(x, y, 100, 100)

        if self.isTopLadder(y):
            if x >= 1107:
                self.winnerSignal.emit()


    def isTopLadder(self, y):
        if y == 2 or y == 1 or y == 0:
            return True
        else:
            return False
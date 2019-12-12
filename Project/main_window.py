from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget, QComboBox
from PyQt5.QtGui import QPixmap
import sys

from level_generator import LevelGenerator



class MainWindow(QWidget):
    MainWindowHeight = 1080
    MainWindowWidth = 1920

    def __init__(self):
        super().__init__()
        self.initUI()

    def run(self):
        self.levelGenerator = LevelGenerator()

    def quit(self):
        app = QApplication.instance()
        app.closeAllWindows()


    def initUI(self):

        self.setWindowsOptions()

        self.initPlayerSelectionLabels()
        self.initPlayerSelectionComboBoxes()

        self.initGameModeSelection()

        self.initMainMenuButtons()
        self.initMainMenuImages()


        self.showFullScreen()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


    def setWindowsOptions(self):
        self.resize(self.MainWindowHeight, self.MainWindowWidth)
        self.center()

        self.setWindowTitle('Donkey Kong')

        self.setMinimumHeight(self.MainWindowHeight)
        self.setMinimumWidth(self.MainWindowWidth)
        self.setMaximumHeight(self.MainWindowHeight)
        self.setMaximumWidth(self.MainWindowWidth)
        self.setStyleSheet("background-color: black;")

    def initPlayerSelectionLabels(self):
        self.player1Lb = QtWidgets.QLabel(self)
        self.player1Lb.setText("Select player 1: ")
        self.player1Lb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        self.player1Lb.move(200, 300)

        self.player2Lb = QtWidgets.QLabel(self)
        self.player2Lb.setText("Select player 2: ")
        self.player2Lb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        self.player2Lb.move(200, 350)

        self.player3Lb = QtWidgets.QLabel(self)
        self.player3Lb.setText("Select player 3: ")
        self.player3Lb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        self.player3Lb.move(200, 400)

        self.player3InfoLb = QtWidgets.QLabel(self)
        self.player3InfoLb.setText("(Only in tournament!)")
        self.player3InfoLb.setStyleSheet("color: red;font-size: 14px; font-family: Helvetica;");
        self.player3InfoLb.move(460, 405)

        self.player4Lb = QtWidgets.QLabel(self)
        self.player4Lb.setText("Select player 4: ")
        self.player4Lb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        self.player4Lb.move(200, 450)

        self.player4InfoLb = QtWidgets.QLabel(self)
        self.player4InfoLb.setText("(Only in tournament!)")
        self.player4InfoLb.setStyleSheet("color: red;font-size: 14px; font-family: Helvetica;");
        self.player4InfoLb.move(460, 455)



    def initGameModeSelection(self):
        self.gameModeLb = QtWidgets.QLabel(self)
        self.gameModeLb.setText("Select game mode: ")
        self.gameModeLb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        self.gameModeLb.move(200, 525)

        self.versusRb = QtWidgets.QRadioButton(self)
        self.versusRb.setText("Versus")
        self.versusRb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        self.versusRb.move(390, 522)
        self.versusRb.setChecked(True)

        self.tournamentRb = QtWidgets.QRadioButton(self)
        self.tournamentRb.setText("Tournament")
        self.tournamentRb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        self.tournamentRb.move(490, 522)
        self.tournamentRb.setChecked(False)


    def initPlayerSelectionComboBoxes(self):
        self.player1Cb = QComboBox(self)
        self.player1Cb.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red; font-family: Helvetica;");
        self.player1Cb.addItem("")
        self.player1Cb.addItem("Naruto")
        self.player1Cb.addItem("Sasuke")
        self.player1Cb.addItem("Itachi")
        self.player1Cb.model().item(0).setEnabled(False)
        self.player1Cb.setGeometry(380, 305, 70, 20)

        self.player2Cb = QComboBox(self)
        self.player2Cb.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red; font-family: Helvetica;");
        self.player2Cb.addItem("")
        self.player2Cb.addItem("Naruto")
        self.player2Cb.addItem("Sasuke")
        self.player2Cb.addItem("Itachi")
        self.player2Cb.model().item(0).setEnabled(False)
        self.player2Cb.setGeometry(380, 355, 70, 20)

        self.player3Cb = QComboBox(self)
        self.player3Cb.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red; font-family: Helvetica;");
        self.player3Cb.addItem("")
        self.player3Cb.addItem("Naruto")
        self.player3Cb.addItem("Sasuke")
        self.player3Cb.addItem("Itachi")
        self.player3Cb.model().item(0).setEnabled(False)
        self.player3Cb.setGeometry(380, 405, 70, 20)

        self.player4Cb = QComboBox(self)
        self.player4Cb.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red; font-family: Helvetica;");
        self.player4Cb.addItem("")
        self.player4Cb.addItem("Naruto")
        self.player4Cb.addItem("Sasuke")
        self.player4Cb.addItem("Itachi")
        self.player4Cb.model().item(0).setEnabled(False)
        self.player4Cb.setGeometry(380, 455, 70, 20)

    def initMainMenuButtons(self):
        self.startButton = QtWidgets.QPushButton(self)
        self.startButton.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red;font-size: 26px; font-family: Segoe Script;");
        self.startButton.setText("START GAME")
        self.startButton.setGeometry(200, 600, 350, 50)
        self.startButton.clicked.connect(self.run)

        self.quitButton = QtWidgets.QPushButton(self)
        self.quitButton.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red;font-size: 26px; font-family: Segoe Script;");
        self.quitButton.setText("EXIT TO DESKTOP")
        self.quitButton.setGeometry(200, 700, 350, 50)
        self.quitButton.clicked.connect(self.quit)

    def initMainMenuImages(self):
        self.logoPic = QPixmap('images\menu\donkey_logo.png')
        self.logoLabel = QtWidgets.QLabel(self)
        self.logoLabel.setPixmap(self.logoPic)
        self.logoLabel.move(880, 120)

        self.monkeyPic = QPixmap('images\menu\donkey_monkey.png')
        self.monkeyLabel = QtWidgets.QLabel(self)
        self.monkeyLabel.setPixmap(self.monkeyPic)
        self.monkeyLabel.move(970, 300)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

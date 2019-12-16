
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget, QComboBox, QMessageBox
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt
import sys

from level_generator import LevelGenerator



class MainWindow(QWidget):
    MainWindowHeight = 1080
    MainWindowWidth = 1920

    def __init__(self):
        super().__init__()

        self.initUI()


    def run(self):
        if self.versusRb.isChecked():
            if str(self.player1Cb.currentText()) == "" or str(self.player2Cb.currentText()) == "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.NoIcon)
                msg.setText("You need to select characters for player1 and player2 in order to play versus.")
                msg.setWindowTitle("Error")
                msg.exec_()
            else:
                player1 = str(self.player1Cb.currentText())
                player2 = str(self.player2Cb.currentText())
                gameMode = "versus"
                self.levelGenerator = LevelGenerator(gameMode, player1, player2, "", "")
                self.close()
        else:
            if str(self.player1Cb.currentText()) == "" or str(self.player2Cb.currentText()) == "" or str(self.player3Cb.currentText()) == "" or str(self.player4Cb.currentText()) == "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.NoIcon)
                msg.setText("You need to select characters for all players in order to play tournament.")
                msg.setWindowTitle("Error")
                msg.exec_()
            else:
                player1 = str(self.player1Cb.currentText())
                player2 = str(self.player2Cb.currentText())
                player3 = str(self.player3Cb.currentText())
                player4 = str(self.player4Cb.currentText())
                gameMode = "tournament"
                self.levelGenerator = LevelGenerator(gameMode, player1, player2, player3, player4)

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
        self.player1Lb.move(100, 300)

        self.player2Lb = QtWidgets.QLabel(self)
        self.player2Lb.setText("Select player 2: ")
        self.player2Lb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        self.player2Lb.move(100, 350)

        self.player3Lb = QtWidgets.QLabel(self)
        self.player3Lb.setText("Select player 3: ")
        self.player3Lb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        self.player3Lb.move(100, 400)

        self.player3InfoLb = QtWidgets.QLabel(self)
        self.player3InfoLb.setText("(Only in tournament!)")
        self.player3InfoLb.setStyleSheet("color: red;font-size: 14px; font-family: Helvetica;");
        self.player3InfoLb.move(360, 405)

        self.player4Lb = QtWidgets.QLabel(self)
        self.player4Lb.setText("Select player 4: ")
        self.player4Lb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        self.player4Lb.move(100, 450)

        self.player4InfoLb = QtWidgets.QLabel(self)
        self.player4InfoLb.setText("(Only in tournament!)")
        self.player4InfoLb.setStyleSheet("color: red;font-size: 14px; font-family: Helvetica;");
        self.player4InfoLb.move(360, 455)



    def initGameModeSelection(self):
        self.gameModeLb = QtWidgets.QLabel(self)
        self.gameModeLb.setText("Select game mode: ")
        self.gameModeLb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        self.gameModeLb.move(100, 525)

        self.versusRb = QtWidgets.QRadioButton(self)
        self.versusRb.setCursor(Qt.PointingHandCursor)
        self.versusRb.setText("Versus")
        self.versusRb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        self.versusRb.move(290, 522)
        self.versusRb.setChecked(True)

        self.tournamentRb = QtWidgets.QRadioButton(self)
        self.tournamentRb.setCursor(Qt.PointingHandCursor)
        self.tournamentRb.setText("Tournament")
        self.tournamentRb.setStyleSheet("color: red;font-size: 18px; font-family: Segoe Script;");
        self.tournamentRb.move(390, 522)
        self.tournamentRb.setChecked(False)


    def initPlayerSelectionComboBoxes(self):
        self.player1Cb = QComboBox(self)
        self.player1Cb.setCursor(Qt.PointingHandCursor)
        self.player1Cb.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red; font-family: Helvetica;");
        self.player1Cb.addItem("")
        self.player1Cb.addItem("Naruto")
        self.player1Cb.addItem("Sasuke")
        self.player1Cb.addItem("Itachi")
        self.player1Cb.addItem("Madara")
        self.player1Cb.addItem("Test")
        self.player1Cb.model().item(0).setEnabled(False)
        self.player1Cb.setGeometry(280, 305, 70, 20)

        self.player2Cb = QComboBox(self)
        self.player2Cb.setCursor(Qt.PointingHandCursor)
        self.player2Cb.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red; font-family: Helvetica;");
        self.player2Cb.addItem("")
        self.player2Cb.addItem("Naruto")
        self.player2Cb.addItem("Sasuke")
        self.player2Cb.addItem("Itachi")
        self.player2Cb.addItem("Madara")
        self.player2Cb.addItem("Test")
        self.player2Cb.model().item(0).setEnabled(False)
        self.player2Cb.setGeometry(280, 355, 70, 20)

        self.player3Cb = QComboBox(self)
        self.player3Cb.setCursor(Qt.PointingHandCursor)
        self.player3Cb.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red; font-family: Helvetica;");
        self.player3Cb.addItem("")
        self.player3Cb.addItem("Naruto")
        self.player3Cb.addItem("Sasuke")
        self.player3Cb.addItem("Itachi")
        self.player3Cb.addItem("Madara")
        self.player3Cb.model().item(0).setEnabled(False)
        self.player3Cb.setGeometry(280, 405, 70, 20)

        self.player4Cb = QComboBox(self)
        self.player4Cb.setCursor(Qt.PointingHandCursor)
        self.player4Cb.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red; font-family: Helvetica;");
        self.player4Cb.addItem("")
        self.player4Cb.addItem("Naruto")
        self.player4Cb.addItem("Sasuke")
        self.player4Cb.addItem("Itachi")
        self.player4Cb.addItem("Madara")
        self.player4Cb.model().item(0).setEnabled(False)
        self.player4Cb.setGeometry(280, 455, 70, 20)

    def initMainMenuButtons(self):
        self.startButton = QtWidgets.QPushButton(self)
        self.startButton.setCursor(Qt.PointingHandCursor)
       # self.startButton.setEnabled(False)
        self.startButton.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red;font-size: 26px; font-family: Segoe Script;");
        self.startButton.setText("START GAME")
        self.startButton.setGeometry(100, 600, 350, 50)
        self.startButton.clicked.connect(self.run)

        self.quitButton = QtWidgets.QPushButton(self)
        self.quitButton.setCursor(Qt.PointingHandCursor)
        self.quitButton.setStyleSheet("border:1px solid rgb(220, 20, 60); color: red;font-size: 26px; font-family: Segoe Script;");
        self.quitButton.setText("EXIT TO DESKTOP")
        self.quitButton.setGeometry(100, 700, 350, 50)
        self.quitButton.clicked.connect(self.quit)

    def initMainMenuImages(self):
        self.logoPic = QPixmap('images\menu\logo.png')
        self.logoLabel = QtWidgets.QLabel(self)
        self.logoLabel.setPixmap(self.logoPic)
        self.logoLabel.move(920, 100)

        self.monkeyPic = QPixmap('images\menu\main_menu.png')
        self.monkeyLabel = QtWidgets.QLabel(self)
        self.monkeyLabel.setPixmap(self.monkeyPic)
        self.monkeyLabel.move(530, 410)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
